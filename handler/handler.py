from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from .middleware.middleware import RegisterCheckMiddleware

router = Router()
router.message.middleware(RegisterCheckMiddleware())


@router.message(CommandStart())
async def start_handler(message: Message):
    await message.answer("hello world")
