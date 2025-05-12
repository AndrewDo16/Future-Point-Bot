from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def get_fp_club_keyboard(subscription_status):
    # Создаем пустой список для кнопок
    buttons = [[InlineKeyboardButton("Программа эфиров", callback_data="program_step_1")]]

    # Добавляем кнопки с разными значениями для периода оплаты
    periods = [
        {"label": "1 месяц", "value": "1"},
        {"label": "3 месяца", "value": "3"}
    ]

    if subscription_status == "active":
        buttons.append([InlineKeyboardButton("Мой профиль", callback_data="main_profile")])
    elif subscription_status == "inactive":
        for period in periods:
            label = f"Оплатить ({period['label']})"
            callback_data = f"payment:{period['value']}"
            buttons.append([InlineKeyboardButton(label, callback_data=callback_data)])

    buttons.append([InlineKeyboardButton("Назад", callback_data="main_menu")])

    return InlineKeyboardMarkup(buttons)
