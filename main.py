import logging, sqlite3, random
from telegram import Update
from telegram.ext import filters, MessageHandler, ApplicationBuilder, CommandHandler, ContextTypes, ConversationHandler
from telegram import KeyboardButton, ReplyKeyboardMarkup



logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
"""#---------------------Старт для всего и кнопок------------------------------#"""
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keys = [[KeyboardButton("/help"), KeyboardButton("/home")], [KeyboardButton("/mem")]]
    key_markup = ReplyKeyboardMarkup(keys, resize_keyboard=True)
    await context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text="Приветствую, добро пожаловать в наш развлекательный бот, чтобы продолжить, нужно выпить советский...\nЛадно, шутки в сторону, пока что бот на стадии разработки, можете здесь написать любое сообщение, бот отправит Вам такое же сообщение.",
        reply_markup=key_markup)
"""#-----------------------Заканчивается кусок старта------------------------"""    

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="/mem - прислать мемчик\n/home - проводить тебя домой\nКак-то так")

LOCATION = range(1)
async def home(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Отправьте геолокацию, чтобы доброволец смог бы тебя найти и провести тебя домой')
    return LOCATION

async def location(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    user_location = update.message.location
    #await context.bot.send_message(chat_id=-4103955633, text=update.message.text)
    await context.bot.send_location(chat_id=-4103955633, latitude=user_location.latitude, longitude=user_location.longitude)
    return ConversationHandler.END

async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Прастите, такой команды нет, чтобы узнать какие команды есть, то введите /help")

async def mem(update: Update, context: ContextTypes.DEFAULT_TYPE):
    conn = sqlite3.connect('neodinbot.db')
    cursor = conn.cursor()
    cursor.execute("SELECT MAX(ID) FROM MEMES")
    id_max = cursor.fetchone()[0]
    rand_id = random.randint(1, id_max)
    cursor.execute("SELECT image FROM MEMES WHERE id = ?", (str(rand_id),))
    image_data = cursor.fetchone()[0]
    conn.close()
    await context.bot.send_photo(chat_id=update.effective_chat.id, photo=image_data)


if __name__ == '__main__':
    application = ApplicationBuilder().token('YOUR TOKEN').build()
    
    start_handler = CommandHandler('start', start)
    help_handler = CommandHandler('help', help)
    mem_handler = CommandHandler('mem', mem)

    home_conv_handler = ConversationHandler(
        entry_points=[CommandHandler('home', home)],
        states={LOCATION : [MessageHandler(filters.LOCATION, location)]},
        fallbacks=[CommandHandler('skip_location', home)]

    )
    unknown_handler = MessageHandler(filters.COMMAND, unknown)

    application.add_handler(start_handler)
    application.add_handler(help_handler)
    application.add_handler(mem_handler)
    application.add_handler(home_conv_handler)
    application.add_handler(unknown_handler)
    application.run_polling(allowed_updates=Update.ALL_TYPES)