import os
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from telegram.ext import ApplicationBuilder, MessageHandler, filters
from database import init_db
from handlers.fpClub.coupon.coupon_handler import enter_promo_button_handler
from handlers.fpClub.payment.choose_payment_handler import choose_payment
from handlers.fpClub.profile.profle_handler import profile_handler

# Хендлеры
from handlers.start_handler import start_handler
from handlers.academy_handler import academy_handler
from handlers.fpClub.fp_club_handler import fp_club_handler
from handlers.fpClub.programOfStream.step1 import program_of_streams_step1_handler
from handlers.fpClub.programOfStream.step2 import program_of_streams_step2_handler
from handlers.fpClub.programOfStream.step3 import program_of_streams_step3_handler
from handlers.fpClub.programOfStream.step4 import program_of_streams_step4_handler
from handlers.fpClub.transaction.transactoin_handler import check_transaction_button_handler
from handlers.fpClub.payment.payment_hanlder import payment_handler
from handlers.main_menu_handler import main_menu_handler
from handlers.user_message_handlers import handle_message
from service.scheduler.scheduler import check_subscriptions

if __name__ == '__main__':

    # Токен бота берется из переменной окружения
    BOT_TOKEN = os.getenv("BOT_TOKEN")

    if not BOT_TOKEN:
        raise ValueError("BOT_TOKEN не найден в переменных окружения!")

    init_db()

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(start_handler)
    app.add_handler(academy_handler)
    app.add_handler(fp_club_handler)
    app.add_handler(program_of_streams_step1_handler)
    app.add_handler(program_of_streams_step2_handler)
    app.add_handler(program_of_streams_step3_handler)
    app.add_handler(program_of_streams_step4_handler)
    app.add_handler(check_transaction_button_handler)
    # app.add_handler(transaction_input_handler)
    app.add_handler(enter_promo_button_handler)
    # app.add_handler(promo_input_handler)
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(payment_handler)
    app.add_handler(choose_payment)
    app.add_handler(main_menu_handler)
    app.add_handler(profile_handler)

    # Настройка шедулера
    scheduler = AsyncIOScheduler(timezone="Europe/Moscow")  # Указываем часовой пояс МСК
    scheduler.add_job(check_subscriptions, "cron", hour=10, minute=0, args=[BOT_TOKEN])
    # Для тестирования: выполнить задачу через 5 секунд после запуска
    # scheduler.add_job(check_subscriptions, "interval", seconds=5, args=[BOT_TOKEN], id="test_job")
    scheduler.start()

    app.run_polling()