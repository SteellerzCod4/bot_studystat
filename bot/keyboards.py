import bot.messages as mes
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

# --------------------- Buttons ---------------------
add_subject = KeyboardButton(mes.ADD_SUBJECT)
get_subject = KeyboardButton(mes.GET_SUBJECTS)
add_subsubject = KeyboardButton(mes.ADD_SUBSUBJECT)
add_stat = KeyboardButton(mes.ADD_STAT)
view_data = KeyboardButton(mes.VIEW_DATA)
set_timer = KeyboardButton(mes.SET_TIMER)
# ---------------------------------------------------

# -------------------- Keyboards --------------------
main_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
main_keyboard.add(get_subject, add_subject, add_subsubject, add_stat, view_data, set_timer)
# ---------------------------------------------------

# ----------------- Inline Keyboards ----------------
# ---------------------------------------------------