from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage


bot = Bot(token='5055994485:AAEE0rmZJimnhxplrfrPCkxSIBrD8c2b4Oc')
dp = Dispatcher(bot, storage=MemoryStorage())
