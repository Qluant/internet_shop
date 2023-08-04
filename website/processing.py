from db.processing import get_prod_ind, get_products


def product_index_dispatcher(index: int, activity: str, category: int = -1) -> int:
    indexes = get_prod_ind(category=category)
    if activity == "next":
        if indexes.index(index)+1 >= len(indexes):
            return indexes[0]
        return indexes[indexes.index(index)+1]
    elif activity == "previous":
        return indexes[indexes.index(index)-1]
    return indexes[0]


def group_product_index_dispatcher(pos_1: int, pos_2: int):
    products = get_products()
    if len(products) < 6:
        return products, None, None
    if pos_2 < 0:
        new_pos = len(products) - (len(products)%5)
        back_posses = f"{new_pos-5}-{new_pos}"
        products = products[-5:]
        next_posses = None
        print("Case 1")
    elif len(products) < pos_2 or len(products) < pos_1:
        new_pos = len(products) - (len(products)%5)
        back_posses = f"{new_pos-5}-{new_pos}"
        products = products[-5:]
        next_posses = None
        print("Case 2")
    else:
        products = products[pos_1:pos_2]
        next_posses = f"{pos_1+5}-{pos_2+5}"
        back_posses = f"{pos_1-5}-{pos_2-5}"
        print("Case 3")
    if back_posses.count('-') > 1:
        back_posses = None
    return products, back_posses, next_posses
