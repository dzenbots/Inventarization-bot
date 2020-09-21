from telebot.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton

GO_TO_MAIN = 'На главную'
MAIN_SEARCH_CALLBACK = 'Main_Search'
MAIN_MOVE_CALLBACK = 'Main_Move'
MAIN_SYNC_CALLBACK = 'Main_Sync'

go_main_keyboard = ReplyKeyboardMarkup(True)
go_main_keyboard.row(GO_TO_MAIN)

main_inline_keyboard = InlineKeyboardMarkup()
main_inline_button1 = InlineKeyboardButton(text='Поиск оборудования', callback_data=MAIN_SEARCH_CALLBACK)
main_inline_button2 = InlineKeyboardButton(text='Перемещение оборудования', callback_data=MAIN_MOVE_CALLBACK)
main_inline_button3 = InlineKeyboardButton(text='Синхронизация с Google-таблицей', callback_data=MAIN_SYNC_CALLBACK)
main_inline_keyboard.row(main_inline_button1)
main_inline_keyboard.row(main_inline_button2)
main_inline_keyboard.row(main_inline_button3)
