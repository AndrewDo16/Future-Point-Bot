from telegram import Update
from telegram.ext import CallbackQueryHandler, ContextTypes

from keyboards.payment.choose_payment_keyboard import get_fp_club_choose_payment_keyboard


async def handle_choose_payment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    await query.edit_message_text(
        text="Выберите удобный способ оплаты",
        reply_markup=get_fp_club_choose_payment_keyboard()
    )

choose_payment = CallbackQueryHandler(handle_choose_payment, pattern="^choose_payment")