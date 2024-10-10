from PySide6.QtWidgets import QApplication, QPushButton, QMenu, QVBoxLayout, QWidget

# Crear la aplicación
app = QApplication([])

# Crear un widget principal
window = QWidget()
window.setWindowTitle('Botón desplegable con QMenu')

# Crear un botón
button = QPushButton('Menú de usuario')

# Crear un menú y añadir opciones
menu = QMenu()
menu.addAction('Configuración de perfil')
menu.addAction('Ayuda')
menu.addSeparator()  # Línea separadora
menu.addAction('Salir')

# Asignar el menú al botón
button.setMenu(menu)

# Configurar el layout
layout = QVBoxLayout()
layout.addWidget(button)
window.setLayout(layout)

# Mostrar la ventana
window.show()

# Ejecutar la aplicación
app.exec()
