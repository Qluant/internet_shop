from sqlalchemy import Column, Unicode, BigInteger, ForeignKey
from sqlalchemy.orm import relationship

from .. import Base

__all__ = ["Base"]


class Role(Base):
    
    __tablename__ = "roles"

    title = Column(
        Unicode(50),
        primary_key=True,
    )
    description = Column(
        Unicode(250),
    )
    users = relationship(
        "User",
        back_populates="role"
    )
