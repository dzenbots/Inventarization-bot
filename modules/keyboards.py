from telebot.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton

from settings import main_reply_keyboard_text, callbacks

# MAIN_SEARCH_CALLBACK = 'Main_Search'
MAIN_SYNC_CALLBACK = 'Main_Sync'

go_main_keyboard = ReplyKeyboardMarkup(True)
go_main_keyboard.row(main_reply_keyboard_text)

main_inline_keyboard = InlineKeyboardMarkup()
main_inline_keyboard.row(InlineKeyboardButton(text='Поиск и перемещение оборудования',
                                              callback_data=callbacks.get('main_search')))
main_inline_keyboard.row(InlineKeyboardButton(text='Синхронизация с Google-таблицей',
                                              callback_data=MAIN_SYNC_CALLBACK))

search_keyboard = InlineKeyboardMarkup()
search_keyboard.row(InlineKeyboardButton(text='По инвентарному номеру',
                                         callback_data=callbacks.get('invent_search')))
search_keyboard.row(InlineKeyboardButton(text='По серийному номеру',
                                         callback_data=callbacks.get('serial_search')))


def get_edit_inline_keyboard(it_id):
    main_edit_inline_keyboard = InlineKeyboardMarkup()
    main_edit_inline_keyboard.row(
        InlineKeyboardButton(text='Марка', callback_data=callbacks.get('mark').format(it_id=it_id)))
    main_edit_inline_keyboard.row(
        InlineKeyboardButton(text='Модель', callback_data=callbacks.get('model').format(it_id=it_id)))
    main_edit_inline_keyboard.row(
        InlineKeyboardButton(text='Серийный номер', callback_data=callbacks.get('serial').format(it_id=it_id)))
    return main_edit_inline_keyboard


korpusa_keyboard = InlineKeyboardMarkup()
for i in range(1, 11):
    korpusa_keyboard.row(InlineKeyboardButton(text=f'УК {i}', callback_data=callbacks.get('UK').format(uk=i)))
# korpus_button = []
# korpus_button.append(InlineKeyboardButton(text='УК 1', callback_data='UK1'))
# korpus_button.append(InlineKeyboardButton(text='УК 2', callback_data='UK2'))
# korpus_button.append(InlineKeyboardButton(text='УК 3', callback_data='UK3'))
# korpus_button.append(InlineKeyboardButton(text='УК 4', callback_data='UK4'))
# korpus_button.append(InlineKeyboardButton(text='УК 5', callback_data='UK5'))
# korpus_button.append(InlineKeyboardButton(text='УК 6', callback_data='UK6'))
# korpus_button.append(InlineKeyboardButton(text='УК 7', callback_data='UK7'))
# korpus_button.append(InlineKeyboardButton(text='УК 8', callback_data='UK8'))
# korpus_button.append(InlineKeyboardButton(text='УК 9', callback_data='UK9'))
# korpus_button.append(InlineKeyboardButton(text='УК 10', callback_data='UK10'))
#
# for i in korpus_button:
#     korpusa_keyboard.row(i)
