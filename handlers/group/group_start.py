from filters import IsGroup, GroupNotRegister, GroupReRegister, SwearCheck, CheckSubscribe, IsNightTime, EstateCheck, \
    GroupDelete
from loader import dp
from aiogram import types
from aiogram.dispatcher import FSMContext

from utils import check_code, is_chat_member


# @dp.message_handler(GroupFilter())
# async def echo_group(message: types.Message, state: FSMContext):
#     print(await state.get_data())
#     print(await state.get_data())
#     print(dir(state))
#     await message.answer(message.text)


@dp.message_handler(IsNightTime())
async def night_messages(message: types.Message):
    await message.answer('Публиковать объявления можно только с 7:00 до 22:00')
    admin_list = [i[:-1] for i in open('data/admins.txt', 'r').readlines()]
    for admin in admin_list:
        await message.forward(admin)
    await message.delete()


@dp.message_handler(SwearCheck())
async def swearing_check(message: types.Message):
    admin_list = [i[:-1] for i in open('data/admins.txt', 'r').readlines()]
    print(admin_list)
    for admin in admin_list:
        await message.forward(int(admin))
    await message.delete()


@dp.message_handler(IsGroup(), GroupNotRegister())
async def register(message: types.Message):
    if check_code(message.text):
        with open('data/chats.txt', 'a') as f:
            f.write(str(message.chat.id) + '\n')
    await message.answer('Группа была успешно добавлена в список рассылки')
    await message.delete()


@dp.message_handler(GroupReRegister())
async def re_register(message: types.Message):
    await message.answer(text='Данная группа уже находится в списке рассылки')
    await message.delete()


@dp.message_handler(GroupDelete())
async def group_delete(message: types.Message):
    code_list = [i[:-1] for i in open('data/chats.txt', 'r').readlines()]
    code_list.remove(str(message.chat.id))
    print(code_list)
    with open('data/chats.txt', 'w') as f:
        f.writelines(code_list)

    await message.answer('Группа была удалена из списка рассылки')
    await message.delete()
    # await message.chat.leave()


@dp.message_handler(IsGroup(), CheckSubscribe())
async def non_subscriber(message: types.Message):
    keyboard = types.InlineKeyboardMarkup().add(
        types.InlineKeyboardButton('Инвестиции без границ', url='https://t.me/investbezgranic'))
    await message.answer(text=f'{message.from_user.first_name} {message.from_user.last_name} для того, что бы '
                              f'опубликовать объявление в группе Вам необходимо подписаться на наш канал 👇️',
                         reply_markup=keyboard)
    await message.delete()


@dp.message_handler(IsGroup(), EstateCheck())
async def for_all(message: types.Message):
    keyboard = types.InlineKeyboardMarkup().add(
        types.InlineKeyboardButton("МойДом", url="https://t.me/MoyDom_Rielty_bot"))
    await message.answer(text=f'Вы можете разместить объявление по недвижимости только через публикацию объявления в '
                              f'нашем боте "МойДом"',
                         reply_markup=keyboard)
    admin_list = [i[:-1] for i in open('data/admins.txt', 'r').readlines()]
    for admin in admin_list:
        await message.forward(admin)
    await message.delete()
