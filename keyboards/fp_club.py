from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def get_fp_club_keyboard(subscription_status):
    # Создаем пустой список для кнопок
    buttons = [[InlineKeyboardButton("Программа эфиров", callback_data="program_step_1")]]

    if subscription_status == "active":
        buttons.append([InlineKeyboardButton("Мой профиль", callback_data="main_profile")])
    elif subscription_status == "inactive":
        buttons.append([InlineKeyboardButton("Оплатить", callback_data="choose_payment")])

    buttons.append([InlineKeyboardButton("Назад", callback_data="main_menu")])

    return InlineKeyboardMarkup(buttons)
