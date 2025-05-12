from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes, CallbackQueryHandler
from keyboards.academy import get_academy_keyboard
from texts.intro_texts import ACADEMY_TEXT
from texts.course_texts import course_texts

async def handle_academy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "academy":
        await query.edit_message_text(ACADEMY_TEXT, reply_markup=get_academy_keyboard())

    elif data in course_texts:
        course = course_texts[data]
        buttons = [
            [InlineKeyboardButton("Иду на курс", url=course["url"])],
            [InlineKeyboardButton("Назад", callback_data="academy")]
        ]
        await query.edit_message_text(course["text"], reply_markup=InlineKeyboardMarkup(buttons))

academy_handler = CallbackQueryHandler(handle_academy, pattern="^(academy|crypto|trading|culture|aesthetics|religion|psychology|ethics)$")