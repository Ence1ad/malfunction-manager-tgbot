from aiogram import Dispatcher
from .admin_filter import AdminFilter


def setup(dp: Dispatcher):
    dp.filters_factory.bind(AdminFilter)

