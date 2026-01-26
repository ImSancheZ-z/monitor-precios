import requests
from bs4 import BeautifulSoup
import os

def enviar_telegram(mensaje):
    token = os.getenv('TELEGRAM_TOKEN')
    chat_id = os.getenv('TELEGRAM_CHAT_ID')
    url = f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={mensaje}"
    requests.get(url)

def check_precio():
    url = "https://es.alpinestars.com/products/andes-v3-drystar-jacket-dark-blue-black?variant=48380228993359"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Selector exacto para la web de Alpinestars
        precio_elem = soup.find("span", class_="price-item--sale")
        
        if precio_elem:
            # Limpiamos el texto: quitamos '€', espacios y cambiamos coma por punto
            precio_texto = precio_elem.text.strip().replace('€', '').replace(',', '.').strip()
            precio_actual = float(precio_texto)
            
            print(f"Precio detectado: {precio_actual}€")
            
            # CONFIGURACIÓN: Si baja de 230€, avísame (puedes cambiar este número)
            if precio_actual < 230.00:
                enviar_telegram(f"📉 ¡OJO! Bajada de precio en Alpinestars: {precio_actual}€\nLink: {url}")
        else:
            print("No se encontró el elemento del precio.")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_precio()
