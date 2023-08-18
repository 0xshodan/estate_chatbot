import asyncio

from filters import (
    IsGroup,
    GroupNotRegister,
    GroupReRegister,
    SwearCheck,
    CheckSubscribe,
    IsNightTime,
    EstateCheck,
    GroupDelete,
)
from loader import dp, bot
from aiogram import types
from aiogram.dispatcher import FSMContext
from admin.models import Group, BotAdmin, BotSettings
from utils import check_code, is_chat_member


# @dp.message_handler(GroupFilter())
# async def echo_group(message: types.Message, state: FSMContext):
#     print(await state.get_data())
#     print(await state.get_data())
#     print(dir(state))
#     await message.answer(message.text)


@dp.message_handler(IsGroup(), IsNightTime(), content_types=types.ContentTypes.ANY)
async def night_messages(message: types.Message):
    settings = (await BotSettings.first()).night_mode
    start_time, end_time = settings.split("-")
    try:
        basket = await BotSettings.first()
        await message.forward(basket.basket_channel)
        await message.delete()
    except Exception as ex:
        print(ex)
    system_message = await message.answer(
        f"Публиковать объявления можно только с {start_time} до {end_time}"
    )

    await asyncio.sleep(10)
    await system_message.delete()


@dp.message_handler(IsGroup(), SwearCheck(), content_types=types.ContentTypes.ANY)
async def swearing_check(message: types.Message):
    basket = await BotSettings.first()
    await message.forward(basket.basket_channel)
    await message.delete()


@dp.message_handler(IsGroup(), GroupNotRegister())
async def register(message: types.Message):
    if check_code(message.text):
        await Group.create(group_id=str(message.chat.id))
        admin_list = await BotAdmin.all()
        for admin in admin_list:
            await bot.send_message(
                chat_id=admin.telegram_id,
                text="Группа была успешно добавлена в список рассылки",
            )
        await message.delete()


@dp.message_handler(IsGroup(), GroupReRegister())
async def re_register(message: types.Message):
    print(f"re_register")
    admin_list = [i[:-1] for i in open("src/data/admins.txt", "r").readlines()]
    for admin in admin_list:
        await bot.send_message(
            chat_id=admin, text="Данная группа уже находится в списке рассылки"
        )
    await message.delete()


@dp.message_handler(IsGroup(), GroupDelete())
async def group_delete(message: types.Message):
    code_list = [i[:-1] for i in open("src/data/chats.txt", "r").readlines()]
    code_list.remove(str(message.chat.id))
    print(code_list)
    with open("src/data/chats.txt", "w") as f:
        f.writelines(code_list)

    admin_list = [i[:-1] for i in open("src/data/admins.txt", "r").readlines()]
    for admin in admin_list:
        await bot.send_message(
            chat_id=admin, text="Группа была удалена из списка рассылки"
        )
    await message.delete()
    # await message.chat.leave()


@dp.message_handler(IsGroup(), CheckSubscribe())
async def non_subscriber(message: types.Message):
    keyboard = types.InlineKeyboardMarkup().add(
        types.InlineKeyboardButton(
            "Инвестиции без границ", url="https://t.me/investbezgranic"
        )
    )
    system_message = await message.answer(
        text=f"{message.from_user.first_name} {message.from_user.last_name} для того, что бы "
        f"опубликовать объявление в группе Вам необходимо подписаться на наш канал 👇️",
        reply_markup=keyboard,
    )
    await message.delete()
    await asyncio.sleep(60)
    await system_message.delete()


# @dp.message_handler(IsGroup(), EstateCheck())
# async def for_all(message: types.Message):
#     keyboard = types.InlineKeyboardMarkup().add(
#         types.InlineKeyboardButton("МойДом", url="https://t.me/MoyDom_Rielty_bot")
#     )
#     system_message = await message.answer(
#         text=f"Вы можете разместить объявление по недвижимости только через публикацию объявления в "
#         f'нашем боте "МойДом"',
#         reply_markup=keyboard,
#     )
#     await message.forward(-1001573131520)
#     await message.delete()

#     await asyncio.sleep(60)
#     await system_message.delete()


# @dp.message_handler(IsGroup(), EstateCheck(), content_types=types.ContentTypes.ANY)
# async def for_all(message: types.Message):
#     keyboard = types.InlineKeyboardMarkup().add(
#         types.InlineKeyboardButton("МойДом", url="https://t.me/MoyDom_Rielty_bot")
#     )
#     system_message = await message.answer(
#         text=f"Вы можете разместить объявление по недвижимости только через публикацию объявления в "
#         f'нашем боте "МойДом"',
#         reply_markup=keyboard,
#     )
#     await message.forward(-1001573131520)
#     print(await message.delete())

#     await asyncio.sleep(60)
#     await system_message.delete()


# @dp.message_handler(content_types=types.ContentTypes.PHOTO)
# async def hi(message: types.Message):
#     print(message.caption)
