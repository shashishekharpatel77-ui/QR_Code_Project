import qrcode
from qrcode.constants import ERROR_CORRECT_L, ERROR_CORRECT_M, ERROR_CORRECT_Q, ERROR_CORRECT_H
from PIL import Image

import config

Error_Levels = {
    "L": ERROR_CORRECT_L,
    "M": ERROR_CORRECT_M,
    "Q": ERROR_CORRECT_Q,
    "H": ERROR_CORRECT_H,
}


def generate_qr(data, fill_color=config.Default_Fill_Color, back_color=config.Default_Back_Color,
                box_size=config.Default_Box_Size, error_level=config.Default_Error_Level):
    if data is None or data.strip() == "":
        raise ValueError("Data khali hai")

    if error_level not in Error_Levels:
        raise ValueError("Error level L, M, Q ya H hona chahiye")

    qr = qrcode.QRCode(
        version=None,
        error_correction=Error_Levels[error_level],
        box_size=box_size,
        border=config.Default_Border,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color=fill_color, back_color=back_color)
    return img.convert("RGB")


def add_logo(qr_image, logo_path):
    logo = Image.open(logo_path).convert("RGBA")
    qr_image = qr_image.convert("RGBA")

    max_size = int(qr_image.size[0] * config.Logo_Max_Ratio)
    logo.thumbnail((max_size, max_size))

    x = (qr_image.size[0] - logo.size[0]) // 2
    y = (qr_image.size[1] - logo.size[1]) // 2
    qr_image.paste(logo, (x, y), logo)

    return qr_image.convert("RGB")


if __name__ == "__main__":
    img = generate_qr("https://github.com")
    img.save(config.Output_Dir / "test.png")
    print("Saved")