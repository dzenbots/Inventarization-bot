import time

from telebot import TeleBot, apihelper
from telebot.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

from modules.GoogleSheetsAPI import GoogleSynchronizer
from modules.authorization import authorized
from modules.keyboards import main_inline_keyboard, go_main_keyboard, search_keyboard, \
    korpusa_keyboard, get_edit_inline_keyboard
from modules.models import initialize_db, User, Equipment, Movement
from settings import BOT_PROXY, BOT_TOKEN, SPREADSHEET_ID, CREDENTIAL_FILE, bot_messages_text, \
    main_reply_keyboard_text, callbacks, INVENT_SEARCH, SERIAL_SEARCH, MAIN_SEARCH, MAIN_EDIT

initialize_db()
apihelper.proxy = BOT_PROXY
bot = TeleBot(token=BOT_TOKEN)

users = {}


# Шаблон вывода информации
def found_item_template(item, movement):
    return f"""Я нашел оборудование:
ID: {item.it_id}
Инвентарный номер: {item.invent_num}
Тип: {item.type}
Марка: {item.mark}
Модель: {item.model}
Серийный номер: {item.serial_num}

Корпус: {movement.korpus}
Кабинет: {movement.room}"""


# Шаблон показа найденого оборудрования
def show_equipments(found_items, bot, message):
    if len(found_items) != 0:
        users[f'{message.chat.id}']['invent_num_for_show_again'] = found_items[0].invent_num
        movement = None
        for item in found_items:
            temp_movements = item.movements
            if temp_movements.count() > 0:
                for temp in temp_movements:
                    movement = temp
            else:
                movement = Movement.create(it_id=item,
                                           korpus='N/A',
                                           room='N/A')
            item_inline_keyboard = InlineKeyboardMarkup()
            item_inline_keyboard.row(
                InlineKeyboardButton(text=bot_messages_text.get('change_values'),
                                     callback_data=callbacks.get('main_edit').format(it_id=item.it_id)))
            item_inline_keyboard.row(
                InlineKeyboardButton(text=bot_messages_text.get('move'),
                                     callback_data=callbacks.get('main_move').format(it_id=item.it_id)))
            bot.send_message(chat_id=message.chat.id, text=found_item_template(item, movement),
                             reply_markup=item_inline_keyboard)
    else:
        bot.send_message(chat_id=message.chat.id,
                         text=bot_messages_text.get('item_not_found'))


# User.drop_table()
# Equipment.drop_table()
# Movement.drop_table()

# Команда start
@bot.message_handler(commands=['start'])
def start(message: Message):
    if authorized(message=message, bot=bot):
        bot.send_message(chat_id=message.chat.id,
                         text=bot_messages_text.get('welcome_back'),
                         reply_markup=go_main_keyboard)


# Обработка текстовых сообщений
@bot.message_handler(content_types=['text'])
def plain_text_message(message: Message):
    if authorized(message=message, bot=bot):

        # для вновь подключенного пользователя свой синхронизатор с Google-таблицей
        if users.get(f'{message.chat.id}') is None:
            users[f'{message.chat.id}'] = {
                'operator': GoogleSynchronizer(spreadsheet_id=SPREADSHEET_ID,
                                               credentials_file_name=CREDENTIAL_FILE)
            }

        # Обработка нажатия кнопки показа основных функций
        if message.text == main_reply_keyboard_text:
            User.update(status='').where(User.telegram_id == message.chat.id).execute()
            bot.send_message(chat_id=message.chat.id,
                             text=bot_messages_text.get('show_functions'),
                             reply_markup=main_inline_keyboard)
            return

        # Поиск по инвентарному или серийному номеру
        if User.get(telegram_id=message.chat.id).status == INVENT_SEARCH or \
                User.get(telegram_id=message.chat.id).status == SERIAL_SEARCH:
            found_items = None
            temp_item = None
            if User.get(telegram_id=message.chat.id).status == INVENT_SEARCH:
                bot.send_message(chat_id=message.chat.id,
                                 text=bot_messages_text.get('invent_search').format(invent_num=message.text))
                found_items = Equipment.select().where(Equipment.invent_num == message.text)
            elif User.get(telegram_id=message.chat.id).status == SERIAL_SEARCH:
                bot.send_message(chat_id=message.chat.id,
                                 text=bot_messages_text.get('serial_search').format(serial_num=message.text))
                found_items = Equipment.select().where(Equipment.serial_num == message.text)
            show_equipments(found_items, bot, message)

        # Выполнить перемещение в базе
        if User.get(telegram_id=message.chat.id).status.split('_')[0] == 'MOVE':
            Movement.update(room=message.text). \
                where(Movement.it_id == Equipment.get(it_id=User.get(telegram_id=message.chat.id).status.split('_')[1])
                      and Movement.room == 'N/A'). \
                execute()
            users[f'{message.chat.id}'].get('operator').add_new_movement(
                id=User.get(telegram_id=message.chat.id).status.split('_')[1])
            bot.send_message(chat_id=message.chat.id,
                             text=bot_messages_text.get('complete_move'))
            found_items = Equipment.select().where(
                Equipment.invent_num == users[f'{message.chat.id}']['invent_num_for_show_again'])
            show_equipments(found_items, bot, message)

        if User.get(telegram_id=message.chat.id).status.split('_')[0] == 'edit-type':
            Equipment.update(type=message.text). \
                where(Equipment.it_id == User.get(telegram_id=message.chat.id).status.split('_')[1]). \
                execute()
            users[f'{message.chat.id}'].get('operator').edit_in_table(
                item=Equipment.get(Equipment.it_id == User.get(telegram_id=message.chat.id).status.split('_')[1]))
            bot.send_message(chat_id=message.chat.id,
                             text=bot_messages_text.get('edit_complete'))
            found_items = Equipment.select().where(
                Equipment.invent_num == users[f'{message.chat.id}']['invent_num_for_show_again'])
            show_equipments(found_items, bot, message)

        if User.get(telegram_id=message.chat.id).status.split('_')[0] == 'edit-mark':
            Equipment.update(mark=message.text). \
                where(Equipment.it_id == User.get(telegram_id=message.chat.id).status.split('_')[1]). \
                execute()
            users[f'{message.chat.id}'].get('operator').edit_in_table(
                item=Equipment.get(Equipment.it_id == User.get(telegram_id=message.chat.id).status.split('_')[1]))
            bot.send_message(chat_id=message.chat.id,
                             text=bot_messages_text.get('edit_complete'))
            found_items = Equipment.select().where(
                Equipment.invent_num == users[f'{message.chat.id}']['invent_num_for_show_again'])
            show_equipments(found_items, bot, message)

        if User.get(telegram_id=message.chat.id).status.split('_')[0] == 'edit-model':
            Equipment.update(model=message.text). \
                where(Equipment.it_id == User.get(telegram_id=message.chat.id).status.split('_')[1]). \
                execute()
            users[f'{message.chat.id}'].get('operator').edit_in_table(
                item=Equipment.get(Equipment.it_id == User.get(telegram_id=message.chat.id).status.split('_')[1]))
            bot.send_message(chat_id=message.chat.id,
                             text=bot_messages_text.get('edit_complete'))
            found_items = Equipment.select().where(
                Equipment.invent_num == users[f'{message.chat.id}']['invent_num_for_show_again'])
            show_equipments(found_items, bot, message)

        if User.get(telegram_id=message.chat.id).status.split('_')[0] == 'edit-serial':
            Equipment.update(serial_num=message.text). \
                where(Equipment.it_id == User.get(telegram_id=message.chat.id).status.split('_')[1]). \
                execute()
            users[f'{message.chat.id}'].get('operator').edit_in_table(
                item=Equipment.get(Equipment.it_id == User.get(telegram_id=message.chat.id).status.split('_')[1]))
            bot.send_message(chat_id=message.chat.id,
                             text=bot_messages_text.get('edit_complete'))
            found_items = Equipment.select().where(
                Equipment.invent_num == users[f'{message.chat.id}']['invent_num_for_show_again'])
            show_equipments(found_items, bot, message)

        User.update(status='').where(User.telegram_id == message.chat.id).execute()


# Выбор параметра поиска
@bot.callback_query_handler(func=lambda call: call.data == callbacks.get('main_search'))
def main_search(call):
    if authorized(message=call.message, bot=bot):
        User.update(status=MAIN_SEARCH).where(User.telegram_id == call.message.chat.id).execute()
        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text=bot_messages_text.get('searching_parameter'),
                              reply_markup=search_keyboard)


# Выбор поиска по инвентарному номеру
@bot.callback_query_handler(func=lambda call: call.data == callbacks.get('invent_search'))
def invent_search(call):
    if authorized(message=call.message, bot=bot):
        User.update(status=INVENT_SEARCH).where(User.telegram_id == call.message.chat.id).execute()
        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text=bot_messages_text.get('enter_invent_num'))


# Выбор поиска по серийному номеру
@bot.callback_query_handler(func=lambda call: call.data == callbacks.get('serial_search'))
def serial_search(call):
    if authorized(message=call.message, bot=bot):
        User.update(status=SERIAL_SEARCH).where(User.telegram_id == call.message.chat.id).execute()
        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text=bot_messages_text.get('enter_serial_num'))


# Выбор поля для редактирования
@bot.callback_query_handler(func=lambda call: call.data.split('_')[0] == 'EDIT')
def main_edit(call):
    if authorized(message=call.message, bot=bot):
        User.update(status=MAIN_EDIT).where(User.telegram_id == call.message.chat.id).execute()
        bot.send_message(chat_id=call.message.chat.id,
                         text=bot_messages_text.get('what_edit'),
                         reply_markup=get_edit_inline_keyboard(it_id=call.data.split('_')[1]))


# Ввод новой марки
@bot.callback_query_handler(func=lambda call: call.data.split('_')[0] == 'edit-mark')
def main_edit(call):
    if authorized(message=call.message, bot=bot):
        User.update(status=call.data).where(User.telegram_id == call.message.chat.id).execute()
        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text=bot_messages_text.get('enter_new_mark'))


# Ввод новой марки
@bot.callback_query_handler(func=lambda call: call.data.split('_')[0] == 'edit-type')
def main_edit(call):
    if authorized(message=call.message, bot=bot):
        User.update(status=call.data).where(User.telegram_id == call.message.chat.id).execute()
        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text=bot_messages_text.get('enter_new_type'))


# Ввод новой модели
@bot.callback_query_handler(func=lambda call: call.data.split('_')[0] == 'edit-model')
def main_edit(call):
    if authorized(message=call.message, bot=bot):
        User.update(status=call.data).where(User.telegram_id == call.message.chat.id).execute()
        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text=bot_messages_text.get('enter_new_model'))


# Ввод нового серийника
@bot.callback_query_handler(func=lambda call: call.data.split('_')[0] == 'edit-serial')
def main_edit(call):
    if authorized(message=call.message, bot=bot):
        User.update(status=call.data).where(User.telegram_id == call.message.chat.id).execute()
        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text=bot_messages_text.get('enter_new_serial'))


# Выбор корпуса для перемещения
@bot.callback_query_handler(func=lambda call: call.data.split('_')[0] == 'MOVE')
def main_move(call):
    if authorized(message=call.message, bot=bot):
        User.update(status=call.data).where(User.telegram_id == call.message.chat.id).execute()
        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text=bot_messages_text.get('enter_korpus_num'),
                              reply_markup=korpusa_keyboard)


# Выбор кабинета в корпусе для перемещения
@bot.callback_query_handler(func=lambda call: call.data.split('_')[0] == 'UK')
def choose_uk(call):
    if authorized(message=call.message, bot=bot):
        if User.get(telegram_id=call.message.chat.id).status.split('_')[0] == 'MOVE':
            uk_num = call.data.split('_')[1]
            it_id = User.get(telegram_id=call.message.chat.id).status.split('_')[1]
            movement = Movement.create(it_id=Equipment.get(it_id=it_id),
                                       korpus=f'УК {uk_num}',
                                       room='N/A')
            # movement.update(korpus=f'УК {uk_num}').execute()
            # Movement.create(it_id=it_id,
            #                 korpus=f'УК {uk_num}',
            #                 room='___')
            bot.edit_message_text(chat_id=call.message.chat.id,
                                  message_id=call.message.message_id,
                                  text=bot_messages_text.get('enter_room_num'))


@bot.callback_query_handler(func=lambda call: call.data == callbacks.get('get_equipments'))
def main_sync(call):
    if authorized(message=call.message, bot=bot):
        User.update(status=call.data).where(User.telegram_id == call.message.chat.id).execute()
        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text=bot_messages_text.get('getting_equipments'))
        values = users[f'{call.message.chat.id}'].get('operator').get_equipments()
        for i in range(len(values)):
            item = values[i]
            if i % 50 == 9:
                bot.edit_message_text(chat_id=call.message.chat.id,
                                      message_id=call.message.message_id,
                                      text=bot_messages_text.get('process_equipment_list').format(cur_item=i,
                                                                                                  sum_item=len(values)))
            if len(item) < 7:
                for j in range(len(item), 7):
                    item.append('')
            Equipment.get_or_create(it_id=item[0],
                                    defaults={
                                        'pos_in_buh': item[1],
                                        'invent_num': item[2],
                                        'type': item[3],
                                        'mark': item[4],
                                        'model': item[5],
                                        'serial_num': item[6]})
        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text=bot_messages_text.get('equipment_list_getting_complete'))
        # Добавить отправку данных из таблицы БД перемещение
        # values = users[f'{call.message.chat.id}'].get('operator').get_movements_list()
        # move_data = []
        # sync_data = []
        # if values == None:
        #     values = []
        # movements = Movement.select()
        # for movement in movements:
        #     move_data.append(
        #         [Equipment.get(id=movement.it_id).it_id, Equipment.get(id=movement.it_id).invent_num, movement.korpus,
        #          movement.room])
        # if len(move_data) > len(values):
        #     for i in range(len(values), len(move_data)):
        #         sync_data.append(move_data[i])
        #     users[f'{call.message.chat.id}'].get('operator').sync_moves(start_line=len(values) + 2,
        #                                                                 data=sync_data)
        # bot.edit_message_text(chat_id=call.message.chat.id,
        #                       message_id=call.message.message_id,
        #                       text='Данные синхронизированы')


if __name__ == '__main__':
    while True:
        try:
            bot.polling(none_stop=False, interval=0, timeout=20)
        except Exception as e:
            print(e)
            time.sleep(15)
