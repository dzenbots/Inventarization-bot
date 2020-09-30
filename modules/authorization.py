from telebot import TeleBot
from telebot.types import Message

from modules.keyboards import go_main_keyboard
from modules.models import User
from modules.settings import USER_SECRET, FINISH_REGISTRATION, IN_REGISTRATION_PROCCESS, bot_messages_text


def authorized(message: Message, bot: TeleBot):
    user, created = User.get_or_create(telegram_id=message.chat.id,
                                       defaults={'status': IN_REGISTRATION_PROCCESS,
                                                 'authorized': 0})
    if user.authorized == 0 and user.status == IN_REGISTRATION_PROCCESS:
        bot.send_message(chat_id=message.chat.id,
                         text=bot_messages_text.get('start_registration'))
        User.update(status=FINISH_REGISTRATION).where(User.telegram_id == message.chat.id).execute()
        return False
    if user.authorized == 0 and user.status == FINISH_REGISTRATION:
        if message.text == USER_SECRET:
            User.update(status='', authorized=1).where(User.telegram_id == message.chat.id).execute()
            bot.send_message(chat_id=message.chat.id,
                             text=bot_messages_text.get('auth_ok'),
                             reply_markup=go_main_keyboard)
            return True
        else:
            bot.send_message(chat_id=message.chat.id,
                             text=bot_messages_text.get('wrong_auth_key'))
            return False
    if user.authorized == 1:
        return True
