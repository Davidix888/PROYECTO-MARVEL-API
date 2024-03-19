import sys
import hashlib
import requests
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLabel, QLineEdit, QListWidget, QListWidgetItem, QHBoxLayout, QDialog, QTextBrowser, QComboBox, QMessageBox, QScrollArea
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
API_PUBLIC_KEY = '77cd9227f30d31a1e8a6e54a7d12658b'
API_PRIVATE_KEY = '184b87f35ab3b8d461ef993c5b782d0001237fea'

class MarvelAPI:
    # Definición de la clase MarvelAPI
    def __init__(self):
        self.base_url = 'https://gateway.marvel.com/v1/public/'

    def get_auth_params(self):
        ts = '1'
        hash_value = hashlib.md5((ts + API_PRIVATE_KEY + API_PUBLIC_KEY).encode('utf-8')).hexdigest()
        return {'ts': ts, 'apikey': API_PUBLIC_KEY, 'hash': hash_value}

    def get_characters(self, offset=0, limit=10, order_by='name'):
        url = f"{self.base_url}characters"
        params = self.get_auth_params()
        params['limit'] = limit
        params['offset'] = offset
        params['orderBy'] = order_by

        response = requests.get(url, params=params)
        data = response.json()

        if data['code'] == 200:
            return data['data']['results']
        else:
            print("Error al obtener los personajes:", data['status'])

    def search_characters(self, name=None, creator=None):
        url = f"{self.base_url}characters"
        params = self.get_auth_params()
        if name:
            params['nameStartsWith'] = name
        if creator:
            params['creator'] = creator

        response = requests.get(url, params=params)
        data = response.json()

        if data['code'] == 200:
            return data['data']['results']
        else:
            print("Error al buscar los personajes:", data['status'])

    def get_character_details(self, character_id):
        url = f"{self.base_url}characters/{character_id}"
        params = self.get_auth_params()

        response = requests.get(url, params=params)
        data = response.json()

        if data['code'] == 200:
            return data['data']['results'][0]
        else:
            print("Error al obtener los detalles del personaje:", data['status'])

    def get_comic_cover(self, comic_url):
        params = self.get_auth_params()
        response = requests.get(comic_url, params=params)
        data = response.json()

        if data['code'] == 200:
            comic_data = data['data']['results'][0]
            return comic_data['thumbnail']['path'] + '.' + comic_data['thumbnail']['extension']
        else:
            print("Error al obtener la portada del cómic:", data['status'])


class CharacterPopup(QDialog):
    # Definición de la clase CharacterPopup
    def __init__(self, character_details, comic_images, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Detalles del Personaje")
        self.setGeometry(200, 200, 600, 400)

        layout = QVBoxLayout()
        self.setLayout(layout)

        scroll_area = QScrollArea()
        layout.addWidget(scroll_area)

        content_widget = QWidget()
        scroll_area.setWidget(content_widget)
        scroll_area.setWidgetResizable(True)

        detail_layout = QVBoxLayout(content_widget)
        detail_layout.setContentsMargins(0, 0, 0, 0)

        detail_text = QTextBrowser()
        detail_text.setOpenExternalLinks(True)
        detail_text.setHtml(character_details)
        detail_layout.addWidget(detail_text)

        comic_text = QComboBox()
        for comic in comic_images:
            comic_text.addItem(comic['title'], userData=comic['resourceURI'])
        detail_layout.addWidget(comic_text)

        open_button = QPushButton("Abrir")
        open_button.clicked.connect(lambda: self.open_comic(comic_text.currentData()))
        detail_layout.addWidget(open_button)

        self.label = QLabel()
        detail_layout.addWidget(self.label)

        comics_list = "<h3>Comics:</h3><ul>"
        for comic in comic_images:
            comics_list += f"<li>{comic['title']}</li>"
        comics_list += "</ul>"
        detail_text.append(comics_list)

    def open_comic(self, comic_url):
        api = MarvelAPI()
        cover_url = api.get_comic_cover(comic_url)
        if cover_url:
            response = requests.get(cover_url)
            if response.ok:
                pixmap = QPixmap()
                pixmap.loadFromData(response.content)
                if not pixmap.isNull():
                    self.label.setPixmap(pixmap)
                    self.label.setWindowTitle("Portada del Cómic")
                    self.label.show()
                else:
                    QMessageBox.information(self, "Portada del Cómic", "La imagen de la portada del cómic está vacía.")
            else:
                QMessageBox.information(self, "Portada del Cómic", f"No se pudo obtener la portada del cómic. Código de estado: {response.status_code}")
        else:
            QMessageBox.information(self, "Portada del Cómic", "No se encontró la portada del cómic.")



class MainWindow(QMainWindow):
    # Definición de la clase MainWindow
    def __init__(self):
        super().__init__()

        self.api = MarvelAPI()
        self.characters = []
        self.current_offset = 0
        self.limit = 10
        self.order_by = 'name'
        self.search_name = None
        self.search_creator = None

        self.setWindowTitle("Marvel Comics Character Viewer")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.custom_button = QPushButton("MARVEL")
        self.custom_button.setStyleSheet("background-color: #FF0000; color: #FFFFFF; border: none; padding: 10px 20px; font-size: 16px;")
        self.layout.addWidget(self.custom_button)

        self.create_search_bar()
        self.create_buttons()
        self.create_character_list()

        self.update_character_list()

    def create_search_bar(self):
        search_layout = QHBoxLayout()
        self.layout.addLayout(search_layout)

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Buscar por nombre")
        self.name_input.textChanged.connect(self.on_name_input_change)
        search_layout.addWidget(self.name_input)

        self.creator_input = QLineEdit()
        self.creator_input.setPlaceholderText("Buscar por creador")
        self.creator_input.textChanged.connect(self.on_creator_input_change)
        search_layout.addWidget(self.creator_input)

        search_button = QPushButton("Buscar")
        search_button.clicked.connect(self.on_search_button_click)
        search_layout.addWidget(search_button)

    def create_buttons(self):
        button_layout = QHBoxLayout()
        self.layout.addLayout(button_layout)

        prev_button = QPushButton("Anterior")
        prev_button.clicked.connect(self.on_prev_button_click)
        prev_button.setStyleSheet("background-color: #FF0000; color: #FFFFFF; border: none; padding: 10px 20px; font-size: 16px;font-family: 'Comic Sans MS', sans-serif;;")
        button_layout.addWidget(prev_button)

        next_button = QPushButton("Siguiente")
        next_button.clicked.connect(self.on_next_button_click)
        next_button.setStyleSheet("background-color: #FF0000; color: #FFFFFF; border: none; padding: 10px 20px; font-size: 16px;")
        button_layout.addWidget(next_button)

        sort_button = QPushButton("Ordenar por Nombre")
        sort_button.clicked.connect(self.on_sort_button_click)
        sort_button.setStyleSheet("background-color: #FF0000; color: #FFFFFF; border: none; padding: 10px 20px; font-size: 16px;")
        button_layout.addWidget(sort_button)


    def create_character_list(self):
        self.list_widget = QListWidget()
        self.list_widget.itemDoubleClicked.connect(self.on_character_double_clicked)
        self.layout.addWidget(self.list_widget)

    def update_character_list(self):
        self.list_widget.clear()
        for character in self.characters:
            item = QListWidgetItem(character['name'])
            item.setData(1, character['id'])
            self.list_widget.addItem(item)

    def update_search_params(self):
        self.search_name = self.name_input.text() or None
        self.search_creator = self.creator_input.text() or None

    def on_name_input_change(self, text):
        self.update_search_params()

    def on_creator_input_change(self, text):
        self.update_search_params()

    def on_search_button_click(self):
        self.current_offset = 0
        self.update_search_params()
        self.characters = self.api.search_characters(name=self.search_name, creator=self.search_creator)
        self.update_character_list()

    def on_prev_button_click(self):
        if self.current_offset - self.limit >= 0:
            self.current_offset -= self.limit
            self.characters = self.api.get_characters(offset=self.current_offset, limit=self.limit, order_by=self.order_by)
            self.update_character_list()

    def on_next_button_click(self):
        self.current_offset += self.limit
        self.characters = self.api.get_characters(offset=self.current_offset, limit=self.limit, order_by=self.order_by)
        self.update_character_list()

    def on_sort_button_click(self):
        if self.order_by == 'name':
            self.order_by = 'modified'
        else:
            self.order_by = 'name'
        self.current_offset = 0
        self.characters = self.api.get_characters(offset=self.current_offset, limit=self.limit, order_by=self.order_by)
        self.update_character_list()

    def on_character_double_clicked(self, item):
        character_id = item.data(1)
        character_details = self.api.get_character_details(character_id)
        if character_details:
            detail_message = f"<h2>Nombre: {character_details['name']}</h2>"
            detail_message += f"<p>Descripción: {character_details['description']}</p>"

            comics = character_details.get('comics', {}).get('items', [])
            comics_data = []
            for comic in comics:
                comics_data.append({
                    'title': comic['name'],
                    'resourceURI': comic['resourceURI']
                })

            if comics_data:
                comic_popup = CharacterPopup(detail_message, comics_data)
                comic_popup.exec()
            else:
                QMessageBox.information(self, "Cómics", "No hay cómics disponibles para este personaje.")
        else:
            QMessageBox.warning(self, "Error", "No se pudo obtener los detalles del personaje.")



class PantallaInicio(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.ventana_personajes = None

    def initUI(self):
        self.resize(600, 400)  
        self.setWindowTitle('Pantalla de Inicio')
        self.setStyleSheet("background-color: #808080;")
        layout = QVBoxLayout()
        
        imagen_encabezado = QLabel(self)
        imagen_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/6/63/Marvel_Studios_logo.svg/2560px-Marvel_Studios_logo.svg.png"
        imagen_data = requests.get(imagen_url).content
        imagen_pixmap = QPixmap()
        imagen_pixmap.loadFromData(imagen_data)
        imagen_pixmap = imagen_pixmap.scaledToHeight(200)  
        imagen_encabezado.setPixmap(imagen_pixmap)
        imagen_encabezado.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(imagen_encabezado)
        
        self.btn_personajes = QPushButton('Personajes', self)
        self.btn_personajes.setStyleSheet("background-color: red;")  
        self.btn_personajes.clicked.connect(self.mostrar_personajes)
        layout.addWidget(self.btn_personajes)
        
        self.btn_comics = QPushButton('Comics', self)
        self.btn_comics.setStyleSheet("background-color: red;")  
        self.btn_comics.clicked.connect(self.mostrar_comics)
        layout.addWidget(self.btn_comics)
        
        self.setLayout(layout)

    def mostrar_personajes(self):
       if self.ventana_personajes is None:
            self.ventana_personajes = MainWindow()
            self.ventana_personajes.show()

    def mostrar_comics(self):
        if self.ventana_comics is None:
            self.ventana_comics = MainWindow()
            self.ventana_comics.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ventana = PantallaInicio()
    ventana.show()
    sys.exit(app.exec())

