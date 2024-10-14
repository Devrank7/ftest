from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery, Message

from db.db import async_session
from db.enum.enums import Category, Language
from db.model.model import User
from db.service import UserService
from util import util

route = Router()
user_service = UserService(session=async_session)


class RegisterData(StatesGroup):
    name = State()
    category = State()
    lang = State()


@route.callback_query(F.data == "register")
async def handler(callback: CallbackQuery, state: FSMContext):
    await callback.answer(text='Type name')
    await state.set_state(RegisterData.name)
    await callback.message.answer("type your name or type 0 that use telegram name")


@route.message(RegisterData.name)
async def handler1(message: Message, state: FSMContext):
    await state.update_data(name=message.chat.first_name if message.text == "0" else message.text)
    await state.set_state(RegisterData.category)
    await message.answer("Select default category",
                         reply_markup=util.build_buttons([category.value for category in Category], 'cat1').as_markup())


@route.callback_query(F.data.startswith("cat1_"))
async def handle_category_selection(callback: CallbackQuery, state: FSMContext):
    category_name = callback.data.split("_")[1]
    await state.update_data(category=category_name.upper())
    await callback.answer(f"You selected category: {category_name}")
    await callback.message.answer("Category saved. You can now proceed with the next step.")
    await state.set_state(RegisterData.lang)
    await callback.message.answer("Select your language",
                                  reply_markup=util.build_buttons([lang.value for lang in Language], 'lang1').as_markup())


@route.callback_query(F.data.startswith("lang1_"))
async def handle_category_selection(callback: CallbackQuery, state: FSMContext):
    lang = callback.data.split("_")[1]
    await callback.answer(text='All settings is configured')
    await state.update_data(lang=Language.from_initials(lang))
    data = await state.get_data()
    await user_service.create(
        User(id=callback.message.chat.id, name=data["name"], category=data["category"], lang=data["lang"]))
    await state.clear()
    await callback.message.answer("All settings is configured now you can test our bot")
