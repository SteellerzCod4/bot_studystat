from aiogram import types
from bot import dp
import bot.messages as mes
import database.operations as oper
import bot.states as states
import bot.keyboards as kb
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


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
        await message.answer(mes.ADD_SUBSUBJECT_WARNING)
    else:
        keyboard_with_subjects = InlineKeyboardMarkup()
        for subject in subjects:
            keyboard_with_subjects.add(InlineKeyboardButton(text=str(subject),
                                                            callback_data=f"{states.ADD_SUBSUBJECT}_{str(subject)}"))
        keyboard_with_subjects.add(
            InlineKeyboardButton(text=mes.CANCEL_SUBSUBJECT,
                                 callback_data=f"{states.ADD_SUBSUBJECT}_{str(mes.CANCEL_SUBSUBJECT)}"))
        await message.answer(mes.SELECT_SUBSUBJECT, reply_markup=keyboard_with_subjects)


# --------------------- handle states ---------------------
# state: WAIT_FOR_ACTION
async def handle_wait_for_action(message, user_id, text):
    actions = {mes.ADD_SUBJECT: add_subject_start,
               mes.GET_SUBJECTS: get_subjects,
               mes.ADD_SUBSUBJECT: add_subsubject_start,
               # mes.ADD_STAT: add_stat,
               # mes.VIEW_DATA: view_data,
               # mes.SET_TIMER: set_timer
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
        await message.answer(mes.ALL_SUBJECTS + "\n".join(map(str, all_subjects)))


# --------------------- handle message ---------------------
@dp.message_handler()
async def handle_message(message: types.message):
    user_id = message.from_user.id
    text = message.text
    state = oper.get_user_state(user_id)

    handle_functions = {states.WAIT_FOR_ACTION: handle_wait_for_action,
                        states.ADD_SUBJECT: add_subject}

    function = handle_functions.get(state)
    if function:
        await function(message, user_id, text)
