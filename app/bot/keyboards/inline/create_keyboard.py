from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from ...db_commands import select_location, select_priority, select_equip_category, select_equipments

choice = CallbackData("data", "level", "location", "priority", "equip_category")
add_nc = CallbackData("name_for_nc", "location", "priority", "equip_category", "equipment_id")


# нулевые значения ставим для дефолтных значений
def make_callback_data(level, location="0", priority="", equip_category="0"):
    return choice.new(level=level, location=location, priority=priority,
                      equip_category=equip_category)


# функция чтобы показать категории
async def location_keys():
    CURRENT_LEVEL = 0
    markup = InlineKeyboardMarkup(row_width=2)

    # получаем из db_commands для взаимодействия с бд
    locations = await select_location()
    for location in locations:
        button_text = f"{location.location_title}"
        callback_data = make_callback_data(level=CURRENT_LEVEL + 1, location=location.pk)
        markup.insert(
            InlineKeyboardButton(text=button_text, callback_data=callback_data)
        )
    markup.row(
        InlineKeyboardButton(
            text="Отмена",
            callback_data="cancel"
        )
    )
    return markup


async def priority_keys(location):
    CURRENT_LEVEL = 1
    markup = InlineKeyboardMarkup(row_width=1)
    priority_groups = await select_priority(location)
    for group in priority_groups:
        button_text = f"{group.priority_group}"
        callback_data = make_callback_data(level=CURRENT_LEVEL + 1, location=location, priority=group.priority_group
                                           )
        markup.insert(
            InlineKeyboardButton(text=button_text, callback_data=callback_data)
        )

    # делаем кнопку назад для
    markup.row(
        InlineKeyboardButton(
            text="Назад",
            callback_data=make_callback_data(level=CURRENT_LEVEL - 1)
        )
    )
    return markup


async def equip_category_keys(location, priority):
    CURRENT_LEVEL = 2
    markup = InlineKeyboardMarkup(row_width=1)
    # получаем вагон используя функцию из базы данных
    equip_categories = await select_equip_category(location, priority)
    for category in equip_categories:
        button_text = f"{category.equipment_category}"
        callback_data = make_callback_data(level=CURRENT_LEVEL + 1, location=location, priority=priority,
                                           equip_category=category.equipment_category.pk)
        markup.insert(
            InlineKeyboardButton(text=button_text, callback_data=callback_data)
        )
    markup.row(
        InlineKeyboardButton(
            text="Назад",
            callback_data=make_callback_data(level=CURRENT_LEVEL - 1,
                                             location=location)
        )
    )
    return markup


async def equipment_keys(location, priority, equip_category):
    CURRENT_LEVEL = 3
    markup = InlineKeyboardMarkup(row_width=1)
    # получаем вагон используя функцию из базы данных
    equipments = await select_equipments(location, priority, equip_category)
    for e in equipments:
        button_text = f"{e.equipment_title}"
        callback_data = add_nc.new(location=location, priority=priority,
                                   equip_category=equip_category, equipment_id=e.pk)
        markup.insert(
            InlineKeyboardButton(text=button_text, callback_data=callback_data)
        )
    markup.row(
        InlineKeyboardButton(
            text="Назад",
            callback_data=make_callback_data(level=CURRENT_LEVEL - 1,
                                             location=location, priority=priority)
        )
    )
    return markup


async def save_message_keys():
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(
                text="сохранить",
                callback_data="save",
                row_width=1
            )],
            [InlineKeyboardButton(
                text="отмена",
                callback_data="cancel",
                row_width=1
            )],
        ]
    )
    return markup
