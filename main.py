import requests
from bs4 import BeautifulSoup
import os

def enviar_telegram(mensaje):
    token = os.getenv('TELEGRAM_TOKEN')
    chat_id = os.getenv('TELEGRAM_CHAT_ID')
    url = f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={mensaje}"
    requests.get(url)

def check_zapatillas_eci():
    url = "https://www.elcorteingles.es/deportes/A48114055-zapatillas-de-running-de-hombre-cloudrunner-2-on/"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}
    
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Buscamos el contenedor de la talla 43 usando el ID que sale en tu captura
        # El ID parece ser dinámico, así que buscamos por el atributo aria-label que suele tener la talla
        boton_talla = soup.find("button", {"aria-label": "43"}) or soup.select_one('button[class*="size-element"]')
        
        # Basándonos en tu captura, el botón tiene la clase "veiled" cuando no hay stock
        if boton_talla:
            clases = boton_talla.get("class", [])
            if "veiled" not in clases:
                print("✅ ¡STOCK DISPONIBLE!")
                enviar_telegram(f"👟 ¡CORRE! La talla 43 de las On Cloudrunner 2 ya está disponible en ECI.\n{url}")
            else:
                print("⏳ Talla 43 sigue 'veiled' (agotada).")
    except Exception as e:
        print(f"Error en ECI: {e}")

def check_alpinestars():
    # Tu código anterior de Alpinestars
    url = "https://es.alpinestars.com/products/andes-v3-drystar-jacket-dark-blue-black?variant=48380228993359"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        r = requests.get(url, headers=headers)
        soup = BeautifulSoup(r.text, 'html.parser')
        precio_elem = soup.find("dd", class_="price__item--sale")
        if precio_elem:
            precio = float(precio_elem.get_text().strip().replace('€', '').replace(',', '.').strip())
            if precio < 230:
                enviar_telegram(f"🧥 Alpinestars rebajada: {precio}€\n{url}")
    except:
        print("Error en Alpinestars")

if __name__ == "__main__":
    check_alpinestars()
    check_zapatillas_eci()
