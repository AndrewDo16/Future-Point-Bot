from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def get_payment_keyboard(total_price, total_days):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("Оплатить в Telegram", callback_data="pay_in_telegram")],
        [InlineKeyboardButton("Проверить оплату криптой", callback_data=f"check_transaction:{total_price}:{total_days}")],
        [InlineKeyboardButton("Назад", callback_data="choose_payment")]
    ])