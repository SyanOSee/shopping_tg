# Third-party
from aiogram.fsm.state import StatesGroup, State


class AdminStates(StatesGroup):
    get_user_name = State()
    get_password = State()