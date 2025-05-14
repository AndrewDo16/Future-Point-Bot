from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def get_profile_keyboard():

    return InlineKeyboardMarkup([

        [InlineKeyboardButton("Продлить", callback_data="choose_payment"),
         InlineKeyboardButton("Вести промокод", callback_data="enter_promo")],

        [InlineKeyboardButton("Доступы к чатам и каналам", callback_data="list_group")],

        [InlineKeyboardButton("Назад", callback_data="fp_club")],
    ])