from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def get_card_payment_keyboard(total_price, total_days):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("Назад", callback_data=f"payment_card")]
    ])