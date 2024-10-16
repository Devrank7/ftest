import asyncio
import os

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv

from db.db import init_db
from handler import handler, reg_handler, set_handler, view_handler, ai_handler

load_dotenv()
API_KEY = os.getenv("API_TOKEN")

bot = Bot(token=API_KEY)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)


async def main():
    print("Hello World!")
    await init_db()
    dp.include_router(handler.router)
    dp.include_router(reg_handler.route)
    dp.include_router(set_handler.router)
    dp.include_router(view_handler.router)
    dp.include_router(ai_handler.router)
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


def shutdown():
    for task in asyncio.all_tasks():
        task.cancel()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("Программа была прервана.")
