from aiogram.dispatcher.filters.state import State, StatesGroup

class AdminForm(StatesGroup):
    product = State()
    cost = State()
    image_id = State()