import logging

from telegram import Update
from telegram.ext import CommandHandler, ContextTypes

from perisist.group.group_dao import get_all_group
from keyboards.main_menu import get_main_menu


async def helper(update: Update, context: ContextTypes.DEFAULT_TYPE):
    all_group = get_all_group()
    chat_id = update.effective_chat.id

    for group in all_group:
        if chat_id == group:
            logging.info("Был вызов команды из группы. Прекращаем выполнение")
            return

    first_name = update.effective_user.first_name
    text = (
        f"Привет, {first_name}! 🌟\n"
        "Если у тебя возникли какие-либо вопросы или нужна помощь — "
        "смело пиши нам на почту или в личные сообщения Telegram. Мы всегда на связи и готовы помочь!"
    )
    keyboard = get_main_menu()

    await update.message.reply_text(text, reply_markup=keyboard)

helper_handler = CommandHandler("help", helper)