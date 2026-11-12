import cv2

detector = cv2.QRCodeDetector()


def scan_frame(frame):
    data, points, straight = detector.detectAndDecode(frame)
    if data == "":
        return None
    return data


def scan_image(path):
    img = cv2.imread(str(path))
    if img is None:
        return None
    return scan_frame(img)


if __name__ == "__main__":
    import config
    from qr_generator import generate_qr

    img = generate_qr("hello test")
    path = config.Output_Dir / "scan_test.png"
    img.save(path)
    print(scan_image(path))