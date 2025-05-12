from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def get_program_menu(current_block, next_block, prev_block):
    buttons = [
        [InlineKeyboardButton("Оплатить", callback_data="payment")],
        [InlineKeyboardButton("Назад", callback_data="fp_club")],

        [InlineKeyboardButton("<-", callback_data=prev_block),
         InlineKeyboardButton(f"{current_block + 1} / 4", callback_data="dont_click"),
         InlineKeyboardButton("->", callback_data=next_block)]

    ]
    return InlineKeyboardMarkup(buttons)