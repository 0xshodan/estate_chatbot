from dotenv import load_dotenv
import os

load_dotenv(".env")

ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
# 6246196730:AAHzlTnQz5RV4eadlQecNODLTM3Hh7KCnD0
ACCESS_TOKEN_2 = os.getenv("ACCESS_TOKEN2")

DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = "db"
DB_TABLE_NAME = "botadmin"
