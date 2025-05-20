from utils import detect_cms
from scanners.wordpress_scanner import scan_wordpress
from scanners.joomla_scanner import scan_joomla
from scanners.drupal_scanner import scan_drupal

def main():
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
    main()
