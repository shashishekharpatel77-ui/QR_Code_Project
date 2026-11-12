import csv
import re

import config
from qr_generator import generate_qr
from file_handler import save_image


def bulk_generate(csv_path, fmt="PNG"):
    folder = config.Output_Dir / "bulk"
    count = 0
    errors = []

    with open(csv_path, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)

        if reader.fieldnames is None or "data" not in reader.fieldnames:
            raise ValueError("CSV needs a column named 'data'")

        i = 0
        for row in reader:
            i += 1
            data = (row.get("data") or "").strip()
            name = (row.get("name") or "").strip()
            if name == "":
                name = "qr_" + str(i)
            name = re.sub(r"[^\w\-]", "_", name)

            try:
                img = generate_qr(data)
                save_image(img, fmt, name, folder)
                count += 1
            except ValueError as e:
                errors.append(f"Row {i}: {e}")

    return count, errors