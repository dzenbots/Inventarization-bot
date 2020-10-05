import os

from dotenv import load_dotenv

load_dotenv()

BOT_PROXY = {'https': os.environ.get('BOT_PROXY')}
BOT_TOKEN = os.environ.get('BOT_TOKEN')

SPREADSHEET_ID = os.environ.get('SPREADSHEET_ID')
CREDENTIAL_FILE = os.environ.get('CREDENTIAL_FILE')

DB_FILE_PATH = os.environ.get('DB_FILE_PATH')
USER_SECRET = os.environ.get('USER_SECRET')

# user statuses
IN_REGISTRATION_PROCCESS = 'in_reg_proc'
FINISH_REGISTRATION = 'finish_registration'
MAIN_SEARCH = 'main_search'
INVENT_SEARCH = 'Invent_search'
SERIAL_SEARCH = 'Serial_search'
MAIN_EDIT = 'Main_edit'

# bot messages
bot_messages_text = {'start_registration': 'Для авторизации введите ключ доступа',
                     'wrong_auth_key': 'Авторизация не пройдена. Попробуйте ввести пароль еще раз',
                     'auth_ok': 'Авторизация пройдена', 'welcome_back': 'С возвращением!',
                     'show_functions': 'Мои функции',
                     'invent_search': 'Ищу оборудование с инвентарным номером {invent_num}',
                     'searching_parameter': 'По какому параметру ищем?',
                     'enter_invent_num': 'Введите инвентарный номер оборудования',
                     'enter_serial_num': 'Введите серийный номер оборудования',
                     'enter_korpus_num': 'В какой корпус перемещаем?',
                     'enter_room_num': 'В какой кабинет перемещаем?',
                     'item_not_found': 'Я не нашел оборудование с указанным инвентарным номером',
                     'change_values': 'Изменить данные',
                     'move': 'Переместить',
                     'enter_new_mark': 'Введите новое название марки',
                     'enter_new_model': 'Введите новое название модели',
                     'enter_new_serial': 'Введите новый серийный номер',
                     'what_edit': 'Что редактировать?',
                     'complete_move': 'Перемещение выполнено',
                     'edit_complete': 'Редактирование завершено'}

# button text at the end of screen (reply_keyboard)
main_reply_keyboard_text = 'На главную'

# inline keyboards callbacks
callbacks = {'main_search': 'main_search',
             'invent_search': 'invent_search',
             'serial_search': 'serial_search',
             'main_move': 'MOVE_{it_id}',
             'main_edit': 'EDIT_{it_id}',
             'UK': 'UK_{uk}',
             'mark': 'edit-mark_{it_id}',
             'model': 'edit-model_{it_id}',
             'serial': 'edit-serial_{it_id}'}
