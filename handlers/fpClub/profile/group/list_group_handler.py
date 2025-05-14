from telegram import Update
from telegram.ext import ContextTypes, CallbackQueryHandler

from keyboards.profile.group.list_group_keyboard import get_list_group_keyboard


async def list_group(update: Update, context: ContextTypes.DEFAULT_TYPE):

    # Отправляем ссылку
    await update.callback_query.edit_message_text("👀 Вот наши доступные группы — нажимайте и подключайтесь!", reply_markup=get_list_group_keyboard())


list_group_handler = CallbackQueryHandler(list_group, pattern="^list_group")