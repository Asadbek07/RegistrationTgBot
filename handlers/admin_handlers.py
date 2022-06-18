from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher import FSMContext

from loader import dp
from services.ProductService import ProductService
from states import AdminForm
from states.DeleteProductAdminForm import DeleteProductAdminForm


@dp.message_handler(commands="delete_product")
async def delete_product_in_progress(message: types.Message):
    await DeleteProductAdminForm.product.set()
    await message.answer("Demak, mahsulot o'chirmoqchisiz! Iltimos, o'chirmoqchi bo'lgan mahsulotingizning nomini kiriting!")

@dp.message_handler(state=DeleteProductAdminForm.product)
async def delete_product(message: types.Message, state: FSMContext):
    deleted_product = ProductService.delete_by_name(message.text)
    if delete_product is not None:
        await message.answer_photo(photo=deleted_product.image_id, caption=f"Siz quyidagi mahsulotni muvaffaqiyatli o'chirdingiz:\n{deleted_product.name} ({deleted_product.cost})")
        await state.finish()
        return 
    await message.answer(f"{message.text} nomli mahsulot topilmadi, iltimos qayta tekshirib yana bir bor urinib ko'ring!")

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

    await message.answer("Endi, mahsulotning rasmini yuboring!")

    await AdminForm.image_id.set()

@dp.message_handler(content_types=types.ContentTypes.PHOTO, state=AdminForm.image_id)
async def process_image(message: types.Message, state: FSMContext):
    image_id = message.photo[-1].file_id
    
    await state.update_data({
        "image_id" : image_id
    })

    data = await state.get_data()
    product_name = data.get("product")
    cost = data.get("cost")
    added_product = ProductService.add_product(product_name, cost, image_id)

    await message.answer_photo(photo=image_id, caption=f"Qo'shgan mahsulotingiz haqida ma'lumot: \n{added_product.name} ({added_product.cost})")

    await state.finish()