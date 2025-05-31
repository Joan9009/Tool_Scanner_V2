import requests
import sys


def scan_drupal(base_url, paths_file='payloads/drupal.txt', output_func=print):
    def out(msg):
        output_func(msg)
        sys.stdout.flush()

    out(f"\n--- Escaneo de Vulnerabilidades Drupal ---\n")

    try:
        with open(paths_file, 'r') as file:
            paths = file.read().splitlines()
    except FileNotFoundError:
        out(f"[ERROR] Archivo de rutas no encontrado: {paths_file}")
        return

    for path in paths:
        full_url = base_url.rstrip('/') + '/' + path.lstrip('/')
        try:
            response = requests.get(full_url, timeout=10)
            status = response.status_code

            if status == 200:
                if 'CHANGELOG.txt' in full_url:
                    out(f"[!] {full_url}")
                    out(f"[!] Exposición de versión en CHANGELOG.txt")
                elif 'user/register' in full_url:
                    out(f"[!] {full_url}")
                    out(f"[!] Registro de usuario habilitado públicamente")
                else:
                    out(f"[!] Posible hallazgo en: {full_url}")

            elif status == 403:
                out(f"[-] Acceso prohibido: {full_url}")
            elif status == 405:
                out(f"[!] Método no permitido en: {full_url}")
            elif status == 500:
                out(f"[!] Error del servidor en: {full_url}")
            elif status == 401:
                out(f"[!] Requiere autenticación: {full_url}")
            elif status == 404:
                out(f"[404] {full_url} - No encontrado")
            else:
                out(f"[{status}] {full_url}")

        except requests.RequestException as e:
            out(f"[ERROR] No se pudo conectar a {full_url} - {e}")
