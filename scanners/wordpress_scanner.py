import requests
import sys

GRAY = "\033[90m"
RESET = "\032[91m"

def scan_wordpress(base_url, paths_file='payloads/wordpress.txt', output_func=print):
    def out(msg):
        output_func(msg)
        sys.stdout.flush()

    out(f"\n--- Escaneo de Vulnerabilidades WordPress ---\n")

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
                if 'wp-json' in full_url:
                    out(f"[!] {full_url}")
                    out(f"[!] API REST habilitada - Posible enumeración de usuarios.")
                elif 'wp-content/plugins' in full_url:
                    out(f"[!] {full_url}")
                    out(f"[!] Plugins visibles - Riesgo de enumeración.")
                elif 'wp-config.php.bak' in full_url:
                    out(f"[!] {full_url}")
                    out(f"[!] Archivo de configuración de respaldo accesible - ¡ALTO RIESGO!")
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
                out(f"[404] {full_url} - No encontrado (puede ser seguro o no expuesto)")
            else:
                out(f"[{status}] {full_url}")

        except requests.RequestException as e:
            out(f"[ERROR] No se pudo conectar a {full_url} - {e}")

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
            out(f"[!] Pingback habilitado - Puede ser usado para ataques DDoS (pingback.ping)")
        elif response.status_code == 405:
            out(f"[-] Pingback deshabilitado - Método no permitido (405)")
        elif "faultString" in response.text:
            out(f"[-] Pingback parece estar deshabilitado - faultString detectado")
        else:
            out(f"[+] xmlrpc.php responde pero no se detectó pingback.ping activado")
    except requests.RequestException as e:
        out(f"[ERROR] No se pudo verificar pingback: {e}")
