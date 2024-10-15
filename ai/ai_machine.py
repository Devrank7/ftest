import asyncio

import nest_asyncio
from aiogram import Bot
from aiogram.types import Message
from g4f.client import Client

nest_asyncio.apply()
client = Client()


async def handle_request(message: Message, cat: str, prompt: str) -> None:
    typing_task = asyncio.create_task(send_typing_status(message.bot, message.chat.id))
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": str(cat), "content": prompt}]
        )
        generated_text = response.choices[0].message.content
        await message.answer(f"Answer: {generated_text}")
    finally:
        typing_task.cancel()


async def send_typing_status(bot: Bot, chat_id: int):
    while True:
        await bot.send_chat_action(chat_id=chat_id, action="typing")
        await asyncio.sleep(5)
