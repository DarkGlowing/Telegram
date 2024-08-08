from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

from app.states import AI

import time
import asyncio

# Настройки для Chrome
chrome_options = Options()
chrome_options.add_argument("--use-fake-ui-for-media-stream")
chrome_options.add_argument("--use-fake-device-for-media-stream")

# Стартуем драйвер
driver = webdriver.Chrome(options=chrome_options)

# Список геолокаций для смены, добавьте начальные координаты по умолчанию
storage = MemoryStorage()
router1 = Router()

def change_geolocation(lat, lon):
    driver.execute_cdp_cmd('Emulation.setGeolocationOverride', {
        'latitude': lat,
        'longitude': lon,
        'accuracy': 100
    })
# Открытие страницы
driver.get("https://yandex.ru/maps")	

@router1.message(F.text.startswith('/set_location'))
async def change_gps(message: Message, state: FSMContext):
    user_input = message.text[len('/set_location '):].strip()
    coordinates = user_input.split()
# Список геолокаций для смены
    try:
        if len(coordinates) != 2:
            await message.answer("Please provide both latitude(широта) and longitude(долгота). /set_location (широта) (долгота)")
            return

        user_lat = float(coordinates[0])
        user_lon = float(coordinates[1])
        locations = [(user_lat, user_lon)]

        for lat, lon in locations:
            change_geolocation(lat, lon)
            print(f"Изменение геолокации на: {lat}, {lon}")
            await message.answer(f"Location set to:\nLatitude(широта): {user_lat}\nLongitude(долгота): {user_lon}")
            await asyncio.sleep(0.5)  # Ждать 0.5 секунды
            
    except ValueError:
        await message.answer("Invalid input. Please provide valid numeric values for latitude and longitude.")
    except Exception as e:
        await message.answer(f"An error occurred: {str(e)}")