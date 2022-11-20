from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters, _callbackcontext
import os
from aliresinparser import create_resin
from dotenv import load_dotenv
import datetime
import sqlitemanager as sqlm
import json
import sqlite3

with open('./data/static_data.json', 'r') as f:
    data = json.load(f)
    tables = data['tables']
models = ["M68-1000", "M58-500"]
load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')
TIMEZONE = datetime.timezone(datetime.timedelta(hours=3))
TIME_INFO = datetime.time(12, 00, tzinfo=TIMEZONE)
REFRESH_TIME = datetime.time(11, 00, tzinfo=TIMEZONE)
CHANGE_TIMER_ENABLE = False
ADMIN_ID = 430666779

def admin(func):
    async def check_admin(*args):
        for arg in args:
            if type(arg) is _callbackcontext.CallbackContext:
                user_id = arg._chat_id
                break
        else:
            print('foo')
        if user_id == ADMIN_ID:
            await func(*args)
        else:
            await arg.bot.send_message(chat_id=user_id, 
                                text=f'Отказанно в доступе. Используйте аккаунт админа.')
            
    return check_admin

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await hello(update, context)
    await help(update, context)

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Это бот для поиска фотополимерной смолы на AliExpress, вот его команды: \
                                    \n/info - запрос текущих данных по смоле \
                                    \n/timer - настройка таймера сообщений \
                                    \n/hello - привтествие и ID')
    if update.message.chat_id == ADMIN_ID:
        await update.message.reply_text(f'Команды админа: \
                                        \n/refresh - запуск процесса обновления БД\
                                        \n/refresh_daily - ежедневное обновление БД в 11:00')                                   
     
async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_name = update.effective_user.full_name
    await update.message.reply_text(f'Привет, {user_name}. Твой id: {update.message.chat_id}')

async def change_timer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global CHANGE_TIMER_ENABLE

    await update.message.reply_text(f'Введите время вывода сообщений в формате: ЧЧ-ММ')
    CHANGE_TIMER_ENABLE = True
 
async def set_timer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global CHANGE_TIMER_ENABLE, TIME_INFO
    if CHANGE_TIMER_ENABLE:
        timer = update.message.text
        timer_hours = timer.split("-")[0]
        timer_minutes = timer.split("-")[1]
        TIME_INFO = datetime.time(int(timer_hours), int(timer_minutes), tzinfo=TIMEZONE)
        await update.message.reply_text(f'Сообщения будут поступать в {timer_hours}:{timer_minutes}')
        context.job_queue.run_daily(show_data, TIME_INFO,
                                    chat_id=update.message.chat_id)
        CHANGE_TIMER_ENABLE = False


async def show_data(context: ContextTypes.DEFAULT_TYPE) -> None:
    sql_data = []
    for t in tables:
        for m in models:
            try:
                model_data = sqlm.select_data(f'SELECT * \
                                                FROM {t["name"]} \
                                                WHERE ({t["name"]}.product_model = "{m}") \
                                                ORDER BY {t["name"]}.date DESC LIMIT 1')
            except sqlite3.OperationalError:
                pass
            sql_data.append(model_data)
        for sd in sql_data:
            await context.bot.send_message(chat_id=context.job.chat_id,
                                        text=f'{sd[3]} \
                                        \n{sd[0]} {sd[1]}: {sd[2]} \
                                        \nurl: {sd[4]} \
                                        \n\n{sd[5]}')

@admin
async def refresh_data(context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = context.job.chat_id
    if user_id == ADMIN_ID: 
        await context.bot.send_message(chat_id=user_id,
                                    text=f'Данные обновляются, процесс может занять несколько минут...') 
        create_resin(db_acces=True, verbose=False)
        await context.bot.send_message(chat_id=user_id,
                                    text=f'Данные успешно обновлены!')
    else:
        await context.bot.send_message(chat_id=user_id,
                                    text=f'Отказанно в доступе. Используйте аккаунт админа.')

@admin
async def refresh_data_once(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text=f'Запущен процесс обновления данных')
    await context.job_queue.run_once(refresh_data, 0,
                               chat_id=update.message.chat_id)

@admin
async def refresh_data_daily(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text=f'Данные будут обновляться каждый день в {REFRESH_TIME}')
    await context.job_queue.run_daily(refresh_data, REFRESH_TIME, 
                                chat_id=update.message.chat_id)

async def show_data_once(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await context.job_queue.run_once(show_data, 0,
                               chat_id=update.message.chat_id)


app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("hello", hello))
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", help))
app.add_handler(CommandHandler('refresh', refresh_data_once))
app.add_handler(CommandHandler('refresh_daily', refresh_data_daily))
app.add_handler(CommandHandler('info', show_data_once))
app.add_handler(CommandHandler('timer', change_timer))
app.add_handler(MessageHandler(filters.TEXT, set_timer))

app.run_polling()
