from telegram import InlineKeyboardMarkup, InlineKeyboardButton

def get_main_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("Академия", callback_data="academy")],
        [InlineKeyboardButton("FP Club", callback_data="fp_club")]
    ])