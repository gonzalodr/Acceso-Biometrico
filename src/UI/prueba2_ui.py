import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QStackedWidget, QLabel
#Pequeño ejemplo de manejo de vistas sin cambiar de ventana
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Manejo de Vistas con QStackedWidget")
    
        # Crear el QStackedWidget
        self.stacked_widget = QStackedWidget()
        
        # Crear las vistas
        self.vista1 = QWidget()
        self.vista2 = QWidget()

        # Configurar vista 1
        layout_vista1 = QVBoxLayout()
        layout_vista1.addWidget(QLabel("Esta es la Vista 1"))
        
        boton_ir_a_vista2 = QPushButton("Ir a Vista 2")
        self.estilo_boton(boton_ir_a_vista2)
        
        boton_ir_a_vista2.clicked.connect(self.mostrar_vista2)
        layout_vista1.addWidget(boton_ir_a_vista2)
        self.vista1.setLayout(layout_vista1)

        # Configurar vista 2
        layout_vista2 = QVBoxLayout()
        layout_vista2.addWidget(QLabel("Esta es la Vista 2"))
        
        boton_ir_a_vista1 = QPushButton("Ir a Vista 1")
        self.estilo_boton(boton_ir_a_vista1)
        
        boton_ir_a_vista1.clicked.connect(self.mostrar_vista1)
        layout_vista2.addWidget(boton_ir_a_vista1)
        self.vista2.setLayout(layout_vista2)

        # Añadir vistas al QStackedWidget
        self.stacked_widget.addWidget(self.vista1)
        self.stacked_widget.addWidget(self.vista2)

        # Establecer el widget central
        self.setCentralWidget(self.stacked_widget)

    def estilo_boton(self, boton):## aplicando colores
        boton.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50; /* Color de fondo */
                color: white; /* Color del texto */
                border: none; /* Sin borde */
                padding: 10px; /* Espaciado interno */
                border-radius: 5px; /* Bordes redondeados */
                font-size: 16px; /* Tamaño de fuente */
            }
            QPushButton:hover {
                background-color: #45a049; /* Color al pasar el mouse */
            }
            QPushButton:pressed {
                background-color: #3e8e41; /* Color al presionar */
            }
        """)

    def mostrar_vista1(self):
        self.stacked_widget.setCurrentIndex(0)  # Cambia a la vista 1

    def mostrar_vista2(self):
        self.stacked_widget.setCurrentIndex(1)  # Cambia a la vista 2

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = MainWindow()
    ventana.resize(300, 200)  # Tamaño inicial de la ventana
    ventana.show()
    sys.exit(app.exec())


