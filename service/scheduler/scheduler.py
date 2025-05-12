from datetime import datetime

from telegram import Bot, InlineKeyboardMarkup, InlineKeyboardButton

from database import update_subscription, get_active_users

PAYMENT_BUTTON = InlineKeyboardMarkup([
                [InlineKeyboardButton("Продлить", callback_data="choose_payment")]
            ])

# Функция для проверки подписок
async def check_subscriptions(bot_token):
    bot = Bot(token=bot_token)
    today = datetime.now().date()

    # Получаем всех активных пользователей из базы данных
    active_users = get_active_users()

    for user in active_users:
        user_id, subscription_end_date = user

        # Преобразуем дату окончания подписки в объект date
        if isinstance(subscription_end_date, str):
            end_date = datetime.strptime(subscription_end_date, "%Y-%m-%d").date()
        else:
            end_date = subscription_end_date

        # Вычисляем количество оставшихся дней
        days_left = (end_date - today).days

        # Если до конца подписки осталось 7 дней или меньше
        if 0 < days_left <= 7:
            # Отправляем напоминание
            message = f"⚠️ У вас осталось {days_left} дней до окончания подписки. Пожалуйста, продлите её!"
            await bot.send_message(chat_id=user_id, text=message, reply_markup=PAYMENT_BUTTON)

        if days_left == 0:
            # Отправляем напоминание
            message = f"⚠️ Сегодня заканчивается подписка. Пожалуйста, продлите её!"
            await bot.send_message(chat_id=user_id, text=message, reply_markup=PAYMENT_BUTTON)


        # Если подписка истекла
        elif days_left < 0:
            # Отправляем сообщение о том, что подписка истекла
            message = "❌ Ваша подписка истекла. Пожалуйста, продлите её, чтобы продолжить использование."
            await bot.send_message(chat_id=user_id, text=message, reply_markup=PAYMENT_BUTTON)

            # Меняем статус подписки на inactive
            update_subscription(user_id, "inactive", None)