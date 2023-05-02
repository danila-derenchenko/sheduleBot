from aiogram import types

from .consts import faculties

menu = types.InlineKeyboardMarkup()
menu.add(types.InlineKeyboardButton("Установить своё расписание", callback_data="set_faculty"))

faculties_btn = [[]]
faculties_kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
for e, key in enumerate(faculties):
    faculties_kb.add(types.KeyboardButton(faculties[key]))

# Курсы 1 - 6
course_kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
for i in range(1, 7):
    course_kb.add(types.KeyboardButton(i))
