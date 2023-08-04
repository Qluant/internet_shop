from aiogram.types import ReplyKeyboardMarkup, KeyboardButton,InlineKeyboardButton, InlineKeyboardMarkup
from .scripts import product_index_dispatcher, basket_index_dispatcher
from db.processing import get_product, get_categories, is_product_category_exist, User


def get_menu(admin_vision: bool = False, contact_status: bool = False, basket_emptiness: bool = False) -> InlineKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(row_width=2)
    category = KeyboardButton("Товари по категоріям")
    product = KeyboardButton("Всі товари")
    contact = KeyboardButton("Змінити номер телефону" if contact_status else "Додати номер телефону", request_contact=True)
    basket = KeyboardButton("Мій кошик")
    help = KeyboardButton("Інструкція до бота")
    if admin_vision:
        add = KeyboardButton("Додати продукт")
        categories = KeyboardButton("Редагувати категорії")
        add_category = KeyboardButton("Додати категорію")
        keyboard.row(add, categories, add_category)
    if basket_emptiness:
        keyboard.row(KeyboardButton("Замовити все, що в кошику"))
    keyboard.row(contact, basket)
    keyboard.add(category, product, help)
    return keyboard


def product_list_buttons(current_product_id: int, admin_vision: bool = False, delete_vison: bool = False, is_boughten: bool = False, category: int = None) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=2)
    back = InlineKeyboardButton('<--', callback_data=f'back|{product_index_dispatcher(current_product_id, "back", category=category)}|{category}')
    next = InlineKeyboardButton('-->', callback_data=f'next|{product_index_dispatcher(current_product_id, "next", category=category)}|{category}')
    if not delete_vison:
        if admin_vision:
            edit = InlineKeyboardButton('Редагувати', callback_data=f'type|{current_product_id}|{category}')
            delete = InlineKeyboardButton('Видалити', callback_data=f'delete|{current_product_id}|{category}')
            keyboard.row(edit, delete)
    keyboard.row(back, next)
    if not delete_vison:
        if is_boughten:
            keyboard.add(InlineKeyboardButton('Прибрати з кошику', callback_data=f'cancel|{current_product_id}|{category}'))
        else:
            keyboard.add(InlineKeyboardButton('Додати до кошику', callback_data=f'add|{current_product_id}|{category}'))
    return keyboard


def basket_editing(current_product_id: int, user: User, is_header=False):
    keyboard = InlineKeyboardMarkup(row_width=2)
    back = InlineKeyboardButton('<--', callback_data=f'basack|{basket_index_dispatcher(current_product_id, "back", user=user)}')
    next = InlineKeyboardButton('-->', callback_data=f'basext|{basket_index_dispatcher(current_product_id, "next", user=user)}')
    if is_header:
        keyboard.add(back, next)
        return keyboard
    cancel = InlineKeyboardButton('Прибрати з кошика', callback_data=f'bascel|{current_product_id}')
    keyboard.add(back, next, cancel)
    return keyboard


def state_buttons(button_text: str = "Скасувати форму") -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=1)
    stop = InlineKeyboardButton(button_text, callback_data='stop')
    keyboard.row(stop)
    return keyboard


def choose_edit_type(product_id: int, category: int = None) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=1)
    edit = InlineKeyboardButton('Редагувати інфо', callback_data=f'edit|{product_id}|{category}')
    categories = InlineKeyboardButton('Редагувати категорії', callback_data=f'category|{product_id}|{category}')
    back = InlineKeyboardButton('Назад до товарів', callback_data=f'next|{product_id}|{category}')
    keyboard.row(edit, categories)
    keyboard.row(back)
    return keyboard


def set_categories(product_id: int, category_id: int = -1) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=1)
    categories = get_categories()
    for category in categories:
        if is_product_category_exist(get_product(id=product_id), category):
            keyboard.add(InlineKeyboardButton(f'Видалити категорію "{category.title}"', callback_data=f'disable|{product_id}|{category_id}|{category.id}'))
        else:
            keyboard.add(InlineKeyboardButton(f'Додати категорію "{category.title}"', callback_data=f'enable|{product_id}|{category_id}|{category.id}'))
    back = InlineKeyboardButton("Назад", callback_data=f"type|{product_id}|{category_id}")
    keyboard.add(back)
    return keyboard


def category_choice(is_editing: bool = False) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=1)
    categories = get_categories()
    for category in categories:
        if not is_editing:
            keyboard.add(InlineKeyboardButton(f'Категорія "{category.title}"', callback_data=f'viewer|{category.id}'))
        else:
            keyboard.add(InlineKeyboardButton(f'Редагувати "{category.title}"', callback_data=f'cattyp|{category.id}'))
    return keyboard


def category_type(category_id: int) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=1)
    edit = InlineKeyboardButton('Редагувати категорію', callback_data=f"change|{category_id}")
    delete = InlineKeyboardButton('Видалити категорію', callback_data=f"catdel|{category_id}")
    keyboard.add(edit, delete)
    return keyboard
