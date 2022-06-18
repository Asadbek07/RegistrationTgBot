from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Regexp

from states import Form
from loader import CHANNEL_ID, PHONE_NUM, dp, bot
from services.ProductService import ProductService

@dp.message_handler(state=Form.product)
async def process_product_name(message: types.Message, state: FSMContext):
    product_name = message.text
    if not ProductService.validate_product(product_name):
        await message.reply("Xush kelibsiz! Qaysi mahsulotni tanlashni istaysiz ?")
        return 
    
    await state.update_data({
        "product" : product_name
    })
    product = ProductService.get_by_name(product_name)
    await Form.name.set()
    await message.answer_photo(photo=product.image_id, caption="Ismingizni kiriting!", reply_markup=types.ReplyKeyboardRemove())


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

    await message.answer("Buyurtma uchun rahmat, siz bilan tez orada call center dan bog'lanishadi!")

@dp.message_handler()
async def start_handler(message: types.Message):
    await Form.product.set()
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, selective=True)
    products = ProductService.get_all_products()
    markup.add(*(types.KeyboardButton(text=f"{product.name} ({product.cost})") for product in products))
    await message.answer("Xush kelibsiz! Qaysi mahsulotni tanlashni istaysiz ?", reply_markup=markup)
