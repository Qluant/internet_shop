from sqlalchemy import Table, Column, ForeignKey


from .. import Base

__all__ = ["Base"]

category_product_rel = Table(
    "category_product_rel",
    Base.metadata,
    Column("category_id", ForeignKey("categories.id"), primary_key=True),
    Column("product_id", ForeignKey("products.id"), primary_key=True),
)