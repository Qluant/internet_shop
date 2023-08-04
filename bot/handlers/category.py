from bot import bot, dp
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from db.processing import get_user_data, category_existance, get_category, add_category, edit_category, delete_category
from ..processing.buttons import state_buttons, category_choice, category_type

states_sessions = dict()

class CategoryForm(StatesGroup): # TODO
    title = State()
    description= State()


state_button_add_text = "Скасувати додавання категорії"
state_button_edit_text = "Скасувати зміну категорії"


@dp.message_handler(lambda message: message.text in ["Редагувати категорії", "/edit_category"])
async def edit_category_choose(message: types.Message):
    user = get_user_data(telegram_id=message.from_id)
    if user.role.title != "Admin":
        await message.reply(f"У вас недостатньо прав для цієї команди\n")
        return None
    await bot.send_message(message.chat.id, text="Всі категорії товарів:", reply_markup=category_choice(is_editing=True))


@dp.callback_query_handler(lambda c: "cattyp" in c.data)
async def type_category(callback_query: types.CallbackQuery) -> None:
    category_id = int(callback_query.data.split('|')[-1])
    category = get_category(id=category_id)
    text=f"Категорія, яку ви редагуєте:\n{category.title}\n\n{category.description}"
    await bot.edit_message_text(message_id=callback_query.message.message_id, chat_id=callback_query.message.chat.id, text=text, reply_markup=category_type(category_id))


@dp.callback_query_handler(lambda c: "catdel" in c.data)
async def del_category(callback_query: types.CallbackQuery) -> None:
    category_id = int(callback_query.data.split('|')[-1])
    category = get_category(id=category_id)
    text=f"Категорію з такою інформацією, було видалено:\n{category.title}\n\n{category.description}"
    delete_category(id=category_id)
    await bot.edit_message_text(message_id=callback_query.message.message_id, chat_id=callback_query.message.chat.id, text=text)


@dp.callback_query_handler(lambda c: "change" in c.data)
async def editing_category(callback_query: types.CallbackQuery) -> None:
    global states_sessions
    if states_sessions.get(callback_query.from_user.id):
        await bot.edit_message_text(message_id=callback_query.message.message_id, chat_id=callback_query.message.chat.id, text="Виникла помилка: ви ще редагуєте іншу категорії")
        return None
    category_id = int(callback_query.data.split('|')[-1])
    category = get_category(id=category_id)
    states_sessions[callback_query.from_user.id] = {"category_id": category_id, "is_edit": True}
    text=f"Категорію з такою інформацією, зараз ви редагуєте:\n{category.title}\n\n{category.description}"
    await bot.edit_message_text(message_id=callback_query.message.message_id, chat_id=callback_query.message.chat.id, text=text)
    await CategoryForm.title.set()
    await bot.send_message(chat_id=callback_query.message.chat.id, text="Напишіть назву категорії, або '-', якщо хочете залишити стару інформацію.", reply_markup=state_buttons(state_button_edit_text))


@dp.message_handler(lambda message: message.text in ["Додати категорію", "/add_category"])
async def entering_category(message: types.Message):
    user = get_user_data(telegram_id=message.from_id)
    if user.role.title != "Admin":
        await message.reply(f"У вас недостатньо прав для цієї команди\n")
        return None
    if states_sessions.get(message.from_user.id):
        await message.reply("Виникла помилка: ви ще редагуєте іншу категорію")
        return None
    states_sessions[message.from_user.id] = {"category_id": -1, "is_edit": False}
    await CategoryForm.title.set()
    await message.reply(f"Напишіть назву категорії\n", reply_markup=state_buttons(state_button_add_text))


@dp.message_handler(lambda message: category_existance(title=message.text), state=CategoryForm.title)
async def invalid_entering_title(message: types.Message, state: FSMContext):
    is_editing = states_sessions.get(message.from_user.id).get("is_edit")
    text = "Категорія з такою назвою вже існує!" \
    + ("\nНапишіть '-', якщо хочете залишити стару інформацію." if is_editing else "")
    await message.reply(text, reply_markup=state_buttons(state_button_edit_text if is_editing else state_button_add_text))


@dp.message_handler(lambda message: len(message.text)>255, state=CategoryForm.title)
async def overloaded_entering_title(message: types.Message, state: FSMContext):
    is_editing = states_sessions.get(message.from_user.id).get("is_edit")
    text = "Занадто багато символів для назви продукта!" \
    + ("\nНапишіть '-', якщо хочете залишити стару інформацію." if is_editing else "")
    await message.reply(text, reply_markup=state_buttons(state_button_edit_text if is_editing else state_button_add_text))


@dp.message_handler(lambda message: message.text == '-' and not states_sessions.get(message.from_user.id).get("is_edit"), state=CategoryForm.title)
async def invalid_text_title(message: types.Message, state: FSMContext):
    await message.reply("Повідомлення '-' доступно лише при редагуванні", reply_markup=state_buttons(state_button_add_text))


@dp.message_handler(lambda message: (not category_existance(title=message.text) and len(message.text)<=255) or (message.text == '-' and states_sessions.get(message.from_user.id).get("is_edit")), state=CategoryForm.title)
async def entering_title(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["title"] = message.text
    await CategoryForm.next()
    is_editing = states_sessions.get(message.from_user.id).get("is_edit")
    text = "Напишіть опис для цього продукта" \
    + ("\nНапишіть '-', якщо хочете залишити стару інформацію." if is_editing else "")
    await message.reply(text, reply_markup=state_buttons(state_button_edit_text if is_editing else state_button_add_text))


@dp.message_handler(lambda message: len(message.text)>1000, state=CategoryForm.description)
async def overloaded_entering_description(message: types.Message, state: FSMContext):
    is_editing = states_sessions.get(message.from_user.id).get("is_edit")
    text = "Занадто багато символів для опису продукта!" \
    + ("\nНапишіть '-', якщо хочете залишити стару інформацію." if is_editing else "")
    await message.reply(text, reply_markup=state_buttons(state_button_edit_text if is_editing else state_button_add_text))


@dp.message_handler(lambda message: message.text == '-' and not states_sessions.get(message.from_user.id).get("is_edit"), state=CategoryForm.description)
async def invalid_text_description(message: types.Message, state: FSMContext):
    await message.reply("Повідомлення '-' доступно лише при редагуванні", reply_markup=state_buttons(state_button_add_text))


@dp.message_handler(lambda message: len(message.text)<=1000 or (message.text == '-'and states_sessions.get(message.from_user.id).get("is_edit")), state=CategoryForm.description)
async def entering_description(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if states_sessions.get(message.from_user.id).get("is_edit"):
            edit_category(id=states_sessions.get(message.from_user.id).get("category_id"), title=data["title"], description=message.text)
            await message.reply("Категорію було змінено!")
        else:
            await message.reply(add_category(title=data["title"], description=message.text))
    states_sessions.pop(message.from_user.id)
    await state.reset_state(with_data=False)


@dp.callback_query_handler(lambda c: "stop" in c.data, state=CategoryForm.title)
async def state_callback_handler(callback_query: types.CallbackQuery, state: FSMContext):
    states_sessions.pop(callback_query.from_user.id)
    await state.reset_state(with_data=False)
    await bot.send_message(chat_id=callback_query.message.chat.id, text="Додавання товару було скасовано")


@dp.callback_query_handler(lambda c: "stop" in c.data, state=CategoryForm.description)
async def state_callback_handler(callback_query: types.CallbackQuery, state: FSMContext):
    states_sessions.pop(callback_query.from_user.id)
    await state.reset_state(with_data=False)
    await bot.send_message(chat_id=callback_query.message.chat.id, text="Додавання товару було скасовано")
