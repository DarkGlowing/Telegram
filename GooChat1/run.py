import asyncio

from aiogram import Bot, Dispatcher
from app.select import router

from config import TELEGRAM


async def main():
	bot = Bot(token=TELEGRAM)
	dp = Dispatcher()
	dp.include_router(router)
	await dp.start_polling(bot)


if  __name__ == '__main__':
	try:
		asyncio.run(main())
	except KeyboardInterrupt:
		pass
