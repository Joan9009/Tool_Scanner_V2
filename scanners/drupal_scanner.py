import requests
import sys

# Colores ANSI
RESET = "\033[0m"
YELLOW = "\033[93m"
RED = "\033[91m"
BLUE = "\033[94m"
MAGENTA = "\033[95m"
GRAY = "\033[90m"
GREEN = "\033[92m"

def scan_drupal(base_url, paths_file='payloads/drupal.txt', output_func=print):
    def out(msg):
        output_func(msg)
        sys.stdout.flush()

    out(f"\n{MAGENTA}--- Escaneo de Vulnerabilidades Drupal ---{RESET}\n")

    try:
        with open(paths_file, 'r') as file:
            paths = file.read().splitlines()
    except FileNotFoundError:
        out(f"{RED}[ERROR] Archivo de rutas no encontrado: {paths_file}{RESET}")
        return

    for path in paths:
        full_url = base_url.rstrip('/') + '/' + path.lstrip('/')
        try:
            response = requests.get(full_url, timeout=10)
            status = response.status_code

            if status == 200:
                if 'CHANGELOG.txt' in full_url:
                    out(f"{YELLOW}[!] {full_url}{RESET}")
                    out(f"{YELLOW}[!] Exposición de versión en CHANGELOG.txt{RESET}")
                elif 'user/register' in full_url:
                    out(f"{YELLOW}[!] {full_url}{RESET}")
                    out(f"{YELLOW}[!] Registro de usuario habilitado públicamente{RESET}")
                else:
                    out(f"{YELLOW}[!] Posible hallazgo en: {full_url}{RESET}")

            elif status == 403:
                out(f"{RED}[-] Acceso prohibido: {full_url}{RESET}")
            elif status == 405:
                out(f"{RED}[!] Método no permitido en: {full_url}{RESET}")
            elif status == 500:
                out(f"{MAGENTA}[!] Error del servidor en: {full_url}{RESET}")
            elif status == 401:
                out(f"{BLUE}[!] Requiere autenticación: {full_url}{RESET}")
            elif status == 404:
                out(f"{GRAY}[404] {full_url} - No encontrado{RESET}")
            else:
                out(f"[{status}] {full_url}")

        except requests.RequestException as e:
            out(f"{RED}[ERROR] No se pudo conectar a {full_url} - {e}{RESET}")
