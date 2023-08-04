from bot import bot, dp
from aiogram import types

from ..processing.buttons import product_list_buttons, choose_edit_type, set_categories, basket_editing
from .product import editing_product
from ..processing.scripts import basket_index_dispatcher

from db.processing import (
    get_product, delete_product, is_in_basket, count_basket,
    get_user_data, get_prod_ind, add_products_category, 
    delete_products_category, get_category, 
    add_to_basket, remove_from_basket, is_banned
    )
from storage.proccessing import get_product_picture_path, get_main_picture_name


@dp.callback_query_handler(lambda c: "viewer" in c.data and not is_banned(telegram_id=c.message.from_user.id))
async def viewer_callback_handler(callback_query: types.CallbackQuery):
    activity, category_id = callback_query.data.split('|')
    if get_prod_ind(category=category_id) == []:
        await bot.edit_message_caption(
            chat_id=callback_query.message.chat.id,
            message_id=callback_query.message.message_id,
            caption="Вибачте, але у нас ще не продаються товари такої категорії")
        return None
    current_index = get_prod_ind(category=category_id)[0]
    product = get_product(current_index)
    user = get_user_data(telegram_id=callback_query.from_user.id)
    text = f"{product.name}\n\n{product.description}\n\nРозмір: {product.size}\nЦіна: {product.price}\n\nКатегорії товару:\n\n"
    for category in product.categories:
        text += category.title + '\n'
    keyboard = product_list_buttons(int(current_index), category=int(category_id),
                                    admin_vision = True if user.role.title == "Admin" else False, 
                                    is_boughten=is_in_basket(user=user, product=product))
    await bot.edit_message_media(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        media=types.InputMedia(media=open(get_product_picture_path(product.product_picture_name), "rb"))
    )
    await bot.edit_message_caption(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        caption=text,
        reply_markup=keyboard
    )

@dp.callback_query_handler(lambda c: ("next" in c.data or "back" in c.data) and not is_banned(telegram_id=c.message.from_user.id))
async def product_callback_handler(callback_query: types.CallbackQuery):
    user = get_user_data(telegram_id=callback_query.from_user.id)
    admin_vision = True if user.role.title == "Admin" else False

    activity, current_product_id, is_category = callback_query.data.split('|')
    current_product_id = int(current_product_id)
    try:
        product = get_product(current_product_id)
    except:
        await bot.edit_message_caption(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        caption="Ця панель застаріла. Відкрийте іншу за допомоги кнопок нижче, або напишіть '/help'"
        )
        return None
    text = f"{product.name}\n\n{product.description}\n\nРозмір: {product.size}\nЦіна: {product.price}\n\nКатегорії товару:\n\n"
    for category in product.categories:
        text += category.title + '\n'
    keyboard = product_list_buttons(current_product_id, admin_vision=admin_vision, category=int(is_category), 
                                    is_boughten=is_in_basket(user=user, product=product))

    await bot.edit_message_media(
            chat_id=callback_query.message.chat.id,
            message_id=callback_query.message.message_id,
            media=types.InputMedia(media=open(get_product_picture_path(product.product_picture_name), "rb"))
    )
    await bot.edit_message_caption(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        caption=text,
        reply_markup=keyboard
    )


@dp.callback_query_handler(lambda c: "type" in c.data and not is_banned(telegram_id=c.message.from_user.id))
async def type_callback_handler(callback_query: types.CallbackQuery):
    activity, current_product_id, is_category = callback_query.data.split('|')
    current_product_id = int(current_product_id)
    keyboard = choose_edit_type(current_product_id, category=int(is_category))
    try:
        product = get_product(current_product_id)
    except:
        await bot.edit_message_caption(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        caption="Ця панель застаріла. Відкрийте іншу за допомоги кнопок нижче, або напишіть '/help'"
        )
        return None
    text = f"{product.name}\n\n{product.description}\n\nРозмір: {product.size}\nЦіна: {product.price}"

    await bot.edit_message_media(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        media=types.InputMedia(media=open(get_product_picture_path(product.product_picture_name), "rb"))
    )
    await bot.edit_message_caption(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        caption="Що ви саме хочете змінити в товарі з такою інформацією:\n\n" + text,
        reply_markup=keyboard
    )


@dp.callback_query_handler(lambda c: "category" in c.data and not is_banned(telegram_id=c.message.from_user.id))
async def category_callback_handler(callback_query: types.CallbackQuery):
    activity, current_product_id, is_category = callback_query.data.split('|')
    current_product_id = int(current_product_id)
    keyboard = set_categories(current_product_id, category_id=int(is_category))
    try:
        product = get_product(current_product_id)
    except:
        await bot.edit_message_caption(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        caption="Ця панель застаріла. Відкрийте іншу за допомоги кнопок нижче, або напишіть '/help'"
        )
        return None
    text = f"{product.name}\n\n{product.description}\n\nРозмір: {product.size}\nЦіна: {product.price}"
    await bot.edit_message_media(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        media=types.InputMedia(media=open(get_product_picture_path(product.product_picture_name), "rb"))
    )
    await bot.edit_message_caption(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        caption="Ви почали редагувати товар с такою інформацію:\n\n" + text,
        reply_markup=keyboard
    )


@dp.callback_query_handler(lambda c: "disable" in c.data and not is_banned(telegram_id=c.message.from_user.id))
async def disable_callback_handler(callback_query: types.CallbackQuery):
    activity, current_product_id, is_category, category_id = callback_query.data.split('|')
    current_product_id = int(current_product_id)
    try:
        product = get_product(current_product_id)
    except:
        await bot.edit_message_caption(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        caption="Ця панель застаріла. Відкрийте іншу за допомоги кнопок нижче, або напишіть '/help'"
        )
        return None
    delete_products_category(product, get_category(category_id))
    text = f"{product.name}\n\n{product.description}\n\nРозмір: {product.size}\nЦіна: {product.price}"
    if category_id == is_category:
        is_category = -1
    keyboard = set_categories(current_product_id, category_id=int(is_category))
    await bot.edit_message_media(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        media=types.InputMedia(media=open(get_product_picture_path(product.product_picture_name), "rb"))
    )
    await bot.edit_message_caption(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        caption="Ви почали редагувати товар с такою інформацію:\n\n" + text,
        reply_markup=keyboard
    )


@dp.callback_query_handler(lambda c: "enable" in c.data and not is_banned(telegram_id=c.message.from_user.id))
async def enable_callback_handler(callback_query: types.CallbackQuery):
    activity, current_product_id, is_category, category_id = callback_query.data.split('|')
    current_product_id = int(current_product_id)
    try:
        product = get_product(current_product_id)
    except:
        await bot.edit_message_caption(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        caption="Ця панель застаріла. Відкрийте іншу за допомоги кнопок нижче, або напишіть '/help'"
        )
        return None
    add_products_category(product, get_category(category_id))
    text = f"{product.name}\n\n{product.description}\n\nРозмір: {product.size}\nЦіна: {product.price}"
    keyboard = set_categories(current_product_id, category_id=int(is_category))
    await bot.edit_message_media(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        media=types.InputMedia(media=open(get_product_picture_path(product.product_picture_name), "rb"))
    )
    await bot.edit_message_caption(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        caption="Ви почали редагувати товар с такою інформацію:\n\n" + text,
        reply_markup=keyboard
    )


@dp.callback_query_handler(lambda c: "edit" in c.data and not is_banned(telegram_id=c.message.from_user.id))
async def edit_callback_handler(callback_query: types.CallbackQuery):
    activity, current_product_id, is_category = callback_query.data.split('|')
    current_product_id = int(current_product_id)
    try:
        product = get_product(current_product_id)
    except:
        await bot.edit_message_caption(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        caption="Ця панель застаріла. Відкрийте іншу за допомоги кнопок нижче, або напишіть '/help'"
        )
        return None
    text = f"{product.name}\n\n{product.description}\n\nРозмір: {product.size}\nЦіна: {product.price}"

    await bot.edit_message_media(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        media=types.InputMedia(media=open(get_product_picture_path(product.product_picture_name), "rb"))
    )
    await bot.edit_message_caption(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        caption="Ви почали редагувати товар с такою інформацію:\n\n" + text,
    )
    await editing_product(callback_query, current_product_id)


@dp.callback_query_handler(lambda c: "delete" in c.data and not is_banned(telegram_id=c.message.from_user.id))
async def delete_callback_handler(callback_query: types.CallbackQuery):
    activity, current_product_id, is_category = callback_query.data.split('|')
    current_product_id = int(current_product_id)
    keyboard = product_list_buttons(int(current_product_id), delete_vison=True, category=int(is_category))
    try:
        product = get_product(current_product_id)
    except:
        await bot.edit_message_caption(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        caption="Ця панель застаріла. Відкрийте іншу за допомоги кнопок нижче, або напишіть '/help'"
        )
        return None
    text = f"{product.name}\n\n{product.description}\n\nРозмір: {product.size}\nЦіна: {product.price}"
    text = "Продукт було видалено!!!\n\n Ось його інформація:\n\n" + text

    await bot.edit_message_media(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        media=types.InputMedia(media=open(get_product_picture_path(product.product_picture_name), "rb"))
    )
    await bot.edit_message_caption(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        caption=text,
        reply_markup=keyboard
    )

    delete_product(int(current_product_id))


@dp.callback_query_handler(lambda c: "add" in c.data and not is_banned(telegram_id=c.message.from_user.id))
async def add_to_basket_callback_handler(callback_query: types.CallbackQuery):
    user = get_user_data(telegram_id=callback_query.from_user.id)
    admin_vision = True if user.role.title == "Admin" else False

    activity, current_product_id, is_category = callback_query.data.split('|')
    current_product_id = int(current_product_id)
    try:
        product = get_product(current_product_id)
    except:
        await bot.edit_message_caption(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        caption="Ця панель застаріла. Відкрийте іншу за допомоги кнопок нижче, або напишіть '/help'"
        )
        return None
    add_to_basket(user=user, product=product)
    text = f"Ви тілько, що додали в кошик цей товар!\n\n{product.name}\n\n{product.description}\n\nРозмір: {product.size}\nЦіна: {product.price}\n\nКатегорії товару:\n\n"
    for category in product.categories:
        text += category.title + '\n'
    keyboard = product_list_buttons(current_product_id, admin_vision=admin_vision, category=int(is_category), 
                                    is_boughten=is_in_basket(user=user, product=product))

    await bot.edit_message_media(
            chat_id=callback_query.message.chat.id,
            message_id=callback_query.message.message_id,
            media=types.InputMedia(media=open(get_product_picture_path(product.product_picture_name), "rb"))
    )
    await bot.edit_message_caption(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        caption=text,
        reply_markup=keyboard
    )


@dp.callback_query_handler(lambda c: "cancel" in c.data and not is_banned(telegram_id=c.message.from_user.id))
async def remove_from_basket_callback_handler(callback_query: types.CallbackQuery):
    user = get_user_data(telegram_id=callback_query.from_user.id)
    admin_vision = True if user.role.title == "Admin" else False

    activity, current_product_id, is_category = callback_query.data.split('|')
    current_product_id = int(current_product_id)
    try:
        product = get_product(current_product_id)
        remove_from_basket(user=user, product=product)
    except:
        await bot.edit_message_caption(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        caption="Ця панель застаріла. Відкрийте іншу за допомоги кнопок нижче, або напишіть '/help'"
        )
        return None
    text = f"Ви тілько, що прибрали з кошик цей товар!\n\n{product.name}\n\n \
        {product.description}\n\nРозмір: {product.size}\nЦіна: {product.price}\n\nКатегорії товару:\n\n"
    for category in product.categories:
        text += category.title + '\n'
    keyboard = product_list_buttons(current_product_id, admin_vision=admin_vision, category=int(is_category), 
                                    is_boughten=is_in_basket(user=user, product=product))

    await bot.edit_message_media(
            chat_id=callback_query.message.chat.id,
            message_id=callback_query.message.message_id,
            media=types.InputMedia(media=open(get_product_picture_path(product.product_picture_name), "rb"))
    )
    await bot.edit_message_caption(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        caption=text,
        reply_markup=keyboard
    )


@dp.callback_query_handler(lambda c: ("basext" in c.data or "basack" in c.data) and not is_banned(telegram_id=c.message.from_user.id))
async def basket_move_callback_handler(callback_query: types.CallbackQuery):
    user = get_user_data(telegram_id=callback_query.from_user.id)

    activity, current_product_id = callback_query.data.split('|')
    current_product_id = int(current_product_id)
    try:
        product = get_product(current_product_id)
    except:
        await bot.edit_message_caption(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        caption="Ця панель застаріла. Відкрийте іншу за допомоги кнопок нижче, або напишіть '/help'"
        )
        return None
    
    if current_product_id == -1:
        await bot.edit_message_media(
            chat_id=callback_query.message.chat.id,
            message_id=callback_query.message.message_id,
            media=types.InputMedia(media=open(get_main_picture_name('basket'), 'rb'))
            )
        if count_basket(user) == 0:
            await bot.edit_message_caption(
                chat_id=callback_query.message.chat.id,
                message_id=callback_query.message.message_id,
                caption="Ваш кошик порожній.",
            )
            return None
        text = "У вашому кошику знаходятся такі товари:"
        _sum = 0
        for product in user.basket:
            text = text + "\n" + product.name
            _sum += product.price
        text = text + f"\n\nЗагальна сума всіх товарів: {_sum} гривень"
        await bot.edit_message_caption(
                chat_id=callback_query.message.chat.id,
                message_id=callback_query.message.message_id,
                caption=text,
                reply_markup=basket_editing(current_product_id, user=user, is_header=True)
            )
        return None

    text = f"{product.name}\n\n{product.description}\n\nРозмір: {product.size}\nЦіна: {product.price}\n\nКатегорії товару:\n\n"
    for category in product.categories:
        text += category.title + '\n'
    keyboard = basket_editing(current_product_id, user=user)

    await bot.edit_message_media(
            chat_id=callback_query.message.chat.id,
            message_id=callback_query.message.message_id,
            media=types.InputMedia(media=open(get_product_picture_path(product.product_picture_name), "rb"))
    )
    await bot.edit_message_caption(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        caption=text,
        reply_markup=keyboard
    )


@dp.callback_query_handler(lambda c: "bascel" in c.data and not is_banned(telegram_id=c.message.from_user.id))
async def remove_from_basket_callback_handler(callback_query: types.CallbackQuery):
    user = get_user_data(telegram_id=callback_query.from_user.id)

    activity, product_id = callback_query.data.split('|')
    product_id = int(product_id)
    try:
        current_product_id = basket_index_dispatcher(product_id, 'next', user=user)
        remove_from_basket(user=user, product=get_product(product_id))
        product = get_product(current_product_id)
    except:
        await bot.edit_message_caption(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        caption="Ця панель застаріла. Відкрийте іншу за допомоги кнопок нижче, або напишіть '/help'"
        )
        return None

    if current_product_id == -1:
        await bot.edit_message_media(
            chat_id=callback_query.message.chat.id,
            message_id=callback_query.message.message_id,
            media=types.InputMedia(media=open(get_main_picture_name('basket'), 'rb'))
            )
        if count_basket(user) == 0:
            await bot.edit_message_caption(
                chat_id=callback_query.message.chat.id,
                message_id=callback_query.message.message_id,
                caption="Ваш кошик порожній.",
            )
            return None
        text = "У вашому кошику знаходятся такі товари:"
        _sum = 0
        for product in user.basket:
            text = text + "\n" + product.name
            _sum += product.price
        text = text + f"\n\nЗагальна сума всіх товарів: {_sum} гривень"
        await bot.edit_message_caption(
                chat_id=callback_query.message.chat.id,
                message_id=callback_query.message.message_id,
                caption=text,
                reply_markup=basket_editing(current_product_id, user=user, is_header=True)
            )
        return None
    
    text = f"{product.name}\n\n{product.description}\n\nРозмір: {product.size}\nЦіна: {product.price}\n\nКатегорії товару:\n\n"
    for category in product.categories:
        text += category.title + '\n'
    keyboard = basket_editing(current_product_id, user=user)

    await bot.edit_message_media(
            chat_id=callback_query.message.chat.id,
            message_id=callback_query.message.message_id,
            media=types.InputMedia(media=open(get_product_picture_path(product.product_picture_name), "rb"))
    )
    await bot.edit_message_caption(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        caption=text,
        reply_markup=keyboard
    )
