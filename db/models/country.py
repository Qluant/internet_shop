from sqlalchemy import Column, Unicode, Float, Integer, BigInteger

from .. import Base

__all__ = ["Base"]


class Country(Base):
    __tablename__ = "countries"

    id = Column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
    )
    title = Column(
        Unicode(225),
        unique=True,
        nullable=False,
    )
    
    # country_id