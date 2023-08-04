import os
import platform

from PIL import Image
import io


def get_path_to_storage() -> str|None:
    separator = '\\' if platform.system() == 'Windows' else '/'
    current_directory = os.getcwd()
    for _ in range(5):
        if "storage" in os.listdir(current_directory) and "product_photos" in os.listdir(os.path.join(current_directory.rstrip(separator), "storage")):
            break
        current_directory[:current_directory.rfind(separator)]
    else:
        print(f"Wasn't find current directory file. Path:\n{os.getcwd()}")
        return None
    return current_directory.rstrip(separator)


def is_folder_exist(name: str) -> bool:
    current_directory = get_path_to_storage()
    if current_directory is None:
        return False
    if name in os.listdir(os.path.join(current_directory, "storage", "product_photos")):
        return True
    return False


def is_photo_exist(name: str, picture_name: str) -> bool:
    current_directory = get_path_to_storage()
    if current_directory is None:
        return False
    if picture_name in os.listdir(os.path.join(current_directory, "storage", "product_photos", name)):
        return True
    return False

def add_product_folder(name: str) -> bool:
    current_directory = get_path_to_storage()
    if current_directory is None:
        return False
    if not is_folder_exist(name):
        os.mkdir(os.path.join(current_directory, "storage", "product_photos", name))
    return True


def delete_product_folder(name: str) -> bool:
    if name == "main":
        return False
    current_directory = get_path_to_storage()
    if current_directory is None:
        return False
    if is_folder_exist(name):
        for file_name in os.listdir(os.path.join(current_directory, "storage", "product_photos", name)):
            os.remove(os.path.join(current_directory, "storage", "product_photos", name, file_name))
        os.rmdir(os.path.join(current_directory, "storage", "product_photos", name))
    return True


def delete_all_products() -> None:
    current_directory = get_path_to_storage()
    if current_directory is None:
        return False
    for name in os.listdir(os.path.join(current_directory, "storage", "product_photos")):
        if name != "main":
            delete_product_folder(name)


def get_main_picture_name(picture_name: str) -> str:
    if ".jpg" not in picture_name:
        picture_name = picture_name + ".jpg"
    current_directory = get_path_to_storage()
    if current_directory is None:
        return False
    if picture_name in os.listdir(os.path.join(current_directory, "storage", "product_photos", "main")):
        return os.path.join(current_directory, "storage", "product_photos", "main", picture_name)


def get_picture_name(name: str) -> str:
    current_directory = get_path_to_storage()
    if current_directory is None:
        return False
    items =[int(item) for item in os.listdir(os.path.join(current_directory, "storage", "product_photos", name))]
    if len(items) == 0:
        items = [0]
    if min(items) > 0:
        return str(min(items) - 1) + ".jpg"
    return str(max(items) + 1) + ".jpg"
        


def save_product_picture(name: str, picture: Image) -> bool:
    if add_product_folder(name):
        current_directory = get_path_to_storage()
        if current_directory is None:
            return False
        picture.save(os.path.join(current_directory, "storage", "product_photos", name, get_picture_name(name)))
    return False


def get_product_picture_path(name: str, absolute_path=True) -> list[str]:
    current_directory = get_path_to_storage()
    if current_directory is None:
        return None
    picture_name = ""
    for i in range(6):
        picture_name = f"{i}.jpg"
        if is_photo_exist(name, picture_name):
            break
    else:
        return ""
    if absolute_path:
        return os.path.join(current_directory, "storage", "product_photos", name, picture_name)
    return os.path.join("product_photos", name, picture_name)


def get_all_product_pictures_pathes(name: str, absolute_path=True) -> list[str]:
    current_directory = get_path_to_storage()
    if current_directory is None:
        return None
    pictures_names = []
    for i in range(6):
        picture_name = f"{i}.jpg"
        if is_photo_exist(name, picture_name):
            if absolute_path:
                pictures_names.append(os.path.join(current_directory, "storage", "product_photos", name, picture_name))
            pictures_names.append(os.path.join("product_photos", name, picture_name))
    return pictures_names


def delete_first_picture(name: str) -> None:
    path = get_product_picture_path(name)
    try:
        os.remove(path)
    except:
        return None
