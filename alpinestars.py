import requests
from bs4 import BeautifulSoup
import os

def enviar_telegram(mensaje):
    token = os.getenv('TELEGRAM_TOKEN')
    chat_id = os.getenv('TELEGRAM_CHAT_ID')
    url = f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={mensaje}"
    requests.get(url)

url = "https://es.alpinestars.com/products/andes-v3-drystar-jacket-dark-blue-black?variant=48380228993359"
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}

try:
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    precio_elem = soup.find("dd", class_="price__item--sale")
    if precio_elem:
        texto_sucio = precio_elem.get_text().strip()
        precio_texto = "".join(filter(lambda x: x.isdigit() or x == ',', texto_sucio)).replace(',', '.')
        precio_actual = float(precio_texto)
        if precio_actual < 210.00:
            enviar_telegram(f"🧥 **OFERTA ALPINESTARS**\nPrecio: {precio_actual}€\nLink: {url}")
except Exception as e:
    print(f"Error Alpinestars: {e}")
