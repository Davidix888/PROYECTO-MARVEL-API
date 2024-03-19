#Consumir API
import requests
import json
from pprint import pprint
ts = 1
private_key = "d0d3897f351a05612129a56a28fab348d45c99aa"
public_key = "058bfc8399d452e011be32a08c89ec22"
#1d0d3897f351a05612129a56a28fab348d45c99aa058bfc8399d452e011be32a08c89ec22
hashed = "3073884984e0024a395fbffbaf61f594"
url = f"http://gateway.marvel.com/v1/public/comics?ts={ts}&apikey={public_key}&hash={hashed}"
lista = []
response = requests.get(url)

if response.status_code == 200:
    response_json = response.json()
    
    for i in response_json["data"]["results"]:
        nombre = i["title"]
        descripcion = i["description"]
        
        # Verificar si "comics" y "series" están presentes antes de acceder a sus valores
        comics_disponibles = i.get("comics", {}).get("available", "No disponible")
        series_disponibles = i.get("series", {}).get("available", "No disponible")
        
        dic = {"nombre": nombre, "descripcion": descripcion, "comics disponibles": comics_disponibles, "series disponibles": series_disponibles}
        lista.append(dic)

    print(f"Se encontraron {len(lista)} resultados.")
    
    # Preguntar al usuario si desea ver los datos
    mostrar_datos = input("¿Desea ver los datos? (s/n): ")
    if mostrar_datos.lower() == "s":
        pprint(lista)
else:
    print("Error al hacer la solicitud. Código de estado:", response.status_code)


