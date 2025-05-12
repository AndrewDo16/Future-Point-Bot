from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def get_profile_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("Продлить", callback_data="access_chat")],
        [InlineKeyboardButton("Вести промокод", callback_data="access_chat")],
        [InlineKeyboardButton("Доступы к чатам и каналам", callback_data="access_chat")]
    ])