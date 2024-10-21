from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *
from UI.stilosInterfaz import *
import os

class VentanaEmergente(QDialog):
    def __init__(self, title="Advertencia", message="¡Advertencia!", Icono="Warning", show_accept_button=True, show_cancel_button=False):
        super().__init__()
        # Eliminar el borde de la ventana
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setWindowTitle(title)
        self.setStyleSheet("border: 2px solid #4A90E2;border-radius: 10px;")
        
        self.setMinimumSize(300,300)
        self.setMaximumSize(550, 550)  # Establece un tamaño máximo de 600x400 píxeles

        # Crear un layout vertical
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0,0,0,0)
        
        # Crear un QFrame con un fondo de color
        self.frame = QFrame()
        self.frame.setStyleSheet("background-color:#FFFFFF;border: 1px solid transparent;border-radius: 10px;")
        self.layout.addWidget(self.frame)
        
        # Crear el layout para el contenido del QFrame
        self.frameLayout = QVBoxLayout()
        self.frameLayout.setContentsMargins(10,10,10,20)
        self.frame.setLayout(self.frameLayout)

        # Diccionario de iconos con sus rutas
        self.path_icono = {"Warning": "iconos/Warning.png", "Check": "iconos/Check.png", "Error": "iconos/Error.png","Save":"iconos/Save.png","Question":"iconos/Question.png"}

        # Agregar un QLabel para el icono
        if Icono:
            self.icon_label = QLabel()
            #direccion del icono
            path_url = os.path.join(os.path.dirname(__file__), self.path_icono.get(Icono, "iconos/Warning.png"))
            # Cargar el icono PNG
            icon_pixmap = QPixmap(path_url).scaled(128, 128, Qt.KeepAspectRatio)
            self.icon_label.setPixmap(icon_pixmap)
            self.icon_label.setAlignment(Qt.AlignCenter)
            self.frameLayout.addWidget(self.icon_label)  # Añadir el QLabel al layout del frame

        self.icon_label.setStyleSheet("QLabel {border-radius: 10px;background-color: #F0F2FF;}")

        # Agregar un QLabel para el mensaje
        self.message_label = QLabel(message)
        self.message_label.setAlignment(Qt.AlignCenter)
        self.message_label.setStyleSheet("font: 700 10pt \"Segoe UI\";")
        self.message_label.setWordWrap(True)
        
        #Titulo
        self.titulo_label = QLabel(title)
        self.titulo_label.setAlignment(Qt.AlignCenter)
        self.titulo_label.setStyleSheet("font: 700 16pt \"Segoe UI\";")
        self.titulo_label.setWordWrap(True)
        
        self.frameLayout.addWidget(self.titulo_label)
        self.frameLayout.addWidget(self.message_label)

        # Crear un layout horizontal para los botones
        self.button_layout = QHBoxLayout()
        # Agregar botones personalizados según los parámetros proporcionados
        if show_accept_button:
            ok_button = QPushButton("Aceptar")
            ok_button.setStyleSheet(btnStyleSheet)
            ok_button.clicked.connect(self.accept)
            self.button_layout.addWidget(ok_button)

        if show_cancel_button:
            cancel_button = QPushButton("Cancelar")
            cancel_button.setStyleSheet(btnEliminarStyleSheet)
            cancel_button.clicked.connect(self.reject)
            self.button_layout.addWidget(cancel_button)  # Corregir el nombre de la variable

        # Agregar el layout de botones solo si hay botones visibles
        if show_accept_button or show_cancel_button:
            self.frameLayout.addLayout(self.button_layout)

        # Establecer el layout principal en el diálogo
        self.setLayout(self.layout)

