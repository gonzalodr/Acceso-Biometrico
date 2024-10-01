import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QLineEdit, QMessageBox, QVBoxLayout, QWidget

class MainWindow(QMainWindow):#heredacion
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ejemplo de PySide6")

        # Crear un widget central
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Crear layout vertical
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        # Crear un cuadro de texto
        self.text_input = QLineEdit()
        self.text_input.setPlaceholderText("Escribe algo aquí...")
        
        # Crear un botón
        self.button = QPushButton("Mostrar Mensaje")
        self.button.clicked.connect(self.mostrar_mensaje)

        # Añadir widgets al layout
        self.layout.addWidget(self.text_input)
        self.layout.addWidget(self.button)

    def mostrar_mensaje(self):
        texto = self.text_input.text()
        QMessageBox.information(self, "Texto ingresado", f"Has escrito: {texto}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = MainWindow()
    ventana.resize(300, 200)  # Tamaño inicial de la ventana
    ventana.show()
    sys.exit(app.exec())

