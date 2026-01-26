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
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Usamos el selector exacto que encontraste en el inspector
        # Buscamos la etiqueta <dd> con esa clase específica
        precio_elem = soup.find("dd", class_="price__item--sale")
        
        if precio_elem:
            # Limpiamos el texto para quedarnos solo con el número
            # Quitamos el símbolo €, espacios y cambiamos la coma por punto
            texto_sucio = precio_elem.get_text().strip()
            precio_texto = "".join(filter(lambda x: x.isdigit() or x == ',', texto_sucio)).replace(',', '.')
            precio_actual = float(precio_texto)
            
            print(f"✅ ¡Conseguido! Precio detectado: {precio_actual}€")
            
            # Ponemos el aviso en 300€ para que te llegue el mensaje de prueba YA
            if precio_actual < 300.00:
                enviar_telegram(f"📉 ¡Bajada de precio! La chaqueta Alpinestars está a {precio_actual}€\nLink: {url}")
        else:
            print("❌ Seguimos sin encontrar el elemento. Revisa si la clase ha cambiado.")
            
    except Exception as e:
        print(f"Error técnico: {e}")

if __name__ == "__main__":
    check_precio()
