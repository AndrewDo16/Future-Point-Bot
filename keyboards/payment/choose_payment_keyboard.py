from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def get_fp_club_choose_payment_keyboard():
    # Создаем пустой список для кнопок
    buttons = []

    # Добавляем кнопки с разными значениями для периода оплаты
    periods = [
        {"label": "1 месяц", "value": "1"},
        {"label": "3 месяца", "value": "3"}
    ]

    for period in periods:
        label = f"Оплатить ({period['label']})"
        callback_data = f"payment:{period['value']}"
        buttons.append([InlineKeyboardButton(label, callback_data=callback_data)])

    buttons.append([InlineKeyboardButton("Ввести промокод", callback_data="enter_promo")])
    buttons.append([InlineKeyboardButton("Назад", callback_data="fp_club")])

    return InlineKeyboardMarkup(buttons)
