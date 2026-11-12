import cv2
from PyQt6.QtWidgets import (
    QApplication, QWidget, QMainWindow, QTabWidget, QVBoxLayout, QHBoxLayout,
    QFormLayout, QLabel, QLineEdit, QPushButton, QComboBox, QSpinBox,
    QStackedWidget, QFileDialog, QColorDialog, QMessageBox, QTextEdit, QListWidget,
)
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtCore import Qt, QTimer

import config
from qr_generator import generate_qr, add_logo
from wifi_qr import build_wifi_string
from contact_qr import build_vcard
from validators import is_valid_url, is_valid_phone, is_valid_email, is_valid_wifi_password
from file_handler import save_image
from qr_scanner import scan_image, scan_frame
from bulk_generator import bulk_generate
from history_db import add_history, get_history


def pil_to_pixmap(img):
    img = img.convert("RGB")
    data = img.tobytes("raw", "RGB")
    qimg = QImage(data, img.width, img.height, img.width * 3, QImage.Format.Format_RGB888)
    return QPixmap.fromImage(qimg)


class GenerateTab(QWidget):
    def __init__(self):
        super().__init__()
        self.fill_color = config.Default_Fill_Color
        self.back_color = config.Default_Back_Color
        self.logo_path = None
        self.current_image = None

        self.type_box = QComboBox()
        self.type_box.addItems(["Text", "URL", "Wi-Fi", "Contact"])
        self.type_box.currentIndexChanged.connect(self.change_type)

        # page for text and url
        self.text_input = QLineEdit()
        self.text_input.setPlaceholderText("Enter text or URL")
        page0 = QWidget()
        form0 = QFormLayout(page0)
        form0.addRow("Data:", self.text_input)

        # page for wifi
        self.ssid_input = QLineEdit()
        self.pass_input = QLineEdit()
        self.security_box = QComboBox()
        self.security_box.addItems(["WPA", "WEP", "nopass"])
        page1 = QWidget()
        form1 = QFormLayout(page1)
        form1.addRow("Wi-Fi name:", self.ssid_input)
        form1.addRow("Password:", self.pass_input)
        form1.addRow("Security:", self.security_box)

        # page for contact
        self.name_input = QLineEdit()
        self.phone_input = QLineEdit()
        self.email_input = QLineEdit()
        self.org_input = QLineEdit()
        page2 = QWidget()
        form2 = QFormLayout(page2)
        form2.addRow("Name:", self.name_input)
        form2.addRow("Phone:", self.phone_input)
        form2.addRow("Email:", self.email_input)
        form2.addRow("Organization:", self.org_input)

        self.stack = QStackedWidget()
        self.stack.addWidget(page0)
        self.stack.addWidget(page1)
        self.stack.addWidget(page2)

        # options
        self.size_spin = QSpinBox()
        self.size_spin.setRange(5, 30)
        self.size_spin.setValue(config.Default_Box_Size)

        self.error_box = QComboBox()
        self.error_box.addItems(["L", "M", "Q", "H"])
        self.error_box.setCurrentText(config.Default_Error_Level)

        options = QFormLayout()
        options.addRow("Size:", self.size_spin)
        options.addRow("Error level:", self.error_box)

        self.fill_btn = QPushButton("QR colour")
        self.fill_btn.clicked.connect(self.pick_fill)
        self.back_btn = QPushButton("Background colour")
        self.back_btn.clicked.connect(self.pick_back)
        self.logo_btn = QPushButton("Add logo")
        self.logo_btn.clicked.connect(self.pick_logo)

        colors = QHBoxLayout()
        colors.addWidget(self.fill_btn)
        colors.addWidget(self.back_btn)
        colors.addWidget(self.logo_btn)

        self.generate_btn = QPushButton("Generate QR")
        self.generate_btn.clicked.connect(self.generate)
        self.png_btn = QPushButton("Save PNG")
        self.png_btn.clicked.connect(lambda: self.save("PNG"))
        self.jpg_btn = QPushButton("Save JPG")
        self.jpg_btn.clicked.connect(lambda: self.save("JPG"))

        buttons = QHBoxLayout()
        buttons.addWidget(self.generate_btn)
        buttons.addWidget(self.png_btn)
        buttons.addWidget(self.jpg_btn)

        self.preview = QLabel("QR will show here")
        self.preview.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.preview.setMinimumSize(300, 300)

        self.status = QLabel("")

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("QR type:"))
        layout.addWidget(self.type_box)
        layout.addWidget(self.stack)
        layout.addLayout(options)
        layout.addLayout(colors)
        layout.addLayout(buttons)
        layout.addWidget(self.preview)
        layout.addWidget(self.status)

    def change_type(self, index):
        pages = [0, 0, 1, 2]
        self.stack.setCurrentIndex(pages[index])

    def pick_fill(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.fill_color = color.name()
            self.fill_btn.setStyleSheet("background-color: " + self.fill_color)

    def pick_back(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.back_color = color.name()
            self.back_btn.setStyleSheet("background-color: " + self.back_color)

    def pick_logo(self):
        path = QFileDialog.getOpenFileName(self, "Choose logo", "", "Images (*.png *.jpg *.jpeg)")[0]
        if path:
            self.logo_path = path
            self.logo_btn.setText("Logo added")

    def get_data(self):
        index = self.type_box.currentIndex()

        if index == 0:
            text = self.text_input.text().strip()
            if text == "":
                raise ValueError("Text is empty")
            return text

        if index == 1:
            url = self.text_input.text().strip()
            if not is_valid_url(url):
                raise ValueError("URL is not valid (start with http:// or https://)")
            return url

        if index == 2:
            ssid = self.ssid_input.text()
            password = self.pass_input.text()
            security = self.security_box.currentText()
            if not is_valid_wifi_password(password, security):
                raise ValueError("Wi-Fi password is not valid (WPA needs 8 to 63 characters)")
            return build_wifi_string(ssid, password, security)

        name = self.name_input.text()
        phone = self.phone_input.text().strip()
        email = self.email_input.text().strip()
        org = self.org_input.text().strip()
        if phone and not is_valid_phone(phone):
            raise ValueError("Phone number is not valid")
        if email and not is_valid_email(email):
            raise ValueError("Email is not valid")
        return build_vcard(name, phone, email, org)

    def generate(self):
        try:
            data = self.get_data()

            level = self.error_box.currentText()
            if self.logo_path:
                level = "H"

            img = generate_qr(data, self.fill_color, self.back_color,
                              self.size_spin.value(), level)

            if self.logo_path:
                img = add_logo(img, self.logo_path)

            self.current_image = img
            pixmap = pil_to_pixmap(img).scaled(
                300, 300, Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation)
            self.preview.setPixmap(pixmap)
            self.status.setText("QR generated")

            add_history(self.type_box.currentText(), data)

        except ValueError as e:
            QMessageBox.warning(self, "Error", str(e))
        except Exception as e:
            QMessageBox.critical(self, "Error", "Something went wrong: " + str(e))

    def save(self, fmt):
        if self.current_image is None:
            QMessageBox.information(self, "No QR", "Generate a QR first")
            return
        try:
            path = save_image(self.current_image, fmt)
            self.status.setText("Saved: " + str(path))
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))


class ScanTab(QWidget):
    def __init__(self):
        super().__init__()
        self.cap = None
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)

        self.image_btn = QPushButton("Scan from image")
        self.image_btn.clicked.connect(self.scan_from_file)
        self.start_btn = QPushButton("Start webcam")
        self.start_btn.clicked.connect(self.start_webcam)
        self.stop_btn = QPushButton("Stop webcam")
        self.stop_btn.clicked.connect(self.stop_webcam)
        self.copy_btn = QPushButton("Copy")
        self.copy_btn.clicked.connect(self.copy_result)

        buttons = QHBoxLayout()
        buttons.addWidget(self.image_btn)
        buttons.addWidget(self.start_btn)
        buttons.addWidget(self.stop_btn)
        buttons.addWidget(self.copy_btn)

        self.video = QLabel("Webcam will show here")
        self.video.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.video.setMinimumSize(400, 300)

        self.result = QTextEdit()
        self.result.setReadOnly(True)
        self.result.setPlaceholderText("Scan result will show here")

        layout = QVBoxLayout(self)
        layout.addLayout(buttons)
        layout.addWidget(self.video)
        layout.addWidget(self.result)

    def scan_from_file(self):
        path = QFileDialog.getOpenFileName(self, "Choose QR image", "", "Images (*.png *.jpg *.jpeg *.bmp)")[0]
        if not path:
            return
        data = scan_image(path)
        if data is None:
            self.result.setText("No QR found")
        else:
            self.result.setText(data)

    def start_webcam(self):
        if self.cap is not None:
            return
        self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        if not self.cap.isOpened():
            self.cap.release()
            self.cap = None
            QMessageBox.warning(self, "Camera", "Camera not found")
            return
        self.timer.start(30)

    def update_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            return

        h, w, c = frame.shape
        qimg = QImage(frame.data, w, h, 3 * w, QImage.Format.Format_BGR888).copy()
        self.video.setPixmap(QPixmap.fromImage(qimg))

        data = scan_frame(frame)
        if data:
            self.result.setText(data)
            self.stop_webcam()

    def stop_webcam(self):
        self.timer.stop()
        if self.cap is not None:
            self.cap.release()
            self.cap = None
        self.video.clear()
        self.video.setText("Webcam is off")

    def copy_result(self):
        text = self.result.toPlainText()
        if text:
            QApplication.clipboard().setText(text)


class BulkTab(QWidget):
    def __init__(self):
        super().__init__()

        self.info = QLabel("CSV needs a 'data' column (optional 'name' column)")
        self.btn = QPushButton("Choose CSV and generate")
        self.btn.clicked.connect(self.run_bulk)
        self.result = QTextEdit()
        self.result.setReadOnly(True)

        layout = QVBoxLayout(self)
        layout.addWidget(self.info)
        layout.addWidget(self.btn)
        layout.addWidget(self.result)

    def run_bulk(self):
        path = QFileDialog.getOpenFileName(self, "Choose CSV", "", "CSV (*.csv)")[0]
        if not path:
            return
        try:
            count, errors = bulk_generate(path)
            text = str(count) + " QR codes created in " + str(config.Output_Dir / "bulk")
            if errors:
                text += "\n\nErrors:\n" + "\n".join(errors)
            self.result.setText(text)
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))


class HistoryTab(QWidget):
    def __init__(self):
        super().__init__()

        self.list_widget = QListWidget()
        self.refresh_btn = QPushButton("Refresh")
        self.refresh_btn.clicked.connect(self.load_history)

        layout = QVBoxLayout(self)
        layout.addWidget(self.refresh_btn)
        layout.addWidget(self.list_widget)

        self.load_history()

    def load_history(self):
        self.list_widget.clear()
        for qr_type, data, created_at in get_history():
            short = data.replace("\n", " ")[:60]
            self.list_widget.addItem(created_at + " | " + qr_type + " | " + short)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QR Code Generator & Scanner")
        self.resize(650, 750)

        self.generate_tab = GenerateTab()
        self.scan_tab = ScanTab()
        self.bulk_tab = BulkTab()
        self.history_tab = HistoryTab()

        tabs = QTabWidget()
        tabs.addTab(self.generate_tab, "Generate")
        tabs.addTab(self.scan_tab, "Scan")
        tabs.addTab(self.bulk_tab, "Bulk")
        tabs.addTab(self.history_tab, "History")
        self.setCentralWidget(tabs)

    def closeEvent(self, event):
        self.scan_tab.stop_webcam()
        event.accept()