from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


button1 = KeyboardButton(text="/register")
button2 = KeyboardButton(text="/task")
button3 = KeyboardButton(text="/list")
button4 = KeyboardButton(text="/cancel")

start = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
start.add(button1, button3).row(button2)
