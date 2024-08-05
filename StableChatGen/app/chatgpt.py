from aiogram import Router, F, Bot
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from g4f.client import Client
from pathlib import Path
import requests
import time
import os

from app.states import AI
from config import SPEECHFLOW_KEYID, SPEECHFLOW_KEYSECRET, TELEGRAM

bot = Bot(token=TELEGRAM)

API_KEY_ID = SPEECHFLOW_KEYID
API_KEY_SECRET = SPEECHFLOW_KEYSECRET

LANG = "ru"
RESULT_TYPE = 1

router2 = Router()
client = Client()
conversation_history = {}  # Хранение истории общения для каждого пользователя

@router2.message(F.voice)
async def voice_translator(message: Message):
    file_id = message.voice.file_id
    file = await bot.get_file(file_id)  
    file_path = file.file_path  
    file_name = f"temp_{file_id}.mp3"  
    await bot.download_file(file_path, file_name)

    headers = {"keyId": API_KEY_ID, "keySecret": API_KEY_SECRET}
    create_url = "https://api.speechflow.io/asr/file/v1/create?lang=ru"
    query_url = "https://api.speechflow.io/asr/file/v1/query?taskId="

    with open(file_name, "rb") as f:
        response = requests.post(create_url, headers=headers, files={"file": f})  
        
    if response.status_code == 200:  
        create_result = response.json()  
        query_url += create_result["taskId"] + "&resultType=4"  

        while True:  
            response = requests.get(query_url, headers=headers)  
            if response.status_code == 200:  
                query_result = response.json()  
                if query_result["code"] == 11000:  
                    if query_result["result"]:  
                        result = query_result["result"].replace("\n\n", " ")   
                        os.remove(file_name)  
                    break  
                elif query_result["code"] == 11001:  
                    time.sleep(3)  
                    continue  
                else:  
                    break  
            else:  
                break
    else:  
        await message.reply("Произошла ошибка при отправке файла на обработку.")

# Запрашиваем ответ у ChatGPT
    try:
        response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[{"role": "user", "content": result}],
        )
        await message.reply(response.choices[0].message.content)  # Ответ GPT
    except Exception as e:
        await message.reply(f"Произошла ошибка: {e}")


@router2.message(F.text.startswith('/chatgpt'))
async def ai(message: Message, state: FSMContext):
    # Получаем текст сообщения после команды
    user_message = message.text[len('/chatgpt '):]  # отрезаем '/chatgpt '
    # Запрашиваем ответ у ChatGPT
    try:
        response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[{"role": "user", "content": user_message}],
        )
        await message.reply(response.choices[0].message.content)  # Ответ GPT
    except Exception as e:
        await message.reply(f"Произошла ошибка: {e}")







