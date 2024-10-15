from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils.keyboard import InlineKeyboardBuilder


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
