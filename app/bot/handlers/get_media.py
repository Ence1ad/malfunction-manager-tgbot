import os

from aiogram import types, Dispatcher
from aiogram.dispatcher import filters, FSMContext
from aiogram.dispatcher.filters import Command

from .states import Media
from ..configuration.config import admins
from ..db_commands import fetch_media
from ..filters import AdminFilter
from ..loader import bot, dp


async def show_media(message: types.Message):
    private_chat = message.chat.id
    group_chat = int(os.getenv("CHAT_ID"))
    if private_chat == group_chat:
        await bot.delete_message(chat_id=group_chat,
                                 message_id=message.message_id)
        await bot.send_message(chat_id=message.from_user.id,
                               text="Введите ID несоответствия")
        await Media.id.set()
    else:
        await bot.send_message(chat_id=message.from_user.id,
                               text="Введите ID несоответствия")
        await Media.id.set()


async def enter_media_id(message: types.Message, state: FSMContext):
    try:
        nc_id = int(message.text)
        media_id = await fetch_media(nc_id)
        if media_id is not None:
            text = f"<b>Дата:</b> {media_id.created_at.strftime('%Y-%m-%d %H:%M:%S')}" \
                   f"\n<b>Оборудование:</b> {media_id.equipment}" \
                   f"\n<b>Описание:</b> {media_id.nc_description}"
            if len(media_id.photo) > 80:
                await message.answer_photo(photo=media_id.photo, caption=text,)
                await state.reset_state()
            else:
                await message.answer_video(video=media_id.video, caption=text, duration=5)
                await state.reset_state()
        else:
            await message.reply(text="Введите номер несоответствия, например = 123"
                                "\n\nЧтобы выйти пиши 'отмена'")
    except ValueError:
        await message.reply(text="Вы ввели некорректное значение\nВведите число""\n\nЧтобы выйти пиши 'отмена'")


async def cancel(message: types.Message, state: FSMContext):
    await message.answer("<b>Вы отменили действие!</b>", parse_mode="HTML")
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.delete()


def register_handler_get_media(dp: Dispatcher):
    dp.register_message_handler(show_media, Command('media'), AdminFilter(), user_id=admins)
    dp.register_message_handler(cancel, filters.Text(equals="отмена", ignore_case=True), state="*")
    dp.register_message_handler(enter_media_id, state=Media.id)
