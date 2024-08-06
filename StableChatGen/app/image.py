from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from deep_translator import GoogleTranslator
import requests
import json

from app.states import AI
from config import SHUTTLEAI

router3 = Router()

Image_URL = "https://api.shuttleai.app/v1/images/generations"

conversation_history = {}  # Хранение истории общения для каждого пользователя

@router3.message(F.text.startswith('/image'))
async def ai(message: Message, state: FSMContext):
    # Получаем текст сообщения после команды
    user_message = message.text[len('/image '):]  # отрезаем '/image '
    # Переводим текст
    try:
        translated = GoogleTranslator(source='auto', target='en').translate(user_message)
    except Exception as e:
        await message.reply("Ошибка при переводе: " + str(e))
        return
    
    # Запрашиваем ответ у DALL-E 3
    try:
        response = requests.post(
            Image_URL,
            headers={
                "Authorization": f"Bearer {SHUTTLEAI}",
                "Content-Type": "application/json"
            },
            json={
                "model": "shuttle-2-diffusion",  # Убедитесь, что это правильная модель
                "prompt": translated,
                "n": 1,
                "size": "1024x1024"
            }
        )

        if response.status_code == 200:
            response_data = response.json()
            image_url = response_data['data'][0]['url']  # Убедитесь, что структура ответа верная

            await message.reply(f"Вот твоя картинка, по запросу: {user_message}: {image_url}")  # Используем f-string для подстановки URL
        else:
            await message.reply("Ошибка при генерации изображения!")  # Выводим текст ошибки из ответа
    
    except Exception as e:
        await message.reply("Ошибка: " + str(e))  # Ловим любые исключения
    
    await state.clear()  # Очищаем состояние после обработки

