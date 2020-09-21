import os

from dotenv import load_dotenv
from telebot import TeleBot
from telebot.types import Message, ReplyKeyboardMarkup

from modules.keyboards import go_main_keyboard
from modules.models import User

load_dotenv()


def authorized(message: Message, bot: TeleBot):
    user, created = User.get_or_create(telegram_id=message.chat.id, defaults={'status': 'registration',
                                                                              'authorized': 0})
    if user.authorized == 0 and user.status == 'registration':
        bot.send_message(chat_id=message.chat.id, text='Для авторизации введите ключ доступа')
        User.update(status='finish_registration').where(User.telegram_id == message.chat.id).execute()
        return False
    if user.authorized == 0 and user.status == 'finish_registration':
        if message.text == os.environ.get('USER_SECRET'):
            User.update(status='', authorized=1).where(User.telegram_id == message.chat.id).execute()
            bot.send_message(chat_id=message.chat.id, text="Авторизация пройдена", reply_markup=go_main_keyboard)
            return True
        else:
            bot.send_message(chat_id=message.chat.id, text="Авторизация не пройдена. Попробуйте ввести пароль еще раз")
            return False
    if user.authorized == 1:
        return True
