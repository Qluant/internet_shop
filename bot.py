import logging
from aiogram import Bot, Dispatcher, executor, types
from settings import Settings
import asyncio
import sys
import uvloop
from main import DB_Worker

logging.basicConfig(level=logging.INFO)
bot = Bot(token=Settings.API_TOKEN)
dp = Dispatcher(bot)

# # Додавання запису
# with DB_Worker() as db:
#         db.insert('countries', {'title' : 'USA'})

@dp.callback_query_handler(lambda query: query.data == 'add_country')
async def add_country(call: types.CallbackQuery):
    with DB_Worker() as db:
        db.insert('countries', {'title' : 'USA'})
    await call.message.answer('Done')


@dp.message_handler(commands=["start", "help"])
async def send_welcome(message: types.Message):
    markup = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                types.InlineKeyboardButton("Add country", callback_data="add_country"),
            ],
        ],
    )
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await message.reply("Hi!\nI'm EchoBot!\nPowered by aiogram.", reply_markup=markup)


@dp.message_handler()
async def echo(message: types.Message):
    # old style:
    # await bot.send_message(message.chat.id, message.text)

    await message.answer(message.text)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
