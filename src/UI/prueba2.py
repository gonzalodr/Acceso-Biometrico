import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Configurar la ventana principal
        self.setWindowTitle("Interfaz Básica con PySide6")
        self.setGeometry(100, 100, 400, 200)  # x, y, width, height

        # Crear un widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Crear un layout vertical
        layout = QVBoxLayout()

        # Crear un botón
        self.button = QPushButton("Haz clic aquí")
        self.button.clicked.connect(self.on_button_clicked)

        # Crear una etiqueta
        self.label = QLabel("¡Bienvenido a PySide6!")
        
        # Agregar los widgets al layout
        layout.addWidget(self.label)
        layout.addWidget(self.button)

        # Asignar el layout al widget central
        central_widget.setLayout(layout)

    def on_button_clicked(self):
        # Cambiar el texto de la etiqueta al hacer clic en el botón
        self.label.setText("¡Has hecho clic en el botón!")

# Configurar la aplicación
app = QApplication(sys.argv)
window = MainWindow()
window.show()

# Ejecutar el bucle de eventos
sys.exit(app.exec())
