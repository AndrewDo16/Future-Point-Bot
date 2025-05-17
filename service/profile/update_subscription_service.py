from perisist.users.users_dao import get_subscription_status, update_subscription
from datetime import datetime, timedelta


STATUS_ACTIVE = "active"

def update_subscription_service(total_days, user_id):
    # Получаем текущий статус подписки и дату окончания
    subscription_status, subscription_end_date = get_subscription_status(user_id)

    # Рассчитываем новую дату окончания подписки
    if subscription_status == STATUS_ACTIVE and subscription_end_date:
        # Если подписка активна, добавляем 30 дней к текущей дате окончания
        current_end_date = datetime.strptime(subscription_end_date, "%Y-%m-%d")
        new_end_date = (current_end_date + timedelta(days=total_days)).strftime("%Y-%m-%d")
    else:
        # Если подписка неактивна, устанавливаем новую дату от текущего момента
        new_end_date = (datetime.now() + timedelta(days=total_days)).strftime("%Y-%m-%d")

    # Обновляем статус подписки
    update_subscription(user_id, STATUS_ACTIVE, new_end_date)

    return new_end_date