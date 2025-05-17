import logging

from telegram import Update
from telegram.ext import ContextTypes

from handlers.fpClub.coupon.coupon_handler import handle_promo_input
from handlers.fpClub.payment.crypto.transaction.transactoin_handler import handle_transaction_input

logger = logging.getLogger(__name__)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text.strip()

    chat_id = update.effective_chat.id
    logger.info(f"ID этого сообщения: {chat_id}. UserId: {user_id}")

    # Проверяем, что мы ожидаем ввод
    if context.user_data.get("waiting_for_promo"):
        # Если ожидаем промокод, вызываем обработчик промокода
        await handle_promo_input(update, context)
    elif context.user_data.get("waiting_for_tx"):
        # Если ожидаем хэш транзакции, вызываем обработчик транзакции
        await handle_transaction_input(update, context)