import os

from dotenv import load_dotenv
from telebot import TeleBot, apihelper
from telebot.types import Message

from modules.GoogleSheetsAPI import GoogleSheetOperator
from modules.authorization import authorized
from modules.models import initialize_db

load_dotenv()
initialize_db()
apihelper.proxy = {'https': 'socks5://1rje3TFpVJ:Er2GduoOmw@45.92.172.55:55276'}
bot = TeleBot(token=os.environ.get('BOT_TOKEN'))


@bot.message_handler(commands=['start'])
def start(message: Message):
    user_id = message.chat.id
    if authorized(message=message, bot=bot):
        operator = GoogleSheetOperator(spreadsheet_id=os.environ.get('SPREADSHEET_ID'),
                                       credentials_file_name=os.environ.get('CREDENTIAL_FILE'))
        bot.send_message(chat_id=message.chat.id,
                         text=str(operator.read_range(list_name='Общий лист', range_in_list='A1:D2')))


@bot.message_handler(content_types=['text'])
def plain_text_message(message: Message):
    if authorized(message=message, bot=bot):
        bot.send_message(chat_id=message.chat.id, text='OMG!')


if __name__ == '__main__':
    bot.polling(none_stop=True)
