from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from ...db_commands import get_my_nc

del_nc = CallbackData("delete_user_nc", "id_nc")


async def delete_nc_keyboard(user_id):
    markup = InlineKeyboardMarkup(row_width=4)
    my_list = await get_my_nc(user_id)
    if my_list:
        for i in my_list:
            button_text = f"{i.pk}"
            callback_data = del_nc.new(id_nc=i.pk)
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
        button_text = "У вас нет записей. Завершить"
        callback_data = "cancel"
        markup.insert(
            InlineKeyboardButton(text=button_text, callback_data=callback_data))
        return markup