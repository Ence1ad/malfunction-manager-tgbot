from aiogram import types
from aiogram.dispatcher.filters import BoundFilter
from aiogram.types import chat


class AdminFilter(BoundFilter):

    async def check(self, message: types.Message):
        return message.chat.type == chat.ChatType.PRIVATE
