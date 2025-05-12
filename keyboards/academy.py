from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def get_academy_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("Криптоиндустрия", callback_data="crypto"),
         InlineKeyboardButton("Трейдинг:База", callback_data="trading")],

        [InlineKeyboardButton("Культурология", callback_data="culture"),
         InlineKeyboardButton("Эстетика", callback_data="aesthetics")],

        [InlineKeyboardButton("Религиоведение", callback_data="religion"),
         InlineKeyboardButton("Психология", callback_data="psychology")],

        [InlineKeyboardButton("Этика и этикет", callback_data="ethics")],

        [InlineKeyboardButton("Главное меню", callback_data="main_menu")]
    ])

