import requests
from bs4 import BeautifulSoup
import os

def enviar_telegram(mensaje):
    token = os.getenv('TELEGRAM_TOKEN')
    chat_id = os.getenv('TELEGRAM_CHAT_ID')
    url = f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={mensaje}"
    requests.get(url)

def check_alpinestars():
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
            
            print(f"✅ Alpinestars: {precio_actual}€")
            # Te avisará si baja de 230€
            if precio_actual < 230.00:
                enviar_telegram(f"📉 ¡Bajada de precio! La chaqueta Alpinestars está a {precio_actual}€\nLink: {url}")
    except Exception as e:
        print(f"Error en Alpinestars: {e}")

def check_zapatillas_eci():
    url = "https://www.elcorteingles.es/deportes/A48114055-zapatillas-de-running-de-hombre-cloudrunner-2-on/"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}
    
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Buscamos el botón de la talla 43 basándonos en tu captura del inspector
        boton_talla = soup.find("button", {"aria-label": "43"})
        
        if boton_talla:
            clases = boton_talla.get("class", [])
            if "veiled" not in clases:
                print("✅ ¡STOCK DISPONIBLE en ECI!")
                enviar_telegram(f"👟 ¡STOCK DETECTADO! La talla 43 de las On Cloudrunner 2 ya se puede comprar.\nLink: {url}")
            else:
                print("⏳ Talla 43 sigue 'veiled' (agotada).")
                # LÍNEA DE PRUEBA: Borra o comenta la siguiente línea tras recibir el mensaje
                enviar_telegram("⏳ Bot activo: En las On Cloudrunner talla 43 sigue sin haber stock.")
        else:
            print("❌ No se encontró el botón de la talla 43.")
            
    except Exception as e:
        print(f"Error en El Corte Inglés: {e}")

if __name__ == "__main__":
    print("Iniciando rastreo...")
    check_alpinestars()
    check_zapatillas_eci()
    print("Rastreo finalizado.")
