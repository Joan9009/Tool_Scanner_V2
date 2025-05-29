import argparse
from utils import detect_cms
from scanners.wordpress_scanner import scan_wordpress
from scanners.joomla_scanner import scan_joomla
from scanners.drupal_scanner import scan_drupal

scanners = {
    "WordPress": scan_wordpress,
    "Joomla": scan_joomla,
    "Drupal": scan_drupal,
}

def run_cli():
    url = input("Introduce la URL del sitio a escanear (con http/https): ").strip()

    cms = detect_cms(url)
    print(f"[+] CMS detectado: {cms}")

    if cms == "WordPress":
        scan_wordpress(url)
    elif cms == "Joomla":
        scan_joomla(url)
    elif cms == "Drupal":
        scan_drupal(url)
    else:
        print("[-] No se pudo detectar un CMS compatible.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="CMS Vulnerability Scanner")
    parser.add_argument('--gui', action='store_true', help='Iniciar interfaz gráfica (PyQt5)')
    args = parser.parse_args()

    if args.gui:
        try:
            from PyQt5.QtWidgets import QApplication
            from ui.main_window import MainWindow
        except ImportError as e:
            print(f"[ERROR] Fallo de importación: {e}")
            print("[ERROR] PyQt5 no está instalado. Puedes instalarlo con: pip install PyQt5")
            exit(1)

        import sys
        app = QApplication(sys.argv)
        window = MainWindow(detect_cms, scanners)
        window.show()
        sys.exit(app.exec_())
    else:
        run_cli()
