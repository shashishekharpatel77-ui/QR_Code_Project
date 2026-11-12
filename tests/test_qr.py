import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pytest

from qr_generator import generate_qr
from wifi_qr import build_wifi_string
from contact_qr import build_vcard
from validators import is_valid_url, is_valid_email, is_valid_phone
from qr_scanner import scan_image


def test_wifi_string():
    assert build_wifi_string("Home", "pass1234", "WPA") == "WIFI:T:WPA;S:Home;P:pass1234;;"


def test_wifi_special_characters():
    assert "Home\\;Net" in build_wifi_string("Home;Net", "pass1234", "WPA")


def test_vcard():
    card = build_vcard("Shashi", "9876543210")
    assert card.startswith("BEGIN:VCARD")
    assert "FN:Shashi" in card
    assert card.endswith("END:VCARD")


def test_url():
    assert is_valid_url("https://github.com") is True
    assert is_valid_url("github") is False


def test_email_and_phone():
    assert is_valid_email("a@b.com") is True
    assert is_valid_email("abc") is False
    assert is_valid_phone("9876543210") is True
    assert is_valid_phone("123") is False


def test_empty_data():
    with pytest.raises(ValueError):
        generate_qr("")


def test_generate_then_scan(tmp_path):
    img = generate_qr("hello round trip")
    path = tmp_path / "test.png"
    img.save(path)
    assert scan_image(path) == "hello round trip"