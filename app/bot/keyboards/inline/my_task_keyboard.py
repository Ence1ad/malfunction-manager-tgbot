from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from ...db_commands import get_tasks, get_task_status

upd_status_nc = CallbackData("update_status_nc", "pk_nc", "task_pk")
status_task = CallbackData("status_task", "status_pk",)


async def choose_my_task_keyboard(user_id):
    markup = InlineKeyboardMarkup(row_width=2)
    my_tasks = await get_tasks(user_id)
    if my_tasks:
        for i in my_tasks:
            button_text = f"Задание №{i.pk}"
            callback_data = upd_status_nc.new(pk_nc=i.nc_id, task_pk=i.pk)
            markup.insert(
                InlineKeyboardButton(text=button_text, callback_data=callback_data))
        markup.row(
            InlineKeyboardButton(
                text="Отменить",
                callback_data="cancel"
            )
        )
        return markup
    else:
        button_text = "Для вас нет задач. Завершить"
        callback_data = "cancel"
        markup.insert(
            InlineKeyboardButton(text=button_text, callback_data=callback_data))
        return markup


async def choose_keys():
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(
                text="Добавить текст",
                callback_data="description",
                row_width=1
            )],
            # [InlineKeyboardButton(
            #     text="назад",
            #     callback_data="back",
            #     row_width=1
            # )],
            [InlineKeyboardButton(
                text="Отменить",
                callback_data="cancel",
                row_width=1
            )],
        ]
    )
    return markup


async def choose_keys_2():
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(
                text="Добавить фото/видео",
                callback_data="media",
                row_width=1
            )],
            [InlineKeyboardButton(
                text="Отправить только текст",
                callback_data="text",
                row_width=1
            )],
            [InlineKeyboardButton(
                text="Отменить",
                callback_data="cancel",
                row_width=1
            )],
        ]
    )
    return markup


async def status_keys():
    markup = InlineKeyboardMarkup(row_width=2)
    work_status = await get_task_status()
    for ws in work_status:
        button_text = f"{ws.status_title}"
        callback_data = status_task.new(status_pk=ws.pk)
        markup.insert(
            InlineKeyboardButton(text=button_text, callback_data=callback_data))
    markup.row(
        InlineKeyboardButton(
            text="Отменить",
            callback_data="cancel"
        )
    )
    return markup