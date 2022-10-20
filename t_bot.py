from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

from ali_resione_parser import search_product_by_attributes

TOKEN = '5790801631:AAF1rk_MZJH5bBhRV5Rn3nS-s4z9i7mAemI'


async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_name = update.effective_user.full_name
    await update.message.reply_text(f'Hello {user_name}')

async def start_search(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    resione = search_product_by_attributes()
    await update.message.reply_text(f'{resione["title"]} \n{resione["price"]} \n{ resione["url"]}')

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("hello", hello))
app.add_handler(CommandHandler("search", start_search))

# app.run_webhook(listen='0.0.0.0',
#     port=8443,
#     url_path='TOKEN',
#     webhook_url='https://api.render.com/deploy/srv-cd7i3o2en0hgupusmas0?key=FYfTJtPiyRY/' + TOKEN)

# Запускаем приложение
app.run_polling()