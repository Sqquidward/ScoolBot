# print(nltk.edit_distance(s1, s2)/max(len(s1), len(s2)))
import logging
import aiogram.utils.markdown as md
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import ParseMode
from aiogram.utils import executor

logging.basicConfig(level=logging.INFO)

API_TOKEN = '2015387636:AAHwWe9wWssykiHh7jSAaQQSfUDs_UMWds0'


bot = Bot(token=API_TOKEN)

storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


# States
class Form(StatesGroup):
    classs = State()

@dp.message_handler(commands='start')
async def cmd_start(message: types.Message):
    await Form.classs.set()
    await message.reply("Привет в каком классе ты учишься?")

@dp.message_handler(state=Form.classs)
async def process_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['class'] = message.text

        await bot.send_message(
            message.chat.id, md.text(md.text(data['class']))
        )


    await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
