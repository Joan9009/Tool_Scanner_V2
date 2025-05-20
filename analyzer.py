def analyze_response(url, response, cms):
    status = response.status_code
    print(f"[{status}] {url}")

    if cms == "WordPress":
        if "/wp-json" in url and status == 200 and "routes" in response.text:
            print("[!] API REST habilitada - Posible enumeración de usuarios.")
        if "wp-content/plugins" in url and "Index of" in response.text:
            print("[!] Plugins expuestos - Directorio sin proteger.")
        if "wp-config.php.bak" in url and "DB_NAME" in response.text:
            print("[!!!] ¡Archivo de configuración filtrado!")
        if "/readme.html" in url and "WordPress" in response.text:
            version = extract_version(response.text)
            if version:
                print(f"[+] Versión detectada: WordPress {version}")

def extract_version(text):
    import re
    match = re.search(r'Version (\d+\.\d+(\.\d+)?)', text)
    return match.group(1) if match else None
