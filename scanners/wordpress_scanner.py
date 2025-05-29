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

def scan_wordpress(base_url, paths_file='payloads/wordpress.txt', output_func=print):
    def out(msg):
        output_func(msg)
        sys.stdout.flush()

    out(f"\n{MAGENTA}--- Escaneo de Vulnerabilidades WordPress ---{RESET}\n")

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
                if 'wp-json' in full_url:
                    out(f"{YELLOW}[!] {full_url}{RESET}")
                    out(f"{YELLOW}[!] API REST habilitada - Posible enumeración de usuarios.{RESET}")
                elif 'wp-content/plugins' in full_url:
                    out(f"{YELLOW}[!] {full_url}{RESET}")
                    out(f"{YELLOW}[!] Plugins visibles - Riesgo de enumeración.{RESET}")
                elif 'wp-config.php.bak' in full_url:
                    out(f"{RED}[!] {full_url}{RESET}")
                    out(f"{RED}[!] Archivo de configuración de respaldo accesible - ¡ALTO RIESGO!{RESET}")
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
                out(f"{GRAY}[404] {full_url} - No encontrado (puede ser seguro o no expuesto){RESET}")
            else:
                out(f"[{status}] {full_url}")

        except requests.RequestException as e:
            out(f"{RED}[ERROR] No se pudo conectar a {full_url} - {e}{RESET}")

    check_pingback(base_url, output_func=output_func)

def check_pingback(base_url, output_func=print):
    def out(msg):
        output_func(msg)
        sys.stdout.flush()

    url = base_url.rstrip('/') + '/xmlrpc.php'
    headers = {'Content-Type': 'text/xml'}
    payload = """<?xml version="1.0" encoding="UTF-8"?>
<methodCall>
   <methodName>pingback.ping</methodName>
   <params>
      <param><value><string>http://example.com</string></value></param>
      <param><value><string>""" + base_url + """</string></value></param>
   </params>
</methodCall>"""

    try:
        response = requests.post(url, data=payload, headers=headers, timeout=10)
        if "faultCode" in response.text and "33" in response.text:
            out(f"{YELLOW}[!] Pingback habilitado - Puede ser usado para ataques DDoS (pingback.ping){RESET}")
        elif response.status_code == 405:
            out(f"{BLUE}[-] Pingback deshabilitado - Método no permitido (405){RESET}")
        elif "faultString" in response.text:
            out(f"{BLUE}[-] Pingback parece estar deshabilitado - faultString detectado{RESET}")
        else:
            out(f"{GREEN}[+] xmlrpc.php responde pero no se detectó pingback.ping activado{RESET}")
    except requests.RequestException as e:
        out(f"{RED}[ERROR] No se pudo verificar pingback: {e}{RESET}")
