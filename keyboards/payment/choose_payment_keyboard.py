from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def get_fp_club_choose_payment_keyboard():
    buttons = [[InlineKeyboardButton("Оплатить криптой", callback_data="payment_crypto")],
               [InlineKeyboardButton("Оплатить банковской картой", callback_data="payment_card")],
               [InlineKeyboardButton("Ввести промокод", callback_data="enter_promo")],
               [InlineKeyboardButton("Назад", callback_data="fp_club")]]

    return InlineKeyboardMarkup(buttons)


def get_fp_club_choose_period_keyboard(method):
    # Создаем пустой список для кнопок
    buttons = []

    # Добавляем кнопки с разными значениями для периода оплаты
    periods = [
        {"label": "1 месяц", "value": "1"},
        {"label": "3 месяца", "value": "3"}
    ]

    for period in periods:
        label = f"Оплатить ({period['label']})"
        callback_data = f"payment_{method}:{period['value']}"
        buttons.append([InlineKeyboardButton(label, callback_data=callback_data)])

    buttons.append([InlineKeyboardButton("Назад", callback_data="choose_payment")])

    return InlineKeyboardMarkup(buttons)
