from aiogram import Router, F, Bot
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from config import GOOGLE, TELEGRAM
from app.states import AI

import google.generativeai as genai

router1 = Router()
genai.configure(api_key=GOOGLE)
model = genai.GenerativeModel('gemini-1.5-flash')

conversation_history = {}  # Хранение истории общения для каждого пользователя

@router1.message(F.text.startswith('/google'))
async def ai(message: Message, state: FSMContext):
    user_message = message.text[len('/chatgpt '):]  # отрезаем '/chatgpt '
    await state.set_state(AI.answer)
    user_id = message.from_user.id

    try:
        chat = conversation_history.get(user_id, None)
        if chat is None:
            chat = model.start_chat(history=[])
            conversation_history[user_id] = chat

        response = await chat.send_message_async(user_message)
        await message.reply(response.text)
        await state.clear()  # Обязательно очищаем состояние

    except Exception as e:
        await message.reply(f"Произошла ошибка: {e}")
        chat = model.start_chat(history=[])
        conversation_history[user_id] = chat
