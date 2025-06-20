from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *
from Utils.Utils import *
import os

class DialogoEmergente(QDialog):
    def __init__(self, title="Advertencia", message="¡Advertencia!", Icono="Warning", show_accept_button=True, show_cancel_button=False):
        """
            DialogoEmergente: Muestra pequeños avisos al usuario
            :param title: Es el pequeño titulo que se le mostrar en la ventanita
            :param message: Este el mensaje que se quiere dar
            :param Icono: es el icono que se debe mostrar, "Warning","Error","Check","Question" y "Save".
            :param show_accept_button: boleano, si se ingresa True muestra el boton aceptar
            :param show_cancel_button: boleano, si se ingresa True muestra el boton cancelar
            
            Nota: si no se ingresa que boton va a mostrar por defecto saldra activo el boton aceptar
        """
        super().__init__()
        self.setObjectName("DialEmergente")
        self.setWindowFlags(Qt.FramelessWindowHint) #elimina el borde de la ventana
        self.setWindowTitle(title)
        cargar_estilos('claro','dialogoEmergent.css',self)#carga los estilos de la ventana

        ##ajusta el tamano maximo de la ventana
        self.final_width = 300
        self.final_height = 300
        self.setMaximumSize(QSize(self.final_width,self.final_height))

        # Crear un layout vertical
        self.layoutPrincipal = QVBoxLayout()
        self.layoutPrincipal.setContentsMargins(0,0,0,0)
        
        # Crear un QFrame con un fondo de color
        self.frame = QFrame()
        self.frame.setObjectName("frameEmerg")
        self.layoutPrincipal.addWidget(self.frame)
        
        # Crear el layout para el contenido del QFrame
        self.frameLayout = QVBoxLayout()
        self.frameLayout.setContentsMargins(10,10,10,20)
        self.frame.setLayout(self.frameLayout)

        # Diccionario de iconos con sus rutas
        self.path_icono = {"Warning"    : "Warning.png", 
                           "Check"      : "Check.png", 
                           "Error"      : "Error.png",
                           "Save"       : "Save.png",
                           "Question"   : "Question.png"
                           }

        # Agregar un QLabel para el icono
        if Icono:
            self.icon_label = QLabel()
            cargar_Icono(self.icon_label, self.path_icono.get(Icono, "Warning.png"), QSize(128, 128))
            self.icon_label.setAlignment(Qt.AlignCenter)
            self.frameLayout.addWidget(self.icon_label)  # Añadir el QLabel al layout del frame

        Sombrear(self.icon_label,20,0,5)
        
        #Qlable para el titulot Titulo
        self.titulo_label = QLabel(title)
        self.titulo_label.setObjectName("titulo")
        self.titulo_label.setAlignment(Qt.AlignCenter)
        self.titulo_label.setWordWrap(True)

        # Agregar un QLabel para el mensaje
        self.message_label = QLabel(message)
        self.message_label.setObjectName("mensaje")
        self.message_label.setAlignment(Qt.AlignCenter)
        self.message_label.setWordWrap(True)

        self.frameLayout.addWidget(self.titulo_label)
        self.frameLayout.addWidget(self.message_label)

        # Crear un layout horizontal para los botones
        self.button_layout = QHBoxLayout()
        # Agregar botones personalizados según los parámetros proporcionados
        if show_accept_button or not show_cancel_button and not show_accept_button:
            ok_button = QPushButton("Aceptar")
            ok_button.setObjectName("acept")
            ok_button.setMinimumHeight(30)
            ok_button.clicked.connect(self.accept)
            self.button_layout.addWidget(ok_button)
            Sombrear(ok_button,20,0,5)

        if show_cancel_button:
            cancel_button = QPushButton("Cancelar")
            cancel_button.setObjectName("cancel")
            cancel_button.setMinimumHeight(30)
            cancel_button.clicked.connect(self.reject)
            self.button_layout.addWidget(cancel_button)
            Sombrear(cancel_button,20,0,5)

        # Agregar el layout de botones solo si hay botones visibles
        if show_accept_button or show_cancel_button:
            self.frameLayout.addLayout(self.button_layout)
            
        # Establecer el layout principal en el diálogo
        self.setLayout(self.layoutPrincipal)
        self.animation = QPropertyAnimation(self, b"geometry",self)
        self.animation.setDuration(700)

    def showEvent(self, event):
        """Ejecutar la animación de apertura con rebote cuando se muestra el diálogo."""
        start_rect = QRect(self.x() + self.final_width // 2, self.y() + self.final_height // 2, 1, 1)
        bounce_rect = QRect(self.x() - 15, self.y() - 15, self.final_width + 30, self.final_height + 30)
        end_rect = QRect(self.x(), self.y(), self.final_width-1, self.final_height-1)
        self.animation.setKeyValueAt(0, start_rect)
        self.animation.setKeyValueAt(0.7, bounce_rect)
        self.animation.setKeyValueAt(1, end_rect)
        self.animation.setEasingCurve(QEasingCurve.OutBounce)
        self.animation.start()
        super().showEvent(event)   
