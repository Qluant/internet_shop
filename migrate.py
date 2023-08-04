'''
By running this file you create/recreate db.
For notice:
  If you have such as error:
  "ImportError: cannot import name 'Iterator' from 'collections' (/usr/lib/python3.10/collections/__init__.py)"
  You should remake string "from collections import Iterator" to "from collections.abc import Iterator" in
  certain path such as "../.venv/lib/python3.10/site-packages/sqlalchemy_imageattach/file.py"
'''
    

from db import engine, migrate, Role, Category, session
from sqlalchemy.orm import Session


def create_roles(session: Session, Role: object) -> None:
    session.add(Role(title="Admin", description="Administator or owner of this shop"))
    session.add(Role(title="Regular", description="Regular customer"))
    session.add(Role(title="Newbie", description="Hey, are you a new here?"))
    session.add(Role(title="Banned", description="Person that not allowed there."))
    session.commit()


def create_categories(session: Session, Category: object) -> None:
    session.add(Category(title="Одежа", description="Традиційна українська одежа"))
    session.add(Category(title="Аксесуари", description="Традиційна українські аксесуари"))
    session.add(Category(title="Прикраси", description="Традиційна українські прикарси для інтер'єру"))
    session.add(Category(title="Сувеніри", description="Українські сувеніри"))
    session.add(Category(title="Традиційні речі", description="Традиційна українські речі"))
    session.add(Category(title="Запорізьке", description="Традиційна речі Запорізбкого краю!"))
    session.add(Category(title="Івано-Франківське", description="Традиційна речі Івано-Франківського краю!"))
    session.commit()


migrate(engine)
create_roles(session, Role)
create_categories(session, Category)
