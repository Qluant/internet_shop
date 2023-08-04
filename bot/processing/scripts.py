from db.processing import get_prod_ind, User


def product_index_dispatcher(index: int, activity: str, category: int = -1) -> int:
    indexes = get_prod_ind(category=category)
    if activity == "next":
        if indexes.index(index)+1 >= len(indexes):
            return indexes[0]
        return indexes[indexes.index(index)+1]
    elif activity == "back":
        return indexes[indexes.index(index)-1]
    return indexes[0]


def basket_index_dispatcher(index: int, activity: str, user: User) -> int:
    indexes = []
    for product in user.basket:
        indexes.append(product.id)
    if indexes == []:
        return -1
    if activity == "next":
        if index == -1:
            return indexes[0]
        if indexes.index(index)+1 >= len(indexes):
            return -1
        return indexes[indexes.index(index)+1]
    elif activity == "back":
        if index == -1:
            return indexes[-1]
        if indexes.index(index)-1 < 0:
            return -1
        return indexes[indexes.index(index)-1]
