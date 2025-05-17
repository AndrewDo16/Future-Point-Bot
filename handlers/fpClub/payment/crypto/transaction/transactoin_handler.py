import logging
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes, CallbackQueryHandler
from web3 import Web3
from perisist.transaction.transaction_dao import is_transaction_used, save_transaction
from keyboards.payment.payment_error_keyboard import get_payment_error_keyboard
from perisist.transaction.wallet.crypto_wallet_dao import get_primary_wallet
from service.profile.update_subscription_service import update_subscription_service

# Настройка логирования
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO,
    handlers=[
        logging.StreamHandler(),  # Вывод логов в консоль
    ]
)
logger = logging.getLogger()

# Подключение к Binance Smart Chain
bsc_url = "https://bsc-dataseed.binance.org/"
web3 = Web3(Web3.HTTPProvider(bsc_url))

# Проверка подключения к BSC
if not web3.is_connected():
    logger.error("Не удалось подключиться к Binance Smart Chain.")
else:
    logger.info("Подключение к Binance Smart Chain успешно.")

# Целевой адрес для проверки пополнений
TARGET_ADDRESS = "0x695bf46a362204B370e2914bbd5667068bE8f7d0".lower()

# Адрес контракта USDT на BSC
USDT_CONTRACT_ADDRESS = "0x55d398326f99059fF775485246999027B3197955"

# ABI для BEP-20
bep20_abi = [
    {
        "constant": True,
        "inputs": [],
        "name": "symbol",
        "outputs": [{"name": "", "type": "string"}],
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [],
        "name": "decimals",
        "outputs": [{"name": "", "type": "uint8"}],
        "type": "function"
    },
    {
        "constant": False,
        "inputs": [{"name": "_to", "type": "address"}, {"name": "_value", "type": "uint256"}],
        "name": "transfer",
        "outputs": [{"name": "", "type": "bool"}],
        "type": "function"
    }
]

async def handle_check_transaction_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    # Извлекаем данные из callback_data
    action, total_price, total_days = query.data.split(':')  # Разделяем по ":"
    total_price = int(total_price)  # Преобразуем стоимость в число
    total_days = int(total_days)  # Преобразуем количество дней в число

    # Получаем пользователя из CallbackQuery
    user = query.from_user

    # Сохраняем total_price и total_days в контексте пользователя
    context.user_data["total_price"] = total_price
    context.user_data["total_days"] = total_days

    # Отправляем сообщение с запросом хэша транзакции
    await query.edit_message_text("Привет! Введи хэш транзакции на BSC, чтобы проверить оплату.",
                                  reply_markup=
                                  InlineKeyboardMarkup([
                                      [InlineKeyboardButton("Назад", callback_data="choose_payment")]
                                  ])
                                  )

    # Устанавливаем флаг, что мы ждём ввод хэша
    context.user_data["waiting_for_tx"] = True

    logger.info(f"Запрос на проверку транзакции от пользователя {user.id}")

check_transaction_button_handler = CallbackQueryHandler(handle_check_transaction_button, pattern=r"^check_transaction:\d+:\d+$")


async def handle_transaction_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("Проверяем транзакцию")
    if not context.user_data.get("waiting_for_tx"):
        logger.info("Игнорируем ввод, так как не запрашивали хэш транзакции.")
        return  # Игнорируем, если мы не запрашивали ввод

    tx_hash = update.message.text.strip()
    context.user_data["waiting_for_tx"] = False  # Сбросим флаг

    total_amount = context.user_data["total_price"]
    total_days = context.user_data["total_days"]

    # Получаем пользователя из текстового сообщения
    user = update.message.from_user

    logger.info(f"Получен хэш транзакции от пользователя {user.id}: {tx_hash}")
    try:
        # Проверяем, был ли хэш уже использован
        if is_transaction_used(tx_hash):
            logger.error(f"Хэш транзакции {tx_hash} уже был использован.")
            await update.message.reply_text("❌ Ошибка: Этот хэш транзакции уже был использован.", reply_markup=get_payment_error_keyboard(total_amount, total_days))
            return

        # Проверяем, существует ли транзакция
        if not web3.is_connected():
            logger.error("Не удалось подключиться к Binance Smart Chain.")
            await update.message.reply_text("❌ Ошибка: Не удалось подключиться к сети BSC.", reply_markup=get_payment_error_keyboard(total_amount, total_days))
            return

        logger.info("Подключение к BSC успешно.")

        # Получение данных о транзакции
        transaction = web3.eth.get_transaction(tx_hash)
        if not transaction:
            logger.error(f"Транзакция {tx_hash} не найдена.")
            await update.message.reply_text("❌ Ошибка: Транзакция не найдена.", reply_markup=get_payment_error_keyboard(total_amount, total_days))
            return

        logger.info(f"Данные транзакции получены: {transaction}")

        receipt = web3.eth.get_transaction_receipt(tx_hash)
        if receipt['status'] != 1:
            logger.error(f"Транзакция {tx_hash} завершилась с ошибкой.")
            await update.message.reply_text("❌ Ошибка: Транзакция завершилась с ошибкой.", reply_markup=get_payment_error_keyboard(total_amount, total_days))
            return

        logger.info("Транзакция успешно выполнена.")

        # Проверка, является ли адрес контрактом
        is_contract = web3.eth.get_code(transaction['to']) != b''
        if not is_contract or transaction['to'].lower() != USDT_CONTRACT_ADDRESS.lower():
            logger.error(f"Транзакция {tx_hash} не связана с контрактом USDT.")
            await update.message.reply_text("❌ Ошибка: Транзакция не связана с контрактом USDT.", reply_markup=get_payment_error_keyboard(total_amount, total_days))
            return

        logger.info("Транзакция связана с контрактом USDT.")

        # Декодирование входных данных
        contract = web3.eth.contract(address=transaction['to'], abi=bep20_abi)
        decoded_input = contract.decode_function_input(transaction['input'])
        recipient = decoded_input[1]['_to']
        amount = decoded_input[1]['_value']

        token_decimals = contract.functions.decimals().call()
        amount_in_tokens = amount / (10 ** token_decimals)

        logger.info(f"Расшифрованы данные транзакции: получатель={recipient}, сумма={amount_in_tokens}.")

        # Проверка адреса получателя и суммы

        wallet, chain = get_primary_wallet()

        if recipient != wallet:
            logger.error(f"Транзакция {tx_hash} проведена не на указанный кошелек {recipient}.")
            message = "❌ Ошибка: Транзакция не соответствует требованиям\\. " \
                      "Указанный получатель не соответствует нашему кошельку\\. \n" \
                      "В случае возникновения вопросов обратитесь к [@Avgust52](https://t.me/Avgust52 )\\."

            await update.message.reply_text(
                message,
                reply_markup=get_payment_error_keyboard(total_amount, total_days),
                parse_mode='MarkdownV2'
            ),

            return

        if amount_in_tokens < total_amount:
            logger.error(f"Транзакция {tx_hash} проведена на сумму {amount_in_tokens}.")
            message = (
                "❌ Ошибка: Транзакция не соответствует требованиям\\. "
                "Переведенная сумма не соответствует тарифному плану\\. "
                f"В рамках транзакции была переведена сумма {amount_in_tokens}\\. \n"
                "В случае возникновения вопросов обратитесь к [@Avgust52](https://t.me/Avgust52 )\\."
            )

            await update.message.reply_text(
                message,
                reply_markup=get_payment_error_keyboard(total_amount, total_days),
                parse_mode='MarkdownV2'
            )
            return

        # Обновляем подписку у юзера
        new_end_date = update_subscription_service(total_days, user.id)

        reply = (
            f"📥 Пополнение обнаружено!\n"
            f"📦 Получатель: `{recipient}`\n"
            f"🪙 Токен: USDT\n"
            f"💰 Сумма: `{amount_in_tokens:.6f} USDT`\n"
            f"🎉 Подписка активирована до {new_end_date}"
        )

        # Сохраняем успешную транзакцию в базу данных
        save_transaction(tx_hash, amount_in_tokens, "USDT", user.id)

        await update.message.reply_text(reply, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Мой профиль", callback_data="main_profile")]])
                                        )

    except Exception as e:
        logger.error(f"Ошибка при обработке транзакции {tx_hash}: {str(e)}")
        await update.message.reply_text(f"❌ Ошибка при обработке транзакции: {str(e)}", reply_markup=get_payment_error_keyboard(total_amount, total_days))

