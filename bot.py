import os

from dotenv import load_dotenv
from telebot import TeleBot, apihelper
from telebot.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

from modules.GoogleSheetsAPI import GoogleSynchronizer
from modules.authorization import authorized
from modules.keyboards import main_inline_keyboard, MAIN_SEARCH_CALLBACK, MAIN_SYNC_CALLBACK, \
    go_main_keyboard, search_keyboard, INVENT_SEARCH, SERIAL_SEARCH, korpusa_keyboard
from modules.models import initialize_db, User, Equipment, Movement

load_dotenv()
initialize_db()
apihelper.proxy = {'https': os.environ.get('BOT_PROXY')}
bot = TeleBot(token=os.environ.get('BOT_TOKEN'))

users = {}


def found_item(item, movement):
    return f"""Я нашел оборудование:
ID: {item.it_id}
Инвентарный номер: {item.invent_num}
Тип: {item.type}
Марка: {item.mark}
Модель: {item.model}
Серийный номер: {item.serial_num}

Корпус: {movement.korpus}
Кабинет: {movement.room}"""


# User.drop_table()
# Equipment.drop_table()
# Movement.drop_table()

# Команда start
@bot.message_handler(commands=['start'])
def start(message: Message):
    if authorized(message=message, bot=bot):
        bot.send_message(chat_id=message.chat.id, text='С возвращением!', reply_markup=go_main_keyboard)


# Обработка текстовых сообщений
@bot.message_handler(content_types=['text'])
def plain_text_message(message: Message):
    if authorized(message=message, bot=bot):
        if users.get(f'{message.chat.id}') is None:
            users[f'{message.chat.id}'] = {
                'operator': GoogleSynchronizer(spreadsheet_id=os.environ.get('SPREADSHEET_ID'),
                                               credentials_file_name=os.environ.get('CREDENTIAL_FILE'))
            }
        if message.text == 'На главную':
            User.update(status='').where(User.telegram_id == message.chat.id).execute()
            bot.send_message(chat_id=message.chat.id, text='Мои функции', reply_markup=main_inline_keyboard)
            return
        if User.get(telegram_id=message.chat.id).status == INVENT_SEARCH:
            invent_num = message.text
            bot.send_message(chat_id=message.chat.id, text=f'Ищу оборудование с инвентарным номером {invent_num}')
            found_items = Equipment.select().where(Equipment.invent_num == invent_num)
            if len(found_items) != 0:
                movement = None
                for item in found_items:
                    temp_movements = item.movements
                    if temp_movements.count() > 0:
                        for temp in temp_movements:
                            movement = temp
                    else:
                        movement = Movement.create(it_id=item.it_id,
                                                   korpus='N/A',
                                                   room='N/A')
                    move_key = InlineKeyboardMarkup()
                    button = InlineKeyboardButton(text='Переместить', callback_data=f'Move_{item.it_id}')
                    move_key.row(button)
                    bot.send_message(chat_id=message.chat.id, text=found_item(item, movement), reply_markup=move_key)
            else:
                bot.send_message(chat_id=message.chat.id,
                                 text='Я не нашел оборудование с указанным инвентарным номером')
        if User.get(telegram_id=message.chat.id).status == SERIAL_SEARCH:
            serial_num = message.text
            bot.send_message(chat_id=message.chat.id, text=f'Ищу оборудование с серийным номером {serial_num}')
            found_items = Equipment.select().where(Equipment.serial_num == serial_num)
            if len(found_items) != 0:
                movement = None
                for item in found_items:
                    temp_movements = item.movements
                    if temp_movements.count() > 0:
                        for temp in temp_movements:
                            movement = temp
                    else:
                        movement = Movement.create(it_id=item.it_id,
                                                   korpus='N/A',
                                                   room='N/A')
                    move_key = InlineKeyboardMarkup()
                    button = InlineKeyboardButton(text='Переместить', callback_data=f'Move_{item.it_id}')
                    move_key.row(button)
                    bot.send_message(chat_id=message.chat.id, text=found_item(item, movement), reply_markup=move_key)
            else:
                bot.send_message(chat_id=message.chat.id,
                                 text='Я не нашел оборудование с указанным серийным номером')
        if User.get(telegram_id=message.chat.id).status.split('_')[0] == 'Move':
            Movement.update(room=message.text).where(
                Movement.it_id == User.get(telegram_id=message.chat.id).status.split('_')[
                    1] and Movement.room == '___').execute()
            bot.send_message(chat_id=message.chat.id,
                             text='Перемещение выполнено. Не забудьте выполнить синхронизацию!')
        User.update(status='').where(User.telegram_id == message.chat.id).execute()


# Выбор параметра поиска
@bot.callback_query_handler(func=lambda call: call.data == MAIN_SEARCH_CALLBACK)
def main_search(call):
    if authorized(message=call.message, bot=bot):
        User.update(status=MAIN_SEARCH_CALLBACK).where(User.telegram_id == call.message.chat.id).execute()
        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text='По какому параметру ищем?',
                              reply_markup=search_keyboard)


# Выбор поиска по инвентарному номеру
@bot.callback_query_handler(func=lambda call: call.data == INVENT_SEARCH)
def invent_search(call):
    if authorized(message=call.message, bot=bot):
        User.update(status=INVENT_SEARCH).where(User.telegram_id == call.message.chat.id).execute()
        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text='Введите инвентарный номер оборудования')


# Выбор поиска по серийному номеру
@bot.callback_query_handler(func=lambda call: call.data == SERIAL_SEARCH)
def serial_search(call):
    if authorized(message=call.message, bot=bot):
        User.update(status=SERIAL_SEARCH).where(User.telegram_id == call.message.chat.id).execute()
        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text='Введите серийный номер оборудования')


@bot.callback_query_handler(func=lambda call: call.data.split('_')[0] == 'Move')
def main_move(call):
    if authorized(message=call.message, bot=bot):
        User.update(status=call.data).where(User.telegram_id == call.message.chat.id).execute()
        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text='В какой корпус перемещаем?',
                              reply_markup=korpusa_keyboard)


@bot.callback_query_handler(func=lambda call: call.data[:2] == 'UK')
def choose_uk(call):
    if authorized(message=call.message, bot=bot):
        if User.get(telegram_id=call.message.chat.id).status.split('_')[0] == 'Move':
            uk_num = call.data[2:]
            it_id = User.get(telegram_id=call.message.chat.id).status.split('_')[1]
            Movement.create(it_id=it_id,
                            korpus=f'УК{uk_num}',
                            room='___')
            bot.edit_message_text(chat_id=call.message.chat.id,
                                  message_id=call.message.message_id,
                                  text='В какой кабинет перемещаем?')


@bot.callback_query_handler(func=lambda call: call.data == MAIN_SYNC_CALLBACK)
def main_sync(call):
    if authorized(message=call.message, bot=bot):
        User.update(status='main_sync').where(User.telegram_id == call.message.chat.id).execute()
        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text='Выполняется синхронизация')
        values = users[f'{call.message.chat.id}'].get('operator').get_equipments()
        for i in range(len(values)):
            item = values[i]
            if i % 10 == 0:
                bot.edit_message_text(chat_id=call.message.chat.id,
                                      message_id=call.message.message_id,
                                      text=f'Выполняется синхронизация {int(i * 100 / len(values))}%')
            if len(item) < 7:
                for j in range(len(item), 7):
                    item.append('')
            Equipment.get_or_create(it_id=item[0],
                                    defaults={
                                        'invent_num': item[2],
                                        'type': item[3],
                                        'mark': item[4],
                                        'model': item[5],
                                        'serial_num': item[6]})
        User.update(status='').where(User.telegram_id == call.message.chat.id).execute()
        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text='Обновляю перемещения')
        # Добавить отправку данных из таблицы БД перемещение
        values = users[f'{call.message.chat.id}'].get('operator').get_movements_list()
        move_data = []
        sync_data = []
        if values == None:
            values = []
        movements = Movement.select()
        for movement in movements:
            move_data.append(
                [Equipment.get(id=movement.it_id).it_id, Equipment.get(id=movement.it_id).invent_num, movement.korpus,
                 movement.room])
        if len(move_data) > len(values):
            for i in range(len(values), len(move_data)):
                sync_data.append(move_data[i])
            users[f'{call.message.chat.id}'].get('operator').sync_moves(start_line=len(values) + 2,
                                                                        data=sync_data)
        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text='Данные синхронизированы')


if __name__ == '__main__':
    bot.polling(none_stop=True)
