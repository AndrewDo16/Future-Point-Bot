import os

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from telegram.ext import ApplicationBuilder, MessageHandler, filters

from config.bot_config import BOT_TOKEN
from perisist.database import init_db
from handlers.fpClub.coupon.coupon_handler import enter_promo_button_handler
from handlers.fpClub.payment.card.card_payment_handler import choose_period_card_payment, card_payment, \
    successful_card_payment, precheckout_card_operation
from handlers.fpClub.payment.choose_payment_handler import choose_payment
from handlers.fpClub.payment.crypto.crypto_payment_handler import choose_period_crypto_payment, crypto_payment
from handlers.fpClub.profile.group.chat_member_handler import handle_chat_member_update
from handlers.fpClub.profile.group.list_group_handler import list_group_handler
from handlers.fpClub.profile.group.invite.generate_invite_handler import generate_invite_handler
from handlers.fpClub.profile.profle_handler import profile_handler
from handlers.help_handler import helper_handler

# Хендлеры
from handlers.start_handler import start_handler
from handlers.academy_handler import academy_handler
from handlers.fpClub.fp_club_handler import fp_club_handler
from handlers.fpClub.programOfStream.step1 import program_of_streams_step1_handler
from handlers.fpClub.programOfStream.step2 import program_of_streams_step2_handler
from handlers.fpClub.programOfStream.step3 import program_of_streams_step3_handler
from handlers.fpClub.programOfStream.step4 import program_of_streams_step4_handler
from handlers.fpClub.payment.crypto.transaction.transactoin_handler import check_transaction_button_handler
from handlers.main_menu_handler import main_menu_handler
from handlers.user_message_handlers import handle_message
from service.scheduler.scheduler import check_subscriptions

if __name__ == '__main__':

    # Токен бота берется из переменной окружения
    BOT_TOKEN = BOT_TOKEN

    if not BOT_TOKEN:
        raise ValueError("BOT_TOKEN не найден в переменных окружения!")

    init_db()

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # CommandHandler отправляются c слешем
    app.add_handler(start_handler)
    app.add_handler(helper_handler)

    # Message Handler
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Academy Handler
    app.add_handler(academy_handler)


    app.add_handler(fp_club_handler)
    app.add_handler(program_of_streams_step1_handler)
    app.add_handler(program_of_streams_step2_handler)
    app.add_handler(program_of_streams_step3_handler)
    app.add_handler(program_of_streams_step4_handler)
    app.add_handler(main_menu_handler)
    app.add_handler(profile_handler)


    # Хендлеры отвечающие за оплату подписки
    app.add_handler(choose_period_card_payment)
    app.add_handler(choose_period_crypto_payment)
    app.add_handler(crypto_payment)
    app.add_handler(card_payment)
    app.add_handler(choose_payment)
    app.add_handler(precheckout_card_operation)
    app.add_handler(successful_card_payment)
    app.add_handler(check_transaction_button_handler)
    app.add_handler(enter_promo_button_handler)


    app.add_handler(generate_invite_handler)
    app.add_handler(list_group_handler)

    # Отслеживание плохишей, которые не купили подписку
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, handle_chat_member_update))

    # Настройка шедулера
    scheduler = AsyncIOScheduler(timezone="Europe/Moscow")  # Указываем часовой пояс МСК
    scheduler.add_job(check_subscriptions, "cron", hour=10, minute=0, args=[BOT_TOKEN])
    # Для тестирования: выполнить задачу через 5 секунд после запуска
    # scheduler.add_job(check_subscriptions, "interval", seconds=5, args=[BOT_TOKEN], id="test_job")
    scheduler.start()

    app.run_polling()