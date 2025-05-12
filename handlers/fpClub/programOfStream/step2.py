from telegram import Update
from telegram.ext import CallbackQueryHandler, ContextTypes, ConversationHandler
from texts.fp_club_program_texts import PROGRAM_OF_STREAMS_TEXT, PROGRAM_OF_STREAMS_END_TEXT, BLOCK_TEXTS
from texts.fp_club_texts import FP_CLUB_TEXT

from keyboards.fp_club import get_fp_club_keyboard
from keyboards.program_of_streams_handler import get_program_menu


# Состояние разговоров
BLOCK_1, BLOCK_2, BLOCK_3, BLOCK_4 = range(4)

# Хендлеры, действия и ConversationHandler
async def handle_program_of_streams_step2(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    # Отправляем сообщение с блоком 1

    await query.edit_message_text(PROGRAM_OF_STREAMS_TEXT + BLOCK_TEXTS[1] + PROGRAM_OF_STREAMS_END_TEXT, reply_markup=get_program_menu(1, "program_step_3", "program_step_1"))

# Регистрация хендлеров
program_of_streams_step2_handler = CallbackQueryHandler(handle_program_of_streams_step2, pattern="^program_step_2")