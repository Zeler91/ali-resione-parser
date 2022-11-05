from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import os
from ali_resione_parser import search_product_by_attributes
from dotenv import load_dotenv
import datetime

load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')
LOCAL_TIMEZONE = datetime.datetime.now(datetime.timezone.utc).astimezone().tzinfo
time_info = datetime.time(23, 59, 00, 0000, tzinfo=LOCAL_TIMEZONE)

async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_name = update.effective_user.full_name
    await update.message.reply_text(f'Hello {user_name}')

async def start_search(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    resione = search_product_by_attributes()
    if type(resione) is dict:
        await update.message.reply_text(f'{resione["title"]} \n{resione["price"]} \n{resione["url"]}')
    else:
        await update.message.reply_text(resione)

async def callback_daily_hello(context: ContextTypes.DEFAULT_TYPE) -> None:
    await context.bot.send_message(chat_id=context.job.chat_id, text=f'Today: {datetime.datetime.now()}')

async def callback_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await context.bot.send_message(chat_id=update.effective_chat.id, text=f'Вы будете получать инфо каждый день в {time_info}')
    context.job_queue.run_daily(callback_daily_hello, time_info, chat_id=update.message.chat_id)

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("hello", hello))
app.add_handler(CommandHandler("search", start_search))
app.add_handler(CommandHandler('callback', callback_start))

app.run_polling()
