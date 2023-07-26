# Файл описания классов для работы с внешними API

import requests
import random
from googletrans import Translator  # требует "pip install googletrans==3.1.0a0, httpcore, httpx==0.13.3"


# Инициализируем переводчик
tr = Translator()


# Класс для работы с сайтом чисел
class Numbers:
    def __init__(self, url: str):
        self.url = url

    def get_random_fact(self):  # Получить случайный факт
        response = requests.get(f"{self.url}/random/trivia")
        return response.text + '\n' + tr.translate(response.text, dest='ru').text

    def get_random_year(self):  # Получить случайный факт - год
        response = requests.get(f"{self.url}/random/year")
        return response.text + '\n' + tr.translate(response.text, dest='ru').text

    def get_random_date(self):  # Получить случайный факт - дата
        response = requests.get(f"{self.url}/random/date")
        return response.text + '\n' + tr.translate(response.text, dest='ru').text

    def get_random_math(self):  # Получить случайный факт - математика
        response = requests.get(f"{self.url}/random/math")
        return response.text + '\n' + tr.translate(response.text, dest='ru').text


# Класс для работы с сайтом котиков
class Cats:
    test_list = ['100', '101', '102', '103', '200', '201', '202', '203', '204', '206', '207', '300', '301', '302',
                 '303', '304', '305', '307', '308', '400', '401', '402', '403', '404', '405', '406', '407', '408',
                 '409', '410', '411', '412', '413', '414', '415', '416', '417', '418', '420', '421', '422',
                 '423', '424', '425', '426', '429', '431', '444', '450', '451', '497', '498', '499', '500', '501',
                 '502', '503', '504', '506', '507', '508', '509', '510', '511', '521', '522', '523', '525', '599']

    def __init__(self, url: str):
        self.url = url

    def get_cat(self, number: int = 404):
        r_num = random.choice(self.test_list)  # выбираем случайное значение из списка
        return f"{self.url}/{r_num}.jpg"


# Класс для работы с сайтом погоды
class Weather:
    def __init__(self, url: str):
        self.url = url

    def get_weather(self, city: str = ''):
        response = requests.get(f"{self.url}{city}_0_lang=ru.png")
        return response.url
