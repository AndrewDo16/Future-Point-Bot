from telegram import Update
from telegram.ext import CallbackQueryHandler, ContextTypes
from keyboards.main_menu import get_main_menu
from texts.intro_texts import WELCOME_TEXT

async def handle_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    text = WELCOME_TEXT.format(first_name=query.from_user.first_name)
    await query.message.reply_text(text, reply_markup=get_main_menu())

main_menu_handler = CallbackQueryHandler(handle_main_menu, pattern="^main_menu$")