from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import os
from ali_resione_parser import search_product_by_attributes

TOKEN = os.getenv('BOT_TOKEN')


async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_name = update.effective_user.full_name
    await update.message.reply_text(f'Hello {user_name}')

async def start_search(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    resione = search_product_by_attributes()
    await update.message.reply_text(f'{resione["title"]} \n{resione["price"]} \n{ resione["url"]}')

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("hello", hello))
app.add_handler(CommandHandler("search", start_search))

app.run_webhook(listen='52.41.36.82',
    port=8443,
    url_path='TOKEN',
    key=os.getenv('private-ssh'),
    cert=os.getenv('public-ssh'),
    webhook_url='https://api.render.com/deploy/srv-cdc54oo2i3msb93n6jl0?key=kM26ZCQrJbg/' + TOKEN)

# Запускаем приложение
# app.run_polling()