from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


# start_menu = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
#     [
#         KeyboardButton(text='Опубликовать объявление')
#     ],
#     [
#         KeyboardButton(text='Добавить группу'),
#         KeyboardButton(text='Удалить группу')
#     ]
# ])

def create_menu(is_admin=False):
    start_menu = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
        [
            KeyboardButton(text='Опубликовать объявление')
        ],
        [
            KeyboardButton(text='Добавить группу'),
            KeyboardButton(text='Удалить группу')
        ]
    ])
    if is_admin:
        return start_menu.add(
            KeyboardButton(text='Добавить слово исключение'),
            KeyboardButton(text='Добавить матерное слово')
        )
    return start_menu