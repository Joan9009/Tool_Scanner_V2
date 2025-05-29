from PyQt5.QtCore import QThread, pyqtSignal
import sys

class ScanWorker(QThread):
    output_signal = pyqtSignal(str)
    cms_detected = pyqtSignal(str)

    def __init__(self, url, cms_detector, scanners):
        super().__init__()
        self.url = url
        self.cms_detector = cms_detector
        self.scanners = scanners

    def run(self):
        self.output_signal.emit("[+] Detectando CMS...")
        cms = self.cms_detector(self.url)
        if not cms:
            self.cms_detected.emit("No detectado")
            self.output_signal.emit("[-] No se pudo detectar un CMS compatible.")
            return

        self.cms_detected.emit(cms)
        self.output_signal.emit(f"[+] CMS detectado: {cms}")
        self.output_signal.emit(f"[+] Iniciando escaneo de {cms}...\n")

        scanner_func = self.scanners.get(cms)
        if scanner_func:

            def real_time_print(*args, **kwargs):
                line = ' '.join(str(arg) for arg in args)
                self.output_signal.emit(line)

            scanner_func(self.url, output_func=real_time_print)
        else:
            self.output_signal.emit("[-] No hay escáner disponible para este CMS.")
