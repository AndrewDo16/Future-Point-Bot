import logging

from telegram import Update
from telegram.ext import CommandHandler, ContextTypes

from perisist.users.users_dao import add_user
from perisist.group.group_dao import get_all_group
from keyboards.main_menu import get_main_menu
from texts.intro_texts import WELCOME_TEXT


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    all_group = get_all_group()
    chat_id = update.effective_chat.id

    for group in all_group:
        if chat_id == group:
            logging.info("Был вызов команды из группы. Прекращаем выполнение")
            return

    first_name = update.effective_user.first_name
    text = WELCOME_TEXT.format(first_name=first_name)
    keyboard = get_main_menu()

    user = update.effective_user
    user_id = user.id
    username = user.username or user.first_name

    # Добавляем пользователя в базу данных
    add_user(user_id, username)

    await update.message.reply_text(text, reply_markup=keyboard)

start_handler = CommandHandler("start", start)