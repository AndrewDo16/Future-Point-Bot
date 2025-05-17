from telegram import Update
from telegram.ext import CallbackQueryHandler, ContextTypes

from perisist.price.price_dao import get_price_for_usdt_by_period, get_total_day_for_usdt
from keyboards.payment.choose_payment_keyboard import get_fp_club_choose_period_keyboard
from keyboards.payment.crypto.payment_crypto_keyboard import get_crypto_payment_keyboard
from perisist.transaction.wallet.crypto_wallet_dao import get_wallet_for_usdt

CRYPTO_METHOD = "crypto"

async def handle_choose_period_crypto_payment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    # Формируем динамический текст с учетом стоимости
    payment_text = ("""
        Выберите срок на который хотите получить подписку
    """
    )

    await query.edit_message_text(
        text=payment_text,
        reply_markup=get_fp_club_choose_period_keyboard(CRYPTO_METHOD)
    )

choose_period_crypto_payment = CallbackQueryHandler(handle_choose_period_crypto_payment, pattern="^payment_crypto$")


async def handle_crypto_payment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    # Извлекаем значение из callback_data
    action, value = query.data.split(':')  # Разделяем по ":"
    value = int(value)  # Преобразуем значение в число

    # Вычисляем стоимость на основе переданного значения
    total_price = get_price_for_usdt_by_period(value)  # Cтоимость в usdt, берем из базы
    total_days = get_total_day_for_usdt(value) # кол-во дней подписки, берем из базы

    wallet, chain = get_wallet_for_usdt()

    # Формируем динамический текст с учетом стоимости
    payment_text = (
        "💰 <b>Оплата составляет:</b>\n\n"
        f"Стоимость: <b>{total_price} USDT</b>\n"
        f"Сеть: <b>{chain}</b>\n"
        f"Кошелек: <code>{wallet}</code>\n\n"
        # "📲 Или можно оплатить <b>внутри Telegram</b>"
    )

    await query.edit_message_text(
        text=payment_text,
        reply_markup=get_crypto_payment_keyboard(total_price, total_days),
        parse_mode="HTML"
    )

crypto_payment = CallbackQueryHandler(handle_crypto_payment, pattern=r"^payment_crypto:\d+$")