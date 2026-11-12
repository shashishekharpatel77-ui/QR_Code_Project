def escape_text(text):
    for ch in ["\\", ";", ",", ":", '"']:
        text = text.replace(ch, "\\" + ch)
    return text


def build_wifi_string(ssid, password, security="WPA"):
    if ssid.strip() == "":
        raise ValueError("Wi-Fi ka naam khali hai")

    ssid = escape_text(ssid)

    if security == "nopass":
        return f"WIFI:T:nopass;S:{ssid};;"

    password = escape_text(password)
    return f"WIFI:T:{security};S:{ssid};P:{password};;"


if __name__ == "__main__":
    print(build_wifi_string("Home;WiFi", "pass:1234", "WPA"))