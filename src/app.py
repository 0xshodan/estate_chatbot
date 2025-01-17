import asyncio
from typing import Union

from aiogram import executor, types
from loader import DB_URL
from handlers import dp

# from filters import setup
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.dispatcher.handler import CancelHandler
from tortoise import Tortoise
from admin.models import BotAdmin
from aiohttp import ClientSession


class AlbumMiddleware(BaseMiddleware):
    """This middleware is for capturing media groups."""

    album_data: dict = {}

    def __init__(self, latency: Union[int, float] = 0.01):
        """
        You can provide custom latency to make sure
        albums are handled properly in highload.
        """
        self.latency = latency
        super().__init__()

    async def on_process_message(self, message: types.Message, data: dict):
        if not message.media_group_id:
            return

        try:
            self.album_data[message.media_group_id].append(message)
            raise CancelHandler()  # Tell aiogram to cancel handler for this group element
        except KeyError:
            self.album_data[message.media_group_id] = [message]
            await asyncio.sleep(self.latency)

            message.conf["is_last"] = True
            data["album"] = self.album_data[message.media_group_id]

    async def on_post_process_message(
        self, message: types.Message, result: dict, data: dict
    ):
        """Clean up after handling our album."""
        if message.media_group_id and message.conf.get("is_last"):
            del self.album_data[message.media_group_id]


async def on_start_up(dp):
    await Tortoise.init(db_url=DB_URL, modules={"models": ["admin.models"]})
    await Tortoise.generate_schemas()
    await dp.bot.set_my_commands(
        [
            types.BotCommand("start", "Запуск бота"),
            # types.BotCommand('help', 'Помощь'),
            # types.BotCommand('menu', 'Вывести меню')
        ]
    )


if __name__ == "__main__":
    dp.middleware.setup(AlbumMiddleware())
    print("Bot started")
    executor.start_polling(dp, on_startup=on_start_up)
