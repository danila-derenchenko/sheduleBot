from aiogram import types
from controller.func import faculties

# Главное меню через /start или /help
menu = types.InlineKeyboardMarkup()
# menu.add(types.InlineKeyboardButton("Удалить клавиатуру", callback_data="remove_kb"))
menu.add(types.InlineKeyboardButton("Посмотреть профиль", callback_data="get_profile"))
menu.add(types.InlineKeyboardButton("Добавить запись", callback_data="add_note"))
menu.add(types.InlineKeyboardButton("Посмотреть записи", callback_data="check_notes"))

action_note = types.InlineKeyboardMarkup()
action_note.add(types.InlineKeyboardButton("Добавить запись", callback_data="add_note"))
action_note.add(types.InlineKeyboardButton("Посмотреть записи", callback_data="check_notes"))
action_note.add(types.InlineKeyboardButton("Выбрать факультет", callback_data="set_faculty"))
action_note.add(types.InlineKeyboardButton("Выбрать курс", callback_data="set_course"))
action_note.add(types.InlineKeyboardButton("Посмотреть расписание", callback_data="get_schedule_1"))

courses = types.InlineKeyboardMarkup()
for i in range(1, 7): courses.add(types.InlineKeyboardButton(f"{i} курс", callback_data=f"set_course_{i}"))

faculty = types.InlineKeyboardMarkup()
for i in faculties: faculty.add(types.InlineKeyboardButton(faculties[i], callback_data=f"set_faculty_{i}"))
