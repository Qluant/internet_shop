import logging
from settings import Settings
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage



logging.basicConfig(level=logging.INFO)

bot = Bot(token=Settings.API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# async def main():
#     engine = create_async_engine(url=Settings.DATABASE, echo=True)
#     sessionmaker = async_sessionmaker(engine, expire_on_commit=False)

#     bot = Bot(token=Settings.API_TOKEN, parse_mode="HTML")
#     storage = MemoryStorage()
#     # Setup dispatcher and bind routers to it
#     dp = Dispatcher(bot=bot, storage=storage)
#     dp.update.middleware(BaseMiddleware(session_pool=sessionmaker))
#     # Automatically reply to all callbacks
#     dp.callback_query.middleware(CallbackAnswerMiddleware())

#     # Register handlers
#     dp.include_router(commands.router)
#     dp.include_router(callbacks.router)

#     # Set bot commands in UI
#     await set_ui_commands(bot)

#     # Run bot
#     await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


# if __name__ == "__main__":
#     asyncio.run(main())