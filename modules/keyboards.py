from telebot.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton

GO_TO_MAIN = 'На главную'
MAIN_SEARCH_CALLBACK = 'Main_Search'
SERIAL_SEARCH = 'Serial_search'
INVENT_SEARCH = 'Invent_search'
MAIN_SYNC_CALLBACK = 'Main_Sync'

go_main_keyboard = ReplyKeyboardMarkup(True)
go_main_keyboard.row(GO_TO_MAIN)

main_inline_keyboard = InlineKeyboardMarkup()
main_inline_button1 = InlineKeyboardButton(text='Поиск и перемещение оборудования', callback_data=MAIN_SEARCH_CALLBACK)
main_inline_button2 = InlineKeyboardButton(text='Синхронизация с Google-таблицей', callback_data=MAIN_SYNC_CALLBACK)
main_inline_keyboard.row(main_inline_button1)
main_inline_keyboard.row(main_inline_button2)

search_keyboard = InlineKeyboardMarkup()
search_keyboard_button1 = InlineKeyboardButton(text='По инвентарному номеру', callback_data=INVENT_SEARCH)
search_keyboard_button2 = InlineKeyboardButton(text='По серийному номеру', callback_data=SERIAL_SEARCH)
search_keyboard.row(search_keyboard_button1)
search_keyboard.row(search_keyboard_button2)


korpusa_keyboard = InlineKeyboardMarkup()
korpus_button = []
korpus_button.append(InlineKeyboardButton(text='УК 1', callback_data='UK1'))
korpus_button.append(InlineKeyboardButton(text='УК 2', callback_data='UK2'))
korpus_button.append(InlineKeyboardButton(text='УК 3', callback_data='UK3'))
korpus_button.append(InlineKeyboardButton(text='УК 4', callback_data='UK4'))
korpus_button.append(InlineKeyboardButton(text='УК 5', callback_data='UK5'))
korpus_button.append(InlineKeyboardButton(text='УК 6', callback_data='UK6'))
korpus_button.append(InlineKeyboardButton(text='УК 7', callback_data='UK7'))
korpus_button.append(InlineKeyboardButton(text='УК 8', callback_data='UK8'))
korpus_button.append(InlineKeyboardButton(text='УК 9', callback_data='UK9'))
korpus_button.append(InlineKeyboardButton(text='УК 10', callback_data='UK10'))

for i in korpus_button:
    korpusa_keyboard.row(i)

