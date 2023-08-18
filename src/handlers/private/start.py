from typing import List

from filters import SwearCheck, isPrivate
from loader import dp, bot
from aiogram import types
import keyboards

from utils import (
    generate_code,
    distribution_publications,
    is_admin_check,
    add_state,
    add_swear,
)
from aiogram.dispatcher import FSMContext
from states import PublicationState, EstateState, SwearState
from aiogram.dispatcher.filters import CommandStart

# from aiogram.dispatcher.filters import Media


@dp.message_handler(isPrivate(), CommandStart())
async def start(message: types.Message, state: FSMContext):
    # print(await state.get_data())
    # print(message.from_user.id)
    await message.answer(
        text=f"Привет, {message.from_user.first_name}",
        reply_markup=keyboards.create_menu(await is_admin_check(message.from_user.id)),
    )


@dp.message_handler(isPrivate(), text="Добавить слово исключение")
async def add_estate_handler(message: types.Message):
    await message.answer("Введите слово исключение")
    await EstateState.word.set()


@dp.message_handler(state=EstateState.word)
async def add_estate_to_file(message: types.Message, state: FSMContext):
    add_state(message.text)
    await message.answer("Слово исключение было успешно добавлено!")
    await state.finish()


@dp.message_handler(isPrivate(), text="Добавить матерное слово")
async def add_swear_handler(message: types.Message):
    await message.answer("Введите слово исключение")
    await SwearState.word.set()


@dp.message_handler(isPrivate(), state=SwearState.word)
async def add_swear_to_file(message: types.Message, state: FSMContext):
    add_swear(message.text)
    await message.answer("Слово исключение было успешно добавлено!")
    await state.finish()


@dp.message_handler(isPrivate(), text="Удалить группу")
async def delete_group(message: types.Message):
    code = generate_code()
    await message.answer(
        text=f"Для удаления группы, напишите код `{code}` в чате группы",
        parse_mode=types.ParseMode.MARKDOWN,
    )
    file = open("src/data/delete_codes.txt", "a")
    file.write(code + "\n")


@dp.message_handler(isPrivate(), text="Добавить группу")
async def add_group(message: types.Message):
    code = generate_code()
    await message.answer(
        text=f"Сначала добавьте бота в группу, затем напишите код `{code}` в чате группы",
        parse_mode=types.ParseMode.MARKDOWN,
    )
    file = open("src/data/codes.txt", "a")
    file.write(code + "\n")


@dp.message_handler(isPrivate(), text="Опубликовать объявление")
async def add_publication(message: types.Message):
    await message.answer("Перешлите объявление")
    await PublicationState.text.set()


# @dp.message_handler(content_types=types.ContentTypes.PHOTO)
# async def handle_photo(message: types.Message):
#     # Получаем список всех фотографий из альбома
#     photos = message.photo
#     # Отправляем каждую фотографию в альбоме в том же чате
#     for photo in photos:
#         await bot.forward_message(chat_id=message.chat.id, from_chat_id=message.chat.id, message_id=message.message_id)


# @dp.message_handler(content_types=types.ContentTypes.PHOTO, state=PublicationState.text)
# # @dp.message_handler(MediaGroupFilter, content_types=types.ContentType.ANY)
# async def check_publication(message: types.Message, state: FSMContext):
#     print(message.message_id)
#     messages = await bot.get_message()
#     # print(album)
#     # await message.reply_media_group()
#     await message.forward(message.from_user.id)
#     print(message.photo[0].file_unique_id)
#     keyboard = types.InlineKeyboardMarkup() \
#         .add(types.InlineKeyboardButton('Опубликовать во всех группах', callback_data=f'publish:{message.message_id}')) \
#         .add(types.InlineKeyboardButton('Отменить', callback_data=f'delete:{message.message_id}'))
#     await message.answer('Проверьте правильность объявления и нажмите кнопку "Опубликовать"',
#                          reply_markup=keyboard)
#
#     await state.finish()
#     await state.update_data(message_id=message.message_id)


@dp.message_handler(
    is_media_group=True,
    content_types=types.ContentType.ANY,
    state=PublicationState.text,
)
async def check_publication(
    message: types.Message, album: List[types.Message], state: FSMContext
):
    """This handler will receive a complete album of any type."""
    media_group = types.MediaGroup()
    for obj in album:
        if obj.photo:
            file_id = obj.photo[-1].file_id
        else:
            file_id = obj[obj.content_type].file_id

        try:
            # We can also add a caption to each file by specifying `"caption": "text"`
            media_group.attach(
                {
                    "media": file_id,
                    "type": obj.content_type,
                    "caption": f"{message.text}",
                }
            )
        except ValueError:
            return await message.answer(
                "This type of album is not supported by aiogram."
            )
    await message.answer_media_group(media_group)
    # print(message_group)
    message_id = await message.answer(message.caption)
    # print(message.caption)
    await state.finish()

    keyboard = (
        types.InlineKeyboardMarkup()
        .add(
            types.InlineKeyboardButton(
                "Опубликовать во всех группах",
                callback_data=f"publish:{message.message_id}",
            )
        )
        .add(
            types.InlineKeyboardButton(
                "Отменить", callback_data=f"delete:{message.message_id}"
            )
        )
    )
    await message.answer(
        'Проверьте правильность объявления и нажмите кнопку "Опубликовать"',
        reply_markup=keyboard,
    )

    await state.update_data(message_id=message_id.message_id, message_group=media_group)


@dp.message_handler(state=PublicationState.text)
async def check_publication_with_no_text(message: types.Message, state: FSMContext):
    message_id = await message.answer(message.text)
    # print(message.caption)
    await state.finish()

    keyboard = (
        types.InlineKeyboardMarkup()
        .add(
            types.InlineKeyboardButton(
                "Опубликовать во всех группах",
                callback_data=f"publish:{message.message_id}",
            )
        )
        .add(
            types.InlineKeyboardButton(
                "Отменить", callback_data=f"delete:{message.message_id}"
            )
        )
    )
    await message.answer(
        'Проверьте правильность объявления и нажмите кнопку "Опубликовать"',
        reply_markup=keyboard,
    )

    await state.update_data(message_id=message_id.message_id, message_group=None)


@dp.message_handler(content_types=types.ContentTypes.PHOTO, state=PublicationState.text)
# @dp.message_handler(MediaGroupFilter, content_types=types.ContentType.ANY)
async def check_publication(message: types.Message, state: FSMContext):
    # print(message.message_id)
    # print(album)
    # await message.reply_media_group()
    await message.forward(message.from_user.id)
    # print(message.photo[0].file_unique_id)
    keyboard = (
        types.InlineKeyboardMarkup()
        .add(
            types.InlineKeyboardButton(
                "Опубликовать во всех группах",
                callback_data=f"publish:{message.message_id}",
            )
        )
        .add(
            types.InlineKeyboardButton(
                "Отменить", callback_data=f"delete:{message.message_id}"
            )
        )
    )
    await message.answer(
        'Проверьте правильность объявления и нажмите кнопку "Опубликовать"',
        reply_markup=keyboard,
    )

    await state.finish()
    await state.update_data(message_id=message.message_id, message_group=None)


@dp.callback_query_handler(text_startswith="publish:")
async def publish_publication(callback_data: types.CallbackQuery, state: FSMContext):
    messages = await state.get_data()
    if await distribution_publications(
        callback_data.from_user.id, messages["message_id"], messages["message_group"]
    ):
        await callback_data.message.edit_text("Публикация успешно завершена")
        # await callback_data.message.delete_reply_markup()


@dp.callback_query_handler(text_startswith="delete:")
async def decline_publish_publication(callback_data: types.CallbackQuery):
    await callback_data.message.answer("Публикация отменена")
