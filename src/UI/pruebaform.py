from PySide6.QtWidgets import (
    QApplication, QPushButton, QMenu, QVBoxLayout, QWidget, QDialog,
    QLabel, QDialogButtonBox, QVBoxLayout, QLineEdit, QFormLayout, QMessageBox
)
from PySide6.QtCore import Qt  # Importar Qt para usar los flags de la ventana

# Crear la aplicación
app = QApplication([])

# Crear un widget principal
window = QWidget()
window.setWindowTitle('Botón desplegable con formulario de registro')

# Crear un botón
button = QPushButton('Menú de usuario')

# Crear un menú y añadir opciones
menu = QMenu()
registro_action = menu.addAction('Registrar usuario')
menu.addSeparator()  # Línea separadora
salir_action = menu.addAction('Salir')

# Asignar el menú al botón
button.setMenu(menu)

# Función para mostrar el formulario de registro sin botones de la barra de título
def mostrar_formulario_registro():
    dialog = QDialog(window)
    dialog.setWindowTitle('Formulario de registro')

    # Quitar los botones de cerrar, minimizar y maximizar de la barra de título
    dialog.setWindowFlags(Qt.Window | Qt.CustomizeWindowHint | Qt.WindowTitleHint )

    # Crear el layout del formulario
    form_layout = QFormLayout()

    # Campos del formulario
    nombre_input = QLineEdit()
    email_input = QLineEdit()
    form_layout.addRow('Nombre:', nombre_input)
    form_layout.addRow('Correo electrónico:', email_input)

    # Añadir botones al diálogo (Guardar o Cancelar)
    botones = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel)
    botones.accepted.connect(lambda: guardar_registro(nombre_input.text(), email_input.text(), dialog))
    botones.rejected.connect(dialog.reject)
    form_layout.addWidget(botones)

    dialog.setLayout(form_layout)
    dialog.exec()

# Función para guardar el registro
def guardar_registro(nombre, email, dialog):
    if nombre and email:
        dialog.accept()  # Cierra el diálogo si los datos son válidos
        QMessageBox.information(window, 'Registro exitoso', f'Usuario {nombre} registrado con éxito!')
    else:
        QMessageBox.warning(window, 'Error', 'Por favor, completa todos los campos del formulario.')

# Conectar la acción del menú a la función que muestra el formulario
registro_action.triggered.connect(mostrar_formulario_registro)

# Configurar el layout
layout = QVBoxLayout()
layout.addWidget(button)
window.setLayout(layout)

# Mostrar la ventana principal
window.show()

# Ejecutar la aplicación
app.exec()
