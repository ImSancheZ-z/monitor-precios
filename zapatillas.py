import requests
from bs4 import BeautifulSoup
import os

def enviar_telegram(mensaje):
    token = os.getenv('TELEGRAM_TOKEN')
    chat_id = os.getenv('TELEGRAM_CHAT_ID')
    url = f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={mensaje}"
    requests.get(url)

url = "https://www.elcorteingles.es/deportes/A48114055-zapatillas-de-running-de-hombre-cloudrunner-2-on/"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "es-ES,es;q=0.9"
}

try:
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    boton_talla = next((b for b in soup.find_all("button") if "43" in b.get_text()), None)
    
    if boton_talla:
        if "veiled" in str(boton_talla.get("class", [])):
            enviar_telegram("👟 **STOCK ECI (Talla 43)**\nEstado: Sigue sin haber stock disponible.")
        else:
            enviar_telegram(f"👟 **¡STOCK DISPONIBLE! (Talla 43)**\nLink: {url}")
    else:
        enviar_telegram("⚠️ **AVISO ECI**\nNo se localiza el botón de la talla 43.")
except Exception as e:
    print(f"Error ECI: {e}")
