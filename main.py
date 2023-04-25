from aiogram import Bot, Dispatcher, executor, types

from config import TGtoken
from utills.consts import faculties, course
import utills.keyboards as keyboards
# from parsing import get_groups, get_schedule


bot = Bot(token=TGtoken)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply("Моя менюшка", reply_markup=keyboards.menu)


@dp.callback_query_handler(text="set_schedule")
async def add_note(callback: types.CallbackQuery):
    await callback.message.answer(text="Выберите свой факультет", reply_markup=keyboards.faculties_kb)
    await callback.answer()


@dp.message_handler()
async def echo(message: types.Message):
    if message.text in faculties.values():
        await message.answer("Факультет выбран", reply_markup=types.ReplyKeyboardRemove())
        await message.answer(text="Выберите свой курс", reply_markup=keyboards.course_kb)
    elif message.text in course:
        await message.answer("Курс выбран", reply_markup=types.ReplyKeyboardRemove())


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
