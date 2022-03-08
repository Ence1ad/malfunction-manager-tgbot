import os
from typing import Union

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command

from .states import TaskState
from ..db_commands import get_nc_4_tasks, write_task_report, task_count, user_task_list, select_non_conformance, \
    get_equipment_area, get_task_status_title
from ..keyboards.inline.my_task_keyboard import choose_my_task_keyboard, upd_status_nc, choose_keys, choose_keys_2, \
    status_keys, status_task
from ..loader import dp, bot


# @dp.message_handler(Command('confirm'))
async def select_my_task(message: types.Message):
    private_chat = message.chat.id
    group_chat = int(os.getenv("CHAT_ID"))
    if private_chat == group_chat:
        await bot.delete_message(chat_id=group_chat,
                                 message_id=message.message_id)
    await choose_my_task(message)


async def choose_my_task(message: Union[types.Message, types.CallbackQuery]):
    user_id = message.from_user.id
    choose_markup = await choose_my_task_keyboard(user_id)
    if isinstance(message, types.Message):
        await bot.send_message(chat_id=message.from_user.id,
                               text="<b>Список назначенных заданий:</b>", reply_markup=choose_markup)
    elif isinstance(message, types.CallbackQuery):
        call = message
        # тут меняем клавиатуру
        await call.message.edit_text(text="<b>Список назначенных заданий:</b>", reply_markup=choose_markup)


# @dp.callback_query_handler(upd_nc.filter())
async def update_non_conf(call: types.CallbackQuery, state: FSMContext, callback_data: dict,):
    pk = callback_data.get("pk_nc")
    async with state.proxy() as data:
        data["task_pk"] = callback_data.get("task_pk")
        data["nc_id"] = callback_data.get("pk_nc")
    task_pk = data.get("task_pk")
    new_non_conformance = await get_nc_4_tasks(pk)
    await task_count(pk)
    worker_name = await user_task_list(task_pk)
    equipment_area = await get_equipment_area(new_non_conformance.equipment)
    async with state.proxy() as data:
        data["workers"] = worker_name
        data["area"] = equipment_area
    await call.message.edit_text(text="<b>Ознакомьтесь с несоответствием</b>")
    if new_non_conformance.video is not None:
        await call.bot.send_video(chat_id=call.from_user.id,
                                  video=new_non_conformance.video,
                                  caption=f"<b>ID Несоответствия:</b> {new_non_conformance.pk}\n"
                                          f"<b>Оборудование:</b> {new_non_conformance.equipment}\n"
                                          f"<b>Расположение:</b>\n{new_non_conformance.location} - "
                                          f"{equipment_area}\n"
                                          f"<b>Описание несоответствия:</b>\n{new_non_conformance.nc_description}\n"
                                          f"<b>Исполнитель(и):</b>\n{worker_name}"
                                  )
    else:
        await call.bot.send_photo(chat_id=call.from_user.id,
                                  photo=new_non_conformance.photo,
                                  caption=f"<b>ID Несоответствия:</b> {new_non_conformance.pk}\n"
                                          f"<b>Оборудование:</b> {new_non_conformance.equipment}\n"
                                          f"<b>Расположение:</b>\n{new_non_conformance.location} - "
                                          f"{equipment_area}\n"
                                          f"<b>Описание несоответствия:</b>\n{new_non_conformance.nc_description}\n"
                                          f"<b>Исполнитель(и):</b>\n{worker_name}"
                                  )
    await TaskState.show.set()
    await show_choice(call.message)


async def show_choice(message: types.Message):
    choice_markup = await choose_keys()
    await message.answer(text="<b>Выберите действие</b>", reply_markup=choice_markup)
    await TaskState.choice.set()


async def input_description(call: types.CallbackQuery):
    await call.message.edit_text(text="<b>Напечатайте, что было сделано,\nкакие з/ч использовали:</b>")
    await TaskState.start_state.set()


async def show_choice_2(message: types.Message, state: FSMContext):
    users_text = message.text
    if len(users_text) < 20:
        await message.answer(text="<b>Вы ввели слишком короткое сообщение"
                                  "\nСообщение должно быть длиннее 20 символов</b>")
    elif len(users_text) >= 500:
        await message.answer(text="<b>Вы ввели слишком длинное сообщение"
                                  "\nСообщение должно быть короче 500 символов</b>")
    else:
        async with state.proxy() as data:
            data["description"] = users_text
        choice_markup = await choose_keys_2()
        await message.answer(text="<b>Выберите действие</b>", reply_markup=choice_markup)
        await TaskState.description.set()


async def add_just_text(call: types.CallbackQuery):
    status_markup = await status_keys()
    await call.message.edit_text("<b>Выберите новый статус задания</b>", reply_markup=status_markup)
    await TaskState.status.set()


async def input_media(call: types.CallbackQuery):
    await call.message.edit_text(text="<b>Нажмите на 📎 и добавьте фото или видео</b>")
    await TaskState.media.set()


async def add_photo_video(message: types.Message, state: FSMContext):
    """Для добавления фото и видео необходимо прописать в хендлере content_types"""
    status_markup = await status_keys()
    try:
        async with state.proxy() as data:
            data["video"] = message.video.file_id
    except AttributeError:
        async with state.proxy() as data:
            data["photo"] = message.photo[-1].file_id
    await message.answer("<b>Выберите новый статус задания</b>", reply_markup=status_markup)
    await TaskState.status.set()


async def write_report(call: types.CallbackQuery, state: FSMContext, callback_data: dict):
    async with state.proxy() as data:
        data["work_status"] = callback_data.get("status_pk")
    data = await state.get_data()
    task_pk = data.get("task_pk")
    nc_id = data.get("nc_id")
    work_status = data.get("work_status")
    work_status_title = await get_task_status_title(work_status)
    description = data.get("description")
    photo_id = data.get("photo")
    video_id = data.get("video")
    workers = data.get("workers")
    area = data.get("area")
    await write_task_report(task_pk=task_pk, nc_id=nc_id, description=description, work_status=work_status,
                            photo_id=photo_id, video_id=video_id)
    await call.message.edit_text(text="<b>Отчет успешно отправлен</b>")
    non_conformance = await select_non_conformance(nc_id)
    if photo_id is not None:
        await bot.send_photo(chat_id=int(os.getenv("CHAT_ID")),
                             photo=photo_id,
                             caption=f"<b>ОТЧЕТ О ВЫПОЛНЕНИИ ЗАДАНИЯ</b>\n"
                                     f" {'-'*58}\n"
                                     f"<b>Номер задания:</b> {task_pk}\n"
                                     f"<b>Оборудование:</b> {non_conformance.equipment}\n"
                                     f"<b>Описание несоответствия:</b>\n{non_conformance.nc_description}\n"
                                     f"<b>Расположение:</b>\n{non_conformance.location} - "
                                     f"{area}\n"
                                     f"<b>Исполнитель(и):</b>\n{workers}\n"
                                     f"<b>Что сделано:</b>\n{description}\n"
                                     f"<b>Результат задания:</b>\n{work_status_title}"

                             )
    elif video_id is not None:
        await bot.send_video(chat_id=int(os.getenv("CHAT_ID")),
                             video=video_id,
                             caption=f"<b>ОТЧЕТ О ВЫПОЛНЕНИИ ЗАДАНИЯ</b>\n"
                                     f" {'-'*58}\n"
                                     f"<b>Номер задания:</b> {task_pk}\n"
                                     f"<b>Оборудование:</b> {non_conformance.equipment}\n"
                                     f"<b>Описание несоответствия:</b>\n{non_conformance.nc_description}\n"
                                     f"<b>Расположение:</b>\n{non_conformance.location} - "
                                     f"{area}\n"
                                     f"<b>Исполнитель(и):</b>\n{workers}\n"
                                     f"<b>Что сделано:</b>\n{description}\n"
                                     f"<b>Результат задания:</b>\n{work_status_title}"

                             )
    else:
        await bot.send_message(chat_id=int(os.getenv("CHAT_ID")),
                               text=f"<b>ОТЧЕТ О ВЫПОЛНЕНИИ ЗАДАНИЯ</b>\n"
                                    f" {'-'*58}\n"
                                    f"<b>Номер задания:</b> {task_pk}\n"
                                    f"<b>Оборудование:</b> {non_conformance.equipment}\n"
                                    f"<b>Описание несоответствия:</b>\n{non_conformance.nc_description}\n"
                                    f"<b>Расположение:</b>\n{non_conformance.location} - "
                                    f"{area}\n"
                                    f"<b>Исполнитель(и):</b>\n{workers}\n"
                                    f"<b>Что сделано:</b>\n{description}\n"
                                    f"<b>Результат задания:</b>\n{work_status_title}"
                               )
    await state.finish()


def register_handler_get_tasks(dp: Dispatcher):
    dp.register_message_handler(select_my_task, Command('task'))
    dp.register_callback_query_handler(update_non_conf, upd_status_nc.filter())
    dp.register_message_handler(show_choice, state=TaskState.show)
    dp.register_callback_query_handler(input_description, text_contains="description", state=TaskState.choice)
    dp.register_message_handler(show_choice_2, state=TaskState.start_state)
    dp.register_callback_query_handler(add_just_text, text_contains="text", state=TaskState.description,)
    dp.register_callback_query_handler(input_media, text_contains="media", state=TaskState.description,)
    dp.register_message_handler(add_photo_video, state=TaskState.media,
                                content_types=types.ContentTypes.VIDEO | types.ContentTypes.PHOTO)
    dp.register_callback_query_handler(write_report, status_task.filter(), state=TaskState.status)
    # dp.register_callback_query_handler(back, text_contains="back", state="*")


# async def back(call: types.CallbackQuery, state: FSMContext):
#     await state.reset_state()
#     user_id = call.message.from_user.id
#     choose_markup = await choose_my_task_keyboard(user_id)
#     await call.message.edit_text(text="<b>Список назначенных задач:</b>", reply_markup=choose_markup)
