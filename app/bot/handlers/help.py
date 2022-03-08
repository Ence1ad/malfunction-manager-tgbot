import os

from aiogram import types, Dispatcher
from aiogram.dispatcher.filters.builtin import CommandHelp

from ..loader import dp, bot


# @dp.message_handler(CommandHelp())
async def bot_help(message: types.Message):
    private_chat = message.chat.id
    group_chat = int(os.getenv("CHAT_ID"))
    if private_chat == group_chat:
        await bot.delete_message(chat_id=group_chat, message_id=message.message_id)

    text = ("Список доступных команд:\n",
            "/start - Активирует диалог с ботом\n**************************************************",
            "/register - Для внесения записи, выберите поезд, уровень, вагон, "
            "внесите описание несоответствия, добавьте фото или видео, далее сохраните"
            )

    await message.answer("\n".join(text))


def register_handler_get_all_nc(dp: Dispatcher):
    dp.register_message_handler(bot_help, CommandHelp())
