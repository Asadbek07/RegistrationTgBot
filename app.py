import logging

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Regexp
from aiogram.utils import executor
from services.ProductService import ProductService
from states import Form, AdminForm

logging.basicConfig(level=logging.INFO)

API_TOKEN = '1710370980:AAGSHs-LlZaTi64cSnsKTE_Pgf-XZWubQtE'
PHONE_NUM = r'^[\+][0-9]{3}[0-9]{3}[0-9]{6}$'
CHANNEL_ID = -1001632256119

bot = Bot(token=API_TOKEN)

storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

##################
#  ADMIN HANDLERS
##################

@dp.message_handler(commands="add_product")
async def input_new_product(message: types.Message):
    await AdminForm.product.set()
    await message.answer(text="Yangi mahsulot qo'shishingiz uchun nomini kiriting!")

@dp.message_handler(state=AdminForm.product)
async def process_product_name(message: types.Message, state: FSMContext):
    await state.update_data({
        "product" : message.text
    })

    await message.answer("Endi, narxini kiriting!")

    await AdminForm.cost.set()

@dp.message_handler(state=AdminForm.cost)
async def process_cost(message: types.Message, state: FSMContext):
    await state.update_data({
        "cost" : message.text
    })

    data = await state.get_data()
    product_name = data.get("product")
    cost = data.get("cost")
    added_product = ProductService.add_product(product_name, cost)
    await message.answer(f"Qo'shgan mahsulotingiz haqida ma'lumot: \n{added_product.name} ({added_product.cost})")

    await state.finish()
    

##################
#  USER HANDLERS
##################

@dp.message_handler(state=Form.product)
async def process_product_name(message: types.Message, state: FSMContext):
    product_name = message.text
    if not ProductService.validate_product(product_name):
        await message.reply("Xush kelibsiz! Qaysi mahsulotni tanlashni istaysiz ?")
        return 
    
    await state.update_data({
        "product" : product_name
    })
    await Form.name.set()
    await message.answer("Ismingizni kiriting!", reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(state=Form.name)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data({
        "name" : message.text
    })
    await Form.phone_number.set()
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, selective=True, one_time_keyboard=True)
    markup.add(types.KeyboardButton(text="Telefon raqam yuborish", request_contact=True))
    await message.answer("Telefon raqamingizni kiriting!", reply_markup=markup)


@dp.message_handler(content_types=types.ContentType.CONTACT, state=Form.phone_number)
@dp.message_handler(Regexp(PHONE_NUM), state=Form.phone_number)
async def process_phone_number(message : types.Message, state: FSMContext):
    contact = message.contact
    
    if contact is not None:
        phone_number = contact.phone_number
    else:
        phone_number = message.text
    
    await state.update_data({
        "phone_number" : phone_number
    })

    data = await state.get_data()
    name = data.get("name")
    phone_number = data.get("phone_number")
    product = data.get("product")
    await bot.send_message(text=f"{name}| {phone_number}| {product}", chat_id=CHANNEL_ID)
    
    await state.finish()

    await message.answer("Siz bilan tez orada call center dan bog'lanishadi!")

@dp.message_handler()
async def start_handler(message: types.Message):
    await Form.product.set()
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, selective=True)
    products = ProductService.get_all_products()
    markup.add(*(types.KeyboardButton(text=f"{product.name} ({product.cost})") for product in products))
    await message.answer("Xush kelibsiz! Qaysi mahsulotni tanlashni istaysiz ?", reply_markup=markup)





if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)