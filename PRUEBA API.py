import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QListWidget, QListWidgetItem
# from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLabel, QLineEdit, QTextEdit, QListWidget, QMessageBox
from PyQt6.QtGui import QPixmap
import requests
import hashlib

API_PUBLIC_KEY = '77cd9227f30d31a1e8a6e54a7d12658b'
API_PRIVATE_KEY = '184b87f35ab3b8d461ef993c5b782d0001237fea'

def obtener_parametros_autenticacion():
    ts = '1'
    hash_value = hashlib.md5((ts + API_PRIVATE_KEY + API_PUBLIC_KEY).encode('utf-8')).hexdigest()
    return {'ts': ts, 'apikey': API_PUBLIC_KEY, 'hash': hash_value}

def obtener_personajes(offset=0, limit=10, ordenar_por='name'):
    url = 'https://gateway.marvel.com/v1/public/characters'
    params = obtener_parametros_autenticacion()

    # Desactivar la verificación SSL
    response = requests.get(url, params=params, verify=False, timeout=10)

    data = response.json()

    if data['code'] == 200:
        return data['data']['results']
    else:
        print("Error al obtener los personajes:", data['status'])

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Marvel Comics Character Viewer")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.list_widget = QListWidget()
        self.layout.addWidget(self.list_widget)

        self.actualizar_lista()

    def actualizar_lista(self):
        self.personajes = obtener_personajes()
        self.list_widget.clear()
        for personaje in self.personajes:
            item = QListWidgetItem(personaje['name'])
            self.list_widget.addItem(item)


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()