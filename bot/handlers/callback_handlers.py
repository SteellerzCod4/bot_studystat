from aiogram import types
import bot.messages as mes
import database.operations as oper
from bot import dp, our_bot, states


async def add_subsubject_start(callback: types.CallbackQuery):
    oper.set_user_state(callback.from_user.id, states.ADD_SUBSUBJECT)
    await callback.answer()
    state, text = callback.data.split("_")
    await our_bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.message_id,
                                    text=mes.SUBJECT_CHOSEN.format(text), reply_markup=None)


@dp.callback_query_handler()
async def handle_callbacks(callback: types.CallbackQuery):
    state, text = callback.data.split("_")

    all_reactions = {states.ADD_SUBSUBJECT: add_subsubject_start}

    await all_reactions[state](callback)
    # await callback.message.answer("test")
    await callback.answer("добавляем")
    # await our_bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.message_id,
    #                                 text="Предмет добавляется введите подраздел: ", reply_markup=None)
