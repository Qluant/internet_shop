from sqlalchemy import Column, Unicode, Float, Integer, BigInteger

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
    size = Column(
        Float(2),
        nullable=False,
    )
    price = Column(
        Float(2),
        nullable=False,
    )
    name = Column(
        Unicode(225),
        unique=True,
        nullable=False,
    )
    # country_id