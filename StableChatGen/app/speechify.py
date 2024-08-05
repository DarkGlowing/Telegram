from aiogram import Router, F, Bot
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.methods.send_voice import SendVoice
from aiogram.methods import SendVoice
import subprocess
import requests
import json

from app.states import AI
from config import SHUTTLEAI1, TELEGRAM

bot = Bot(token=TELEGRAM)

router4 = Router()

Voice_URL = "https://api.shuttleai.app/v1/audio/speech"

conversation_history = {}  # Хранение истории общения для каждого пользователя

@router4.message(F.text.startswith('/voice'))
async def ai(message: Message, state: FSMContext):
    # Получаем текст сообщения после команды
    user_message = message.text[len('/voice '):]  # отрезаем '/voice '
    
    # Запрашиваем ответ у Speechify
    try:
        response = requests.post(
            Voice_URL,
            json={
                "model": "speechify",  # Замените на нужную модель
                "input": user_message,  # Используем правильное имя переменной
            },
            headers={
                "Authorization": f"Bearer {SHUTTLEAI1}",
                "Content-Type": "application/json"
            }
        )

        if response.status_code == 200:
            response_data = response.json()
            
            # Предполагаем, что API возвращает URL к аудиофайлу
            audio_url = response_data['data']['url']
            if audio_url:
                await message.answer_voice(audio_url)  # Отправляем аудиофайл пользователю
            else:
                await message.answer("Не удалось получить аудио.")
        else:
            await message.answer("Произошла ошибка при генерации речи, попробуйте повторить через минуту...")

    except Exception as e:
        await message.answer("Произошла ошибка: " + str(e))  # Ловим любые исключения