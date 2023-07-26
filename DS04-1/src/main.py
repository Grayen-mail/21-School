# Основной исполняемый файл

import asyncio
import os
from aiogram import Bot, Dispatcher, executor   # требует "pip install aiogram"
from dotenv.main import load_dotenv  # требует "pip install python-dotenv"
from sys import exit


load_dotenv()  # Загружаем .env в переменные окружения
bot_token = os.environ["BOT_TOKEN"]  # загружаем из переменных окружения
if not bot_token:
    exit("Error: no token provided")

#proxy = os.environ["PROXY_URL"]
#if not proxy:
#    exit("Error: no proxy provided")
# Для использования прокси убираем комментарии с 3 строк выше...
# ... и закомментируем строку ниже
proxy = None

# создаём необходимые объекты
loop = asyncio.get_event_loop()
bot = Bot(token=bot_token, parse_mode='HTML', proxy=proxy)
dp = Dispatcher(bot=bot, loop=loop)

if __name__ == '__main__':
    from handlers import dp, send_to_admin
    executor.start_polling(dp, on_startup=send_to_admin)
