from aiogram.dispatcher.filters import BoundFilter
from aiogram import types
from utils import chat_registration, check_code, check_swears, check_estate, check_delete_code


class IsGroup(BoundFilter):
    async def check(self, message, *args, **kwargs) -> bool:
        return message.chat.type in (
            types.ChatType.GROUP,
            types.ChatType.SUPERGROUP
        )


class GroupNotRegister(BoundFilter):
    async def check(self, message: types.Message, *args, **kwargs) -> bool:
        return not chat_registration(message.chat.id)


class GroupReRegister(BoundFilter):
    async def check(self, message: types.Message, *args, **kwargs) -> bool:
        return chat_registration(message.chat.id) and check_code(message.text)


class GroupDelete(BoundFilter):
    async def check(self, message: types.Message, *args, **kwargs) -> bool:
        return chat_registration(message.chat.id) and check_delete_code(message.text)


class SwearCheck(BoundFilter):
    async def check(self, message: types.Message):
        # print(check_swears(message.text))
        return check_swears(message.text)


class EstateCheck(BoundFilter):
    async def check(self, message: types.Message, *args) -> bool:
        return check_estate(message.text)


class isPrivate(BoundFilter):
    async def check(self, message, *args) -> bool:
        return message.chat.type in (
            types.ChatType.PRIVATE
        )