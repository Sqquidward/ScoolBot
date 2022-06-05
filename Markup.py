from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import datetime

day = ['понедельник', 'вторник', 'среду', 'четверг', 'пятницу', 'субботу', 'воскресенье']
day_week = datetime.datetime.today().weekday()
i = 1
if day_week == 6: day_week = 0
if day_week == 5: i = 5
day_week = 1

keyboard = InlineKeyboardMarkup()
inline_Raspisanie = KeyboardButton('Расписание', callback_data='raspisanie')
inline_Info = KeyboardButton('Основные сведения', callback_data='info')
inline_Time = KeyboardButton('Звонки', callback_data='time')
mainMenu = InlineKeyboardMarkup(resize_keyboard=True).add(inline_Raspisanie).add(inline_Info).add(inline_Time)

inline_Rasp_thisday = InlineKeyboardButton(f'Расписание на {day[day_week]}', callback_data='Rasp_thisday')
inline_Rasp_nextday = InlineKeyboardButton(f'Расписание на {day[day_week+i]}', callback_data='Rasp_nextday')
inline_Rasp_pdf = InlineKeyboardButton('Расписание PNG',  callback_data='Rasp_png')
inline_cancel = InlineKeyboardButton('Назад',  callback_data='cancel')
Raspisanie = InlineKeyboardMarkup().add(inline_Rasp_thisday).add(inline_Rasp_nextday).add(inline_Rasp_pdf).add(inline_cancel)


inline_cancel = InlineKeyboardButton('Назад',  callback_data='cancel')
Cancel = InlineKeyboardMarkup().add(inline_cancel)

inline_cancel = InlineKeyboardButton('Назад',  callback_data='cancel_png')
Cancel_png = InlineKeyboardMarkup().add(inline_cancel)


inline_cancel = InlineKeyboardButton('Назад',  callback_data='cancel')
inline_url = InlineKeyboardButton('Сайт лицея',  url='https://1523.mephi.ru/')
Info_cancel = InlineKeyboardMarkup().add(inline_url).add(inline_cancel)
