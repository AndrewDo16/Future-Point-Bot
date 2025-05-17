from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def get_crypto_payment_keyboard(total_price, total_days):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("Проверить оплату криптой", callback_data=f"check_transaction:{total_price}:{total_days}")],
        [InlineKeyboardButton("Назад", callback_data=f"payment_crypto")]
    ])