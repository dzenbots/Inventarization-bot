import os

from dotenv import load_dotenv
from telebot import TeleBot
from telebot.types import Message

from GoogleSheetsAPI import GoogleSheetOperator

load_dotenv()
bot = TeleBot(token=os.environ.get('BOT_TOKEN'))


@bot.message_handler(commands=['start'])
def start(message: Message):
    operator = GoogleSheetOperator(spreadsheet_id=os.environ.get('SPREADSHEET_ID'),
                                   credentials_file_name=os.environ.get('CREDENTIAL_FILE'))


if __name__ == '__main__':
    bot.polling(none_stop=True)
