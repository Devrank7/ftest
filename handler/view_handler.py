from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message
from googletrans import Translator

from db.db import async_session
from db.service import UserService
from handler.middleware.middleware import RegisterCheckMiddleware
from util import util

router = Router()
router.message.middleware(RegisterCheckMiddleware())
user_service = UserService(session=async_session)
translator = Translator()


class Translated(StatesGroup):
    translation = State()


@router.message(Command("my"))
async def my_handler(message: Message):
    user = await user_service.read(message.chat.id)
    await message.answer(user.__str__())


@router.message(Command("deep_gcloud"))
async def translate_and_recognize(message: Message, state: FSMContext):
    await state.set_state(Translated.translation)
    await message.answer("Type text to translate.")


@router.message(Translated.translation)
async def translated_text(message: Message, state: FSMContext):
    if await util.exit_handler(message, state, 'translate'):
        return
    user = await user_service.read(message.chat.id)
    val = user.lang.value
    translated = translator.translate(message.text, dest=str(val))
    print(translated.text)
    detected = translator.detect(message.text)
    print(detected.lang)
    await message.answer(f"Translated text {translated.text} from {detected.lang} to {str(val)}")
