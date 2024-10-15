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
from util.tranlate_util import answer_by_lang_with_redis

router = Router()
router.message.middleware(RegisterCheckMiddleware())
user_service = UserService(session=async_session)


class AIQuestion(StatesGroup):
    question = State()


@router.message(Command("qu"))
async def qu(message: Message, state: FSMContext):
    await state.set_state(AIQuestion.question)
    translated_texts = await answer_by_lang_with_redis('Type your question', message.chat.id, user_service)
    await message.answer(translated_texts)


@router.message(AIQuestion.question)
async def qu1(message: Message, state: FSMContext):
    if await util.exit_handler(message, state, 'ai'):
        return
    role = await user_service.read(message.chat.id)
    cat = role.category.name.lower()
    await ai_machine.handle_request(message, cat,
                                    f"Reply as {cat}. {message.text} Reply must be in {role.lang.name.lower()}. ",
                                    user_service)
