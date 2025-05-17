from telegram import Update, LabeledPrice, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CallbackQueryHandler, ContextTypes, PreCheckoutQueryHandler, MessageHandler, filters

from keyboards.payment.choose_payment_keyboard import get_fp_club_choose_period_keyboard
from perisist.price.price_dao import get_price_for_rub_by_period, get_total_day_for_rub
from perisist.transaction.transaction_dao import save_transaction
from service.profile.update_subscription_service import update_subscription_service

CARD_METHOD = "card"

async def handle_choose_period_card_payment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    # Формируем динамический текст с учетом стоимости
    payment_text = ("""
        Выберите срок на который хотите получить подписку
    """
    )

    await query.edit_message_text(
        text=payment_text,
        reply_markup=get_fp_club_choose_period_keyboard(CARD_METHOD)
    )

choose_period_card_payment = CallbackQueryHandler(handle_choose_period_card_payment, pattern="^payment_card$")


async def handle_card_payment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    # Извлекаем значение из callback_data
    action, total_month = query.data.split(':')  # Например: payment_card:5
    total_month = int(total_month)

    # Получаем данные из БД или других функций
    total_price = int(get_price_for_rub_by_period(total_month) * 100)  # сумма в копейках
    total_days = get_total_day_for_rub(total_month)

    # Параметры для счета
    title = "Подписка"
    description = f"Оплата подписки на {total_days} дней"
    payload = f"subscription:{total_month}:{total_days}:{total_price}"
    provider_token = "381764678:TEST:124171"  # заменить на реальный токен
    currency = "RUB"
    start_parameter = "prod"

    # Формируем чек для фискализации
    provider_data = {
        "receipt": {
            "customer": {
                # Email будет передан автоматически, если пользователь его предоставит
            },
            "items": [
                {
                    "description": "Подписка на сервис",
                    "quantity": 1,
                    "amount": {
                        "value": f"{total_price / 100:.2f}",  # сумма в рублях
                        "currency": "RUB"
                    },
                    "vat_code": 1,  # Без НДС
                    "payment_mode": "full_payment",
                    "payment_subject": "commodity"
                }
            ]
        }
    }

    # Цены
    prices = [LabeledPrice(label="Подписка", amount=total_price)]

    # Отправляем счет с фискальными данными и запросом email
    await context.bot.send_invoice(
        chat_id=query.message.chat_id,
        title=title,
        description=description,
        payload=payload,
        provider_token=provider_token,
        currency=currency,
        prices=prices,
        start_parameter=start_parameter,

        # Запрашиваем email у пользователя
        need_email=True,
        send_email_to_provider=True,  # Отправляем email в ЮKassa

        # Передаем чек
        provider_data=provider_data
    )
card_payment = CallbackQueryHandler(handle_card_payment, pattern=r"^payment_card:\d+$")


async def precheckout_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.pre_checkout_query
    # Вы должны ответить в течение 10 секунд!
    await query.answer(ok=True)

precheckout_card_operation = PreCheckoutQueryHandler(precheckout_callback)


async def successful_payment_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    payment = update.message.successful_payment
    payload = payment.invoice_payload
    transaction_id = payment.provider_payment_charge_id

    _, total_month, total_days, total_price = payload.split(':')  # Разделяем по ":"
    total_price = int(total_price)  # Преобразуем стоимость в число
    total_days = int(total_days)  # Преобразуем количество дней в числ

    user_id = update.effective_user.id

    # Обновляем подписку у юзера
    new_end_date = update_subscription_service(total_days, user_id)

    # Сохраняем айди транзакции в базу
    save_transaction(transaction_id, total_price, "RUB", user_id)

    # Логика после оплаты: выдача подписки, запись в БД и т.п.
    chat_id = update.message.chat_id
    await context.bot.send_message(
        chat_id=chat_id,
        text="✅ Спасибо за покупку!\n"
             f"🎉 Подписка активирована до {new_end_date}",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Мой профиль", callback_data="main_profile")]])
    )

    # Здесь можно обновить статус подписки пользователя в БД
    print(f"Платеж прошел: {transaction_id}, payload={payload}")

successful_card_payment = MessageHandler(filters.SUCCESSFUL_PAYMENT, successful_payment_callback)
