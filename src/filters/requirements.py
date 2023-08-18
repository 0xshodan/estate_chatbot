from datetime import datetime, time

from aiogram.dispatcher.filters import BoundFilter
from aiogram import types

from utils import is_chat_member
from admin.models import BotSettings


class CheckSubscribe(BoundFilter):
    async def check(self, message: types.Message, *args) -> bool:
        return not await is_chat_member(int(message.from_user.id))


class IsNightTime(BoundFilter):
    async def check(self, message: types.Message, *args) -> bool:
        settings = (await BotSettings.first()).night_mode
        start_time, end_time = settings.split("-")
        start_h = int(start_time.split(":")[0])
        end_h = int(end_time.split(":")[0])
        return not time(start_h) <= message.date.time() <= time(end_h)
