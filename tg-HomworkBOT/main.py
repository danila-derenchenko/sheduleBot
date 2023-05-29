import config
from os import environ

from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Regexp
from asyncio import new_event_loop, sleep
import asyncio
from utils import parsing
import re

from tg import keyboards
from controller import func


bot = Bot(token=environ.get("tgtoken"))
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    func.registration_people(message=message)
    await message.reply("Система умного обучения приветствует вас!", reply_markup=keyboards.menu)


@dp.callback_query_handler(text="remove_kb")
async def remove_kb(callback: types.CallbackQuery):
    await callback.message.answer("Клавиатура удалена!", reply_markup=types.ReplyKeyboardRemove())
    await callback.answer()


@dp.callback_query_handler(text="get_profile")
async def get_profile(callback: types.CallbackQuery):
    await callback.message.answer(func.get_profile(callback.from_user.id), reply_markup=keyboards.action_note)
    await callback.answer()
#get_schedule

@dp.callback_query_handler(Regexp(regexp='get_schedule_'))
async def get_schedule(callback: types.CallbackQuery):
    if callback.data == "get_schedule_1":
        course, faculty = func.get_course_and_faculty(callback)
        kb = types.InlineKeyboardMarkup()
        for i in await parsing.get_groups(course, faculty):
            kb.add(types.InlineKeyboardButton(i["Name"], callback_data=f'get_schedule_{i["ID"]}'))
        await callback.message.answer(text="Выберите группу", reply_markup=kb)
    else:
        await callback.message.delete()
        i = await parsing.get_schedule(callback.data.split("_")[-1])
        await callback.message.answer(text=str(i), parse_mode="html")
    await callback.answer()

@dp.callback_query_handler(text=["set_course"] + [f"set_course_{i}" for i in range(1, 7)])
async def set_course(callback: types.CallbackQuery):
    if callback.data == "set_course":
        await callback.message.answer(text="Выберите курс", reply_markup=keyboards.courses)
    else:
        await callback.message.delete()
        func.update_course(callback.from_user.id, callback.data)
        await callback.message.answer(text="Ты успешно выбрал курс!")
    await callback.answer()


@dp.callback_query_handler(text=["set_faculty"] + [f"set_faculty_{i}" for i in func.faculties.keys()])
async def set_faculty(callback: types.CallbackQuery):
    if callback.data == "set_faculty":
        await callback.message.answer(text="Выберите факультет", reply_markup=keyboards.faculty)
    else:
        await callback.message.delete() # удаляем огромное сообщение с текстом факультетов
        func.update_faculty(callback.from_user.id, callback.data)
        await callback.message.answer(text="Ты успешно выбрал факультет!")
    await callback.answer()


@dp.callback_query_handler(text="add_note")
async def add_note(callback: types.CallbackQuery):
    await callback.message.answer(text=func.init_create_note(callback))
    await callback.answer()


@dp.callback_query_handler(text="check_notes")
async def check_notes(callback: types.CallbackQuery):
    t, k = func.check_notes(callback)
    await callback.message.answer(t, parse_mode="html", reply_markup=k)
    await callback.answer()


@dp.callback_query_handler()
async def check_notes(callback: types.CallbackQuery):
    if "update_time_" in callback.data:
        await callback.message.answer(func.update_time(callback))
    elif "end_note_" in callback.data:
        await callback.message.answer(func.end_note(callback))
    elif "return_note_" in callback.data:
        await callback.message.answer(func.return_note(callback))
    # t, k = func.check_notes(callback)
    # await callback.message.answer(t, parse_mode="html", reply_markup=k)
    await callback.answer()


@dp.message_handler(content_types=["text"])
async def echo(message: types.Message):
    if message.text.lower() == "профиль":
        await message.answer(func.get_profile(message.from_id), reply_markup=keyboards.action_note)
    result = func.action_handler(message)
    if type(result) == str:
        await message.answer(result)

'''
async def send_push_homework(*args, **kwargs):
    while True:
        data = func.send_push_homework("get")
        for i in data:
            await bot.send_message(i.user_id, f"Предмет: {i.subject}\n\nОписание:{i.text}")
        func.send_push_homework("update", data)
        await sleep(5 * 60) # сон 5 * 60 = 300 секунд = 5 минут
'''



if __name__ == '__main__':
    #executor.start_polling(dp, skip_updates=False, on_startup=send_push_homework)
    executor.start_polling(dp, skip_updates=False)
