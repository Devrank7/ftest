import asyncio

import nest_asyncio
from aiogram import Bot
from aiogram.types import Message
from g4f.client import Client

from db.service import UserService
from util.tranlate_util import answer_by_lang_with_redis

nest_asyncio.apply()
client = Client()


async def handle_request(message: Message, cat: str, prompt: str, user_service: UserService) -> None:
    typing_task = asyncio.create_task(send_typing_status(message.bot, message.chat.id))
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": str(cat), "content": prompt}]
        )
        generated_text = response.choices[0].message.content
        translated_texts = await answer_by_lang_with_redis('Answer', message.chat.id, user_service)
        await message.answer(f"{translated_texts}: {generated_text}")
    finally:
        typing_task.cancel()


async def send_typing_status(bot: Bot, chat_id: int):
    while True:
        await bot.send_chat_action(chat_id=chat_id, action="typing")
        await asyncio.sleep(5)
