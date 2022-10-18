from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

from ali_resione_parser import search_product_by_attributes

T_TOKEN = '5790801631:AAF1rk_MZJH5bBhRV5Rn3nS-s4z9i7mAemI'


async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_name = update.effective_user.full_name
    await update.message.reply_text(f'Hello {user_name}')

async def start_search(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    resione = search_product_by_attributes()
    await update.message.reply_text(f'{resione["title"]} \n{resione["price"]} \n{ resione["url"]}')

app = ApplicationBuilder().token(T_TOKEN).build()

app.add_handler(CommandHandler("hello", hello))
app.add_handler(CommandHandler("search", start_search))

app.run_polling()







# # Update - кусок информации полученный нами от Телеграма
# from telegram import Update

# # ApplicationBuilder - способ создать приложение с указанием настроек
# from telegram.ext import ApplicationBuilder, MessageHandler, filters

# from head_hunter import parse_hh
# from sectoken import TOKEN
# # token - секретный ключ к вашему боту (получить у @BotFather)
# app = ApplicationBuilder().token(TOKEN).build()


# # Функция вызывается при получении сообщения
# # upd - новая информация от ТГ
# # ctx - служебная информация
# async def text_reply(upd: Update, _ctx):
#     user_text = upd.message.text
#     print(f"User: {user_text}")
#     # Запустить парсинг
#     name = upd.message.from_user.full_name
#     reply = f"Уважаемый {name}, мы получили ваш запрос '{user_text}'"
#     print(reply)
#     await upd.message.reply_text(reply)
#     jobs_count = parse_hh(user_text)
#     await upd.message.reply_text(f"Найдено вакансий: {jobs_count}")


# # Handler - обработчик сообщения
# handler = MessageHandler(filters.TEXT, text_reply)
# # MessageHandler - для сообщений (текстовые, аудио, анимации, стикеры...)
# # CommandHandler - для команд (типа /hello /start )

# # Прикрепляем обработчик к приложению
# app.add_handler(handler)

# # Запускаем приложение
# app.run_polling()