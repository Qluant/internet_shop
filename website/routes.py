from website import app
from flask import render_template, redirect, request, session, url_for, flash

from db import Product
from db import session as db_session
from db.processing import (
    get_user_data, add_user, get_product,
    add_product, product_existance, get_prod_ind,
    get_category, get_categories, create_picture_name,
    is_in_basket, add_to_basket, remove_from_basket,
    delete_product, get_users, is_banned, change_user_role,
    ban_user, unban_user, add_category, delete_products_category,
    delete_category, add_products_category
    )

from storage.proccessing import (
    delete_first_picture, get_product_picture_path, save_product_picture
    )

from PIL import Image
from io import BytesIO

from .processing import product_index_dispatcher, group_product_index_dispatcher

from .forms import RegisterForm, LoginForm, AddForm, EditForm, CategoryAddForm, CategoryEditForm


ALLOWED_EXTENSIONS = ['jpg', 'jpeg']


@app.route('/')
@app.route('/index/')
@app.route('/products/')
def index():
    user = None if 'email' not in session else get_user_data(email=session["email"])
    products, back_posses, next_posses = group_product_index_dispatcher(0, 5)
    return render_template("product_list.html", user=user, products=products, get_product_picture_path=get_product_picture_path, is_products=True, next_posses=next_posses, back_posses=back_posses)


@app.route('/products/<string:product_range>')
def product_viewer(product_range):
    divided = product_range.split('-')
    if len(divided) != 2 or not divided[0].isdigit() or not divided[1].isdigit():
        return "Wrong product range in address"
    products, back_posses, next_posses = group_product_index_dispatcher(int(divided[0]), int(divided[1]))
    user = None if 'email' not in session else get_user_data(email=session["email"]) 
    return render_template("product_list.html", user=user, products=products, get_product_picture_path=get_product_picture_path, is_products=True, next_posses=next_posses, back_posses=back_posses)


@app.route('/category/', methods=["GET", "POST"])
def categories_list():
    categories = get_categories()
    user = None if 'email' not in session else get_user_data(email=session["email"]) 
    if request.method == "POST":
        action, category_id = request.form.get('action').split('|')
        if action == "edit":
            return redirect(url_for("edit_category", category_id=category_id))
        elif action == "delete":
            delete_category(id=category_id)
            return render_template("categories.html", user=user, categories=get_categories())
    return render_template("categories.html", user=user, categories=categories)


@app.route('/category/<int:category_id>/')
def category_products(category_id: int):
    category = get_category(id=category_id)
    user = None if 'email' not in session else get_user_data(email=session["email"]) 
    return render_template("product_list.html", user=user, products=category.products, get_product_picture_path=get_product_picture_path)


@app.route('/basket/', methods=["GET", "POST"])
def basket_products():
    if 'email' not in session:
        return redirect(url_for("login"))
    user = get_user_data(email=session["email"])
    if request.method == "POST":
        product_id = request.form.get('product_id')
        remove_from_basket(user, get_product(product_id))
    products = user.basket
    return render_template("product_list.html", user=user, products=products, get_product_picture_path=get_product_picture_path, is_basket=True)


@app.route('/product/<int:product_id>/', methods=["GET", "POST"])
def product_info(product_id):
    if not product_existance(id=product_id):
        return redirect(url_for('product_info', product_id=get_prod_ind()[0]))
    product = get_product(id=product_id)
    previous = product_index_dispatcher(index=product.id, activity="previous")
    next = product_index_dispatcher(index=product.id, activity="next")
    user = None if 'email' not in session else get_user_data(email=session["email"]) 
    if request.method == "POST":
        action = request.form.get('action')
        if action == "basket":
            if is_in_basket(user=user, product=product):
                remove_from_basket(user=user, product=product)
            else:
                add_to_basket(user=user, product=product)
        elif action == "edit":
            return redirect(url_for("edit_product", product_id=product_id))
        elif action == "delete":
            delete_product(id=product_id)
            return redirect(url_for('index'))

    return render_template("product.html", product=product, get_product_picture_path=get_product_picture_path,
                        previous=previous, next=next, user=user, is_in_basket=is_in_basket)


@app.route('/register/', methods=["GET", "POST"])
def register():
    if 'email' in session:
        return redirect(url_for('user_profile', user_id=get_user_data(email=session["email"]).id))
    form = RegisterForm()
    if form.validate_on_submit():
        session['email'] = request.form["email"]
        if add_user({"username": request.form["username"], "email": request.form["email"], "password": request.form["password"]}, "web"):
            return redirect(url_for('user_profile', user_id=get_user_data(email=session["email"]).id))
        return render_template('register.html', form=form)
    return render_template('register.html', form=form)


@app.route('/login/', methods=["GET", "POST"])
def login():
    if 'email' in session:
        return redirect(url_for('user_profile', user_id=get_user_data(email=session["email"]).id))
    form = LoginForm()
    if form.validate_on_submit():
        # Adding user without checking, because validators already check it.
        user = get_user_data(email=request.form["email"])
        session['email'] = request.form["email"]
        return redirect(url_for('user_profile', user_id=get_user_data(email=session["email"]).id))
    return render_template('login.html', form=form)


@app.route('/logout/')
def logout():
    if 'email' in session:
        session.clear()
    return redirect(url_for('index'))


@app.route('/users/', methods=["GET", "POST"])
def users_profiles():
    if 'email' in session:
        page_asker = get_user_data(email=session["email"])
    else:
        page_asker = None
    users = []
    for user in get_users():
        if user.telegram_id is None:
            users.append(user)
    if request.method == "POST":
        action, user_id = request.form.get('action').split('|')
        client = get_user_data(user_id=user_id)
        if action == "promote":
            if client.role.title == "Admin":
                change_user_role("Regular", user_id=user_id)
            else:
                change_user_role("Admin", user_id=user_id)
        elif action == "ban":
            if is_banned(user_id=user_id):
                unban_user(user_id=user_id)
            else:
                ban_user(user_id=user_id)
    return render_template('users.html', users=users, page_asker=page_asker)


@app.route('/user/<int:user_id>/', methods=["GET", "POST"])
def user_profile(user_id: int):
    if 'email' not in session:
        return redirect(url_for("login"))
    profile_owner=get_user_data(user_id=user_id)
    user = get_user_data(email=session["email"])
    if request.method == "POST":
        action = request.form.get('action')
        if action == "promote":
            if profile_owner.role.title == "Admin":
                change_user_role("Regular", user_id=user_id)
            else:
                change_user_role("Admin", user_id=user_id)
        elif action == "ban":
            if is_banned(user_id=user_id):
                unban_user(user_id=user_id)
            else:
                ban_user(user_id=user_id)
    return render_template('user_profile.html', user=user, profile_owner=profile_owner)


@app.route('/add/', methods=["GET", "POST"])
def product_adding():
    if 'email' not in session:  
        return redirect(url_for("login"))
    user = get_user_data(email=session["email"])
    if user.role.title != "Admin":
        return redirect(url_for("index"))
    form = AddForm()
    if form.validate_on_submit():
        if request.files['image'].filename == '':
            return "Файлу не знайдено"
        if request.files['image'].filename.split('.')[-1] not in ALLOWED_EXTENSIONS:
            return "Файл повинен бути з розширенням '.jpg', чи '.jpeg'"
        image_file = request.files['image']
        image_data = image_file.read()
        image_bytes = BytesIO(image_data)
        image = Image.open(image_bytes)
        picture_name = create_picture_name()
        save_product_picture(picture_name, picture=image)
        add_product(Product(name=request.form["name"], description=request.form["description"],
                            size=request.form["size"], price=request.form["price"], 
                            product_picture_name=picture_name))
        return redirect(url_for('product_info', product_id=get_product(name=request.form["name"]).id))
    return render_template("add.html", user=user, form=form)


@app.route('/edit/<int:product_id>/', methods=["GET", "POST"])
def edit_product(product_id: int):
    if 'email' not in session:  
        return redirect(url_for("login"))
    user = get_user_data(email=session["email"])
    if user.role.title != "Admin":
        return redirect(url_for("index"))
    form = EditForm()
    product = get_product(id=product_id)
    if form.validate_on_submit():

        if product_existance(name=request.form["name"]) and product.name != request.form["name"]:
            return render_template("edit.html", user=user, form=form, product=product, get_product_picture_path=get_product_picture_path, reports=["Товар з такою назвою вже існує"])

        product.name=request.form["name"]
        product.description=request.form["description"]
        product.size=request.form["size"]
        product.price=request.form["price"]

        if request.files['image'].filename != '' and request.files['image'].filename.split('.')[-1] not in ALLOWED_EXTENSIONS:
            delete_first_picture(product.product_picture_name)

            image_file = request.files['image']
            image_data = image_file.read()
            image_bytes = BytesIO(image_data)
            image = Image.open(image_bytes)

            save_product_picture(product.product_picture_name, picture=image)
        try:
            db_session.commit()
            return redirect(url_for('product_info', product_id=product.id))
        except:
            db_session.rollback()
            return "Виникла помилка: Товар не було зміненно"
    return render_template("edit.html", user=user, form=form, product=product, get_product_picture_path=get_product_picture_path)


@app.route('/edit/<int:product_id>/categories/', methods=["GET", "POST"])
def edit_product_categories(product_id: int):
    if 'email' not in session:  
        return redirect(url_for("login"))
    user = get_user_data(email=session["email"])
    if user.role.title != "Admin":
        return redirect(url_for("index"))
    categories = get_categories()
    product = get_product(id=product_id)
    if request.method == "POST":
        action, category_id = request.form.get('action').split('|')
        category = get_category(id=category_id)
        if category in product.categories:
            delete_products_category(product=product, category=category)
        else:
            add_products_category(product=product, category=category)
    return render_template("product_categories.html", user=user, product=product, categories=categories)


@app.route('/category/add/', methods=["GET", "POST"])
def category_adding():
    if 'email' not in session:  
        return redirect(url_for("login"))
    user = get_user_data(email=session["email"])
    if user.role.title != "Admin":
        return redirect(url_for("index"))
    form = CategoryAddForm()
    if form.validate_on_submit():
        add_category(title=request.form["title"], description=request.form["description"])
        return redirect(url_for('categories_list'))
    return render_template("category_add.html", user=user, form=form)


@app.route('/category/edit/<int:category_id>/', methods=["GET", "POST"])
def edit_category(category_id: int):
    if 'email' not in session:  
        return redirect(url_for("login"))
    user = get_user_data(email=session["email"])
    if user.role.title != "Admin":
        return redirect(url_for("index"))
    form = CategoryEditForm()
    category = get_category(id=category_id)
    if form.validate_on_submit():

        if not get_category(title=request.form["title"]) is None and category.title != request.form["title"]:
            return render_template("category_edit.html", user=user, form=form, category=category, get_product_picture_path=get_product_picture_path, reports=["Товар з такою назвою вже існує"])

        category.title=request.form["title"]
        category.description=request.form["description"]

        try:
            db_session.commit()
            return redirect(url_for('categories_list'))
        except:
            db_session.rollback()
            return "Виникла помилка: Товар не було зміненно"
    return render_template("category_edit.html", user=user, form=form, category=category, get_product_picture_path=get_product_picture_path)

