from db.base import People, Note, db, Select

from asyncio import get_running_loop
from aiogram import types

from random import choice
from time import time

from utils import parsing

# словарь для ВРЕМЕННОГО ХРАНЕНИЯ СОЗДАВАЕМОЙ ЗАПИСИ
notes = {

}

faculties = {
    "113574": "Высшая биотехнологическая школа",
    "100108": "Инженерно-технологический факультет",
    "104717": "Институт автоматики и информационных технологий",
    "112040": "Институт инженерно-экономического и гуманитарного образования",
    "100105": "Институт нефтегазовых технологий",
    "105807": "Колледж СамГТУ",
    "104765": "Строительно-технологический факультет",
    "100266": "Сызранский филиал СамГТУ",
    "100265": "Сызранский филиал СамГТУ СПО",
    "100110": "Теплоэнергетический факультет",
    "113670": "Управление подготовки научных кадров",
    "103179": "Учебные подразделения филиала ФГБОУ ВО \"СамГТУ\" в г. Белебее Республики Башкортостан",
    "112953": "Факультет архитектуры и дизайна",
    "104748": "Факультет инженерных систем и природоохранного строительства",
    "101029": "Факультет машиностроения, металлургии и транспорта",
    "104758": "Факультет промышленного и гражданского строительства",
    "100106": "Химико-технологический факультет",
    "100111": "Электротехнический факультет"
}


def registration_people(message: types.Message) -> None:
    """Создаём пользователя, если его нет в бд"""
    if People.get_or_none(People.user_id == message.from_id) is None:
        o = People(user_id=message.from_id)
        o.save()
        db.commit()

def get_profile(user_id) -> None:
    """Получаем сообщение профиля"""
    people = People.get(People.user_id == user_id)
    return f"""
Курс: {"(не установлен)"if people.course == 0 else people.course}
Ф-т: {"(не установлен)"if people.faculty_id == 0 else faculties[str(people.faculty_id)]}
"""

def action_handler(message: types.Message):
    people = People.get(People.user_id == message.from_id)
    global notes

    if people.action == "add_name_matter":  # Добавить название предмета
        notes[str(message.from_id)]["subject"] = message.text
        people.action = "add_note_text"
        people.save()
        return "Добавьте описание задания к этому предмету"
    elif people.action == "add_note_text":  # Добавить описание задания
        notes[str(message.from_id)]["text"] = message.text
        people.action = "set_note_time"
        people.save()
        return "Выбери время (в часах) для напоминания (от 1 до 48)\n (Требуется ввести только число)"
    elif people.action == "set_note_time":
        n = notes[str(message.from_id)]
        retry = 3600
        if message.text.isdigit():
            retry = 3600 * int(message.text)
        people.action = "None"
        people.save()
        n |= {
            "retry": retry,
            "date": time(),
            "date_push": time()
        }
        Note.create(**n)
        del notes[str(message.from_id)] ### ОСВОБОЖДАЕМ ПАЯТЬ
        return f"""
    
Название предмета: {n["subject"]}

Время пуш уведомления: {n["retry"] // 3600} ч.

Описание домашнего задания: 
{n["text"]}
        """
    elif "update_time_" in people.action:
        retry = 3600
        if message.text.isdigit():
            retry = 3600 * int(message.text)
        n = Note.get_by_id(int(people.action.split("_")[-1]))
        n.retry = retry
        people.action = "None"
        people.save()
        n.save()
        return "Время не изменено!" if not message.text.isdigit() else f"Буду напоминать каждые {message.text} ч."

def init_create_note(callback: types.CallbackQuery):
    people = People.get(People.user_id == callback.from_user.id)
    global notes
    notes[str(callback.from_user.id)] = {"user_id": callback.from_user.id}
    people.action = "add_name_matter"
    people.save()
    return "Укажите название предмета: "

def check_notes(callback: types.CallbackQuery):
    notes = Note.select().where(Note.user_id == callback.from_user.id and Note.done == False)
    text = "Список записей:"
    kb = types.InlineKeyboardMarkup(row_width=3)
    z = []
    for e, t in enumerate(notes):
        text += f"\n<b>{e + 1}) {t.subject}</b> \n<code>{t.text}</code>\n"
        z.append([types.InlineKeyboardButton(text=f"испр. Время {e + 1}", callback_data=f"update_time_{t.id}"),
                  types.InlineKeyboardButton(text=f"Выполнить №{e + 1}", callback_data=f"{e+1}_end_note_{t.id}"),
                  types.InlineKeyboardButton(text=f"Отменить №{e + 1}", callback_data=f"return_note_{t.id}")])
    for buttons in z:
        kb.row(*buttons)
    return text, kb

def update_time(callback: types.CallbackQuery):
    people = People.get(People.user_id == callback.from_user.id)
    people.action = callback.data
    people.save()
    return "Введите новое время повторения:\n(в часах, число от 1 до 48)"

def end_note(callback: types.CallbackQuery):
    n = Note.get_by_id(int(callback.data.split("_")[-1]))
    if n.done == True:
        return "Ты уже выполнил это задание"
    n.done = True
    n.save()
    ph = ["Поздравляю!", "Ты просто бомба", "Молодец!", "Рад за тебя", "Бытро же ты :)"]
    return f"{choice(ph)}\n\nУбираю задание {callback.data.split('_')[0]} из списка."

def return_note(callback: types.CallbackQuery):
    n = Note.get_by_id(int(callback.data.split("_")[-1]))
    if n.done == False:
        return "Ты ещё не выполнил это задание"
    n.done = False
    n.save()
    ph = ["Ну, вот...", "Обманывать не хорошо!", "А я так надеялся :("]
    return f"{choice(ph)}\n\nВозвращаю задание"

def update_course(user_id, course):
    course = int(course.split("_")[-1])
    people = People.get(People.user_id == user_id)
    people.course = course
    people.save()


def update_faculty(user_id, faculty):
    faculty = int(faculty.split("_")[-1])
    people = People.get(People.user_id == user_id)
    people.faculty_id = faculty
    people.save()

def get_course_and_faculty(callback: types.CallbackQuery):
    people = People.get(People.user_id == callback.from_user.id)
    return people.faculty_id, people.course

def send_push_homework(get_or_update="get", data: list[Note]=[]):
    current_time = time()
    if get_or_update == "get":
        return Note.select().where(Note.date_push + Note.retry >= current_time and Note.done == False)
    elif get_or_update == "update":
        for i in data:
            i.save()
