from .base import Base, session, engine
from .models import User, Role, Category, Product

__all__ = {
    "Base",
    "User",
    "Role",
    "Category",
    "Product"
}

def migrate(engine):
    
    from storage.proccessing import delete_all_products

    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    delete_all_products()

