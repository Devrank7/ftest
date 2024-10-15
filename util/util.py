from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils.keyboard import InlineKeyboardBuilder
from googletrans import Translator

from db.enum.enums import Language
from db.nosql import redis_op
from db.service import UserService

translator = Translator()

MAX_LEN_CACHE = 200


def build_buttons(values: list[str], prefix: str, separator: int = 2) -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    for i, value in enumerate(values):
        if i % separator == 0 and i != 0:
            builder.row()
        builder.button(text=value, callback_data=f"{prefix}_{value}")
    return builder


def build_button_with_back(callback_data: str, values: list[str], prefix: str,
                           separator: int = 2) -> InlineKeyboardBuilder:
    builder = build_buttons(values, prefix, separator)
    builder.row()
    builder.button(text="Back", callback_data=callback_data)
    return builder


async def exit_handler(message: Message, state: FSMContext, state_name: str) -> bool:
    if message.text.strip() == '/exit':
        await state.clear()
        await message.answer(f"Exit {state_name} state")
        return True
    return False


async def adjust_lang(text: str, lang: Language) -> dict[str, str]:
    lan = lang.value.strip().lower()
    detected = translator.detect(text)
    if lan == detected.lang:
        return {"text": text, "lang": detected.lang}
    translated = translator.translate(text, dest=str(lan))
    return {"text": translated.text, "lang": detected.lang}


async def answer_by_lang_with_redis(text: str, chat_id: int, user_service: UserService, max_len: int = 100) -> str:
    user = await user_service.read(chat_id)
    print("user lang = ", user.lang)

    async def cacheable_function(texts: str):
        print("Text = ", texts)
        return await adjust_lang(text=texts, lang=user.lang)

    dic = await redis_op.cacheable(key=f"{text}_{user.lang.value.lower()}", func=cacheable_function) if len(text) < min(
        max_len, MAX_LEN_CACHE) else await cacheable_function(text)
    return dic['text']
