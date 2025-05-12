import logging

from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes, MessageHandler, filters, CallbackQueryHandler

from database import check_promo_code, mark_promo_code_as_used, update_subscription_with_promo, get_subscription_status

logger = logging.getLogger(__name__)

# Обработчик нажатия кнопки "Ввести промокод"
async def handle_enter_promo_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    # Отправляем сообщение с запросом промокода
    await query.edit_message_text("Введите промокод:")

    # Устанавливаем флаг, что мы ждём ввод промокода
    context.user_data["waiting_for_promo"] = True

    logger.info(f"Запрос на ввод промокода от пользователя {update.effective_user.id}")

enter_promo_button_handler = CallbackQueryHandler(handle_enter_promo_button, pattern="^enter_promo$")


# Обработчик ввода промокода
async def handle_promo_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.user_data.get("waiting_for_promo"):
        logger.info("Игнорируем ввод, так как не запрашивали промокод.")
        return  # Игнорируем, если мы не запрашивали ввод

    promo_code = update.message.text.strip()
    context.user_data["waiting_for_promo"] = False  # Сбросим флаг

    user_id = update.effective_user.id
    username = update.effective_user.username or "Неизвестный"

    try:
        # Проверяем, существует ли промокод
        promo_data = check_promo_code(promo_code)
        if not promo_data:
            await update.message.reply_text("❌ Ошибка: Промокод не найден.",
                                            reply_markup=InlineKeyboardMarkup([
                                                [InlineKeyboardButton("Попробовать снова",
                                                                      callback_data="enter_promo")],
                                                [InlineKeyboardButton("Назад", callback_data="fp_club")],
                                            ]))
            return

        days_to_add, is_used = promo_data
        if is_used:
            await update.message.reply_text("❌ Ошибка: Этот промокод уже был использован.",
                                            reply_markup=InlineKeyboardMarkup([
                                                [InlineKeyboardButton("Попробовать снова",
                                                                      callback_data="enter_promo")],
                                                [InlineKeyboardButton("Назад", callback_data="fp_club")],
                                            ]))
            return

        # Помечаем промокод как использованный и сохраняем user_id
        mark_promo_code_as_used(promo_code, user_id)

        # Обновляем подписку пользователя
        update_subscription_with_promo(user_id, days_to_add)

        # Получаем новую дату окончания подписки
        _, subscription_end_date, _ = get_subscription_status(user_id)

        await update.message.reply_text(
            f"🎉 Промокод активирован!\n"
            f"Подписка продлена до {subscription_end_date}."
        )

        logger.info(f"Пользователь {username} (ID: {user_id}) активировал промокод {promo_code}.")

    except Exception as e:
        logger.error(f"Ошибка при обработке промокода {promo_code}: {str(e)}")
        await update.message.reply_text(f"❌ Ошибка при обработке промокода: {str(e)}",
                                        reply_markup=InlineKeyboardMarkup([
                                            [InlineKeyboardButton("Попробовать еще раз", callback_data="fp_club")]
                                        ]))

# promo_input_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, handle_promo_input)