import requests

def detect_cms(url):
    try:
        resp = requests.get(url, timeout=10, allow_redirects=True)
        headers = resp.headers
        content = resp.text.lower()

        if "wp-content" in content or "wp-json" in content or "wordpress" in headers.get("X-Generator", "").lower():
            return "WordPress"
        elif "joomla" in content or "joomla" in headers.get("X-Generator", "").lower():
            return "Joomla"
        elif "drupal" in content or "drupal-settings-json" in content:
            return "Drupal"
        else:
            return "Desconocido"
    except Exception as e:
        print(f"[!] Error al detectar CMS: {e}")
        return "Desconocido"

def load_payloads(cms_name):
    try:
        with open(f"payloads/{cms_name.lower()}.txt", "r") as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"[-] Archivo payloads/{cms_name.lower()}.txt no encontrado.")
        return []
