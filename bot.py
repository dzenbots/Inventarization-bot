import os

from dotenv import load_dotenv
from telebot import TeleBot, apihelper
from telebot.types import Message

from modules.GoogleSheetsAPI import GoogleSheetOperator
from modules.authorization import authorized
from modules.models import initialize_db

load_dotenv()
initialize_db()
apihelper.proxy = {'https': os.environ.get('BOT_PROXY')}
bot = TeleBot(token=os.environ.get('BOT_TOKEN'))


@bot.message_handler(commands=['start'])
def start(message: Message):
    authorized(message=message, bot=bot)


@bot.message_handler(content_types=['text'])
def plain_text_message(message: Message):
    if authorized(message=message, bot=bot):
        bot.send_message(chat_id=message.chat.id, text='OMG!')


if __name__ == '__main__':
    bot.polling(none_stop=True)
