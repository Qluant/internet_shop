This is my big petproject where I tried to do database for both telegram bot and website.

I made this petproject on ubuntu, so I don't know how it will work on Windows or macOS. I used postgresql for my first such big database provided by SQLAlchemy library. For telegram bot I used aiogram and for website flask. Also, I done photos separate from db in folder "storage".



Easy start:

1) Firstly you need to create virtual enviroment and download all libriries in "requirements.txt".

2) Then, you need to create folder named "vendor" and "config.py" in it.
Also, you need to write code like this in "config.py":

'''
import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or '987654321'
    DATABASE='postgresql+psycopg2://postgres:<password_of_your db>@localhost/postgres'
    DATABASE='postgresql+psycopg2://<username>:<password_of_db>@localhost/<database_name>'
    API_TOKEN=<There is a token of your Telegram bot>
    STATIC_FOLDER = <a path for your file called "storage" in this project> For me its:
    "/home/qluant/Desktop/Projects/VScode/internet_shop/storage/"
'''

3) Then, you should launch "migrate.py" - to create your database, if you have any errors look for their explanations in "migrate.py".

4) Finally, you need to made folder "product_photos" in "storage". Then, "main" folder in it,
   and two photos = "basket.jpg" for photo in telegram bot. And "icon.jpg" for main photo in telegram photo.

5) Now, you can turn on bot and website by launching "run.py".
