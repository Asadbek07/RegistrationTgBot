from aiogram.dispatcher.filters.state import State, StatesGroup

class Form(StatesGroup):
    product = State()
    name = State()
    phone_number = State()

