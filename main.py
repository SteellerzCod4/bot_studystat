from database import Base, engine, get_db
from database.models import User
from bot.handlers.callback_handlers import *
from bot.handlers.commands_handlers import *
from bot import dp
from aiogram.utils import executor
from bot.handlers.text_handlers import *

if __name__ == "__main__":
    Base.metadata.create_all(engine)
    executor.start_polling(dp)
