from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CallbackQueryHandler

from database import get_chat_id_by_group_name


async def generate_invite(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    # Извлекаем данные из callback_data
    group_name = query.data

    # Получаем chat_id из базы данных
    chat_id = get_chat_id_by_group_name(group_name)

    if not chat_id:
        await query.edit_message_text("Ошибка: Группа не найдена.")
        return

    try:
        invite_link = await context.bot.create_chat_invite_link(
            chat_id=chat_id,
            name=f"Ссылка для {group_name}",
            expire_date=None,  # никогда не истекает
            member_limit=1  # только один пользователь может присоединиться
        )
        await query.edit_message_text(f"🔗 Ваша индивидуальная ссылка::\n{invite_link.invite_link}",
                                      reply_markup=InlineKeyboardMarkup([
                                          [InlineKeyboardButton("Назад", callback_data="main_profile")]
                                      ])
                                      )
    except Exception as e:
        await query.edit_message_text(f"Ошибка: {e}")


generate_invite_handler = CallbackQueryHandler(generate_invite, pattern="^(fp_club_group|etc)$")
