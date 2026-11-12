# QR Code Generator & Scanner

A desktop app made with Python and PyQt6. You can create QR codes (text, URL, Wi-Fi, contact), scan QR codes from an image or webcam, make many QR codes at once from a CSV file, and see a history of what you generated.

I made this as a Python project to practice modules, GUI building, image handling and file handling.

## Features

- Generate QR codes for text, URL, Wi-Fi and contact (vCard)
- Change QR colour, background colour and size
- Choose the error correction level (L, M, Q, H)
- Add a logo in the middle of the QR (error level switches to H automatically so it still scans)
- Save as PNG or JPG (file name has date and time, so nothing gets overwritten)
- Scan a QR from an image file
- Scan a QR using the webcam
- Copy the scanned result
- Bulk generate QR codes from a CSV file
- History of generated QR codes, saved in SQLite
- Input checks for URL, phone, email and Wi-Fi password
- Basic tests with pytest


## Built with

- Python
- PyQt6 (GUI)
- qrcode (making QR codes)
- Pillow (images, colours, logo)
- OpenCV (scanning)
- SQLite (history)
- pytest (tests)

## How to run

1. Clone the project

```
git clone https://github.com/YOUR_USERNAME/QR_Code_Project.git
cd QR_Code_Project
```

2. Make a virtual environment and activate it (Windows PowerShell)

```
python -m venv venv
venv\Scripts\activate
```

3. Install the libraries

```
pip install -r requirements.txt
```

4. Start the app

```
python main.py
```

## How to use

**Generate tab**
Pick the type (Text, URL, Wi-Fi or Contact), fill the fields and press Generate QR. Then save it as PNG or JPG. Saved files go to the `output` folder.
Keep the QR colour dark and the background light, otherwise phones may not scan it.

**Scan tab**
Use "Scan from image" to pick a QR picture, or "Start webcam" and show the QR to the camera. The webcam stops by itself once a QR is found.

**Bulk tab**
Choose a CSV file with a `data` column. A `name` column is optional and is used for the file names.

```
name,data
google,https://google.com
github,https://github.com
hello,Hello World
```

The QR codes are saved in `output/bulk`.

**History tab**
Shows the QR codes you generated, newest first. Press Refresh to update the list.

## Project structure

```
QR_Code_Project/
├── main.py            # starts the app
├── gui.py             # all the tabs and windows
├── config.py          # default settings
├── qr_generator.py    # makes the QR and adds the logo
├── qr_scanner.py      # reads QR from image or webcam frame
├── wifi_qr.py         # builds the Wi-Fi text
├── contact_qr.py      # builds the vCard text
├── validators.py      # checks URL, phone, email, password
├── file_handler.py    # saves and loads images
├── bulk_generator.py  # CSV to many QR codes
├── history_db.py      # SQLite history
├── tests/
│   └── test_qr.py
├── requirements.txt
└── README.md
```

## Run the tests

```
python -m pytest
```

One test makes a QR and scans it back to check that the text comes out the same.

## Things to know

- History is saved in a local file `history.db`. It stores the data you generate, so a Wi-Fi password will also be saved there. This file is not uploaded to GitHub.
- Webcam scanning is tested on Windows only. If the camera does not open, change the camera number in `gui.py` from `0` to `1`.
- This is a desktop app, so it is not deployed online.

## What I learned

- Splitting a project into small modules and importing them
- Making a GUI with PyQt6 (tabs, forms, dialogs)
- Reading webcam frames with a timer so the window does not freeze
- Wi-Fi and vCard text formats used inside QR codes
- Why a logo needs a higher error correction level
- Writing simple tests with pytest

## Future ideas

- Make an `.exe` with PyInstaller
- Export history to CSV
- Dark mode

## Author

Shashi Shekhar Patel
B.Tech CSE, Rungta College of Engineering and Technology
