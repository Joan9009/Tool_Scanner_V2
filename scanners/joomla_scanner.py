import requests

# Colores ANSI
RESET = "\033[0m"
YELLOW = "\033[93m"
RED = "\033[91m"
BLUE = "\033[94m"
MAGENTA = "\033[95m"
GRAY = "\033[90m"

def scan_joomla(base_url, paths_file='payloads/joomla.txt'):
    print("\n--- Escaneo de Vulnerabilidades Joomla ---\n")

    try:
        with open(paths_file, 'r') as file:
            paths = file.read().splitlines()
    except FileNotFoundError:
        print(f"[ERROR] Archivo de rutas no encontrado: {paths_file}")
        return

    for path in paths:
        full_url = base_url.rstrip('/') + '/' + path.lstrip('/')
        try:
            response = requests.get(full_url, timeout=10)
            status = response.status_code

            if status == 200:
                print(f"{YELLOW}[!] Posible hallazgo en: {full_url}{RESET}")
            elif status == 403:
                print(f"{RED}[-] Acceso prohibido: {full_url}{RESET}")
            elif status == 500:
                print(f"{MAGENTA}[!] Error del servidor en: {full_url}{RESET}")
            elif status == 401:
                print(f"{BLUE}[!] Requiere autenticación: {full_url}{RESET}")
        except requests.RequestException as e:
            print(f"{RED}[ERROR] No se pudo conectar a {full_url} - {e}{RESET}")
