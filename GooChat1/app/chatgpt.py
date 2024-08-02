from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

from config import CHATGPT
from app.states import AI

import openai

router2 = Router()
openai.api_key = CHATGPT

@router2.message(CommandStart())
async def cmd_start(message: Message):
	await message.answer('Привет! CHATGPT')


@router2.message(F.text.startswith('/chatgpt'))
async def answer(message: Message):
    response = openai.Completion.create(
        engine='gpt-4-all',
        prompt=message.text,
        temperature=1,
        max_tokens=2048,
        top_p=0.7,
        frequency_penalty=0,
        presence_penalty=0.9,
    )
    await response.choices[0].text


