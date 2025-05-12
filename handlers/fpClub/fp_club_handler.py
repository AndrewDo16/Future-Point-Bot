from telegram import Update
from telegram.ext import CallbackQueryHandler, ContextTypes

from database import add_user, get_subscription_status
from keyboards.fp_club import get_fp_club_keyboard
from texts.fp_club_texts import FP_CLUB_TEXT

async def handle_fp_club(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user = update.effective_user
    user_id = user.id
    username = user.username or user.first_name

    # Добавляем пользователя в базу данных
    add_user(user_id, username)

    # Проверяем статус подписки пользователя
    subscription_status, end_date, _ = get_subscription_status(user_id)

    if query.data == "fp_club":
        await query.edit_message_text(FP_CLUB_TEXT, reply_markup=get_fp_club_keyboard(subscription_status))

fp_club_handler = CallbackQueryHandler(handle_fp_club, pattern="^fp_club$")