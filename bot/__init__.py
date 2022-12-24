from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from bot.config_data import ConfigData

our_bot = Bot(token=ConfigData.TOKEN)
dp = Dispatcher(our_bot)
