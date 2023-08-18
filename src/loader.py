from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import os
from dotenv import load_dotenv


load_dotenv(".env")

db_user = os.environ["DB_USER"]
db_password = os.environ["DB_PASSWORD"]
db_name = os.environ["DB_NAME"]
DB_URL = f"asyncpg://{db_user}:{db_password}@db:5432/{db_name}"
bot = Bot(token="5368131141:AAEOBnQsV6QVTZu1gWtzfwZ6YH6TNx1WE0M")
dp = Dispatcher(bot, storage=MemoryStorage())
