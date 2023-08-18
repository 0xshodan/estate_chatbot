import random
import re
import time
from admin.models import BotAdmin, Group
from loader import bot


def generate_code():
    random.seed(int(time.time()))
    return f"{random.randint(0, 9999999):06d}"


async def chat_registration(id_chat) -> bool:
    id_list = [group.group_id for group in await Group.all()]
    return str(id_chat) in id_list


def check_code(code):
    code_list = [i[:-1] for i in open("src/data/codes.txt", "r").readlines()]
    # print(code_list)
    return code in code_list


def check_delete_code(code):
    code_list = [i[:-1] for i in open("src/data/delete_codes.txt", "r").readlines()]
    return code in code_list


def check_swears(text):
    profanity_list = [i[:-1] for i in open("src/data/swears.txt", "r").readlines()[:-1]]
    found_any = any(word in str(text) for word in profanity_list)
    return found_any


async def is_chat_member(member_id):
    chat_id = "-1001843717362"
    # chat_id = 'investbezgranic'
    try:
        chat_member = await bot.get_chat_member(chat_id, member_id)
        return chat_member.is_chat_member()
    except Exception:
        return True


async def distribution_publications(chat_id, message_id, message_group=None):
    group_list = await Group.all()

    if message_group:
        for group in group_list:
            await bot.send_media_group(chat_id=group.group_id, media=message_group)
            await bot.forward_message(
                chat_id=group.group_id, from_chat_id=chat_id, message_id=message_id
            )
    else:
        for group in group_list:
            await bot.forward_message(
                chat_id=group.group_id, from_chat_id=chat_id, message_id=message_id
            )
    return True


def check_estate(text):
    estate_list = [i[:-1] for i in open("src/data/estate.txt", "r").readlines()]
    found_any = any(word in str(text) for word in estate_list)
    return found_any


async def is_admin_check(user_id):
    admins_list = await get_admins()
    return user_id in admins_list


def add_state(word):
    with open("src/data/estate.txt", "a") as f:
        f.write(str(word) + "\n")


def add_swear(word):
    with open("src/data/swears.txt", "a") as f:
        f.write(str(word) + "\n")


async def get_admins() -> list[int]:
    admins = await BotAdmin.all()
    return [int(admin.telegram_id) for admin in admins]
