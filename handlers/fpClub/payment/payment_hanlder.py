from telegram import Update
from telegram.ext import CallbackQueryHandler, ContextTypes

from database import get_price
from keyboards.payment_keyboard import get_payment_keyboard


async def handle_payment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    # Извлекаем значение из callback_data
    action, value = query.data.split(':')  # Разделяем по ":"
    value = int(value)  # Преобразуем значение в число

    # Вычисляем стоимость на основе переданного значения
    base_price = get_price()  # Базовая стоимость (30 USDT)
    total_price = base_price * value  # Умножаем базовую стоимость на значение
    total_days = value * 30 # Умножаем на 30, чтобы получить кол-во дней

    # Формируем динамический текст с учетом стоимости
    payment_text = (
        "💰 <b>Оплата составляет:</b>\n\n"
        f"Стоимость: <b>{total_price} USDT</b>\n"
        "Сеть: <b>ВЕР20</b>\n"
        "Кошелек: <code>0x695bf46a362204B370e2914bbd5667068bE8f7d0</code>\n\n"
        # "📲 Или можно оплатить <b>внутри Telegram</b>"
    )

    await query.edit_message_text(
        text=payment_text,
        reply_markup=get_payment_keyboard(total_price, total_days),
        parse_mode="HTML"
    )

payment_handler = CallbackQueryHandler(handle_payment, pattern=r"^payment:\d+$")