from aiogram import Router, F
from aiogram.types import CallbackQuery

callback_rt = Router()


# "Являетесь ли вы членом НКО" - ДА
@callback_rt.callback_query(F.data == 'is_member_yes')
async def process_ismember_yes(callback: CallbackQuery):
    await callback.answer(text='Вы ответили ДА')


# "Являетесь ли вы членом НКО" - НЕТ
@callback_rt.callback_query(F.data == 'is_member_no')
async def process_ismember_no(callback: CallbackQuery):
    await callback.answer(text='Вы ответили НЕТ')
