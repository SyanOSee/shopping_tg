from aiogram import types
from aiogram.dispatcher import FSMContext

from init_loader import dp, logger, anti_spam
from states.example_state import ExampleStates

@dp.message_handler(commands=["command"])
@dp.throttled(anti_spam, rate=0)
async def command(message: types.Message):
    await logger.info("Command")

@dp.message_handler(commands=["state_command"])
@dp.throttled(anti_spam, rate=0)
async def state_command(message: types.Message, state: FSMContext, update_schedule=False):
    await logger.info("STATE COMMAND")
    await state.set_state(ExampleStates.example_state)
    await state.set_data(data={
        "data": "arg"
    })

@dp.message_handler(state=ExampleStates.example_state)
async def handle_state_command(message: types.Message, state: FSMContext):
    await logger.info("HANDLE STATE COMMAND")
    state_data = (await state.get_data())["arg"]
    await ExampleStates.next()
    await state.reset_data()