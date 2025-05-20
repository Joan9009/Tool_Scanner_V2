import requests

# Colores ANSI
RESET = "\033[0m"
YELLOW = "\033[93m"
RED = "\033[91m"
BLUE = "\033[94m"
MAGENTA = "\033[95m"
GRAY = "\033[90m"

def scan_wordpress(base_url, paths_file='payloads/wordpress.txt'):
    print("\n--- Escaneo de Vulnerabilidades WordPress ---\n")

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
                # Casos especiales para WordPress
                if 'wp-json' in full_url:
                    print(f"{YELLOW}[!] {full_url}")
                    print("{YELLOW}[!] API REST habilitada - Posible enumeración de usuarios.")
                elif 'wp-content/plugins' in full_url:
                    print(f"{YELLOW}[!] {full_url}")
                    print("{YELLOW}[!] Plugins visibles - Riesgo de enumeración.")
                elif 'wp-config.php.bak' in full_url:
                    print(f"[!] {full_url}")
                    print("[!] Archivo de configuración de respaldo accesible - ¡ALTO RIESGO!")
                else:
                    print(f"[!] Posible hallazgo en: {full_url}")

            elif status == 403:
                print(f"{RED}[-] Acceso prohibido: {full_url}{RESET}")
            elif status == 405:
                print(f"{RED}[!] Método no permitido en: {full_url}{RESET}")
            elif status == 500:
                print(f"{MAGENTA}[!] Error del servidor en: {full_url}{RESET}")
            elif status == 401:
                print(f"{BLUE}[!] Requiere autenticación: {full_url}{RESET}")
            elif status == 404:
                print(f"{GRAY}[404] {full_url} - No encontrado (puede ser seguro o no expuesto){RESET}")
            else:
                print(f"[{status}] {full_url}")

        except requests.RequestException as e:
            print(f"{RED}[ERROR] No se pudo conectar a {full_url} - {e}{RESET}")
