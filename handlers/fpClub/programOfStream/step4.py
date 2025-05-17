from telegram import Update
from telegram.ext import CallbackQueryHandler, ContextTypes

from perisist.users.users_dao import get_subscription_status
from keyboards.program_of_streams_handler import get_program_menu
from texts.fp_club_program_texts import PROGRAM_OF_STREAMS_TEXT, PROGRAM_OF_STREAMS_END_TEXT, BLOCK_TEXTS


# Хендлеры, действия и ConversationHandler
async def handle_program_of_streams_step4(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user = update.effective_user
    user_id = user.id

    # Проверяем статус подписки пользователя
    subscription_status, end_date = get_subscription_status(user_id)

    # Отправляем сообщение с блоком 1

    await query.edit_message_text(PROGRAM_OF_STREAMS_TEXT + BLOCK_TEXTS[3] + PROGRAM_OF_STREAMS_END_TEXT,
                                  reply_markup=get_program_menu(3, "dont_clik", "program_step_3", subscription_status))

# Регистрация хендлеров
program_of_streams_step4_handler = CallbackQueryHandler(handle_program_of_streams_step4, pattern="^program_step_4")