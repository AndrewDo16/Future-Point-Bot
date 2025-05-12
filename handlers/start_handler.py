from telegram import Update
from telegram.ext import CommandHandler, ContextTypes

from keyboards.main_menu import get_main_menu
from texts.intro_texts import WELCOME_TEXT


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    first_name = update.effective_user.first_name
    text = WELCOME_TEXT.format(first_name=first_name)
    keyboard = get_main_menu()

    await update.message.reply_text(text, reply_markup=keyboard)

start_handler = CommandHandler("start", start)