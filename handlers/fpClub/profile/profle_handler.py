from telegram import Update
from telegram.ext import CallbackQueryHandler, ContextTypes

from database import get_subscription_status
from keyboards.fp_club_profile_keybord import get_profile_keyboard


async def handle_profile(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user = update.effective_user
    user_id = user.id

    # Получаем информацию о профиле
    subscription_status, end_date, _ = get_subscription_status(user_id)

    profile_info = f"👋 Привет, {update.effective_user.first_name}!\n\nВот информация о твоём профиле:"

    if subscription_status == "active":
        profile_info += f"\n\n✅ Подписка: активна\n\n📅 Действует до: {end_date}"
    else:
        profile_info += "\n\n❌ Подписка: неактивна\n\n👉 Вы можете оформить подписку в разделе 'Купить подписку'"

    await query.edit_message_text(
        text=profile_info,
        reply_markup=get_profile_keyboard()
    )

profile_handler = CallbackQueryHandler(handle_profile, pattern="^main_profile")