from sqlalchemy import Column, Unicode, BigInteger
from sqlalchemy.orm import relationship

from .. import Base

from .categ_product import category_product_rel

__all__ = ["Base"]


class Category(Base):
    __tablename__ = "categories"
    
    id = Column(
        BigInteger,
        primary_key=True,
        autoincrement=True
    )
    title = Column(
        Unicode(225),
        unique=True
    )
    description = Column(
        Unicode(1000)
    )
    products = relationship(
        "Product", 
        secondary=category_product_rel, 
        back_populates="categories"
    )
