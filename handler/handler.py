from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from db.db import async_session
from db.service import UserService
from util.util import answer_by_lang
from .middleware.middleware import RegisterCheckMiddleware

router = Router()
router.message.middleware(RegisterCheckMiddleware())
user_service = UserService(session=async_session)


@router.message(CommandStart())
async def start_handler(message: Message):
    await message.answer(await answer_by_lang('Hello World!', message.chat.id, user_service))
