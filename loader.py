from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage


bot = Bot(token='5620182480:AAFnakVfefiVQpS80YW8LUk4vDvcTcfxoTE')
dp = Dispatcher(bot, storage=MemoryStorage())
