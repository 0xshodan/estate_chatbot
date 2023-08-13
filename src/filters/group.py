from aiogram.dispatcher.filters import BoundFilter
from aiogram import types
from utils import (
    chat_registration,
    check_code,
    check_swears,
    check_estate,
    check_delete_code,
    is_admin_check,
)
from admin.models import BotAdmin
from src.loader import bot


class IsGroup(BoundFilter):
    async def check(self, message, *args, **kwargs) -> bool:
        return message.chat.type in (types.ChatType.GROUP, types.ChatType.SUPERGROUP)


class GroupNotRegister(BoundFilter):
    async def check(self, message: types.Message, *args, **kwargs) -> bool:
        return (not chat_registration(message.chat.id)) and check_code(message.text)


class GroupReRegister(BoundFilter):
    async def check(self, message: types.Message, *args, **kwargs) -> bool:
        return chat_registration(message.chat.id) and check_code(message.text)


class GroupDelete(BoundFilter):
    async def check(self, message: types.Message, *args, **kwargs) -> bool:
        return chat_registration(message.chat.id) and check_delete_code(message.text)


class SwearCheck(BoundFilter):
    async def check(self, message: types.Message):
        member = await bot.get_chat_member(message.chat.id, message.from_user.id)
        if member.is_chat_admin():
            return False
        if message.text is None:
            return check_swears(message.caption)
        return check_swears(message.text)


class EstateCheck(BoundFilter):
    async def check(self, message: types.Message, *args) -> bool:
        if message.text:
            return check_estate(message.text)
        elif message.caption:
            return check_estate(message.caption)


class isPrivate(BoundFilter):
    async def check(self, message, *args) -> bool:
        return message.chat.type in (types.ChatType.PRIVATE) and await is_admin_check(
            message.chat.id
        )


async def is_admin(message: types.Message) -> bool:
    admins = await BotAdmin.all()
    for admin in admins:
        if int(admin.telegram_id) == message.from_user.id:
            return True
    return False
