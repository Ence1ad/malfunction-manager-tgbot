import os
import django
from aiogram.types import BotCommand
from self import self
from aiogram import asyncio

from bot.loader import dp, bot
import logging


logger = logging.getLogger(__name__)


# Регистрация команд, отображаемых в интерфейсе Telegram
async def set_commands():
    commands = [
        BotCommand(command="/register", description="Зарегистрировать несоответствие"),
        BotCommand(command="/list", description="Выгрузить список несоответствий"),
        BotCommand(command="/task", description="Назначенные задания"),
        # BotCommand(command="/cancel", description="Отменить текущее действие")
    ]
    await bot.set_my_commands(commands)


async def main():
    # Регистрация хeндлеров
    from bot.handlers import start, create_non_conformance, get_all_nc, get_media, tasks
    start.register_handler_start(dp)
    create_non_conformance.register_handler_write_nc(dp)
    get_media.register_handler_get_media(dp)
    get_all_nc.register_handler_get_all_nc(dp)
    tasks.register_handler_get_tasks(dp)

    from bot import filters
    filters.setup(dp)
    # Парсинг файла конфигурации
    #     config = load_config("config/bot.ini")

    # Установка команд бота
    await set_commands()

    from jobs.updater import Command
    Command.handle(self)

    # Запуск поллинга
    await dp.skip_updates()  # пропуск накопившихся апдейтов (необязательно)
    await dp.start_polling()


def setup_django():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'registrator.settings')
    os.environ.update({'DJANGO_ALLOW_ASYNC_UNSAFE': "true"})
    django.setup()


if __name__ == '__main__':
    # Настройка логирования в stdout
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    setup_django()
    asyncio.run(main())

