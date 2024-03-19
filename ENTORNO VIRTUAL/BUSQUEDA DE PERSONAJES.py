import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLabel, QLineEdit, QListWidget, QMessageBox, QListWidgetItem, QHBoxLayout, QDialog, QTextBrowser, QComboBox
from PyQt6.QtGui import QPixmap
import requests
import hashlib
import webbrowser
import urllib.parse
from bs4 import BeautifulSoup

API_PUBLIC_KEY = '77cd9227f30d31a1e8a6e54a7d12658b'
API_PRIVATE_KEY = '184b87f35ab3b8d461ef993c5b782d0001237fea'

class MarvelAPI:
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
    def __init__(self, character_details, comic_images, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Detalles del Personaje")
        self.setGeometry(200, 200, 600, 400)

        layout = QVBoxLayout()
        self.setLayout(layout)

        detail_text = QTextBrowser()
        detail_text.setOpenExternalLinks(True)
        detail_text.setHtml(character_details)
        layout.addWidget(detail_text)

        comic_text = QComboBox()
        for comic in comic_images:
            comic_text.addItem(comic['title'], userData=comic['resourceURI'])
        layout.addWidget(comic_text)

        open_button = QPushButton("Abrir")
        open_button.clicked.connect(lambda: self.open_comic(comic_text.currentData()))
        layout.addWidget(open_button)

        # Agregar lista de cómics y eventos debajo de la descripción
        comics_list = "<h3>Comics:</h3><ul>"
        for comic in comic_images:
            comics_list += f"<li>{comic['title']}</li>"
        comics_list += "</ul>"
        detail_text.append(comics_list)

    def open_comic(self, comic_url):
        api = MarvelAPI()
        cover_url = api.get_comic_cover(comic_url)
        if cover_url:
            webbrowser.open(cover_url)
        else:
            QMessageBox.information(self, "Portada del Cómic", "No se encontró la portada del cómic.")

class MainWindow(QMainWindow):
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
        button_layout.addWidget(prev_button)

        next_button = QPushButton("Siguiente")
        next_button.clicked.connect(self.on_next_button_click)
        button_layout.addWidget(next_button)

        sort_button = QPushButton("Ordenar por Nombre")
        sort_button.clicked.connect(self.on_sort_button_click)
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

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
