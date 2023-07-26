# Файл обработчиков событий бот-чата Telegam

from main import bot, dp
from aiogram import types
from api_class import Numbers, Cats, Weather
import time
import logging
import os


# Инициализация объектов классов, работающих с сайтами...
w = Weather(f'https://wttr.in/')       # ... погоды
cats = Cats(f'https://http.cat')      # ... ошибок с котиками
nm = Numbers('http://numbersapi.com')  # ... фактов по цифрам/числам/датам

admin_id = os.environ["ADMIN_ID"]  # загружаем из переменных окружения
if not admin_id:
    exit("Error: no admin ID provided")

# уведомление админа о начале работы бота
async def send_to_admin(dp):
    await bot.send_message(chat_id=admin_id, text='Бот запущен')

# Начало работы бота по команде /start
### Кнопки
@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["Погода", "Котики", 'Цифры']
    keyboard.add(*buttons)

    user_id = message.from_user.id
    user_full_name = message.from_user.full_name
    logging.info(f'{user_id=}{user_full_name=}{time.asctime()}')

    await message.reply(f'Привет,{user_full_name}!')
    await message.answer("Нажми на кнопку", reply_markup=keyboard)

### Кнопка погода
@dp.message_handler(lambda message: message.text == "Погода")
async def weather_handler(message: types.Message):
    await message.answer(text='Нажмите на кнопку, чтобы разрешить геолокацию',
                         reply_markup=get_keyb_geo())

# Создание кнопки геолокации
def get_keyb_geo():
    keyb_geo = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    butt_geo = types.KeyboardButton("Разрешить геолокацию", request_location=True)
    keyb_geo.add(butt_geo)
    keyb_geo.add(types.KeyboardButton("Возврат"))
    return keyb_geo

# Если геолокации на устройстве нет
@dp.message_handler(text='Разрешить геолокацию')
async def handle_location(message: types.Message):
    await message.answer_photo(photo=w.get_weather(city="Москва"),
                               reply_markup=types.message.ReplyKeyboardRemove(),
                               caption="Геолокация не разрешена, поэтому погода в Москве")
    await start_handler(message)

# Если на устройстве есть геолокация
@dp.message_handler(content_types=['location'])
async def handle_location(message: types.Message):
    # print(message)
    lat = round(message.location.latitude,2)
    lon = round(message.location.longitude,2)
    await message.answer_photo(photo=w.get_weather(city="{},{}".format(lat, lon)),
                               reply_markup=types.message.ReplyKeyboardRemove())
    await start_handler(message)

# Возврат из запроса геолокации
@dp.message_handler(lambda message: message.text == "Возврат")
async def return_to_start(message: types.Message):
    await message.answer("Возврат", reply_markup=types.message.ReplyKeyboardRemove())
    await start_handler(message)

### Кнопка котики с фото
@dp.message_handler(lambda message: message.text == "Котики")
async def cats_handler(message: types.Message):
    await bot.send_photo(message.chat.id, photo=cats.get_cat(), caption='Мяу')

### Кнопка Цифры
@dp.message_handler(lambda message: message.text == "Цифры")
async def help_handler(message: types.Message):
    await message.answer(text='Интересные факты, связанные с числами')
    #  Создаем дополнительные кнопки
    inline_buttons = [
        types.InlineKeyboardButton(text='Год', callback_data='num_year'),
        types.InlineKeyboardButton(text='Дата', callback_data='num_date'),
        types.InlineKeyboardButton(text='Математика', callback_data='num_math'),
        types.InlineKeyboardButton(text='Разное', callback_data='num_trivia'),
        types.InlineKeyboardButton(text='Выход', callback_data='num_exit')
    ]
    inline_keyboard = types.InlineKeyboardMarkup(row_width=2, resize_keyboard=True, )
    inline_keyboard.add(*inline_buttons)
    await message.answer('Нажми на кнопку, для получения данных', reply_markup=inline_keyboard)

# Случайные данные по году
@dp.callback_query_handler(text='num_year')
async def send_num_trivia(call: types.CallbackQuery):
    await call.message.answer(text=nm.get_random_year())
    await call.message.delete_reply_markup()
    await call.answer()

# Случайные данные по дате
@dp.callback_query_handler(text='num_date')
async def send_num_trivia(call: types.CallbackQuery):
    await call.message.answer(text=nm.get_random_date())
    await call.message.delete_reply_markup()
    await call.answer()

# Случайные данные
@dp.callback_query_handler(text='num_trivia')
async def send_num_trivia(call: types.CallbackQuery):
    await call.message.answer(text=nm.get_random_fact())
    await call.message.delete_reply_markup()
    await call.answer()

# Случайные данные из математики
@dp.callback_query_handler(text='num_math')
async def send_num_trivia(call: types.CallbackQuery):
    await call.message.answer(text=nm.get_random_math())
    await call.message.delete_reply_markup()
    await call.answer()

# Выход из меню работы с цифрами
@dp.callback_query_handler(text='num_exit')
async def send_num_trivia(call: types.CallbackQuery):
    await call.message.delete_reply_markup()
    await call.answer()

# Обработка всех необработанных сообщений
@dp.message_handler()
async def echo(message: types.Message):
    text = f"Привет {message.from_user.full_name}, ты написал: '{message.text}'\n" +\
           f'Я пока не знаю такой команды. ' + \
           f'Набери: /start или нажми на кнопку'
    await message.answer(text=text)
