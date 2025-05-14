from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def get_list_group_keyboard():
    return InlineKeyboardMarkup([

        [InlineKeyboardButton("FP_CLUB", callback_data="fp_club_group")],

        [InlineKeyboardButton("Назад", callback_data="main_profile")]
    ])