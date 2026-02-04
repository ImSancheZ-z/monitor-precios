import requests
from bs4 import BeautifulSoup
import os
import time

def enviar_telegram(mensaje):
    token = os.getenv('TELEGRAM_TOKEN')
    chat_id = os.getenv('TELEGRAM_CHAT_ID')
    url = f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={mensaje}"
    requests.get(url)

url = "https://www.elcorteingles.es/deportes/A48114055-zapatillas-de-running-de-hombre-cloudrunner-2-on/"

# 1. MEJORA: Headers mucho más realistas para evitar bloqueos
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
    "Accept-Language": "es-ES,es;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Referer": "https://www.google.com/"
}

try:
    # 2. MEJORA: Un pequeño retraso para no ser tan agresivos
    time.sleep(2)
    response = requests.get(url, headers=headers, timeout=15)
    
    if response.status_code != 200:
        print(f"❌ Error de acceso (Status {response.status_code})")
        # Si recibes un 403, es que ECI nos ha bloqueado por hoy
        if response.status_code == 403:
            enviar_telegram("⚠️ ECI ha bloqueado el acceso del bot temporalmente.")
        exit()

    soup = BeautifulSoup(response.text, 'html.parser')
    
    # 3. MEJORA: Buscamos la talla 43 de forma más profunda
    # Buscamos en botones o spans que contengan exactamente "43"
    boton_talla = None
    elementos_talla = soup.find_all(["button", "span", "div"], string=lambda t: t and "43" in t)
    
    # Si no lo encuentra por texto, buscamos por el atributo que vimos en tu captura
    if not elementos_talla:
        boton_talla = soup.find("button", {"class": lambda x: x and "size-element" in x and "43" in str(x)})
    else:
        # Cogemos el primer elemento que parezca un botón de talla
        boton_talla = elementos_talla[0]

    if boton_talla:
        # Comprobamos si el botón o su contenedor tienen la clase 'veiled'
        html_boton = str(boton_talla.parent) + str(boton_talla)
        
        if "veiled" in html_boton:
            print("⏳ Talla 43 detectada pero AGOTADA.")
            enviar_telegram("👟 **STOCK ECI (Talla 43)**\nEstado: Sigue agotada.")
        else:
            print("✅ ¡STOCK DISPONIBLE!")
            enviar_telegram(f"👟 **¡STOCK DISPONIBLE! (Talla 43)**\nLink: {url}")
    else:
        print("❌ No se encontró el botón 43.")
        # Esto nos avisará si la estructura de la web ha cambiado mucho
        enviar_telegram("⚠️ No he podido localizar la talla 43. Puede que la web haya cambiado de diseño.")

except Exception as e:
    print(f"Error crítico: {e}")
