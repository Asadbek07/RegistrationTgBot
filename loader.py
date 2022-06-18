from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher

# API_TOKEN = "1710370980:AAGSHs-LlZaTi64cSnsKTE_Pgf-XZWubQtE" # test
API_TOKEN = "5354713153:AAF0THDIksTs6IUl7D7ctpL2YUFKRbuEQKE" # production
PHONE_NUM = r'^[\+][0-9]{3}[0-9]{3}[0-9]{6}$'
CHANNEL_ID = -1001576660374

bot = Bot(token=API_TOKEN)

storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
