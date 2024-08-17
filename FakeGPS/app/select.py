from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart, Command

from app.states import AI
from app.fake import router1

router = Router()

router.include_router(router1)

@router.message(CommandStart())
async def cmd_start(message: Message):
	await message.answer('/set_location (широта) (долгота)')