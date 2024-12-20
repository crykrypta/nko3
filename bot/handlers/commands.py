import logging

from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

from db.requests import create_new_user

from bot.lexicon import LEXICON
from bot.keyboards import is_member_keyboard

logger = logging.getLogger(__name__)

cmd_rt = Router()


# /start
@cmd_rt.message(CommandStart())
async def cmd_start(message: Message):
    if message.from_user is not None:
        await create_new_user(
            tg_id=message.from_user.id,
            username=message.from_user.full_name
        )
    else:
        logger.warning('Сообщение не содержит информацию о пользователе.')

    await message.answer(
        text=LEXICON['commands']['start']
    )


# /help
@cmd_rt.message(Command(commands=['help']))
async def cmd_help(message: Message):
    await message.answer(
        text=LEXICON['commands']['help']
    )
