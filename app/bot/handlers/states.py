from aiogram.dispatcher.filters.state import StatesGroup, State


class NonConformanceState(StatesGroup):
    user = State()
    train_number = State()
    location_name = State()
    wagons_name = State()
    nc_state_descriptions = State()
    photo = State()
    confirm_action = State()
    delete = State()
    save = State()


class Media(StatesGroup):
    id = State()


class TaskState(StatesGroup):
    show = State()
    choice = State()
    start_state = State()
    description = State()
    media = State()
    status = State()
