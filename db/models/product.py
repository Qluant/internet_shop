from sqlalchemy import Column, Unicode, Float, BigInteger, ForeignKey
from sqlalchemy.orm import relationship

from .categ_product import category_product_rel
from .user_product import user_product_rel

from .. import Base

__all__ = ["Base"]


class Product(Base):

    __tablename__ = "products"

    id = Column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
    )
    name = Column(
        Unicode(225),
        unique=True,
        nullable=False,
    )
    description = Column(
        Unicode(1000),
        nullable=False,
    )
    size = Column(
        Unicode(50),
        nullable=False,
    )
    price = Column(
        Float(2),
        nullable=False,
    )
    categories = relationship(
        "Category", 
        secondary=category_product_rel, 
        back_populates="products"
    )
    clients = relationship(
        "User", 
        secondary=user_product_rel, 
        back_populates="basket"
    )
    product_picture_name = Column(
        Unicode(255),
        unique=True,
        nullable=False
    )