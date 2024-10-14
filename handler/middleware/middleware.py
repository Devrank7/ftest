from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from db.db import async_session
from db.service import UserService

user_service = UserService(session=async_session)


class RegisterCheckMiddleware(BaseMiddleware):

    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]
    ) -> Any:
        if await user_service.exists(event.chat.id):
            return await handler(event, data)
        builder = InlineKeyboardBuilder()
        button = InlineKeyboardButton(text="Register settings for this chat", callback_data="register")
        builder.add(button)
        await event.message.answer(
            "Hello world! You need to register", reply_markup=builder.as_markup())
