from typing import Callable

from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils.keyboard import InlineKeyboardBuilder


def build_buttons(values: list[str], prefix: str, t_func: Callable[[int], str],
                  separator: int = 2) -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    for i, value in enumerate(values):
        if i % separator == 0 and i != 0:
            builder.row()
        builder.button(text=t_func(i), callback_data=f"{prefix}_{value}")
    return builder


def build_button_for_reg(values: list[str], prefix: str,
                         separator: int = 2):
    return build_buttons(values, prefix, t_func=lambda i: values[i], separator=separator)


async def build_buttons_for_set(values: list[str], prefix: str, tr_func,
                          separator: int = 2) -> InlineKeyboardBuilder:
    tr_text = ''
    for t in values:
        tr_text += t + '|'
    translated_text = await tr_func(tr_text)
    translated_text = translated_text.split('|')
    return build_buttons(values, prefix, lambda i: translated_text[i], separator)


async def build_button_with_back(callback_data: str, values: list[str], prefix: str, tr_func,
                           back_text: str,
                           separator: int = 2) -> InlineKeyboardBuilder:
    builder = await build_buttons_for_set(values, prefix, tr_func, separator)
    builder.row()
    builder.button(text=back_text, callback_data=callback_data)
    return builder


async def exit_handler(message: Message, state: FSMContext, state_name: str) -> bool:
    if message.text.strip() == '/exit':
        await state.clear()
        await message.answer(f"Exit {state_name} state")
        return True
    return False
