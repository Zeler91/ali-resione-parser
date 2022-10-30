from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import os
from ali_resione_parser import search_product_by_attributes
from dotenv import load_dotenv

load_dotenv()
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

app.run_polling()