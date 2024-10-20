from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

from db.db import async_session
from db.enum.enums import Category, Language, get_all_categories, check_category_exists
from db.service import UserService
from util import util
from util.tranlate_util import answer_by_lang_with_redis
from .middleware.middleware import RegisterCheckMiddleware

router = Router()
router.message.middleware(RegisterCheckMiddleware())
user_service = UserService(session=async_session)


class Form(StatesGroup):
    state_one = State()  # Первое состояние
    state_two = State()  # Второе состояние


@router.message(Command("select"))
async def select_handler(message: Message, state: FSMContext):
    await select(message, state)


@router.callback_query(F.data == "category")
async def category_handler(callback: CallbackQuery, state: FSMContext):
    translated_texts = await answer_by_lang_with_redis('Select category | Back', callback.message.chat.id, user_service)
    tt_split = translated_texts.split("|")
    print('back = ', tt_split[1], ' sc = ', tt_split[0])
    await callback.answer(tt_split[0], )
    await state.set_state(Form.state_two)
    async def translate(text: str) -> str:
        return await answer_by_lang_with_redis(text, callback.message.chat.id,
                                               user_service)
    rep_markup = await util.build_button_with_back("back",
                                                   [category.value for category in Category],
                                                   'cat2', translate,
                                                   tt_split[1])
    await callback.message.edit_text(tt_split[0],
                                     reply_markup=rep_markup.as_markup())


@router.callback_query(F.data == "language")
async def category_handler(callback: CallbackQuery, state: FSMContext):
    translated_texts = await answer_by_lang_with_redis('Select language , Back', callback.message.chat.id,
                                                       user_service)
    tt_split = translated_texts.split(",")
    await callback.answer(tt_split[0], )
    await state.set_state(Form.state_two)

    async def same(text: str) -> str:
        return text

    rep_markup = await util.build_button_with_back("back", [lang.value for lang in Language], 'lang2',
                                                   tr_func=same, back_text=tt_split[1])
    await callback.message.edit_text(tt_split[0], reply_markup=rep_markup.as_markup())


@router.callback_query(F.data.startswith("cat2_"))
async def categ(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    category = callback.data.split("_")[1].upper()
    await user_service.update_category(callback.message.chat.id, Category[category])
    translated_texts = await answer_by_lang_with_redis('Category updated', callback.message.chat.id, user_service)
    await callback.answer(translated_texts)
    await callback.message.answer(translated_texts)


@router.callback_query(F.data.startswith("lang2_"))
async def lang(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    langs = callback.data.split("_")[1].upper()
    await user_service.update_language(callback.message.chat.id, Language.from_initials(langs))
    translated_texts = await answer_by_lang_with_redis('Language updated', callback.message.chat.id, user_service)
    await callback.answer(translated_texts)
    await callback.message.answer(translated_texts)


@router.callback_query(F.data == "back")
async def back_handler(callback: CallbackQuery, state: FSMContext):
    current_state = await state.get_state()
    translated_texts = await answer_by_lang_with_redis('back', callback.message.chat.id, user_service)
    await callback.answer(translated_texts)
    if current_state == Form.state_two:
        await select(message=callback.message, state=state, answer=False)


async def select(message: Message, state: FSMContext, answer: bool = True):
    await state.set_state(Form.state_one)
    translated_texts = await answer_by_lang_with_redis('Select|Category|Language', message.chat.id, user_service)
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f"🎲 {translated_texts.split("|")[1]}", callback_data="category"),
         InlineKeyboardButton(text=f"🌐 {translated_texts.split("|")[2]}", callback_data="language")]
    ])
    await message.answer(text=f"{translated_texts.split("|")[0]}: ", reply_markup=markup) if answer \
        else await message.edit_text(f"{translated_texts.split("|")[0]}: ", reply_markup=markup)
