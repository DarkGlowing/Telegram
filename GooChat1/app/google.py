from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext

from config import GOOGLE
from app.states import AI

import google.generativeai as genai

router1 = Router()
genai.configure(api_key=GOOGLE)
model = genai.GenerativeModel('gemini-1.5-flash')


@router1.message(CommandStart())
async def cmd_start(message: Message):
	await message.answer('Привет! GOOGLE')

@router1.message(Command('clear'))
async def process_clear_command(message: Message):
    user_id = message.from_user.id
    conversation_history[user_id] = []
    await message.reply("История диалога очищена.")


@router1.message(AI.answer)
async def answer(message: Message):
	await message.answer('Пожалуйста, подождите! Идёт генерация вашего запроса!')


@router1.message(F.text.startswith('/google'))
async def ai(message: Message, state: FSMContext):
	await state.set_state(AI.answer)
	try:
		chat = (await state.get_data())['context']
		if len(chat.history) > 10:
			chat = model.start_chat(history=[])
		response = await chat.send_message_async(message.text)
		await state.update_data(context=chat)
	except:
		chat = model.start_chat(history=[])
		response = await chat.send_message_async(message.text)
		await state.update_data(context=chat)
	await message.answer(response.text)
	await state.clear()


