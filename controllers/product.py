from bot import dp
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from db import Product
from sqlalchemy import select, insert, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

"""
name = Column(
    Unicode(225),
    unique=True,
    nullable=False,
)
size = Column(
    Float(2),
    nullable=False,
)
price = Column(
    Float(2),
    nullable=False,
)
name = Column(
    Unicode(225),
    unique=True,
    nullable=False,
)
"""
class ProductForm(StatesGroup): # TODO
    title = State()  

@dp.message_handler(commands=["add_product"], state="*")
async def add_product(message: types.Message):
    await ProductForm.title.set()
    await message.reply(f"What Product title to add for?\n") # TODO

@dp.message_handler(state=ProductForm.title)
async def insert_product(message: types.Message, state: FSMContext, session: AsyncSession):
    async with state.proxy() as data:
        data['title'] = message.text
    await state.finish()
    sql = insert(Product).values(tittle=data['title']) # TODO
    
    try:
        await session.execute(sql)
        await message.reply(f"{data['title']} was added to db")  
    except Exception as e:
        await session.rollback()
        await message.reply(f"{data['title']} wasn't added. Error: {e}")  
    # await message.reply(f"What Product title to add for?\n")
    
