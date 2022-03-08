import os

from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from aiogram.utils.exceptions import MessageCantBeEdited
from bot.keyboards.default import start
from ..loader import dp


# @dp.message_handler(commands="cancel", state="*")
# @dp.message_handler(Text(equals="отмена", ignore_case=True), state="*")
async def cmd_cancel(message: types.Message, state: FSMContext):
    await state.finish()
    try:
        await message.edit_text(text="Вы отменили действие", reply_markup=start)
        await message.delete()
    except MessageCantBeEdited:
        await message.answer(text="Вы отменили действие", reply_markup=start)
        await message.delete()


def register_handlers_cancel(dp: Dispatcher):
    dp.register_message_handler(cmd_cancel, commands="cancel", state="*")
    dp.register_message_handler(cmd_cancel, Text(equals="отмена", ignore_case=True), state="*")
