from bot import dp
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from db import Country, async_session
from sqlalchemy import select, insert, update, delete


class CountryForm(StatesGroup):
    title = State()  

@dp.message_handler(commands=["add_country"], state="*")
async def add_country(message: types.Message):
    await CountryForm.title.set()
    await message.reply(f"What country title to add for?\n")

@dp.message_handler(state=CountryForm.title)
async def insert_country(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['title'] = message.text
    await state.finish()
    sql = insert(Country).values(title=data['title'])
    try:
        async with async_session() as session:
            await session.execute(sql)
        await message.reply(f"{data['title']} was added to db")  
    except Exception as e:
        await message.reply(f"{data['title']} wasn't added. Error: {e}")  

    
