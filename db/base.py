from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import Session

import logging

from settings import Settings

logging.basicConfig(level=logging.INFO)

engine = create_engine(Settings.DATABASE)
Base = declarative_base()
meta = Base.metadata
session = Session(engine)
