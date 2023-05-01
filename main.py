from aiogram import Bot, Dispatcher, executor, types

from config import TGtoken
from utills.consts import faculties
import utills.keyboards as keyboards
# from parsing import get_groups, get_schedule


bot = Bot(token=TGtoken)
dp = Dispatcher(bot)

# Нужно всё сделать через callback

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply("Моя менюшка", reply_markup=keyboards.menu)


@dp.callback_query_handler(text="set_faculty")
async def add_note(callback: types.CallbackQuery):
    await callback.message.answer(text="Выберите свой факультет", reply_markup=keyboards.faculties_kb)
    await callback.answer()


@dp.message_handler()
async def add_course(message: types.Message):
    if message.text in faculties.values():
        await message.answer("Факультет выбран")
        await message.answer(text="Выберите свой курс", reply_markup=keyboards.course_kb)

# Добавить проверку на корректность введённых данных
@dp.message_handler()
async def add_group(message: types.Message):
    if message.text:
        await message.answer("Курс выбран")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
