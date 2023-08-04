from bot import bot, dp
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from PIL import Image

from db import Product, session
from db.processing import get_user_data, add_product, product_existance, get_product, create_picture_name
from ..processing.buttons import state_buttons

from storage.proccessing import save_product_picture, delete_first_picture

states_sessions = dict()

class ProductForm(StatesGroup): # TODO
    name = State()
    description= State()
    size = State()
    price = State()
    photos = State()


state_button_add_text = "Скасувати додавання товару"
state_button_edit_text = "Скасувати зміну товару"


async def editing_product(data: types.CallbackQuery, product_id: int) -> None:
    global states_sessions
    if states_sessions.get(data.from_user.id):
        await bot.send_message(chat_id=data.message.chat.id, text="Виникла помилка: ви ще редагуєте інший товар")
        return None
    states_sessions[data.from_user.id] = {"product_id": product_id, "is_edit": True}
    await ProductForm.name.set()
    await bot.send_message(chat_id=data.message.chat.id, text="Напишіть назву продукта", reply_markup=state_buttons(state_button_edit_text))

@dp.message_handler(lambda message: message.text in ["Додати продукт", "/add"], state="*")
async def entering_product(message: types.Message):
    user = get_user_data(telegram_id=message.from_id)
    if user.role.title != "Admin":
        await message.reply(f"У вас недостатньо прав для цієї команди\n")
        return None
    if states_sessions.get(message.from_user.id):
        await message.reply("Виникла помилка: ви ще редагуєте інший товар")
        return None
    states_sessions[message.from_user.id] = {"product_id": -1, "is_edit": False}
    await ProductForm.name.set()
    await message.reply(f"Напишіть назву продукта\n", reply_markup=state_buttons(state_button_add_text))

@dp.message_handler(lambda message: product_existance(name=message.text), state=ProductForm.name)
async def invalid_entering_name(message: types.Message, state: FSMContext):
    is_editing = states_sessions.get(message.from_user.id).get("is_edit")
    text = "Продукт з такою назвою вже існує!" \
    + ("\nНапишіть '-', якщо хочете залишити стару інформацію." if is_editing else "")
    await message.reply(text, reply_markup=state_buttons(state_button_edit_text if is_editing else state_button_add_text))

@dp.message_handler(lambda message: len(message.text)>255, state=ProductForm.name)
async def overloaded_entering_name(message: types.Message, state: FSMContext):
    is_editing = states_sessions.get(message.from_user.id).get("is_edit")
    text = "Занадто багато символів для назви продукта!" \
    + ("\nНапишіть '-', якщо хочете залишити стару інформацію." if is_editing else "")
    await message.reply(text, reply_markup=state_buttons(state_button_edit_text if is_editing else state_button_add_text))

@dp.message_handler(lambda message: message.text == '-' and not states_sessions.get(message.from_user.id).get("is_edit"), state=ProductForm.name)
async def invalid_text_name(message: types.Message, state: FSMContext):
    await message.reply("Повідомлення '-' доступно лише при редагуванні", reply_markup=state_buttons(state_button_add_text))

@dp.message_handler(lambda message: (not product_existance(name=message.text) and len(message.text)<=255) or (message.text == '-' and states_sessions.get(message.from_user.id).get("is_edit")), state=ProductForm.name)
async def entering_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["name"] = message.text
    await ProductForm.next()
    is_editing = states_sessions.get(message.from_user.id).get("is_edit")
    text = "Напишіть опис для цього продукта" \
    + ("\nНапишіть '-', якщо хочете залишити стару інформацію." if is_editing else "")
    await message.reply(text, reply_markup=state_buttons(state_button_edit_text if is_editing else state_button_add_text))

@dp.message_handler(lambda message: len(message.text)>1000, state=ProductForm.description)
async def overloaded_entering_description(message: types.Message, state: FSMContext):
    is_editing = states_sessions.get(message.from_user.id).get("is_edit")
    text = "Занадто багато символів для опису продукта!" \
    + ("\nНапишіть '-', якщо хочете залишити стару інформацію." if is_editing else "")
    await message.reply(text, reply_markup=state_buttons(state_button_edit_text if is_editing else state_button_add_text))

@dp.message_handler(lambda message: message.text == '-' and not states_sessions.get(message.from_user.id).get("is_edit"), state=ProductForm.description)
async def invalid_text_description(message: types.Message, state: FSMContext):
    await message.reply("Повідомлення '-' доступно лише при редагуванні", reply_markup=state_buttons(state_button_add_text))

@dp.message_handler(lambda message: len(message.text)<=1000 or (message.text == '-'and states_sessions.get(message.from_user.id).get("is_edit")), state=ProductForm.description)
async def entering_description(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["description"] = message.text
    await ProductForm.next()
    is_editing = states_sessions.get(message.from_user.id).get("is_edit")
    text = "Тепер її розмір, використовуйте одиниці вимірювання." \
    + ("\nНапишіть '-', якщо хочете залишити стару інформацію." if is_editing else "")
    await message.reply(text, reply_markup=state_buttons(state_button_edit_text if is_editing else state_button_add_text))

@dp.message_handler(lambda message: len(message.text)>50 , state=ProductForm.size)
async def overloaded_entering_size(message: types.Message, state: FSMContext):
    is_editing = states_sessions.get(message.from_user.id).get("is_edit")
    text = "Занадто багато тексту як для розміру" \
    + ("\nНапишіть '-', якщо хочете залишити стару інформацію." if is_editing else "")
    await message.reply(text, reply_markup=state_buttons(state_button_edit_text if is_editing else state_button_add_text))

@dp.message_handler(lambda message: message.text == '-' and not states_sessions.get(message.from_user.id).get("is_edit"), state=ProductForm.size)
async def invalid_text_size(message: types.Message, state: FSMContext):
    await message.reply("Повідомлення '-' доступно лише при редагуванні", reply_markup=state_buttons(state_button_add_text))

@dp.message_handler(lambda message: len(message.text)<=50 or (message.text == '-'and states_sessions.get(message.from_user.id).get("is_edit")), state=ProductForm.size)
async def entering_size(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["size"] = message.text
    await ProductForm.next()
    is_editing = states_sessions.get(message.from_user.id).get("is_edit")
    text = "Вкажіть ціну товару" \
    + ("\nНапишіть '-', якщо хочете залишити стару інформацію." if is_editing else "")
    await message.reply(text, reply_markup=state_buttons(state_button_edit_text if is_editing else state_button_add_text))

@dp.message_handler(lambda message: len(message.text) > 50, state=ProductForm.price)
async def entering_invalid_price(message: types.Message, state: FSMContext):
    is_editing = states_sessions.get(message.from_user.id).get("is_edit")
    text = "Занадто велике число!" \
    + ("\nНапишіть '-', якщо хочете залишити стару інформацію." if is_editing else "")
    await message.reply(text, reply_markup=state_buttons(state_button_edit_text if is_editing else state_button_add_text))

@dp.message_handler(lambda message: len(message.text)<=50 and not message.text.isdigit() and not message.text == '-', state=ProductForm.price)
async def entering_invalid_price(message: types.Message, state: FSMContext):
    is_editing = states_sessions.get(message.from_user.id).get("is_edit")
    text = "Ціна повина бути числом (в гривнях)! Спробуйте ще раз написати." \
    + ("\nНапишіть '-', якщо хочете залишити стару інформацію." if is_editing else "")
    await message.reply(text, reply_markup=state_buttons(state_button_edit_text if is_editing else state_button_add_text))

@dp.message_handler(lambda message: message.text == '-' and not states_sessions.get(message.from_user.id).get("is_edit"), state=ProductForm.price)
async def invalid_text_price(message: types.Message, state: FSMContext):
    await message.reply("Повідомлення '-' доступно лише при редагуванні", reply_markup=state_buttons(state_button_add_text))

@dp.message_handler(lambda message: (message.text.isdigit() and len(message.text)<=50) or (message.text == '-' and states_sessions.get(message.from_user.id).get("is_edit")),  state=ProductForm.price)
async def entering_price(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["price"] = message.text
    await ProductForm.next()
    is_editing = states_sessions.get(message.from_user.id).get("is_edit")
    text = "Надішліть фото товару" \
    + ("\nНапишіть '-', якщо хочете залишити старе фото." if is_editing else "")
    await message.reply(text, reply_markup=state_buttons(state_button_edit_text if is_editing else state_button_add_text))


@dp.message_handler(lambda message: not message.photo and not message.text == '-', state=ProductForm.photos)
async def entering_photos(message: types.Message, state: FSMContext):
    is_editing = states_sessions.get(message.from_user.id).get("is_edit")
    text = "Ви не надіслали фото в цьому повідомлені, тому я чекаю далі на фото." \
    + ("\nНапишіть '-', якщо хочете залишити старе фото." if is_editing else "")
    await message.reply(text, reply_markup=state_buttons(state_button_edit_text if is_editing else state_button_add_text))

@dp.message_handler(lambda message: message.text == '-' and not states_sessions.get(message.from_user.id).get("is_edit"), state=ProductForm.photos)
async def invalid_text_photo(message: types.Message, state: FSMContext):
    await message.reply("Повідомлення '-' доступно лише при редагуванні", reply_markup=state_buttons(state_button_add_text))

@dp.message_handler(lambda message: message.photo or (message.text == '-' and states_sessions.get(message.from_user.id).get("is_edit")), content_types=[types.ContentType.TEXT, types.ContentType.PHOTO], state=ProductForm.photos)
async def entering_photos(message: types.Message, state: FSMContext):
    if message.photo:
        photo = message.photo[-1]
        file_obj = await bot.get_file(photo.file_id)
        file_data = await bot.download_file(file_obj.file_path)
        image = Image.open(file_data)
    async with state.proxy() as data:
        if states_sessions.get(message.from_user.id).get("is_edit"):
            product = get_product(id=states_sessions.get(message.from_user.id).get("product_id"))
            old_data = {'name': product.name, 'description': product.description, 'size': product.size, 'price': product.price}
            for stage in ['name', 'description', 'size', 'price']:
                if data[stage] == '-':
                    data[stage] = old_data.get(stage)
            product.name=data['name']
            product.description=data['description']
            product.size=data['size']
            product.price=data['price']
            if not message.text == '-':
                delete_first_picture(product.product_picture_name)
                save_product_picture(product.product_picture_name, picture=image)
            try:
                session.commit()
                await bot.send_message(chat_id=message.chat.id, text="Товар було успішно змінено!")
            except:
                session.rollback()
                await bot.send_message(chat_id=message.chat.id, text="Товар не було змінено через помилку")
        else:
            picture_name = create_picture_name()
            save_product_picture(picture_name, picture=image)
            product = Product(name=data['name'], description=data['description'], size=data['size'], price=data['price'], product_picture_name=picture_name)
            await message.reply(add_product(product))
    await state.finish()
    states_sessions.pop(message.from_user.id)


@dp.callback_query_handler(lambda c: "stop" in c.data, state=ProductForm.name)
async def state_callback_handler(callback_query: types.CallbackQuery, state: FSMContext):
    states_sessions.pop(callback_query.from_user.id)
    await state.reset_state(with_data=False)
    await bot.send_message(chat_id=callback_query.message.chat.id, text="Додавання товару було скасовано")


@dp.callback_query_handler(lambda c: "stop" in c.data, state=ProductForm.description)
async def state_callback_handler(callback_query: types.CallbackQuery, state: FSMContext):
    states_sessions.pop(callback_query.from_user.id)
    await state.reset_state(with_data=False)
    await bot.send_message(chat_id=callback_query.message.chat.id, text="Додавання товару було скасовано")


@dp.callback_query_handler(lambda c: "stop" in c.data, state=ProductForm.size)
async def state_callback_handler(callback_query: types.CallbackQuery, state: FSMContext):
    states_sessions.pop(callback_query.from_user.id)
    await state.reset_state(with_data=False)
    await bot.send_message(chat_id=callback_query.message.chat.id, text="Додавання товару було скасовано")


@dp.callback_query_handler(lambda c: "stop" in c.data, state=ProductForm.price)
async def state_callback_handler(callback_query: types.CallbackQuery, state: FSMContext):
    states_sessions.pop(callback_query.from_user.id)
    await state.reset_state(with_data=False)
    await bot.send_message(chat_id=callback_query.message.chat.id, text="Додавання товару було скасовано")


@dp.callback_query_handler(lambda c: "stop" in c.data, state=ProductForm.photos)
async def state_callback_handler(callback_query: types.CallbackQuery, state: FSMContext):
    states_sessions.pop(callback_query.from_user.id)
    await state.reset_state(with_data=False)
    await bot.send_message(chat_id=callback_query.message.chat.id, text="Додавання товару було скасовано")
