from os import path

import openpyxl
import datetime
import logging
import aiogram.utils.markdown as md
from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import callback_query, message
from aiogram.utils import executor
import sqlite3
import Markup as nav
from Token import API_TOKEN


book = openpyxl.open("Raspisanie.xlsx", read_only=True)
table = openpyxl.open("Четность.xlsx", read_only=True)
sheet = table.active


base_main = sqlite3.connect('group_main.db')
cursor = base_main.cursor()
base_main.execute('CREATE TABLE IF NOT EXISTS data(login PRIMARY KEY, class VARCHAR)')
base_main.commit()


base_zamena = sqlite3.connect('group_zamena.db')
cur = base_zamena.cursor()
base_zamena.execute('CREATE TABLE IF NOT EXISTS data(login text, class text)')
base_zamena.commit()






logging.basicConfig(level=logging.INFO)
API_TOKEN = API_TOKEN

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

class Form_2(StatesGroup):
    classs = State()

class Form_1(StatesGroup):
    clas = State()
    zamena = State()


@dp.message_handler(commands='start')
async def cmd_start(message: types.Message):
    await Form_2.classs.set()
    await message.answer("Привет\nВ каком классе ты учишься?\nНапример: 10м1")

@dp.message_handler(state=Form_2.classs)
async def process_name(message: types.Message, state: FSMContext):

    async with state.proxy() as data:
        text = data['class'] = message.text

        textt , clas = check_text(text)
        if clas == 'Error':
            await message.answer('Вводи обязательно с буквой и группой класса!\nПопробуйте еще раз')
            await message.answer('P.S. функцию нужно вызвать еще раз/start')

        else:
            info = cursor.execute('SELECT * FROM data WHERE login == ?', (message.from_user.id,))
            if info.fetchone() is None:
                cursor.execute('INSERT INTO data VALUES(?, ?)',
                               (message.from_user.id, f'{clas}'))
                base_main.commit()
                await bot.send_message(
                    message.chat.id, "Отлично,\nтеперь ты можешь воспользоваться моими функциями",
                    reply_markup=nav.mainMenu
                )
            else:
                cursor.execute('UPDATE data SET class == ? WHERE login == ?',
                               (f'{clas}', message.from_user.id))
                base_main.commit()
                await bot.send_message(
                    message.chat.id, "Отлично,\n данные перезаписаны", reply_markup=nav.mainMenu
                )
        await state.finish()




@dp.message_handler(commands='add_zamena')
async def start(message: types.Message):
    await Form_1.clas.set()
    await message.answer("Какой класс?")

@dp.message_handler(state=Form_1.clas)
async def process_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['clas'] = message.text
    await Form_1.next()
    await message.answer("Назовите замену?")

@dp.message_handler(state=Form_1.zamena)
async def process_number(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['clas'] = data['clas'].upper()
        data['zamena'] = message.text

        textet, clas = check_text(data['clas'])
        if clas == 'Error':
            await bot.send_message(message.from_user.id, 'Попробуйте еще раз,\nЯ такого класса не знаю')
            await bot.send_message(message.from_user.id, 'P.S. функцию нужно вызвать еще раз /add_zamena')

        else:
            list_id = Zamena_check(data["clas"])
            for elem in list_id:
                print(str(elem)[:-2][1:])
                await bot.send_message(str(elem)[:-2][1:], f'Привет, появились измменения в расписании\n {data["clas"]} - {data["zamena"]}')
            await bot.send_message(message.from_user.id, f"Данные занесены")

        await state.finish()


@dp.message_handler(commands='my_class')
async def start(message: types.Message):
    r = f"{cursor.execute('SELECT class FROM data WHERE login == ?', (message.from_user.id,)).fetchone()}"
    await message.answer('Твой класс ' + r.replace("'", "").replace(",", '').replace('(', '').replace(')', ''))

@dp.message_handler(commands='time')
async def start(message: types.Message):
    text = Time().replace("(", "").replace(")", "").replace("'", "").replace(",", "")
    await message.answer(text)

@dp.message_handler(commands='timetable')
async def start(message: types.Message):
    print('Это начало работать')
    clas = f"{(cursor.execute('SELECT class FROM data WHERE login == ?', (message.from_user.id,)).fetchone())}".replace("(", "").replace(")", "").replace("'", "").replace(",", "")
    # print(clas)
    # way = path.join('Raspisanie', f'Class {return_clas(clas)}', f'{Bukva(clas)}.jpg')
    way = f'Raspisanie\Class {return_clas(clas)}\{Bukva(clas)}.png'
    # print(way)
    await bot.send_document(callback_query.from_user.id, open(way, 'rb'), reply_markup=nav.Cancel)

@dp.message_handler(commands=['menu', 'help'])
async def send_welcome(message: types.Message):
    await message.answer("Данный бот создан специально\nдля учеников лицея, чтобы выполнять нетрудные задачи", reply_markup=nav.mainMenu)


@dp.callback_query_handler(lambda c: c.data == 'Rasp_thisday')
async def process_callback_button1(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
    r = f"{(cursor.execute('SELECT class FROM data WHERE login == ?', (callback_query.from_user.id,)).fetchone())}".replace("(", "").replace(")", "").replace("'", "").replace(",", "")
    await bot.send_message(callback_query.from_user.id, Emptiness(do_Smt(r, 0)), reply_markup=nav.Cancel)

@dp.callback_query_handler(lambda c: c.data == 'Rasp_nextday')
async def process_callback_button1(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
    r = f"{(cursor.execute('SELECT class FROM data WHERE login == ?', (callback_query.from_user.id,)).fetchone())}".replace("(", "").replace(")", "").replace("'", "").replace(",", "")
    await bot.send_message(callback_query.from_user.id, Emptiness(do_Smt(r, 1)), reply_markup=nav.Cancel)

@dp.callback_query_handler(lambda c: c.data == 'Rasp_png')
async def process_callback_button1(callback_query: types.CallbackQuery):
    print('да')
    await bot.answer_callback_query(callback_query.id)
    await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
    await bot.send_message(callback_query.from_user.id, 'Подожди пару секунд')
    clas = f"{(cursor.execute('SELECT class FROM data WHERE login == ?', (callback_query.from_user.id,)).fetchone())}".replace("(", "").replace(")", "").replace("'", "").replace(",", "")
    way = f'Raspisanie\Class {return_clas(clas)}\{Bukva(clas)}.png'
    await bot.send_document(callback_query.from_user.id, open(way, 'rb'), reply_markup=nav.Cancel_png)

@dp.callback_query_handler(lambda c: c.data == 'time')
async def process_callback_button1(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
    await bot.send_message(callback_query.from_user.id, f'1 урок 08.45-9.30\n2 урок 09.45-10.30 \n3 урок 10.40-11.25\n'
                                                        f'4 урок 11.35-12.20\n5 урок 12.45-13.30\n6 урок 13.55-14.40\n'
                                                        f'7 урок 14.50-15.35\n8 урок 15.45-16.30' , parse_mode=types.ParseMode.HTML, reply_markup=nav.Cancel)

@dp.callback_query_handler(lambda c: c.data == 'info')
async def process_callback_button1(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
    await bot.send_message(callback_query.from_user.id, f'НАИМЕНОВАНИЕ\nУниверситетский лицей №1523 предуниверситария НИЯУ МИФИ\n'
                                                        f'\nМЕСТОНАХОЖДЕНИЕ\n115142, г. Москва, Кленовый б-р, д. 21\n'
                                                        f'\nКОНТАКТНЫЙ ТЕЛЕФОН\n+7(499)614-50-94\n\nЭЛЕКТРОННАЯ ПОЧТА\n'
                                                        f'1523@mephi.ru', reply_markup=nav.Info_cancel)

@dp.callback_query_handler(lambda c: c.data == 'raspisanie')
async def process_callback_button1(callback_query: types.CallbackQuery):
    day_week = datetime.datetime.today().weekday()
    day = ['понедельник', 'вторник', 'среду', 'четверг', 'пятницу', 'субботу', 'воскресенье']
    day_week = 1
    await bot.answer_callback_query(callback_query.id)
    await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
    await bot.send_message(callback_query.from_user.id, f'Выберите\n{day[day_week]}, {day[day_week+1]}' , reply_markup=nav.Raspisanie)

@dp.callback_query_handler(lambda c: c.data == 'cancel')
async def process_callback_button1(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
    await bot.send_message(callback_query.from_user.id, 'Ты можешь воспользоваться моими функциями', reply_markup=nav.mainMenu)

@dp.callback_query_handler(lambda c: c.data == 'cancel_png')
async def process_callback_button1(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    # await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
    await bot.send_message(callback_query.from_user.id, 'Ты можешь воспользоваться моими функциями', reply_markup=nav.mainMenu)

@dp.callback_query_handler(lambda c: c.data == 'zamena')
async def process_callback_button1(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
    await bot.send_message(callback_query.from_user.id, 'К сожалению эта функция находится пока в разработке', reply_markup=nav.Cancel)

@dp.message_handler(commands=['info'])
async def send_welcome(message: types.Message):
    await message.answer("Данный бот создан специально\nдля учеников лицея, чтобы выполнять нетрудные задачи")

@dp.message_handler(commands=['my_id'])
async def send_welcome(message: types.Message):
    await bot.send_message(message.from_user.id, message.from_user.id)


@dp.message_handler(text=['паша'])
async def send_welcome(message: types.Message):
    await bot.send_message(message.from_user.id, 'Украина наша')

@dp.message_handler()
async def send_welcome(message: types.Message):
    await bot.send_message(message.from_user.id, 'К сожалению я пока что не знаю такой функции')

def do_Smt(text, i):
    try:
        for page_Num in range(0, 9):
            for char in range(66, 79):
                if book.worksheets[page_Num][f'{chr(char)}9'].value == text:
                    print(' Я нашел')
                    return Subject_today(page_Num, char, i)

    except Exception as ex:
        return 'Произошла ошибка', ex

def Zamena_check(text):
    return cursor.execute('SELECT login FROM data WHERE class == ?', (text,)).fetchall()

def check_text(text):
    list_1 = ['8', '9', '10', '11']
    list_2 = ['М', 'Н', 'О', 'П', 'Р', 'C']
    list_3 = ['1', '2']

    flag = False

    print(text.upper())

    for i in range(0, 4):
        if flag == True:
            break
        for j in range(0, 6):
            if flag == True:
                break
            for k in range(0, 2):
                if '10С' in text.upper():
                    return 'Твои данные зарегестированы' , '10С'
                    flag = True
                elif f'{list_1[i]}{list_2[j]}{list_3[k]}' in text.upper():
                    return 'Твои данные зарегестированы', f'{list_1[i]}{list_2[j]}{list_3[k]}'
                    flag = True
    if flag == False:
        return 'Попробуй еще раз, пример ввода: 10м2', 'Error'





def Subject_today(page_Num, char, i):
    if Parity() == 'ч':
        page_Num+=1
    integer = [11, 21, 31, 42, 52, 62]
    today = datetime.datetime.today().weekday()
    if today == 5 and i == 1:
        today = 0; i = 0
    tod = Days(today, i)
    try:
        les = ''
        les += '1. '+book.worksheets[page_Num][f'{chr(char)}{integer[tod+i]}'].value + '\n'
        print(les+'1')
        les += '2. '+book.worksheets[page_Num][f'{chr(char)}{integer[tod+i] + 2}'].value + '\n'
        print(les+'2')
        les += '3. '+book.worksheets[page_Num][f'{chr(char)}{integer[tod+i] + 5}'].value + '\n'
        print(les)
        les += '4. '+book.worksheets[page_Num][f'{chr(char)}{integer[tod+i] + 7}'].value + '\n'
        print(les)
    except Exception as ex:
        pass
    return les

def return_clas(clas):
    try:
        if clas[:2] == '10' or clas[:2] == '11':
            return clas[:2]
        else:
            return clas[:1]
    except Exception as ex:
        pass


def Days(i, j):
    now = datetime.datetime.now()

    if j == 0:
        # для расписания на сегодня

        if i == 6:
            return 0

        elif i == 5 and now.hour > 15:
            return 0

        else:
            return i

        # elif now.hour>17:
        #     return today+1

    elif j == 1:
        # для расписания на завтра

        if i == 6:
            return 1

        elif i == 5 and now.hour > 15:
            return 1

        else:
            return i

def Emptiness(text):
    if text == '':
        return 'У тебя сегодня нет уроков'
    else:
        return text


def Path(way):
    N = 0
    text = ''
    for i in str(way):
        print(i, end=' ')
        if i == f" \  ".replace('', ' '):
            print('Нашел', end=' ')
            if N % 2 == 0:
                text += i
            N += 1
        else:
            text += i

    return text


def Parity():
    now = datetime.datetime.now()
    try:
        for i in range(2, 9):
            if now.day - 1 <= sheet[f'{chr(66)}{i}'].value and now.month == sheet[f'{chr(65)}{i}'].value:
                return sheet[f'{chr(67)}{i}'].value
    except:
        pass

def Bukva(text):
    char = text[-2:-1]
    if char == 'М':
        return f'{text[:-2]}M{text[-1:]}'
    if char == 'Н':
        return f'{text[:-2]}H{text[-1:]}'
    elif char == 'О':
        return f'{text[:-2]}O{text[-1:]}'
    elif char == 'П':
        return f'{text[:-2]}p{text[-1:]}'
    elif char == 'Р':
        return f'{text[:-2]}Pp{text[-1:]}'
    else:
        return text


def Time():
    now = datetime.datetime.now()
    digit = now.hour*100+now.minute
    second = 60-now.second

    count = int(str(digit)[-2:])

    if digit >= 845 and digit<= 930:
        # 1 урок
        if digit<=860:
            time = 60-count+30-1
        else:
            time = 30-count-1
        lesson = f'Сейчас 1 урок \nОсталось: {time}:{second} минут'
        return lesson

    elif digit >= 945 and digit <= 1030:
        # 2 урок
        if digit<=960:
            time = 60-count+30-1
        else:
            time = 30-count-1
        lesson = f'Сейчас 2 урок \nОсталось: {time}:{second} минут'
        return lesson

    elif digit >= 1040 and digit <= 1125:
        # 3 урок
        if digit<=1060:
            time = 60-count+25-1
        else:
            time = 25-count-1
        lesson = f'Сейчас 3 урок \nОсталось: {time}:{second} минут'
        return lesson

    elif digit >= 1135 and digit <= 1220:
        # 4 урок
        if digit<1160:
            time = 60-count+20-1
        else:
            time = 20-count-1
        lesson = f'Сейчас 4 урок \nОсталось: {time}:{second} минут'
        return lesson

    elif digit >= 1245 and digit <= 1330:
        # 5 урок
        if digit<=1260:
            time = 60-count+30-1
        else:
            time = 30-count-1
        lesson = f'Сейчас 5 урок \nОсталось: {time}:{second} минут'
        return lesson

    elif digit >= 1355 and digit <= 1440:
        # 6 урок
        if digit<=1360:
            time = 60-count+40-1
        else:
            time = 40-digit[-2:]-1
        lesson = f'Сейчас 6 урок \nОсталось: {time}:{second} минут'
        return lesson

    elif digit >= 1450 and digit <= 1535:
        # 7 урок
        if digit<=1460:
            time = 60-count+35-1
        else:
            time = 35-count-1
        lesson = f'Сейчас 7 урок \nОсталось: {time}:{second} минут'
        return lesson

    elif digit >= 1545 and digit <= 1630:
        # 8 урок
        if digit<=1560:
            time = 60-count+30-1
        else:
            time = 30-count-1
        lesson = f'Сейчас 8 урок \nОсталось: {time}:{second} минут'
        return lesson

    elif digit>1630:
        return 'Уроки кончились'


    else:
        return 'Сейчас перемена'




if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)