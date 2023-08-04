from bot import bot, dp
from aiogram import types
from db.processing import get_product
from ..processing.buttons import product_list_buttons, get_menu, category_choice, basket_editing

from db.processing import add_user, get_user_data, get_prod_ind, get_admins, count_basket, is_banned
from storage.proccessing import get_product_picture_path, get_main_picture_name


@dp.message_handler(lambda message: message.text in ["Інструкція до бота", "/start", "/help"] and not is_banned(telegram_id=message.from_user.id))
async def help(message: types.Message):
    add_user(message.from_user)
    user = get_user_data(telegram_id=message.from_user.id)
    admin_vision = True if user.role.title == "Admin" else False
    await message.reply(f"Нижче, ви можете побачити команди для управління ботом!", 
                        reply_markup=get_menu(admin_vision=admin_vision, contact_status=bool(user.phone_number), basket_emptiness=(count_basket(user=user)>0)))


@dp.message_handler(lambda message: message.text in ["Товари по категоріям", "Категорії", "/category", "/categories"] and not is_banned(telegram_id=message.from_user.id))
async def category_choose(message: types.Message):
    await bot.send_photo(message.chat.id, photo=open(get_main_picture_name('icon'), 'rb'), caption="Всі категорії товарів:", reply_markup=category_choice())


@dp.message_handler(lambda message: message.text in ["Мій кошик", "Кошик", "/basket"] and not is_banned(telegram_id=message.from_user.id))
async def basket_viewer(message: types.Message):
    user = get_user_data(telegram_id=message.from_user.id)
    if count_basket(user) == 0:
        await bot.send_photo(message.chat.id, photo=open(get_main_picture_name('basket'), 'rb'), caption="Ваш кошик порожній.")
        return None
    text = "У вашому кошику знаходятся такі товари:"
    _sum = 0
    for product in user.basket:
        text = text + "\n" + product.name
        _sum += product.price
    text = text + f"\n\nЗагальна сума всіх товарів: {_sum} гривень"
    await bot.send_photo(message.chat.id, photo=open(get_main_picture_name('basket'), 'rb'), caption=text, reply_markup=basket_editing(-1, user=user, is_header=True))


@dp.message_handler(lambda message: message.text in ["Замовити все, що в кошику", "buy"] and not is_banned(telegram_id=message.from_user.id))
async def buy_all(message: types.CallbackQuery):
    user = get_user_data(telegram_id=message.from_user.id)
    if len(user.basket) == 0:
        await bot.send_message(message.chat.id, "Щоб замовити всі товари з кошику, ви повинні мати хоча б один товару в ньому")
        return None
    if user.phone_number is None:
        await bot.send_message(message.chat.id, "Щоб, адмін міг написати вам, щодо покупки товару. Вам потрібно додати до бота ваш справжній номер телефона.")
        return None
    text = f"Покупець '{user.moniker}' замовив ці товари:\n"
    for product in user.basket:
        text = text + "\n" + product.name
    for admin in get_admins():
        if admin.telegram_id is None:
            continue
        chat = await bot.get_chat(admin.telegram_id)
        await bot.send_message(chat_id=message.chat.id, text=text)

        await bot.send_contact(chat_id=chat.id,
                            phone_number=user.phone_number,
                            first_name='Покупець',
                            last_name=user.moniker)
    await message.reply("Ваш контакт було надіслано адміну! Згодом він напише вам, щодо покупки товару")


@dp.message_handler(lambda message: message.text in ["Всі товари", "Товари", "/product", "/products"] and not is_banned(telegram_id=message.from_user.id))
async def products_viewer(message: types.Message):
    if get_prod_ind() == []:
        await bot.send_message(message.chat.id, "Вибачте, але у нас ще не продаються товари")
        return None
    current_index = get_prod_ind()[0]
    product = get_product(current_index)
    user = get_user_data(telegram_id=message.from_user.id)
    text = f"{product.name}\n\n{product.description}\n\nРозмір: {product.size}\nЦіна: {product.price}\n\nКатегорії товару:\n\n"
    for category in product.categories:
        text += category.title + '\n'
    keyboard = product_list_buttons(int(current_index), admin_vision = True if user.role.title == "Admin" else False, category=-1)
    await bot.send_photo(message.chat.id, photo=open(get_product_picture_path(product.product_picture_name), 'rb'), caption=text, reply_markup=keyboard)
