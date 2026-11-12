import re


def is_valid_url(url):
    pattern = r"^https?://[\w\-]+(\.[\w\-]+)+([/?#]\S*)?$"
    return re.match(pattern, url.strip()) is not None


def is_valid_phone(phone):
    phone = phone.replace(" ", "").replace("-", "")
    return re.match(r"^\+?[0-9]{10,13}$", phone) is not None


def is_valid_email(email):
    pattern = r"^[\w\.\-+]+@[\w\-]+(\.[\w\-]+)+$"
    return re.match(pattern, email.strip()) is not None


def is_valid_wifi_password(password, security):
    if security == "nopass":
        return True
    if security == "WPA":
        return 8 <= len(password) <= 63
    return len(password) > 0