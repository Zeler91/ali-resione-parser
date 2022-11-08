from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import os
from ali_resione_parser import search_product_by_attributes
from dotenv import load_dotenv
import datetime

load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')
TIMEZONE = datetime.timezone(datetime.timedelta(hours=3))
TIME_INFO = datetime.time(22, 40, tzinfo=TIMEZONE)

async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_name = update.effective_user.full_name
    await update.message.reply_text(f'Hello {user_name}')


async def start_search(context: ContextTypes.DEFAULT_TYPE) -> None:
    await context.bot.send_message(chat_id=context.job.chat_id, 
                                   text=f'Сегодня: {datetime.datetime.now()}')  
    resione = search_product_by_attributes()
    resione_coupon = resione['coupon']

    if type(resione) is dict:
        await context.bot.send_message(chat_id=context.job.chat_id, 
                                       text=f'{resione["title"]} \
                                       \n{resione["price"]} \
                                       \n{resione["url"]}')
    else:
        await context.bot.send_message(chat_id=context.job.chat_id, text=resione)

    if type(resione_coupon) is dict:
        await context.bot.send_message(chat_id=context.job.chat_id, 
                                       text=f'Купон на: {resione_coupon["discount"]} \
                                       \n{resione_coupon["info"]} \
                                       \nСрок купона: {resione_coupon["coupon_timer"]}')
    else:
        await context.bot.send_message(chat_id=context.job.chat_id, text=resione_coupon)


async def callback_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text=f'Вы будете получать инфо каждый день в {TIME_INFO}')
    context.job_queue.run_daily(start_search, TIME_INFO, 
                                chat_id=update.message.chat_id)


app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("hello", hello))
app.add_handler(CommandHandler('start', callback_start))

app.run_polling()
