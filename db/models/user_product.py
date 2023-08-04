from sqlalchemy import Table, Column, ForeignKey


from .. import Base

__all__ = ["Base"]

user_product_rel = Table(
    "user_product_rel",
    Base.metadata,
    Column("user_id", ForeignKey("users.id"), primary_key=True),
    Column("product_id", ForeignKey("products.id"), primary_key=True),
)