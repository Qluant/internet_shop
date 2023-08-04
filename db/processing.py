from . import session
from .models import User, Role, Product, Category
from random import choice


from storage.proccessing import delete_product_folder


def get_role(title: str) -> Role:
    return session.query(Role).filter_by(title=title).first()


def is_registered(id: int = None, telegram_id: int = None) -> bool:
    if id:
        return bool(session.query(User).filter_by(id=id).first())
    if telegram_id:
        return bool(session.query(User).filter_by(telegram_id=telegram_id).first())


def get_users() -> list[User]:
    return session.query(User).all()


def get_admins() -> list[User]:
    users = get_users()
    admins = []
    for user in users:
        if user.role.title == "Admin":
            admins.append(user)
    return admins


def get_products() -> list[Product]:
    return session.query(Product).all()


def get_categories() -> list[Category]:
    return session.query(Category).all()


def get_category_products(id: int = None, title: str = None) -> list[Product]:
    if id:
        return session.query(Category).filter_by(id=id).first().products
    if title:
        return session.query(Category).filter_by(title=title).first().products


def get_prod_ind(category: int = -1) -> list[int]:
    products = get_products() if category == -1 else get_category_products(category)
    return [product.id for product in products]


def add_user(user: any, platform="bot") -> bool:
    if platform == "web":
        new_user = User(moniker=user.get("username"), email=user.get("email"), password=user.get("password"))
    elif platform == "bot":
        if is_registered(telegram_id=user.id):
            return False
        new_user = User(telegram_id=user.id, nickname=user.username, last_name=user.last_name, first_name=user.first_name,
                        moniker=user.username or user.first_name or user.last_name)
    else:
        return False
    newbie = get_role("Newbie")
    newbie.users.append(new_user)
    try:
        session.commit()
        return True 
    except Exception as e:
        session.rollback()
        print(f"Error with adding user: {user}. Details:\n{e}")
        return False


def change_user_role(role_title: str, user_id: int = None, user: User = None) -> None:
    if not user:
        if not user_id:
            return None
        user = get_user_data(user_id)
    old_role = user.role
    new_role = get_role(role_title)
    old_role.users.remove(user)
    new_role.users.append(user)
    session.commit()


def is_banned(user_id: int = None, telegram_id: int = None) -> bool:
    if user_id:
        if not is_registered(user_id):
            return False
        user = get_user_data(user_id=user_id)
        return True if user.role.title == "Banned" else False
    if telegram_id:
        if not is_registered(telegram_id=telegram_id):
            return False
        user = get_user_data(telegram_id=telegram_id)
        return True if user.role.title == "Banned" else False


def ban_user(user_id: int = None, telegram_id: int = None) -> None:
    if user_id:
        if not is_registered(user_id):
            return None
        change_user_role("Banned", user_id=user_id)
    if telegram_id:
        if not is_registered(telegram_id=telegram_id):
            return None
        user = get_user_data(telegram_id=telegram_id)
        change_user_role("Banned", user=user)


def unban_user(user_id: int = None, telegram_id: int = None) -> None:
    if user_id:
        if not is_registered(user_id):
            return None
        change_user_role("Regular", user_id=user_id)
    if telegram_id:
        if not is_registered(telegram_id=telegram_id):
            return None
        user = get_user_data(telegram_id=telegram_id)
        change_user_role("Regular", user=user)


def get_user_data(user_id: int = None, telegram_id: int = None, username: str = None, email: str = None) -> User|None:
    if user_id:
        return session.query(User).filter_by(id=user_id).first()
    if telegram_id:
        return session.query(User).filter_by(telegram_id=telegram_id).first()
    if username:
        return session.query(User).filter_by(moniker=username).first()
    if email:
        return session.query(User).filter_by(email=email).first()


def add_phone_number(user: User, phone_number: str) -> None:
    if user is None or phone_number is None:
        return None
    user.phone_number = phone_number
    session.commit()


def product_existance(id: int = None, name: str = None) -> bool:
    if id:
        return bool(session.query(Product).filter_by(id=id).first())
    if name:
        return bool(session.query(Product).filter_by(name=name).first())
    return False


def get_product(id: int = None, name: str = None) -> Product|None:
    if id:
        return session.query(Product).filter_by(id=id).first()
    if name:
        return session.query(Product).filter_by(name=name).first()
    return None


def add_product(product: Product) -> str:
    session.add(product)
    try:
        session.commit()
        return "Товар було успішно додано!"
    except Exception as e:
        session.rollback()
        print(f"Error with adding product:\n{e}")
        return "Помилка((( Товар не додано..."


def picture_name_existance(product_picture_name: str) -> bool:
    return bool(session.query(Product).filter_by(product_picture_name=product_picture_name).first())


def create_picture_name() -> str:
    picture_name = ""
    while picture_name_existance(picture_name) or not picture_name:
        print(picture_name, not picture_name_existance(picture_name))
        picture_name = ""
        for _ in range(15):
            picture_name += choice("qwertyuiopasdfghjklzxcvbnm")
    return picture_name


def add_to_basket(user: User, product: Product) -> None:
    if user is None or product is None:
        return None
    user.basket.append(product)
    session.commit()


def is_in_basket(user: User, product: Product) -> bool:
    if user is None or product is None:
        return False
    return True if product in user.basket else False


def count_basket(user: User) -> int:
    if user is None:
        return -1
    return len(user.basket)


def remove_from_basket(user: User, product: Product) -> None:
    if user is None or product is None:
        return None
    user.basket.remove(product)
    session.commit()


def category_existance(id: str = None, title: str = None) -> bool:
    if id:
        return bool(session.query(Category).filter_by(id=id).first())
    if title:
        return bool(session.query(Category).filter_by(title=title).first())
    return False


def get_category(id: str = None, title: str = None) -> Category|None:
    if id:
        return session.query(Category).filter_by(id=id).first()
    if title:
        return session.query(Category).filter_by(title=title).first()


def add_category(title: str, description: str) -> str:
    if not category_existance(title=title):
        session.add(Category(title=title, description=description))
        session.commit()
        return "Категорію було успішно додано!"
    return "Товар не додано через помилку"


def delete_category(id: int = None, category: Category = None):
    if id:
        category = get_category(id)
    if category:
        session.delete(category)
        session.commit()


def is_product_category_exist(product: Product, category: Category) -> bool:
    if product in category.products:
        return True
    return False


def add_products_category(product: Product, category: Category) -> None:
    if not product or not category:
        return None
    category.products.append(product)
    session.commit()


def delete_products_category(product: Product, category: Category) -> None:
    if not product or not category:
        return None
    category.products.remove(product)
    session.commit()



def delete_product(id: int = None, product: Product = None) -> None:
    if id:
        product = get_product(id)
    delete_product_folder(product.product_picture_name)
    session.delete(product)
    session.commit()


def edit_category(id: int, title: str = '-', description: str = '-') -> None:
    category = get_category(id)
    if not category:
        return None
    if not title:
        title = '-'
    if not description:
        description = '-'
    if title == '-' and description == '-':
        return None
    if title != '-':
        category.title = title
    if description != '-':
        category.description = description
    session.commit()
