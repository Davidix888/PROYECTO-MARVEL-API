import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLabel, QLineEdit, QListWidget, QMessageBox, QListWidgetItem, QHBoxLayout, QDialog, QTextBrowser, QScrollArea
from PyQt6.QtGui import QPixmap
import requests
import hashlib

API_PUBLIC_KEY = '77cd9227f30d31a1e8a6e54a7d12658b'
API_PRIVATE_KEY = '184b87f35ab3b8d461ef993c5b782d0001237fea'

class MarvelAPI:
    def __init__(self):
        self.base_url = 'https://gateway.marvel.com/v1/public/'

    def get_auth_params(self):
        ts = '1'
        hash_value = hashlib.md5((ts + API_PRIVATE_KEY + API_PUBLIC_KEY).encode('utf-8')).hexdigest()
        return {'ts': ts, 'apikey': API_PUBLIC_KEY, 'hash': hash_value}

    def get_comics(self, offset=0, limit=10, order_by='title', title=None, year=None):
        url = f"{self.base_url}comics"
        params = self.get_auth_params()
        params['limit'] = limit
        params['offset'] = offset
        params['orderBy'] = order_by
        if title:
            params['titleStartsWith'] = title
        if year:
            params['startYear'] = year

        response = requests.get(url, params=params)
        data = response.json()

        if data['code'] == 200:
            return data['data']['results']
        else:
            print("Error al obtener los cómics:", data['status'])

    def get_comic_details(self, comic_id):
        url = f"{self.base_url}comics/{comic_id}"
        params = self.get_auth_params()

        response = requests.get(url, params=params)
        data = response.json()

        if data['code'] == 200:
            return data['data']['results'][0]
        else:
            print("Error al obtener los detalles del cómic:", data['status'])

class ComicDetailDialog(QDialog):
    def __init__(self, comic_details, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Detalles del Cómic")
        self.setGeometry(200, 200, 600, 400)

        layout = QVBoxLayout()
        self.setLayout(layout)

        scroll_area = QScrollArea()
        layout.addWidget(scroll_area)

        content_widget = QWidget()
        scroll_area.setWidget(content_widget)
        scroll_area.setWidgetResizable(True)  # Permitir que el contenido se redimensione

        detail_layout = QVBoxLayout(content_widget)
        detail_layout.setContentsMargins(0, 0, 0, 0)  # Eliminar márgenes

        detail_text = QTextBrowser()
        detail_text.setOpenExternalLinks(True)
        detail_text.setHtml(f"<h2>{comic_details['title']}</h2>"
                            f"<p><b>ISBN:</b> {comic_details.get('isbn', 'N/A')}</p>"  # Evitar errores si el ISBN no está disponible
                            f"<p><b>Descripción:</b> {comic_details.get('description', 'N/A')}</p>")  # Evitar errores si la descripción no está disponible
        detail_layout.addWidget(detail_text)

        # Mostrar la imagen del cómic desde la URL proporcionada
        image_label = QLabel()
        pixmap = QPixmap()
        response = requests.get(comic_details['thumbnail']['path'] + '.' + comic_details['thumbnail']['extension'])
        if response.status_code == 200:
            pixmap.loadFromData(response.content)
            image_label.setPixmap(pixmap)
            detail_layout.addWidget(image_label)
        else:
            detail_layout.addWidget(QLabel("Imagen no disponible"))

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.api = MarvelAPI()
        self.comics = []
        self.current_offset = 0
        self.limit = 10
        self.order_by = 'title'
        self.search_title = None
        self.search_year = None

        self.setWindowTitle("Marvel Comics Viewer")
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
        self.create_comic_list()

        self.update_comic_list()

    def create_search_bar(self):
        search_layout = QHBoxLayout()
        self.layout.addLayout(search_layout)

        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Buscar por título")
        self.title_input.textChanged.connect(self.on_title_input_change)
        search_layout.addWidget(self.title_input)

        self.year_input = QLineEdit()
        self.year_input.setPlaceholderText("Buscar por año")
        self.year_input.textChanged.connect(self.on_year_input_change)
        search_layout.addWidget(self.year_input)

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

        sort_button = QPushButton("Ordenar por Título")
        sort_button.clicked.connect(self.on_sort_button_click)
        sort_button.setStyleSheet("background-color: #FF0000; color: #FFFFFF; border: none; padding: 10px 20px; font-size: 16px;")
        button_layout.addWidget(sort_button)

    def create_comic_list(self):
        self.list_widget = QListWidget()
        self.list_widget.itemDoubleClicked.connect(self.on_comic_double_clicked)
        self.layout.addWidget(self.list_widget)

    def update_comic_list(self):
        self.list_widget.clear()
        for comic in self.comics:
            item = QListWidgetItem(comic['title'])
            item.setData(1, comic['id'])
            self.list_widget.addItem(item)

    def update_search_params(self):
        self.search_title = self.title_input.text() or None
        self.search_year = self.year_input.text() or None

    def on_title_input_change(self, text):
        self.update_search_params()

    def on_year_input_change(self, text):
        self.update_search_params()

    def on_search_button_click(self):
        self.current_offset = 0
        self.update_search_params()
        self.comics = self.api.get_comics(title=self.search_title, year=self.search_year)
        self.update_comic_list()

    def on_prev_button_click(self):
        if self.current_offset - self.limit >= 0:
            self.current_offset -= self.limit
            self.comics = self.api.get_comics(offset=self.current_offset, limit=self.limit, order_by=self.order_by)
            self.update_comic_list()

    def on_next_button_click(self):
        self.current_offset += self.limit
        self.comics = self.api.get_comics(offset=self.current_offset, limit=self.limit, order_by=self.order_by)
        self.update_comic_list()

    def on_sort_button_click(self):
        if self.order_by == 'title':
            self.order_by = '-title'  
        else:
            self.order_by = 'title'   
        self.current_offset = 0
        self.comics = self.api.get_comics(offset=self.current_offset, limit=self.limit, order_by=self.order_by)
        self.update_comic_list()

    def on_comic_double_clicked(self, item):
        comic_id = item.data(1)
        comic_details = self.api.get_comic_details(comic_id)
        if comic_details:
            comic_popup = ComicDetailDialog(comic_details)
            comic_popup.exec()
        else:
            QMessageBox.warning(self, "Error", "No se pudieron obtener los detalles del cómic.")

def main():
    app = QApplication(sys.argv)
    app.setStyleSheet("QMainWindow {background-color: #1E1E1E; color: #CCCCCC;}")
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()