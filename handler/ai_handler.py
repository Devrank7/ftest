import g4f
from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message

from db.db import async_session
from db.service import UserService
from handler.middleware.middleware import RegisterCheckMiddleware

router = Router()
router.message.middleware(RegisterCheckMiddleware())
user_service = UserService(session=async_session)


class AIQuestion(StatesGroup):
    question = State()


@router.message(Command("qu"))
async def qu(message: Message, state: FSMContext):
    await state.set_state(AIQuestion.question)
    await message.answer("Type your question")


@router.message(AIQuestion.question)
async def qu1(message: Message, state: FSMContext):
    if message.text.strip() == '/exit':
        await state.clear()
        await message.answer("Exit ai state")
        return
    role = await user_service.read(message.chat.id)
    cat = role.category.name.lower()
    lang = role.lang.name.lower()
    prompt = f"Reply as {cat}. {message.text} Reply must be in {lang}. "
    response = g4f.ChatCompletion.create(model="gpt-4o", messages=[{"role": str(cat), "content": prompt}], stream=True)
    res = response[0]
    await message.answer("Answer: {}".format(res))
