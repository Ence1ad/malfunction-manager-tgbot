import os
from asyncio import sleep
from typing import Union

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from ..loader import bot, dp
from ..db_commands import *
from ..keyboards.inline.create_keyboard import *
from .states import *


# @dp.message_handler(Command('create'))
async def show_choice(message: types.Message):
    private_chat = message.chat.id
    group_chat = int(os.getenv("CHAT_ID"))
    if private_chat == group_chat:
        await bot.delete_message(chat_id=group_chat,
                                 message_id=message.message_id)
    await list_location(message)


async def list_location(message: Union[types.Message, types.CallbackQuery], **kwargs):
    markup = await location_keys()
    # проверяем что за объект ведь можем получить два объекта
    if isinstance(message, types.Message):
        await bot.send_message(chat_id=message.from_user.id,
                               text="<b>Выберите локацию:</b>", reply_markup=markup)
    elif isinstance(message, types.CallbackQuery):
        call = message
        # тут меняем клавиатуру
        # await call.message.edit_reply_markup(markup)
        text = "<b>Выберите локацию:</b>"
        await call.message.edit_text(text=text, reply_markup=markup)


async def list_priority(callback: types.CallbackQuery, location, **kwargs):
    markup = await priority_keys(location)
    await callback.message.edit_reply_markup(markup)
    text = "<b>Выберите группу критичности:</b>"
    await callback.message.edit_text(text=text, reply_markup=markup)


async def list_equip_categories(callback: types.CallbackQuery, location, priority, **kwargs):
    markup = await equip_category_keys(location=location, priority=priority)
    text = "<b>Выберите категорию:</b>"
    await callback.message.edit_text(text=text, reply_markup=markup)


async def list_equipments(callback: types.CallbackQuery, location, priority, equip_category, **kwargs):
    markup = await equipment_keys(location=location, priority=priority, equip_category=equip_category)
    # await callback.message.edit_reply_markup(markup)
    text = "<b>Выберите оборудование:</b>"
    await callback.message.edit_text(text=text, reply_markup=markup)


# Функция обработчик нажатия на кнопки
# @dp.callback_query_handler(choice_cd.filter())
# словарь собран из парметров указанных в my_callback_data_list=CallbackData() (см. в new.key)
async def navigate(call: types.CallbackQuery, callback_data: dict,):
    current_level = callback_data.get("level")
    locations = callback_data.get("location")
    priorities = callback_data.get("priority")
    equip_categories = int(callback_data.get("equip_category"))
    levels = {
        "0": list_location,
        "1": list_priority,
        "2": list_equip_categories,
        "3": list_equipments,
    }
    current_level_function = levels[current_level]
    await current_level_function(call, location=locations, priority=priorities, equip_category=equip_categories)


# @dp.callback_query_handler(add_nc.filter())
async def enter_new_nc(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await call.message.edit_text(text="<b>Введите описание несоответствия</b>")
    async with state.proxy() as data:
        data["creator"] = call.from_user.id
        data["location_data"] = callback_data.get("location")
        data["priority_data"] = callback_data.get("priority")
        data["equip_category_data"] = callback_data.get("equip_category")
        data["equipment_id_data"] = callback_data.get("equipment_id")
    await call.answer("Используйте клавиатуру для ввода текста")
    await NonConformanceState.nc_state_descriptions.set()


# @dp.message_handler(state=NewNonconf.nonconf_descriptions)
async def enter_description(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["description"] = message.text
    await message.answer(text="<b>Добавьте ФОТО или ВИДЕО</b>", parse_mode="HTML")
    await NonConformanceState.photo.set()


# @dp.message_handler(state=NewNonconf.photo, content_types=types.ContentTypes.VIDEO | types.ContentTypes.PHOTO)
async def add_photo_video(message: types.Message, state: FSMContext):
    """Для добавления фото и видео необходимо прописать в хендлере content_types"""
    markup = await save_message_keys()
    try:
        async with state.proxy() as data:
            data["video"] = message.video.file_id
    except AttributeError:
        async with state.proxy() as data:
            data["photo"] = message.photo[-1].file_id
    await message.answer("<b>Подтвердите или  отмените запись</b>", parse_mode="HTML", reply_markup=markup)
    await NonConformanceState.confirm_action.set()


# @dp.callback_query_handler(text_contains="save", state=NewNonconf.confirm_action)
async def save_action(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    user = int(data.get("creator"))
    location = data.get("location_data")
    priority = data.get("priority_data")
    equipment_id = data.get("equipment_id_data")
    description = data.get("description")
    photo_id = data.get("photo")
    video_id = data.get("video")
    new_non_conformance = await create_non_conformance(user, location, priority, equipment_id, description, photo_id,
                                                       video_id)
    if video_id is not None:
        mess_id = await call.bot.send_video(chat_id=os.getenv("CHAT_ID"), video=video_id, duration=3,
                                            caption=f"<b>НОВОЕ НЕСООТВЕТСТВИЕ</b>\n"
                                            f" {'-'*58}\n"
                                            f"<b>Номер несоответствия:</b>  {new_non_conformance.pk}\n"
                                            f"<b>Зарегистрировал:</b> {new_non_conformance.creator}\n"
                                            f"<b>Оборудование:</b>\n{new_non_conformance.equipment}\n"
                                            f"<b>Расположение:</b>  {new_non_conformance.location}\n"
                                            f"<b>Описание:</b>\n{new_non_conformance.nc_description}"
                                            )
    else:
        mess_id = await call.bot.send_photo(chat_id=os.getenv("CHAT_ID"), photo=photo_id,
                                            caption=f"<b>НОВОЕ НЕСООТВЕТСТВИЕ</b>\n"
                                            f" {'-'*58}\n"
                                            f"<b>Номер несоответствия:</b> {new_non_conformance.pk}\n"
                                            f"<b>Зарегистрировал:</b> {new_non_conformance.creator}\n"
                                            f"<b>Оборудование:</b>\n{new_non_conformance.equipment}\n"
                                            f"<b>Расположение:</b> {new_non_conformance.location}\n"
                                            f"<b>Описание:</b>\n{new_non_conformance.nc_description}"
                                            )
    # mess_id = mess_id.message_id

    await call.answer(text="Вы успешно добавили запись", show_alert=True, cache_time=60)
    await call.message.edit_text(text=f"<b>Вы успешно создали запись: ID - {new_non_conformance.pk}</b>")
    await sleep(1)
    await state.finish()


# @dp.callback_query_handler(text="cancel")
async def cancel(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await call.answer("Вы отменили действие", show_alert=True)
    await call.message.delete()


def register_handler_write_nc(dp: Dispatcher):
    """Регистрируем хендлеры"""
    dp.register_message_handler(show_choice, Command("register"))
    dp.register_callback_query_handler(cancel, text="cancel", state="*")
    dp.register_callback_query_handler(navigate, choice.filter())
    dp.register_callback_query_handler(enter_new_nc, add_nc.filter())
    dp.register_message_handler(enter_description, state=NonConformanceState.nc_state_descriptions)
    dp.register_message_handler(add_photo_video, state=NonConformanceState.photo,
                                content_types=types.ContentTypes.VIDEO | types.ContentTypes.PHOTO)
    dp.register_callback_query_handler(save_action, text_contains="save", state=NonConformanceState.confirm_action)
