from flask import Flask
from vendor.config import Config

app = Flask(__name__, static_folder=Config.STATIC_FOLDER)
app.config.from_object(Config)

from .routes import *