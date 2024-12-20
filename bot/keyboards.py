from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot.lexicon import LEXICON  # type: ignore

is_member_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text=LEXICON['buttons']['yes'],
                                 callback_data='is_member_yes'),
            InlineKeyboardButton(text=LEXICON['buttons']['no'],
                                 callback_data='is_member_no')
        ]
    ]
)
