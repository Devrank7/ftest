from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from db.db import async_session
from db.nosql import redis_op
from db.service import UserService
from util.util import answer_by_lang_with_redis
from .middleware.middleware import RegisterCheckMiddleware

router = Router()
router.message.middleware(RegisterCheckMiddleware())
user_service = UserService(session=async_session)


@router.message(CommandStart())
async def start_handler(message: Message):
    translated_text = await answer_by_lang_with_redis('Hello World!', message.chat.id, user_service)
    await message.answer(text=translated_text)
