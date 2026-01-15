import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFileDialog
from PyQt5.QtGui import QPixmap
import qrcode
from PIL import Image
import io

class QRGenerator(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('QR Code Generator')
        layout = QVBoxLayout()

        self.url_input = QLineEdit(self)
        self.url_input.setPlaceholderText('Enter URL')
        layout.addWidget(self.url_input)

        self.generate_btn = QPushButton('Generate QR Code', self)
        self.generate_btn.clicked.connect(self.generate_qr)
        layout.addWidget(self.generate_btn)

        self.qr_label = QLabel(self)
        layout.addWidget(self.qr_label)

        self.save_btn = QPushButton('Save QR Code', self)
        self.save_btn.clicked.connect(self.save_qr)
        layout.addWidget(self.save_btn)

        self.setLayout(layout)
        self.qr_image = None

    def generate_qr(self):
        url = self.url_input.text()
        if url:
            qr = qrcode.QRCode(version=1, box_size=10, border=5)
            qr.add_data(url)
            qr.make(fit=True)
            img = qr.make_image(fill='black', back_color='white')
            # Convert PIL Image to QPixmap
            buffer = io.BytesIO()
            img.save(buffer, format='PNG')
            buffer.seek(0)
            pixmap = QPixmap()
            pixmap.loadFromData(buffer.read())
            self.qr_label.setPixmap(pixmap)
            self.qr_image = img

    def save_qr(self):
        if self.qr_image:
            file_path, _ = QFileDialog.getSaveFileName(self, 'Save QR Code', '', 'PNG Files (*.png)')
            if file_path:
                self.qr_image.save(file_path)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = QRGenerator()
    ex.show()
    sys.exit(app.exec_())