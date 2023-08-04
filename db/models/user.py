from sqlalchemy import Column, Unicode, Float, BigInteger, ForeignKey
from sqlalchemy.orm import relationship

from .user_product import user_product_rel

from .. import Base

__all__ = ["Base"]


class User(Base):
    
    __tablename__ = "users"

    id = Column(
        BigInteger,
        primary_key=True,
        autoincrement=True
    )
    telegram_id = Column(
        BigInteger
    )
    first_name = Column(
        Unicode(50)
    )
    last_name = Column(
        Unicode(50)
    )
    nickname = Column(
        Unicode(50)
    )
    moniker = Column(
        Unicode(50),
        nullable=False
    )
    phone_number = Column(
        Unicode(12),
        unique=True,
        nullable=True
    )
    email = Column(
        Unicode(100),
        unique=True,
        nullable=True
    )
    password = Column(
        Unicode(50)
    )
    role_title = Column(
        Unicode(50),
        ForeignKey('roles.title')
    )
    role = relationship(
        "Role", 
        back_populates="users"
    )
    basket = relationship(
        "Product", 
        secondary=user_product_rel, 
        back_populates="clients"
    )
