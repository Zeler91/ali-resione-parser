from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import os
from aliresinparser import search_product_by_attributes, insert_product_data_in_db
from dotenv import load_dotenv
import datetime
import sqlitemanager as sqlm

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
    table_name = 'resione'
    sql = sql_request_from_table(table_name)
    data = sqlm.select_data(sql['last_row'])
    await update.message.reply_text(f'{data[3]}\n{data[0]} : {data[1]} \n url: {data[2]}')

async def refresh_data(context: ContextTypes.DEFAULT_TYPE) -> None:
    await context.bot.send_message(chat_id=context.job.chat_id, 
                                   text=f'Сегодня: {datetime.datetime.now()}')  
    resione = search_product_by_attributes()
    # resione_coupon = resione['coupon']

    if type(resione) is dict:
        current_date = datetime.datetime.now(TIMEZONE).date().strftime('%d.%m.%Y')
        resione['date'] = f'{current_date}'
        insert_product_data_in_db('resione', resione)
        await context.bot.send_message(chat_id=context.job.chat_id,
                                   text=f'Данные успешно обновились!')
    else:
        await context.bot.send_message(chat_id=context.job.chat_id, text=resione)

    # if type(resione_coupon) is dict:
    #     await context.bot.send_message(chat_id=context.job.chat_id, 
    #                                    text=f'Купон на: {resione_coupon["discount"]} \
    #                                    \n{resione_coupon["info"]} \
    #                                    \nСрок купона: {resione_coupon["coupon_timer"]}')
    # else:
    #     await context.bot.send_message(chat_id=context.job.chat_id, text=resione_coupon)


async def callback_daily(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text=f'Вы будете получать инфо каждый день в {TIME_INFO}')
    context.job_queue.run_daily(refresh_data, TIME_INFO, 
                                chat_id=update.message.chat_id)

async def callback_once(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text=f'Данные обновятся через несколько секунд...')
    context.job_queue.run_once(refresh_data, 0,
                               chat_id=update.message.chat_id)


app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("hello", hello))
app.add_handler(CommandHandler("show", show_data))
app.add_handler(CommandHandler('search', callback_once))
# app.add_handler(CommandHandler('start', callback_start))

app.run_polling()
