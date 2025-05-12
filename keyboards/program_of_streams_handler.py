from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def get_program_menu(current_block, next_block, prev_block, subscription_status):

    buttons = []

    if subscription_status == "active":
        buttons.append([InlineKeyboardButton("Мой профиль", callback_data="main_profile")])
    elif subscription_status == "inactive":
        buttons.append([InlineKeyboardButton("Оплатить", callback_data="choose_payment")])

    buttons.append([InlineKeyboardButton("Назад", callback_data="fp_club")])
    buttons.append([InlineKeyboardButton("<-", callback_data=prev_block),
         InlineKeyboardButton(f"{current_block + 1} / 4", callback_data="dont_click"),
         InlineKeyboardButton("->", callback_data=next_block)])

    return InlineKeyboardMarkup(buttons)