from aiogram import types
from bot import dp
import bot.messages as mes
import database.operations as oper
import bot.states as states
import bot.keyboards as kb


@dp.message_handler(commands=["start"])
async def start_(message: types.Message):
    user_id = message.from_user.id
    if oper.get_user_by_id(user_id):
        await message.answer(mes.WELCOME_HAS_ACC, reply_markup=kb.main_keyboard)
    else:
        oper.set_user_state(user_id, states.WAIT_FOR_ACTION)
        await message.answer(mes.WELCOME, reply_markup=kb.main_keyboard)


@dp.message_handler(commands=["help"])
async def help_(message: types.Message):
    await message.answer(mes.HELP)


@dp.message_handler(commands=["keyboard"])
async def help_(message: types.Message):
    await message.answer(mes.KEYBOARD_SENT, reply_markup=kb.main_keyboard)
