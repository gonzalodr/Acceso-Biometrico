from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import QIntValidator
from Utils.Utils import *

from models.usuario import Usuario
from models.perfil import Perfil

from services.empleadoServices import EmpleadoServices
from services.perfilService import PerfilServices
from services.usuarioService import UsuarioServices
from UI.DialogoEmergente import DialogoEmergente
from datetime import date

import re

class formUsuario(QDialog):
    update: bool = False
    Uservices = UsuarioServices()
    Pempleado = EmpleadoServices()
    Pperfil = PerfilServices()
    idU = 0

    def __init__(self, parent=None, titulo="Registrar Usuario", id=None):
        super().__init__(parent)
        self.setObjectName("form")
        self.setMinimumSize(QSize(400, 350))
        self.setWindowFlags(Qt.FramelessWindowHint)
        cargar_estilos('claro', 'form.css', self)

        frame = QFrame()
        layoutFrame = QVBoxLayout()
        layoutFrame.setObjectName("formFrame")
        layoutFrame.setContentsMargins(10, 20, 10, 20)
        layoutFrame.setSpacing(10)

        lblTitulo = QLabel(text=titulo)
        lblTitulo.setObjectName("titulo")
        lblTitulo.setAlignment(Qt.AlignCenter)
        layoutFrame.addWidget(lblTitulo)

        layoutForm = QGridLayout()
        layoutForm.setContentsMargins(20, 10, 20, 20)
        layoutForm.setHorizontalSpacing(45)
        layoutForm.setVerticalSpacing(1)

        # Crear el ComboBox para seleccionar el empleado
        lblEmpleado = QLabel(text="Empleado")
        self.comboEmpleado = QComboBox()
        self.comboEmpleado.setPlaceholderText("Seleccione un empleado")
        self.errorEmpleado = QLabel()
        Sombrear(self.comboEmpleado, 20, 0, 0)

        # Crear los labels, inputs y labels de error
        lblUsuario = QLabel(text="Usuario")
        self.inputUsuario = QLineEdit()
        self.inputUsuario.setPlaceholderText("Ingrese el usuario")
        self.inputUsuario.installEventFilter(self)
        self.errorUsuario = QLabel()
        Sombrear(self.inputUsuario, 20, 0, 0)

        lblPerfil = QLabel(text="Perfil")
        self.comboPerfil = QComboBox()
        self.comboPerfil.setPlaceholderText("Seleccione el perfil")
        self.comboPerfil.installEventFilter(self)
        self.errorPerfil = QLabel()
        Sombrear(self.comboPerfil, 20, 0, 0)

        lblContrasena = QLabel(text="Contraseña")
        self.inputContrasena = QLineEdit()
        self.inputContrasena.setPlaceholderText("Ingrese la contraseña")
        self.inputContrasena.setEchoMode(QLineEdit.Password)
        self.errorContrasena = QLabel()
        Sombrear(self.inputContrasena, 20, 0, 0)

        # Agregar el checkbox para mostrar/ocultar la contraseña
        self.checkVerContrasena = QCheckBox("Mostrar contraseña")
        self.checkVerContrasena.clicked.connect(self.__accion_checkbox)
        Sombrear(self.checkVerContrasena, 30, 0, 5)

        layoutForm.addLayout(self._contenedor(lblUsuario, self.inputUsuario, self.errorUsuario), 0, 0)  # Fila 0, Columna 0
        layoutForm.addLayout(self._contenedor(lblEmpleado, self.comboEmpleado, self.errorEmpleado), 1, 0)  # Fila 2, Columna 0
        layoutForm.addLayout(self._contenedor(lblPerfil, self.comboPerfil, self.errorPerfil), 2, 0)  # Fila 3, Columna 0
        layoutForm.addLayout(self._contenedor(lblContrasena, self.inputContrasena, self.errorContrasena), 3, 0)  # Contraseña en la fila 1
        layoutForm.addWidget(self.checkVerContrasena, 4, 0)  # Checkbox en la fila 2

        boton_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        boton_box.button(QDialogButtonBox.Cancel).setText("Cancelar")
        boton_box.button(QDialogButtonBox.Cancel).setObjectName("btncancelar")
        boton_box.button(QDialogButtonBox.Cancel).setMinimumSize(QSize(100, 30))

        boton_box.button(QDialogButtonBox.Ok).setText("Registrar" if id is None else "Actualizar")
        boton_box.button(QDialogButtonBox.Ok).setObjectName("btnregistrar")
        boton_box.button(QDialogButtonBox.Ok).setMinimumSize(QSize(100, 30))
        Sombrear(boton_box, 20, 0, 5)

        # Centrar los botones
        boton_layout = QHBoxLayout()
        boton_layout.addStretch()
        boton_layout.addWidget(boton_box)
        boton_layout.addStretch()

        layoutFrame.addLayout(layoutForm)
        layoutFrame.addLayout(boton_layout)

        boton_box.accepted.connect(self._accion_usuario)
        boton_box.rejected.connect(self._cancelar_registro)

        frame.setLayout(layoutFrame)
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(frame)
        self.setLayout(layout)



    def _contenedor(self, label: QLabel, input: QLineEdit, label_error: QLabel):
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)

    def __accion_checkbox(self):
        if self.checkVerContrasena.isChecked():
            self.inputContrasena.setEchoMode(QLineEdit.Normal)  # Cambiar a inputContrasena
            Sombrear(self.checkVerContrasena, 30, 0, 5, "green")
        else:
            self.inputContrasena.setEchoMode(QLineEdit.Password)  # Cambiar a inputContrasena
            Sombrear(self.checkVerContrasena, 30, 0, 5)