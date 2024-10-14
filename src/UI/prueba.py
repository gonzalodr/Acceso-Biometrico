from PySide6.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QDialog,
    QLabel, QLineEdit, QDateEdit, QComboBox, QTextEdit, QFormLayout, QDialogButtonBox, QFrame, QMessageBox
)
from PySide6.QtCore import Qt, QDate
import sys

class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super(VentanaPrincipal, self).__init__()
        self.setWindowTitle("Ventana Principal")
        self.setGeometry(100, 100, 300, 200)

        # Botón para abrir el formulario modal
        self.abrir_formulario_btn = QPushButton("Abrir Formulario")
        self.abrir_formulario_btn.clicked.connect(self.abrir_formulario_modal)

        # Configurar el layout principal
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.abrir_formulario_btn)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def crear_formulario_dialogo(self):
        # Crear el diálogo
        dialogo = QDialog(self)
        dialogo.setWindowTitle("Registro de Persona")
        dialogo.setFixedSize(450, 500)  # Tamaño fijo del modal
                
        # Estilo general del formulario
        form_style = """
            QFrame {
                background-color: White;
            }
            QLineEdit, QDateEdit, QTextEdit, QComboBox {
                background-color: #EBF3FF; 
                border: 1px solid #C6B6FE;  
                border-radius: 5px; 
                padding: 5px;
                font-size: 12px;
            }
            QLabel{
                background-color:transparent;
                color:black;
            }
            QLineEdit:focus, QDateEdit:focus, QTextEdit:focus, QComboBox:focus {
                border: 2px solid #8a2be2;  /* Borde lila oscuro al enfocar */
            }
        """
        dialogo.setStyleSheet(form_style)

        # Frame que contiene el formulario
        frame = QFrame(dialogo)
        form_layout = QFormLayout(frame)

        # Campos del formulario con placeholders
        nombre_edit = QLineEdit()
        nombre_edit.setPlaceholderText("Ingrese su nombre")

        apellido1_edit = QLineEdit()
        apellido1_edit.setPlaceholderText("Ingrese su primer apellido")

        apellido2_edit = QLineEdit()
        apellido2_edit.setPlaceholderText("Ingrese su segundo apellido")

        cedula_edit = QLineEdit()
        cedula_edit.setPlaceholderText("Ingrese su cédula")

        fecha_nacimiento_edit = QDateEdit()
        fecha_nacimiento_edit.setCalendarPopup(True)
        fecha_nacimiento_edit.setDisplayFormat("yyyy-MM-dd")
        fecha_nacimiento_edit.setMaximumDate(QDate.currentDate())  # Limita la fecha al día actual

        correo_edit = QLineEdit()
        correo_edit.setPlaceholderText("Ingrese su correo electrónico")

        estado_civil_combo = QComboBox()
        estado_civil_combo.addItems(["Soltero/a", "Casado/a", "Divorciado/a", "Viudo/a"])

        direccion_edit = QTextEdit()
        direccion_edit.setPlaceholderText("Ingrese su dirección completa")
        direccion_edit.setFixedHeight(50)

        # Agregar campos al layout del formulario
        form_layout.addRow(QLabel("Nombre:"), nombre_edit)
        form_layout.addRow(QLabel("Primer Apellido:"), apellido1_edit)
        form_layout.addRow(QLabel("Segundo Apellido:"), apellido2_edit)
        form_layout.addRow(QLabel("Cédula:"), cedula_edit)
        form_layout.addRow(QLabel("Fecha de Nacimiento:"), fecha_nacimiento_edit)
        form_layout.addRow(QLabel("Correo:"), correo_edit)
        form_layout.addRow(QLabel("Estado Civil:"), estado_civil_combo)
        form_layout.addRow(QLabel("Dirección:"), direccion_edit)

        # Botones del diálogo (Aceptar y Cancelar)
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(lambda: self.validar_campos(dialogo, nombre_edit, apellido1_edit, cedula_edit, correo_edit))
        button_box.rejected.connect(dialogo.reject)

        # Layout principal del diálogo
        main_layout = QVBoxLayout()
        main_layout.addWidget(frame)
        main_layout.addWidget(button_box)
        dialogo.setLayout(main_layout)

        return dialogo, nombre_edit, apellido1_edit, apellido2_edit, cedula_edit, fecha_nacimiento_edit, correo_edit, estado_civil_combo, direccion_edit

    def validar_campos(self, dialogo, nombre_edit, apellido1_edit, cedula_edit, correo_edit):
        # Verifica si los campos requeridos están vacíos
        if not nombre_edit.text().strip() or not apellido1_edit.text().strip() or not cedula_edit.text().strip() or not correo_edit.text().strip():
            QMessageBox.warning(self, "Campos Vacíos", "Por favor, complete todos los campos obligatorios.")
        else:
            dialogo.accept()

    def abrir_formulario_modal(self):
        dialogo, nombre_edit, apellido1_edit, apellido2_edit, cedula_edit, fecha_nacimiento_edit, correo_edit, estado_civil_combo, direccion_edit = self.crear_formulario_dialogo()
        if dialogo.exec_() == QDialog.Accepted:
            # Aquí puedes manejar los datos ingresados si el usuario hizo clic en "Aceptar"
            nombre = nombre_edit.text()
            apellido1 = apellido1_edit.text()
            apellido2 = apellido2_edit.text()
            cedula = cedula_edit.text()
            fecha_nacimiento = fecha_nacimiento_edit.date().toString("yyyy-MM-dd")
            correo = correo_edit.text()
            estado_civil = estado_civil_combo.currentText()
            direccion = direccion_edit.toPlainText()

            print(f"Nombre: {nombre}, Apellido1: {apellido1}, Apellido2: {apellido2}, "
                  f"Cédula: {cedula}, Fecha Nacimiento: {fecha_nacimiento}, Correo: {correo}, "
                  f"Estado Civil: {estado_civil}, Dirección: {direccion}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = VentanaPrincipal()
    ventana.show()
    sys.exit(app.exec())
