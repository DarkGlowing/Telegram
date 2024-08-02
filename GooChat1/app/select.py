from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart, Command

from app.states import AI
from app.google import router1
from app.chatgpt import router2

router = Router()

router.include_router(router1)
router.include_router(router2)

@router.message(CommandStart())
async def cmd_start(message: Message):
	await message.answer('Привет! /chatgpt or /google')