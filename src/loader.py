from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage


bot = Bot(token='5401384083:AAFxS9XWO37oHlIDJe9IfgX6OcltgL-onvM')
dp = Dispatcher(bot, storage=MemoryStorage())
