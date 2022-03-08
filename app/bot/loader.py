from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import os
from dotenv import load_dotenv
load_dotenv()


#Parse_mode необходим для html форматирования текста
# bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
bot = Bot(token=str(os.getenv("BOT_TOKEN")), parse_mode=types.ParseMode.HTML)
#указываем место хранения. можно использовать БД или ОЗУ
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
