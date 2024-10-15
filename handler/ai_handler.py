from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message

from ai import ai_machine
from db.db import async_session
from db.service import UserService
from handler.middleware.middleware import RegisterCheckMiddleware
from util import util

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
    if await util.exit_handler(message, state, 'ai'):
        return
    role = await user_service.read(message.chat.id)
    cat = role.category.name.lower()
    await ai_machine.handle_request(message, cat,
                                    f"Reply as {cat}. {message.text} Reply must be in {role.lang.name.lower()}. ")
