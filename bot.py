from apscheduler.schedulers.asyncio import AsyncIOScheduler
from telegram.ext import ApplicationBuilder
from config import TOKEN
from database import init_db
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
from handlers.fpClub.transaction.transactoin_handler import transaction_input_handler
from handlers.fpClub.payment.payment_hanlder import payment_handler
from handlers.main_menu_handler import main_menu_handler
from service.scheduler.scheduler import check_subscriptions

if __name__ == '__main__':
    init_db()

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(start_handler)
    app.add_handler(academy_handler)
    app.add_handler(fp_club_handler)
    app.add_handler(program_of_streams_step1_handler)
    app.add_handler(program_of_streams_step2_handler)
    app.add_handler(program_of_streams_step3_handler)
    app.add_handler(program_of_streams_step4_handler)
    app.add_handler(check_transaction_button_handler)
    app.add_handler(transaction_input_handler)
    app.add_handler(payment_handler)
    app.add_handler(main_menu_handler)
    app.add_handler(profile_handler)

    # Настройка шедулера
    scheduler = AsyncIOScheduler()
    scheduler.add_job(check_subscriptions, "interval", days=1, args=[TOKEN])
    scheduler.start()

    app.run_polling()