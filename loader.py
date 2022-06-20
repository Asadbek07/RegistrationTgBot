from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher

API_TOKEN = "API TOKEN" # production
PHONE_NUM = r'^[\+][0-9]{3}[0-9]{3}[0-9]{6}$'
CHANNEL_ID = 0 # channel id

bot = Bot(token=API_TOKEN)

storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
