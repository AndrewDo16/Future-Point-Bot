import logging

from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes

from perisist.users.users_dao import get_subscription_status

logger = logging.getLogger(__name__)


async def handle_chat_member_update(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message

    if not message or not message.new_chat_members:
        return

    chat = message.chat
    logger.info(f"Сработал событие new_chat_members в чате {chat.id}")

    for user in message.new_chat_members:
        user_id = user.id
        username = user.username or "N/A"
        logger.info(f"Новый участник через new_chat_members: {user_id} ({username})")

        # Защита от бана самого бота
        if user_id == context.bot.id:
            logger.info("Бот был добавлен в группу как участник")
            continue

        # Проверяем подписку
        subscription_data = get_subscription_status(user_id)
        if subscription_data is None:
            logger.warning(f"Пользователь {user_id} не найден в базе данных")
            subscription_status = "inactive"
        else:
            subscription_status = subscription_data[0]

        if subscription_status != "active":
            logger.warning(f"Пользователь {user_id} не имеет активной подписки. Статус: {subscription_status}")
            try:
                await context.bot.ban_chat_member(chat_id=chat.id, user_id=user_id)
                await context.bot.unban_chat_member(chat_id=chat.id, user_id=user_id)
                logger.info(f"Пользователь {user_id} удален из группы {chat.id}")

                try:
                    await context.bot.send_message(
                        chat_id=user_id,
                        text="Вы были удалены из группы, так как у вас нет активной подписки. Желаете оформить подписку?",
                        reply_markup=InlineKeyboardMarkup([
                            [InlineKeyboardButton("Попробовать снова", callback_data="choose_payment")],
                        ])
                    )
                except Exception as e:
                    logger.error(f"Не удалось отправить сообщение пользователю {user_id}: {e}")

            except Exception as e:
                logger.error(f"Ошибка при удалении пользователя {user_id}: {e}")

# async def handle_chat_member_update(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     logger.info("Сработал handle_chat_member_update")
#     chat_member = update.chat_member
#     chat = chat_member.chat
#     new_member = chat_member.new_chat_member
#
#     # Защита от событий без информации
#     if not chat or not new_member or not new_member.user:
#         logger.debug("Получено некорректное обновление chat_member")
#         return
#
#     user = new_member.user
#     user_id = user.id
#     username = user.username or "N/A"
#
#     logger.info(f"Новый участник в чате {chat.id}: user_id={user_id}, username={username}")
#
#     # Защита от бана самого бота
#     if user_id == context.bot.id:
#         logger.info("Бот был добавлен в группу как участник")
#         return
#
#     # Получаем данные о подписке
#     subscription_data = get_subscription_status(user_id)
#     if subscription_data is None:
#         logger.warning(f"Пользователь {user_id} не найден в базе данных")
#         subscription_status = "inactive"
#     else:
#         subscription_status = subscription_data[0]
#
#     if subscription_status != "active":
#         logger.warning(f"Пользователь {user_id} не имеет активной подписки. Статус: {subscription_status}")
#         try:
#             # Блокируем пользователя
#             await context.bot.ban_chat_member(chat_id=chat.id, user_id=user_id)
#             # Разблокируем, чтобы можно было снова добавить
#             await context.bot.unban_chat_member(chat_id=chat.id, user_id=user_id)
#             logger.info(f"Пользователь {user_id} успешно удален из группы {chat.id}")
#
#             # Уведомляем пользователя
#             try:
#                 await context.bot.send_message(
#                     chat_id=user_id,
#                     text="Вы были удалены из группы, так как у вас нет активной подписки. Желаете оформить подписку?",
#                     reply_markup=InlineKeyboardMarkup([
#                         [InlineKeyboardButton("Попробовать снова", callback_data="choose_payment")],
#                     ])
#                 )
#             except Exception as e:
#                 logger.error(f"Не удалось отправить сообщение пользователю {user_id}: {e}")
#
#         except Exception as e:
#             logger.error(f"Ошибка при удалении пользователя {user_id}: {e}")