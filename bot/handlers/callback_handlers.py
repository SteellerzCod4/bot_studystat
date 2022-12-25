from datetime import timedelta, datetime
from aiogram import types
import bot.messages as mes
import database.operations as oper
from bot import dp, our_bot, states
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns


async def add_subsubject_start(callback: types.CallbackQuery):
    state, text = callback.data.split("_")
    if text == mes.CANCEL:
        await callback.answer()
        await our_bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.message_id,
                                        text=mes.CANCEL_CONFIRMED, reply_markup=None)
        return
    oper.set_user_state(callback.from_user.id, states.ADD_SUBSUBJECT)
    await callback.answer()
    await our_bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.message_id,
                                    text=mes.SUBJECT_CHOSEN.format(text), reply_markup=None)
    oper.create_add_info(callback.from_user.id, text, state)


async def add_stat_start(callback: types.CallbackQuery):
    state, text = callback.data.split("_")
    if text == mes.CANCEL:
        await callback.answer()
        await our_bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.message_id,
                                        text=mes.CANCEL_CONFIRMED, reply_markup=None)
        return
    oper.set_user_state(callback.from_user.id, states.ADD_STAT)
    await callback.answer()
    await our_bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.message_id,
                                    text=mes.STAT_CHOSEN, reply_markup=None)
    oper.create_add_info(callback.from_user.id, text, state)


async def view_data_start(callback: types.CallbackQuery):
    state, text = callback.data.split("_")
    if text == mes.CANCEL:
        await callback.answer()
        await our_bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.message_id,
                                        text=mes.CANCEL_CONFIRMED, reply_markup=None)
        return
    await callback.answer()
    await our_bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.message_id,
                                    text=mes.PERIOD_CHOSEN, reply_markup=None)
    periods = {"день": 1, "неделя": 7, "месяц": 30, "год": 365}
    current_date = datetime.now()
    td = timedelta(days=periods.get(text))
    start_date = current_date - td
    records = oper.get_records(callback.from_user.id, start_date, current_date)
    if len(records) == 0:
        await callback.message.answer(mes.EMPTY_PERIOD)
        return
    sns.set_theme()

    plt.title("Статистика за выбранный период")
    ax = sns.barplot(x='date', y='hours', hue='name', data=records)
    plt.xlabel("Даты")
    plt.ylabel("Часы учебы")
    ax.xaxis.set_minor_locator(mdates.MonthLocator())
    ax.get_figure().savefig("image1.png")
    await callback.message.answer_photo(photo=open("image1.png", "rb"))
    plt.clf()


async def delete_subject_start(callback: types.CallbackQuery):
    state, text = callback.data.split("_")
    if text == mes.CANCEL:
        await callback.answer()
        await our_bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.message_id,
                                        text=mes.CANCEL_CONFIRMED, reply_markup=None)
        return
    await callback.answer()
    await our_bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.message_id,
                                    text=mes.DELETE_COMPLETE, reply_markup=None)
    oper.delete_subject(callback.from_user.id, text)


@dp.callback_query_handler()
async def handle_callbacks(callback: types.CallbackQuery):
    state, text = callback.data.split("_")

    all_reactions = {states.ADD_SUBSUBJECT: add_subsubject_start,
                     states.ADD_STAT: add_stat_start,
                     states.VIEW_DATA: view_data_start,
                     states.DELETE_SUBJECT: delete_subject_start}

    await all_reactions[state](callback)
