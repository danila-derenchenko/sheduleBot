from aiogram import types

from .consts import faculties, course

# Главное меню через /start или /help
menu = types.InlineKeyboardMarkup()
menu.add(types.InlineKeyboardButton("Установить своё расписание", callback_data="set_schedule"))

# (переделать)
# Разбиваем курсы по 2 кнопки в ряду
faculties_btn = [[]]
faculties_kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
for e, key in enumerate(faculties):
    e += 1
    if e % 2 == 0:
        faculties_btn.append([types.KeyboardButton(faculties[key])])
    else:
        faculties_btn[-1].append(types.KeyboardButton(faculties[key]))
for r in faculties_btn:
    faculties_kb.row(*r)

# Курсы 1 - 6
course_kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
for i in course:
    course_kb.add(types.KeyboardButton(i))
