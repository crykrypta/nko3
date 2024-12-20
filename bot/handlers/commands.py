from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

from bot.lexicon import LEXICON

cmd_rt = Router()


# /start
@cmd_rt.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(
        text=LEXICON['commands']['start']
    )


# /help
@cmd_rt.message(Command(commands=['help']))
async def cmd_help(message: Message):
    await message.answer(
        text=LEXICON['commands']['help']
    )
