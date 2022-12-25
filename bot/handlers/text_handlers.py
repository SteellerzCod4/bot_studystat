from aiogram import types
from bot import dp
import bot.messages as mes
import database.operations as oper
import bot.states as states
import bot.keyboards as kb
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from datetime import datetime, timedelta


# --------------------- Terminology -----------------------
# 1-Tier message processing when you on the main 'menu'
# 2-Tier message processing when you in the function that update your state to another one
# 3-Tier message processing is where functions that exactly do what you've chosen

# --------------------- handle text -----------------------
# text: Название предмета
async def add_subject_start(message, user_id):
    user = oper.set_user_state(user_id, states.ADD_SUBJECT)
    subjects = user.subjects
    if not subjects:
        await message.answer(mes.ADD_NEW_SUB + mes.HAVE_NOSUBJECTS)
    else:
        await message.answer(mes.ADD_NEW_SUB + mes.HAVE_SUBJECTS + ", ".join(map(str, subjects)))
    await message.answer(mes.CANCEL_ADD_NEW_SUBJECT)


async def add_subsubject_start(message, user_id):
    user = oper.get_user_by_id(user_id)
    subjects = user.subjects
    if not subjects:
        await message.answer(mes.ADD_SUBJECT_WARNING)
    else:
        keyboard_with_subjects = InlineKeyboardMarkup()
        for subject in subjects:
            keyboard_with_subjects.add(InlineKeyboardButton(text=str(subject),
                                                            callback_data=f"{states.ADD_SUBSUBJECT}_{str(subject)}"))
        keyboard_with_subjects.add(
            InlineKeyboardButton(text=mes.CANCEL,
                                 callback_data=f"{states.ADD_SUBSUBJECT}_{str(mes.CANCEL)}"))
        await message.answer(mes.SELECT_SUBSUBJECT, reply_markup=keyboard_with_subjects)


async def add_stat_start(message, user_id):
    user = oper.get_user_by_id(user_id)
    subjects = user.subjects
    if not subjects:
        await message.answer(mes.ADD_SUBJECT_WARNING)
        return
    keyboard_with_subjects = InlineKeyboardMarkup()
    has_subsubjects = False
    for subject in subjects:
        subsubjects = subject.subsubjects
        for subsubject in subsubjects:
            has_subsubjects = True
            keyboard_with_subjects.add(
                InlineKeyboardButton(text=f"{str(subject)}: {str(subsubject)}",
                                     callback_data=f"{states.ADD_STAT}_{str(subject)}:{str(subsubject)}"))
    keyboard_with_subjects.add(
        InlineKeyboardButton(text=mes.CANCEL,
                             callback_data=f"{states.ADD_STAT}_{str(mes.CANCEL)}"))
    if not has_subsubjects:
        await message.answer(mes.STAT_WARNING)
    else:
        await message.answer(mes.SELECT_SUBSUBJECT, reply_markup=keyboard_with_subjects)


async def view_data_start(message, user_id):
    keyboard_with_subjects = InlineKeyboardMarkup()
    for period in ['день', 'неделя', 'месяц', 'год']:
        keyboard_with_subjects.add(InlineKeyboardButton(text=period,
                                                        callback_data=f"{states.VIEW_DATA}_{period}"))
    keyboard_with_subjects.add(
        InlineKeyboardButton(text=mes.CANCEL,
                             callback_data=f"{states.VIEW_DATA}_{str(mes.CANCEL)}"))
    await message.answer(mes.CHOOSE_PERIOD, reply_markup=keyboard_with_subjects)


async def delete_subject_start(message, user_id):
    user = oper.get_user_by_id(user_id)
    subjects = user.subjects
    if not subjects:
        await message.answer(mes.ADD_SUBJECT_WARNING)
    else:
        keyboard_with_subjects = InlineKeyboardMarkup()
        for subject in subjects:
            keyboard_with_subjects.add(InlineKeyboardButton(text=str(subject),
                                                            callback_data=f"{states.DELETE_SUBJECT}_{str(subject)}"))
        keyboard_with_subjects.add(
            InlineKeyboardButton(text=mes.CANCEL,
                                 callback_data=f"{states.DELETE_SUBJECT}_{str(mes.CANCEL)}"))
        await message.answer(mes.CHOSE_TO_DELETE, reply_markup=keyboard_with_subjects)

# --------------------- handle states ---------------------
# state: WAIT_FOR_ACTION
async def handle_wait_for_action(message, user_id, text):
    actions = {mes.ADD_SUBJECT: add_subject_start,
               mes.GET_SUBJECTS: get_subjects,
               mes.ADD_SUBSUBJECT: add_subsubject_start,
               mes.ADD_STAT: add_stat_start,
               mes.VIEW_DATA: view_data_start,
               mes.DELETE_SUBJECT: delete_subject_start
               }

    process_action = actions.get(text)
    if not process_action:
        await message.answer(mes.UNKNOWN_TEXT)
        return
    await process_action(message, user_id)


# state: ADD_SUBJECT
async def add_subject(message, user_id, text):
    if text.lower() == 'нет':
        oper.set_user_state(user_id, states.WAIT_FOR_ACTION)
        await message.answer(mes.CANCEL_CONFIRMED)
        return
    oper.add_new_subject(user_id, text)
    await message.answer(mes.SUBJECT_ADDED)
    oper.set_user_state(user_id, states.WAIT_FOR_ACTION)


async def get_subjects(message, user_id):
    all_subjects = oper.get_user_subjects(user_id)
    if not all_subjects:
        await message.answer(mes.HAVE_NOSUBJECTS)
    else:
        all_subjects_with_sub = []
        for subject in all_subjects:
            subsubjects = subject.subsubjects
            for subsubject in subsubjects:
                all_subjects_with_sub.append(f"{str(subject)}: {str(subsubject)}")
            if not subsubjects:
                all_subjects_with_sub.append(str(subject))
        await message.answer(mes.ALL_SUBJECTS + "\n".join(all_subjects_with_sub))


async def add_subsubject(message, user_id, text):
    add_info = oper.get_add_info(user_id)
    oper.add_subsubject(user_id, add_info.value, text)
    await message.answer(mes.SUBSUBJECT_ADDED.format(text, add_info.value))
    oper.delete_add_info(add_info)
    oper.set_user_state(user_id, states.WAIT_FOR_ACTION)


async def add_stat(message, user_id, text):
    if text.lower() == 'нет':
        oper.set_user_state(user_id, states.WAIT_FOR_ACTION)
        await message.answer(mes.CANCEL_CONFIRMED)
        return
    try:
        add_info = oper.get_add_info(user_id)
        hours, date, description = text.split('\n')
        time = datetime.strptime(hours, "%H:%M").time()
        date = datetime.strptime(date, "%d/%m/%Y")
        subject, subsubject = add_info.value.split(":")
        oper.add_stat(user_id, subject, subsubject, time, date, description)
        await message.answer(mes.STAT_ADDED)
        oper.delete_add_info(add_info)
        oper.set_user_state(user_id, states.WAIT_FOR_ACTION)
    except Exception:
        await message.answer(mes.PARSING_ERROR)






# --------------------- handle message ---------------------
@dp.message_handler()
async def handle_message(message: types.message):
    user_id = message.from_user.id
    text = message.text
    state = oper.get_user_state(user_id)

    handle_functions = {states.WAIT_FOR_ACTION: handle_wait_for_action,
                        states.ADD_SUBJECT: add_subject,
                        states.ADD_SUBSUBJECT: add_subsubject,
                        states.ADD_STAT: add_stat}

    function = handle_functions.get(state)
    if function:
        await function(message, user_id, text)
