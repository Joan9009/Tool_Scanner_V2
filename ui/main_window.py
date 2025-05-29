from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton,
    QTextEdit, QMessageBox
)
from PyQt5.QtCore import Qt
from ui.scan_worker import ScanWorker

# Importa las funciones necesarias
from utils import detect_cms
from scanners.wordpress_scanner import scan_wordpress
from scanners.joomla_scanner import scan_joomla
from scanners.drupal_scanner import scan_drupal

class MainWindow(QWidget):
    def __init__(self, cms_detector, scanners):
        super().__init__()
        self.cms_detector =cms_detector
        self.scanners = scanners

        self.setWindowTitle("CMS Vulnerability Scanner")
        self.setGeometry(300, 300, 700, 500)

        layout = QVBoxLayout()

        self.label = QLabel("Introduce la URL del sitio a escanear:")
        layout.addWidget(self.label)

        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("https://ejemplo.com")
        layout.addWidget(self.url_input)

        self.detect_button = QPushButton("Detectar CMS y Escanear")
        self.detect_button.clicked.connect(self.run_scan)
        layout.addWidget(self.detect_button)

        self.cms_label = QLabel("CMS detectado: N/A")
        layout.addWidget(self.cms_label)

        self.output = QTextEdit()
        self.output.setReadOnly(True)
        layout.addWidget(self.output)

        self.setLayout(layout)

    def run_scan(self):
        url = self.url_input.text().strip()

        if not url.startswith("http://") and not url.startswith("https://"):
            QMessageBox.warning(self, "Error", "La URL debe comenzar con http:// o https://")
            return

        self.output.clear()
        self.cms_label.setText("CMS detectado: N/A")

        self.scan_thread = ScanWorker(self.url_input.text().strip(), self.cms_detector, self.scanners)
        self.scan_thread.output_signal.connect(self.append_output)
        self.scan_thread.cms_detected.connect(self.update_cms_label)
        self.scan_thread.finished.connect(self.scan_finished)
        self.scan_thread.start()

    def append_output(self, text):
        self.output.append(text)

    def update_cms_label(self, cms):
        self.cms_label.setText(f"CMS detectado: {cms}")

    def scan_finished(self):
        self.output.append("\n[✓] Escaneo finalizado.")
