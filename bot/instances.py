import logging
from settings import Settings
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage



logging.basicConfig(level=logging.INFO)

bot = Bot(token=Settings.API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
