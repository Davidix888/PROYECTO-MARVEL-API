import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLabel, QLineEdit, QListWidget, QMessageBox, QListWidgetItem, QHBoxLayout, QDialog, QTextBrowser, QComboBox
from PyQt6.QtGui import QPixmap
import requests
import hashlib
import webbrowser
import urllib.parse
from bs4 import BeautifulSoup

LLAVE_PUBLICA_API = '77cd9227f30d31a1e8a6e54a7d12658b'
LLAVE_PRIVADA_API = '184b87f35ab3b8d461ef993c5b782d0001237fea'

class MarvelAPI:
    def __init__(self):
        self.base_url = 'https://gateway.marvel.com/v1/public/'

    def obtener_parametros_autenticacion(self):
        ts = '1'
        valor_hash = hashlib.md5((ts + LLAVE_PRIVADA_API + LLAVE_PUBLICA_API).encode('utf-8')).hexdigest()
        return {'ts': ts, 'apikey': LLAVE_PUBLICA_API, 'hash': valor_hash}

    def obtener_personajes(self, offset=0, limite=10, ordenar_por='name'):
        url = f"{self.base_url}characters"
        parametros = self.obtener_parametros_autenticacion()
        parametros['limit'] = limite
        parametros['offset'] = offset
        parametros['orderBy'] = ordenar_por

        respuesta = requests.get(url, params=parametros)
        datos = respuesta.json()

        if datos['code'] == 200:
            return datos['data']['results']
        else:
            print("Error al obtener los personajes:", datos['status'])

    def buscar_personajes(self, nombre=None, creador=None):
        url = f"{self.base_url}characters"
        parametros = self.obtener_parametros_autenticacion()
        if nombre:
            parametros['nameStartsWith'] = nombre
        if creador:
            parametros['creator'] = creador

        respuesta = requests.get(url, params=parametros)
        datos = respuesta.json()

        if datos['code'] == 200:
            return datos['data']['results']
        else:
            print("Error al buscar los personajes:", datos['status'])

    def obtener_detalles_personaje(self, id_personaje):
        url = f"{self.base_url}characters/{id_personaje}"
        parametros = self.obtener_parametros_autenticacion()

        respuesta = requests.get(url, params=parametros)
        datos = respuesta.json()

        if datos['code'] == 200:
            return datos['data']['results'][0]
        else:
            print("Error al obtener los detalles del personaje:", datos['status'])

    def obtener_portada_comic(self, url_comic):
        parametros = self.obtener_parametros_autenticacion()
        respuesta = requests.get(url_comic, params=parametros)
        datos = respuesta.json()

        if datos['code'] == 200:
            datos_comic = datos['data']['results'][0]
            return datos_comic['thumbnail']['path'] + '.' + datos_comic['thumbnail']['extension']
        else:
            print("Error al obtener la portada del cómic:", datos['status'])

class VentanaDetallePersonaje(QDialog):
    def __init__(self, detalles_personaje, imagenes_comic, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Detalles del Personaje")
        self.setGeometry(200, 200, 600, 400)

        diseño = QVBoxLayout()
        self.setLayout(diseño)

        texto_detalles = QTextBrowser()
        texto_detalles.setOpenExternalLinks(True)
        texto_detalles.setHtml(detalles_personaje)
        diseño.addWidget(texto_detalles)

        lista_comics = QComboBox()
        for comic in imagenes_comic:
            lista_comics.addItem(comic['title'], userData=comic['resourceURI'])
        diseño.addWidget(lista_comics)

        boton_abrir = QPushButton("Abrir")
        boton_abrir.clicked.connect(lambda: self.abrir_comic(lista_comics.currentData()))
        diseño.addWidget(boton_abrir)

        lista_comics_html = "<h3>Comics:</h3><ul>"
        for comic in imagenes_comic:
            lista_comics_html += f"<li>{comic['title']}</li>"
        lista_comics_html += "</ul>"
        texto_detalles.append(lista_comics_html)

    def abrir_comic(self, url_comic):
        api = MarvelAPI()
        url_portada = api.obtener_portada_comic(url_comic)
        if url_portada:
            webbrowser.open(url_portada)
        else:
            QMessageBox.information(self, "Portada del Cómic", "No se encontró la portada del cómic.")

class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()

        self.api = MarvelAPI()
        self.personajes = []
        self.offset_actual = 0
        self.limite = 10
        self.ordenar_por = 'name'
        self.buscar_nombre = None
        self.buscar_creador = None

        self.setWindowTitle("Visor de Personajes de Marvel Comics")
        self.setGeometry(100, 100, 800, 600)

        self.widget_central = QWidget()
        self.setCentralWidget(self.widget_central)

        diseño = QVBoxLayout()
        self.widget_central.setLayout(diseño)

        self.crear_barra_busqueda()
        self.crear_botones()
        self.crear_lista_personajes()

        self.actualizar_lista_personajes()

    def crear_barra_busqueda(self):
        diseño_busqueda = QHBoxLayout()
        diseño_busqueda.addWidget(QLabel("Buscar por nombre:"))
        self.nombre_entrada = QLineEdit()
        self.nombre_entrada.setPlaceholderText("Buscar por nombre")
        self.nombre_entrada.textChanged.connect(self.al_cambiar_nombre)
        diseño_busqueda.addWidget(self.nombre_entrada)

        diseño_busqueda.addWidget(QLabel("Buscar por creador:"))
        self.creador_entrada = QLineEdit()
        self.creador_entrada.setPlaceholderText("Buscar por creador")
        self.creador_entrada.textChanged.connect(self.al_cambiar_creador)
        diseño_busqueda.addWidget(self.creador_entrada)

        boton_buscar = QPushButton("Buscar")
        boton_buscar.clicked.connect(self.al_hacer_clic_buscar)
        diseño_busqueda.addWidget(boton_buscar)

        diseño = QVBoxLayout()
        diseño.addLayout(diseño_busqueda)
        self.widget_central.setLayout(diseño)

    def crear_botones(self):
        diseño_botones = QHBoxLayout()

        boton_anterior = QPushButton("Anterior")
        boton_anterior.clicked.connect(self.al_hacer_clic_anterior)
        diseño_botones.addWidget(boton_anterior)

        boton_siguiente = QPushButton("Siguiente")
        boton_siguiente.clicked.connect(self.al_hacer_clic_siguiente)
        diseño_botones.addWidget(boton_siguiente)

        boton_ordenar = QPushButton("Ordenar por Nombre")
        boton_ordenar.clicked.connect(self.al_hacer_clic_ordenar)
        diseño_botones.addWidget(boton_ordenar)

        diseño = QVBoxLayout()
        diseño.addLayout(diseño_botones)
        self.widget_central.setLayout(diseño)

    def crear_lista_personajes(self):
        self.lista_personajes = QListWidget()
        self.lista_personajes.itemDoubleClicked.connect(self.al_hacer_doble_clic_personaje)
        diseño = QVBoxLayout()
        diseño.addWidget(self.lista_personajes)
        self.widget_central.setLayout(diseño)

    def actualizar_lista_personajes(self):
        self.lista_personajes.clear()
        for personaje in self.personajes:
            item = QListWidgetItem(personaje['name'])
            item.setData(1, personaje['id'])
            self.lista_personajes.addItem(item)

    def actualizar_parametros_busqueda(self):
        self.buscar_nombre = self.nombre_entrada.text() or None
        self.buscar_creador = self.creador_entrada.text() or None

    def al_cambiar_nombre(self, texto):
        self.actualizar_parametros_busqueda()

    def al_cambiar_creador(self, texto):
        self.actualizar_parametros_busqueda()

    def al_hacer_clic_buscar(self):
        self.offset_actual = 0
        self.actualizar_parametros_busqueda()
        self.personajes = self.api.buscar_personajes(nombre=self.buscar_nombre, creador=self.buscar_creador)
        self.actualizar_lista_personajes()

    def al_hacer_clic_anterior(self):
        if self.offset_actual - self.limite >= 0:
            self.offset_actual -= self.limite
            self.personajes = self.api.obtener_personajes(offset=self.offset_actual, limite=self.limite, ordenar_por=self.ordenar_por)
            self.actualizar_lista_personajes()

    def al_hacer_clic_siguiente(self):
        self.offset_actual += self.limite
        self.personajes = self.api.obtener_personajes(offset=self.offset_actual, limite=self.limite, ordenar_por=self.ordenar_por)
        self.actualizar_lista_personajes()

    def al_hacer_clic_ordenar(self):
        if self.ordenar_por == 'name':
            self.ordenar_por = 'modified'
        else:
            self.ordenar_por = 'name'
        self.offset_actual = 0
        self.personajes = self.api.obtener_personajes(offset=self.offset_actual, limite=self.limite, ordenar_por=self.ordenar_por)
        self.actualizar_lista_personajes()

    def al_hacer_doble_clic_personaje(self, item):
        id_personaje = item.data(1)
        detalles_personaje = self.api.obtener_detalles_personaje(id_personaje)
        if detalles_personaje:
            mensaje_detalles = f"<h2>Nombre: {detalles_personaje['name']}</h2>"
            mensaje_detalles += f"<p>Descripción: {detalles_personaje['description']}</p>"

            comics = detalles_personaje.get('comics', {}).get('items', [])
            datos_comics = []
            for comic in comics:
                datos_comics.append({
                    'title': comic['name'],
                    'resourceURI': comic['resourceURI']
                })

            if datos_comics:
                ventana_comic = VentanaDetallePersonaje(mensaje_detalles, datos_comics)
                ventana_comic.exec()
            else:
                QMessageBox.information(self, "Cómics", "No hay cómics disponibles para este personaje.")
        else:
            QMessageBox.warning(self, "Error", "No se pudo obtener los detalles del personaje.")

def main():
    app = QApplication(sys.argv)
    ventana = VentanaPrincipal()
    ventana.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
