from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QLabel,
    QMainWindow, QPushButton, QSizePolicy, QSpacerItem,
    QStackedWidget, QStatusBar, QVBoxLayout, QWidget)
import sys
from PySide6.QtWidgets import QApplication, QMainWindow

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(727, 471)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.vboxLayout = QVBoxLayout(self.centralwidget)
        self.vboxLayout.setSpacing(0)
        self.vboxLayout.setObjectName(u"vboxLayout")
        self.vboxLayout.setContentsMargins(0, 0, 0, 0)
        self.superior = QFrame(self.centralwidget)
        self.superior.setObjectName(u"superior")
        self.superior.setMaximumSize(QSize(16777215, 40))
        self.superior.setStyleSheet(u"background-color: rgb(255, 0, 0)")
        self.superior.setFrameShape(QFrame.StyledPanel)
        self.superior.setFrameShadow(QFrame.Raised)
        self.superior.setLineWidth(0)
        self.horizontalLayout_2 = QHBoxLayout(self.superior)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.Menu = QPushButton(self.superior)
        self.Menu.setObjectName(u"Menu")
        self.Menu.setMinimumSize(QSize(200, 30))
        self.Menu.setStyleSheet(u"QPushButton{\n"
"background-color: #ff0000;\n"
"font: 87 12pt \"Arial Black\";\n"
"border-radius:0px;\n"
"}\n"
"\n"
"")
        icon = QIcon()
        icon.addFile(u"../../../../../../Imagenes/barra-de-menus.png", QSize(), QIcon.Normal, QIcon.Off)
        self.Menu.setIcon(icon)
        self.Menu.setIconSize(QSize(25, 20))
        self.horizontalLayout_2.addWidget(self.Menu)
        self.horizontalSpacer = QSpacerItem(406, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(self.horizontalSpacer)
        self.Minimizar = QPushButton(self.superior)
        self.Minimizar.setObjectName(u"Minimizar")
        self.Minimizar.setMinimumSize(QSize(0, 25))
        self.Minimizar.setStyleSheet(u"QPushButton{\n"
"border:0px;\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"border:5px solid #aa00ff;\n"
"background-color:#ffff00;\n"
"\n"
"}")
        icon1 = QIcon()
        icon1.addFile(u"../../../../../../Imagenes/minimizar.png", QSize(), QIcon.Normal, QIcon.Off)
        self.Minimizar.setIcon(icon1)
        self.Minimizar.setIconSize(QSize(25, 23))
        self.horizontalLayout_2.addWidget(self.Minimizar)
        self.restaurar = QPushButton(self.superior)
        self.restaurar.setObjectName(u"restaurar")
        self.restaurar.setMinimumSize(QSize(0, 25))
        self.restaurar.setStyleSheet(u"QPushButton{\n"
"border:0px;\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"border:5px solid #aa00ff;\n"
"background-color:#ffff00;\n"
"\n"
"}")
        icon2 = QIcon()
        icon2.addFile(u"../../../../../../Imagenes/maximizar.png", QSize(), QIcon.Normal, QIcon.Off)
        self.restaurar.setIcon(icon2)
        self.restaurar.setIconSize(QSize(25, 23))
        self.horizontalLayout_2.addWidget(self.restaurar)
        self.Maximizar = QPushButton(self.superior)
        self.Maximizar.setObjectName(u"Maximizar")
        self.Maximizar.setMinimumSize(QSize(0, 25))
        self.Maximizar.setMaximumSize(QSize(16777215, 25))
        self.Maximizar.setStyleSheet(u"QPushButton{\n"
"border:0px;\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"border:5px solid #aa00ff;\n"
"background-color:#ffff00;\n"
"\n"
"}")
        icon3 = QIcon()
        icon3.addFile(u"../../../../../../Imagenes/restaurar.png", QSize(), QIcon.Normal, QIcon.Off)
        self.Maximizar.setIcon(icon3)
        self.Maximizar.setIconSize(QSize(25, 23))
        self.horizontalLayout_2.addWidget(self.Maximizar)
        self.Salir = QPushButton(self.superior)
        self.Salir.setObjectName(u"Salir")
        self.Salir.setMinimumSize(QSize(0, 25))
        self.Salir.setStyleSheet(u"QPushButton{\n"
"border:0px;\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"border:5px solid #aa00ff;\n"
"background-color:#ffff00;\n"
"\n"
"}")
        icon4 = QIcon()
        icon4.addFile(u"../../../../../../Imagenes/cerrar.png", QSize(), QIcon.Normal, QIcon.Off)
        self.Salir.setIcon(icon4)
        self.Salir.setIconSize(QSize(25, 23))
        self.horizontalLayout_2.addWidget(self.Salir)
        self.vboxLayout.addWidget(self.superior)
        self.inferior = QFrame(self.centralwidget)
        self.inferior.setObjectName(u"inferior")
        self.inferior.setFrameShape(QFrame.StyledPanel)
        self.inferior.setFrameShadow(QFrame.Raised)
        self.inferior.setLineWidth(0)
        self.inferior.setMidLineWidth(0)
        self.horizontalLayout = QHBoxLayout(self.inferior)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.Framelateral = QFrame(self.inferior)
        self.Framelateral.setObjectName(u"Framelateral")
        self.Framelateral.setMinimumSize(QSize(200, 0))
        self.Framelateral.setMaximumSize(QSize(200, 16777215))
        self.Framelateral.setStyleSheet(u"QFrame{\n"
"background-color: #ff0000;\n"
"}\n"
"\n"
"QPushButton{\n"
"background-color: #ff0000; \n"
"border-top-left-radius: 20px;\n"
"border-bottom-left-radius: 20px;\n"
"\n"
"font: 75 12pt \"Arial Narrow\";\n"
"}\n"
"\n"
"")
        self.Framelateral.setFrameShape(QFrame.StyledPanel)
        self.Framelateral.setFrameShadow(QFrame.Raised)
        self.verticalLayout = QVBoxLayout(self.Framelateral)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.pushButton_6 = QPushButton(self.Framelateral)
        self.pushButton_6.setObjectName(u"pushButton_6")
        self.pushButton_6.setMinimumSize(QSize(0, 80))
        self.pushButton_6.setMaximumSize(QSize(16777215, 40))
        icon5 = QIcon()
        icon5.addFile(u"../../../../../../Imagenes/626508.png", QSize(), QIcon.Normal, QIcon.Off)
        self.pushButton_6.setIcon(icon5)
        self.pushButton_6.setIconSize(QSize(50, 70))
        self.pushButton_6.setAutoDefault(True)
        self.verticalLayout.addWidget(self.pushButton_6)
        self.pushButton = QPushButton(self.Framelateral)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setMinimumSize(QSize(0, 80))
        self.pushButton.setMaximumSize(QSize(16777215, 80))
        icon6 = QIcon()
        icon6.addFile(u"../../../../../../Imagenes/png-clipart-iron-man-thor-computer-icons-hulk-man-icon-marvel-avengers-assemble-superhero.png", QSize(), QIcon.Normal, QIcon.Off)
        self.pushButton.setIcon(icon6)
        self.pushButton.setIconSize(QSize(50, 70))
        self.verticalLayout.addWidget(self.pushButton)
        self.verticalSpacer = QSpacerItem(20, 235, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.verticalLayout.addItem(self.verticalSpacer)
        self.label = QLabel(self.Framelateral)
        self.label.setObjectName(u"label")
        self.label.setMaximumSize(QSize(16777215, 16777215))
        self.label.setAlignment(Qt.AlignCenter)
        self.verticalLayout.addWidget(self.label)
        self.horizontalLayout.addWidget(self.Framelateral)
        self.frame_2 = QFrame(self.inferior)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_3 = QHBoxLayout(self.frame_2)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.stackedWidget = QStackedWidget(self.frame_2)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.Pag1 = QWidget()
        self.Pag1.setObjectName(u"Pag1")
        self.stackedWidget.addWidget(self.Pag1)
        self.Pag2 = QWidget()
        self.Pag2.setObjectName(u"Pag2")
        self.stackedWidget.addWidget(self.Pag2)
        self.horizontalLayout_3.addWidget(self.stackedWidget)
        self.horizontalLayout.addWidget(self.frame_2)
        self.vboxLayout.addWidget(self.inferior)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.retranslateUi(MainWindow)
        self.stackedWidget.setCurrentIndex(1)
        QMetaObject.connectSlotsByName(MainWindow)
    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.Menu.setText(QCoreApplication.translate("MainWindow", u"MENU", None))
        self.Minimizar.setText("")
        self.restaurar.setText("")
        self.Maximizar.setText("")
        self.Salir.setText("")
        self.pushButton_6.setText(QCoreApplication.translate("MainWindow", u"Comics", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"Personajes", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec())


