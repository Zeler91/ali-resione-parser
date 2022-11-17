from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import os
from aliresinparser import create_resin
from dotenv import load_dotenv
import datetime
import sqlitemanager as sqlm
import json

with open('./data/static_data.json', 'r') as f:
    data = json.load(f)
    tables = data['tables']

load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')
TIMEZONE = datetime.timezone(datetime.timedelta(hours=3))
TIME_INFO = datetime.time(22, 40, tzinfo=TIMEZONE)

def sql_request_from_table(name:str):
    sql_requests = {'all_data':f'SELECT * FROM {name}',
                    'last_row':f'SELECT * FROM {name} DESC LIMIT 1'}
    return sql_requests

async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_name = update.effective_user.full_name
    await update.message.reply_text(f'Hello {user_name}')

async def show_data(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    for t in tables:
        sql = sql_request_from_table(t['name'])
        data = sqlm.select_data(sql['all_data'])
        await update.message.reply_text(f'{data[3]} \
                                        \n{data[0]} {data[1]}: {data[2]} \
                                        \nurl: {data[4]} \
                                        \n\n{data[5]}')

async def refresh_data(context: ContextTypes.DEFAULT_TYPE) -> None:  
    create_resin(db_acces=True, verbose=False)

    # if resione:
    #     resione.insert_product_data_in_db(TABLES[0])
    await context.bot.send_message(chat_id=context.job.chat_id,
                                   text=f'Данные успешно обновились!')
    await context.bot.send_message(chat_id=context.job.chat_id, text=str(resione))

async def callback_daily(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text=f'Вы будете получать инфо каждый день в {TIME_INFO}')
    context.job_queue.run_daily(refresh_data, TIME_INFO, 
                                chat_id=update.message.chat_id)

async def callback_once(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text=f'Данные обновляются, процесс может занять несколько минут...')
    context.job_queue.run_once(refresh_data, 0,
                               chat_id=update.message.chat_id)


app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("hello", hello))
app.add_handler(CommandHandler("show", show_data))
app.add_handler(CommandHandler('refresh', callback_once))
# app.add_handler(CommandHandler('timer', callback_daily))

app.run_polling()
