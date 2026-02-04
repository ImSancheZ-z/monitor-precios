import requests
from bs4 import BeautifulSoup
import os
import time
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

def enviar_telegram(mensaje):
    token = os.getenv('TELEGRAM_TOKEN')
    chat_id = os.getenv('TELEGRAM_CHAT_ID')
    url = f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={mensaje}"
    requests.get(url)

def get_session():
    # Creamos una sesión que reintenta la conexión si falla o tarda
    session = requests.Session()
    retry = Retry(connect=3, backoff_factor=0.5)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session

url = "https://www.elcorteingles.es/deportes/A48114055-zapatillas-de-running-de-hombre-cloudrunner-2-on/"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "es-ES,es;q=0.8",
    "Upgrade-Insecure-Requests": "1"
}

try:
    session = get_session()
    # Primero "visitamos" la home para pillar cookies (truco para parecer humano)
    session.get("https://www.elcorteingles.es/", headers=headers, timeout=10)
    time.sleep(2)
    
    # Ahora vamos al producto
    response = session.get(url, headers=headers, timeout=20)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Buscamos el botón de la talla 43 usando el patrón de tu captura
        # Buscamos el contenedor que tiene el aria-labelledby con el ID de la talla
        boton_talla = soup.find("button", {"class": lambda x: x and "size-element" in x and "veiled" in x}) or \
                      soup.find("button", {"aria-label": "43"})

        # Si el botón tiene la clase 'veiled', está agotada
        if boton_talla and "veiled" in str(boton_talla.get("class", [])):
            print("⏳ Talla 43 detectada: Sigue agotada.")
            enviar_telegram("👟 **STOCK ECI (Talla 43)**\nEstado: Sigue sin stock.")
        elif boton_talla:
            print("✅ ¡STOCK DISPONIBLE!")
            enviar_telegram(f"👟 **¡DISPONIBLES!**\nLink: {url}")
        else:
            # Si no encuentra el botón, intentamos buscar el texto plano "43" en el HTML
            if "43" in response.text:
                 print("⚠️ Encontré el texto 43 pero no el botón. Revisar.")
            else:
                 print("❌ Ni rastro de la talla.")
    else:
        print(f"❌ Error de servidor: {response.status_code}")

except Exception as e:
    print(f"Error crítico corregido: {e}")
    # No enviamos telegram aquí para no saturar si falla la red
