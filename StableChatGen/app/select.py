from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart, Command

from app.states import AI
from app.google import router1
from app.chatgpt import router2
from app.image import router3
from app.speechify import router4

router = Router()

router.include_router(router1)
router.include_router(router2)
router.include_router(router3)
router.include_router(router4)

@router.message(CommandStart())
async def cmd_start(message: Message):
	await message.answer('Привет! Напиши свой текстовый запрос через ChatGPT-4-Turbo через команду /chatgpt (доступна также модель от гугл Gemini-1.5-Flash через /google). Чтобы сгенерировать твое желаемое изображение напиши команду /image. Если вам необходимо сгенерировать аудио файл на английском языке, то используйте команду /voice')