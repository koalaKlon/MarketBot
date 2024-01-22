import asyncio
import logging
import sys
import os
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
from handlers import router

load_dotenv()

dp = Dispatcher()


async def main() -> None:
    bot = Bot(os.getenv("TOKEN_API"))
    dp.include_router(router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())


app = dp





