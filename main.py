import logging

from Student import Student
from Schedule import Schedule
import config
from aiogram import Bot, Dispatcher, executor, types

logging.basicConfig(level=logging.INFO)

bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot)

student = Student('Denis', '119')
mySchedule = Schedule()

def find_schedule(day_name):
    if day_name == "понедельник чётный":
        return  mySchedule.PrintSchedule(student.GetId(), 'Чётная', 1)
    elif day_name == "понедельник нечётный":
        return mySchedule.PrintSchedule(student.GetId(), 'Нечётная', 1)
    elif day_name == "вторник чётный":
        return mySchedule.PrintSchedule(student.GetId(), 'Чётная', 2)
    elif day_name == "вторник нечётный":
        return mySchedule.PrintSchedule(student.GetId(), 'Нечётная', 2)
    elif day_name == "среда чётный":
        return mySchedule.PrintSchedule(student.GetId(), 'Чётная', 3)
    elif day_name == "среда нечётный":
        return mySchedule.PrintSchedule(student.GetId(), 'Нечётная', 3)
    elif day_name == "четверг чётный":
        return mySchedule.PrintSchedule(student.GetId(), 'Чётная', 4)
    elif day_name == "четверг нечётный":
        return mySchedule.PrintSchedule(student.GetId(), 'Нечётная', 4)
    elif day_name == "пятница чётный":
        return mySchedule.PrintSchedule(student.GetId(), 'Чётная', 5)
    elif day_name == "пятница нечётный":
        return mySchedule.PrintSchedule(student.GetId(), 'Нечётная', 5)
    return None

@dp.message_handler()
async def start(message: types.Message):
    lessons = []
    schedule = find_schedule(message.text)
    if schedule:
        await send_schedule(message, schedule)
    else:
        await message.answer("Некорректная неделя!")
    


async def send_schedule(message, shedule):
    for i in shedule:
        await message.answer(i)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=False)