from datetime import datetime, timedelta
from telegram import Bot
from database import get_all_users, get_subscription_status, set_reminder_sent

# Функция для проверки подписок
async def check_subscriptions(bot_token):
    bot = Bot(token=bot_token)
    today = datetime.now().date()

    # Получаем всех пользователей из базы данных
    users = get_all_users()

    for user in users:
        user_id = user[0]
        subscription_status, subscription_end_date, reminder_sent = get_subscription_status(user_id)

        if subscription_status == "active" and subscription_end_date:
            end_date = datetime.strptime(subscription_end_date, "%Y-%m-%d").date()
            days_left = (end_date - today).days

            # Если до конца подписки осталось 7 дней или меньше
            if 0 < days_left <= 7:
                if not reminder_sent:
                    # Отправляем напоминание
                    message = f"⚠️ У вас осталось {days_left} дней до окончания подписки. Пожалуйста, продлите её!"
                    await bot.send_message(chat_id=user_id, text=message)

                    # Обновляем флаг напоминания
                    set_reminder_sent(user_id, True)
            elif days_left <= 0:
                # Подписка истекла
                message = "❌ Ваша подписка истекла. Пожалуйста, продлите её, чтобы продолжить использование."
                await bot.send_message(chat_id=user_id, text=message)
            else:
                # Сбрасываем флаг напоминания, если подписка ещё активна и больше 7 дней
                set_reminder_sent(user_id, False)