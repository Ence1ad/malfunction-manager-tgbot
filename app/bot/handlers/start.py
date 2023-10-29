import os

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart
from ..db_commands import user_create, get_user
from ..keyboards.default import start
from ..loader import bot, dp


async def bot_start(message: types.Message, state: FSMContext):
    await state.finish()
    user_id = message.from_user.id
    name = message.from_user.full_name
    username = message.from_user.username
    private_chat = message.chat.id
    group_chat = int(os.getenv("CHAT_ID"))
    if private_chat == group_chat:
        await bot.delete_message(chat_id=group_chat,
                                 message_id=message.message_id)
    try:
        await get_user(user_id)
        await bot.send_message(chat_id=message.from_user.id,
                               text=f'Приветствую {message.from_user.full_name}!\n',
                               reply_markup=start)
    except:
        await user_create(user_id=user_id, name=name, username=username)
        await bot.send_message(chat_id=message.from_user.id,
                               text=f'Добро пожаловать {message.from_user.full_name}!\nЯ Ваш личный помощник!\n\n',
                               reply_markup=start)


def register_handler_start(dp: Dispatcher):
    """Регистрируем хендлеры"""
    dp.register_message_handler(bot_start, CommandStart(), state="*")

