from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def get_payment_error_keyboard(total_amount, total_days):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("Попробовать снова", callback_data=f"check_transaction:{total_amount}:{total_days}")],
        [InlineKeyboardButton("Назад", callback_data="fp_club")],
    ])
