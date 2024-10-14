from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

from db.db import async_session
from db.enum.enums import Category, Language, get_all_categories, check_category_exists
from db.service import UserService
from util import util
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
    await callback.answer("Select category", )
    print('nnn')
    await state.set_state(Form.state_two)
    await callback.message.edit_text("Select category",
                                     reply_markup=util.build_button_with_back("back",
                                                                              [category.value for category in Category],
                                                                              'cat2').as_markup())


@router.callback_query(F.data == "language")
async def category_handler(callback: CallbackQuery, state: FSMContext):
    await callback.answer("Select language", )
    await state.set_state(Form.state_two)
    await callback.message.edit_text("Select language",
                                     reply_markup=util.build_button_with_back("back",
                                                                              [lang.value for lang in Language],
                                                                              'lang2').as_markup())


@router.callback_query(F.data.startswith("cat2_"))
async def categ(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    category = callback.data.split("_")[1].upper()
    categories = get_all_categories()
    print("Все категории:", categories)

    category_to_check = "BULLY"
    if check_category_exists(category):
        print(f"Категория '{category_to_check}' существует.")
    else:
        print(f"Категория '{category_to_check}' не существует.")
    await user_service.update_category(callback.message.chat.id, Category[category])
    await callback.answer("Category updated")
    await callback.message.answer("Category updated")


@router.callback_query(F.data.startswith("lang2_"))
async def lang(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    langs = callback.data.split("_")[1].upper()
    await user_service.update_language(callback.message.chat.id, Language.from_initials(langs))
    await callback.answer("Language updated")
    await callback.message.answer("Language updated")


@router.callback_query(F.data == "back")
async def back_handler(callback: CallbackQuery, state: FSMContext):
    current_state = await state.get_state()
    await callback.answer('back')
    print('current_state = ', current_state)
    if current_state == Form.state_two:
        await select(message=callback.message, state=state, answer=False)


async def select(message: Message, state: FSMContext, answer: bool = True):
    await state.set_state(Form.state_one)
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎲 Category", callback_data="category"),
         InlineKeyboardButton(text="🌐 Language", callback_data="language")]
    ])
    await message.answer(text="Select: ", reply_markup=markup) if answer \
        else await message.edit_text("Select: ", reply_markup=markup)
