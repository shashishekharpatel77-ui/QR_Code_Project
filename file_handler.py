from datetime import datetime
from PIL import Image

import config


def save_image(image, fmt="PNG", name="qr", folder=None):
    fmt = fmt.upper()
    if fmt not in config.Allowed_Formats:
        raise ValueError("Format must be PNG or JPG")

    if folder is None:
        folder = config.Output_Dir
    folder.mkdir(parents=True, exist_ok=True)

    stamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")

    if fmt == "JPG":
        path = folder / f"{name}_{stamp}.jpg"
        image.convert("RGB").save(path, "JPEG")
    else:
        path = folder / f"{name}_{stamp}.png"
        image.save(path, "PNG")

    return path


def load_image(path):
    try:
        img = Image.open(path)
        img.load()
        return img
    except FileNotFoundError:
        raise ValueError("File not found")
    except Exception:
        raise ValueError("This is not a valid image file")