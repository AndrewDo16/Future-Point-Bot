import logging
from datetime import datetime

from telegram import Bot, InlineKeyboardMarkup, InlineKeyboardButton

from perisist.users.users_dao import update_subscription, get_active_users
from perisist.group.group_dao import get_all_group

PAYMENT_BUTTON = InlineKeyboardMarkup([
                [InlineKeyboardButton("Продлить", callback_data="choose_payment")]
            ])

logger = logging.getLogger(__name__)

# Функция для проверки подписок
async def check_subscriptions(bot_token):
    logger.info("Запуск проверки подписок")
    bot = Bot(token=bot_token)
    today = datetime.now().date()
    logger.info(f"Текущая дата: {today}")

    active_users = get_active_users()
    logger.info(f"Найдено активных пользователей: {len(active_users)}")

    for user in active_users:
        user_id, subscription_end_date = user
        logger.debug(f"Проверяем пользователя {user_id} с датой окончания подписки {subscription_end_date}")

        try:
            if isinstance(subscription_end_date, str):
                end_date = datetime.strptime(subscription_end_date, "%Y-%m-%d").date()
            else:
                end_date = subscription_end_date
        except Exception as e:
            logger.error(f"Ошибка при парсинге даты для пользователя {user_id}: {e}")
            continue

        days_left = (end_date - today).days
        logger.debug(f"Дней до окончания подписки для пользователя {user_id}: {days_left}")

        if 0 < days_left <= 7:
            message = f"⚠️ У вас осталось {days_left} дней до окончания подписки. Пожалуйста, продлите её!"
            try:
                await bot.send_message(chat_id=user_id, text=message, reply_markup=PAYMENT_BUTTON)
                logger.info(f"Отправлено уведомление о продлении подписки пользователю {user_id}")
            except Exception as e:
                logger.error(f"Не удалось отправить сообщение пользователю {user_id}: {e}")

        elif days_left == 0:
            message = "⚠️ Сегодня заканчивается подписка. Пожалуйста, продлите её!"
            try:
                await bot.send_message(chat_id=user_id, text=message, reply_markup=PAYMENT_BUTTON)
                logger.info(f"Отправлено уведомление о завершении подписки пользователю {user_id}")
            except Exception as e:
                logger.error(f"Не удалось отправить сообщение пользователю {user_id}: {e}")

        elif days_left < 0:
            logger.info(f"Подписка истекла у пользователя {user_id}, обрабатываем...")

            all_groups = get_all_group()
            logger.info(f"Список групп для удаления: {all_groups}")

            for group_chat_id in all_groups:
                try:
                    logger.info(f"Удаляем пользователя {user_id} из группы {group_chat_id}")
                    # Сначала бан, затем разбан — это кик без предупреждения
                    await bot.ban_chat_member(chat_id=group_chat_id, user_id=user_id)
                    await bot.unban_chat_member(chat_id=group_chat_id, user_id=user_id)
                    logger.info(f"Пользователь {user_id} успешно удалён из группы {group_chat_id}")
                except Exception as e:
                    logger.error(f"Ошибка при удалении пользователя {user_id} из группы {group_chat_id}: {e}", exc_info=True)

            try:
                message = "❌ Ваша подписка истекла. Пожалуйста, продлите её, чтобы продолжить использование."
                await bot.send_message(chat_id=user_id, text=message, reply_markup=PAYMENT_BUTTON)
                logger.info(f"Отправлено сообщение об истечении подписки пользователю {user_id}")
            except Exception as e:
                logger.error(f"Не удалось отправить сообщение пользователю {user_id}: {e}")

            try:
                update_subscription(user_id, "inactive", None)
                logger.info(f"Статус подписки пользователя {user_id} обновлён на 'inactive'")
            except Exception as e:
                logger.error(f"Не удалось обновить статус подписки для {user_id}: {e}")