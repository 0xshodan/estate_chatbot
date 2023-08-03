from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage


bot = Bot(token='5620182480:AAEQ8WnWXXODcwWbtECo37q5IA1SZ_JvSTI')
dp = Dispatcher(bot, storage=MemoryStorage())
