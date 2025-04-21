from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import QIntValidator
from Utils.Utils import *

from models.usuario import Usuario
from models.usuario_perfil import Usuario_Perfil

from services.personaService import PersonaServices
from services.perfilService import PerfilServices
from services.usuarioService import UsuarioServices
from UI.DialogoEmergente import DialogoEmergente
from datetime import date

import re

class formUsuario(QDialog):
    update: bool = False
    Uservices = UsuarioServices()
    Ppersona = PersonaServices()
    Pperfil = PerfilServices()
    idU = 0
    idUP = 0

    def __init__(self, parent=None, titulo="Registrar Usuario", id=None, id_usuario_perfil=None):
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

        # Crear el ComboBox para seleccionar la persona
        lblPersona = QLabel(text="Nombre")
        self.comboPersona = QComboBox()
        self.comboPersona.setPlaceholderText("Seleccione un nombre")
        self.errorPersona = QLabel()
        Sombrear(self.comboPersona, 20, 0, 0)

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
        layoutForm.addLayout(self._contenedor(lblPersona, self.comboPersona, self.errorPersona), 1, 0)  # Fila 2, Columna 0
        layoutForm.addLayout(self._contenedor(lblPerfil, self.comboPerfil, self.errorPerfil), 2, 0)  # Fila 3, Columna 0
        if id is None:
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

        self.id_persona = 0

        self.id_usuario_perfil = id_usuario_perfil

        print("id del usuario "+ str(id))
        if id ==None:
            self._cargar_personas_sin_usuario(self.id_persona)  # Cargar solo personas sin usuario para la creación


        # Cargar perfiles después de inicializar todos los widgets
        self._cargar_perfiles()

        # Cargar datos si se proporciona un id
        if id:
            self._obtener_registroId(id)

    def _contenedor(self, label: QLabel, input: QLineEdit, label_error: QLabel):
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)

        label_error.setObjectName("lblerror")
        label_error.setMaximumHeight(25)
        label_error.setMinimumHeight(25)
        label_error.setWordWrap(True)

        layout.addWidget(label)
        layout.addWidget(input)
        layout.addWidget(label_error)
        return layout
    
    def _cargar_personas_sin_usuario(self, id_persona=0):
        result = self.Ppersona.obtenerListaPersonasSinUsuario(id_persona)  # Asegúrate de que el método acepte el parámetro
        if result["success"]:
            for persona in result["data"]["lista_personasSinUsuario"]:
                id_persona = persona['id_persona']
                nombre_completo = persona['nombre_completo']
                self.comboPersona.addItem(nombre_completo, id_persona)
            if id_persona > 0:
                self.comboPersona.setCurrentIndex(result["data"]["posicion_id_persona"])
        else:
            dial = DialogoEmergente("Error", "No se pudieron cargar las personas sin usuario.", "Error")
            dial.exec()

    def _cargar_perfiles(self):
        result = self.Pperfil.obtenerListaPerfilCB()  # Llama al servicio para obtener la lista de perfiles
        if result["success"]:
            for perfil in result["data"]["listaPerfiles"]:
                self.comboPerfil.addItem(perfil.nombre, perfil.id)
        else:
            dial = DialogoEmergente("Error", "No se pudieron cargar los perfiles.", "Error")
            dial.exec()

    def eventFilter(self, source, event):
        if event.type() == QEvent.Enter:  # Mouse Enter
            if isinstance(source, QLineEdit):
                text = source.placeholderText()
                QToolTip.showText(event.globalPos(), text, source)
        elif event.type() == QEvent.Leave:  # Mouse Leave
            if isinstance(source, QLineEdit):
                QToolTip.hideText()
        return super().eventFilter(source, event)

    def _cancelar_registro(self):
        if self._validar_inputs_sin_con_datos():
            dialEmergente = DialogoEmergente("¿?", "¿Estás seguro que quieres cancelar?", "Question", True, True)
            opcion = dialEmergente.exec()
            if opcion == QDialog.Accepted:
                self.reject()
        else:
            self.reject()

    def _validar_campos(self):
        if self._validar_inputs_vacios():
            dialEmergente = DialogoEmergente("Advertencia", "Llene todos los campos.", "Warning")
            dialEmergente.exec()
            return False
        if not self.comboPerfil.currentData():  # Verifica si hay una asistencia seleccionada
            Sombrear(self.comboPerfil, 20, 0, 0, "red")
            return False
        return True

    def _validar_inputs_vacios(self):
        vacios = False

        if not self.inputUsuario.text().strip():
            Sombrear(self.inputUsuario, 20, 0, 0, "red")
            vacios = True
        else:
            Sombrear(self.inputUsuario, 20, 0, 0)

        if self.idU == 0:
            if not self.inputContrasena.text().strip():
                Sombrear(self.inputContrasena, 20, 0, 0, "red")
                vacios = True
            else:
                Sombrear(self.inputContrasena, 20, 0, 0)

        if not self.comboPersona.currentData():  # Verifica si no hay empleado seleccionado
            Sombrear(self.comboPersona, 20, 0, 0, "red")
            vacios = True
        else:
            Sombrear(self.comboPersona, 20, 0, 0)

        if not self.comboPerfil.currentData():  # Verifica si no hay empleado seleccionado
            Sombrear(self.comboPerfil, 20, 0, 0, "red")
            vacios = True
        else:
            Sombrear(self.comboPerfil, 20, 0, 0)

        return vacios

    def _validar_inputs_sin_con_datos(self):
        return self.inputUsuario.text().strip() or self.inputUsuario.text().strip()

    def _obtener_registroId(self, id):
        result = self.Uservices.obtenerUsuarioPorId(id)  # Cambiar a obtenerUsuarioPorId
        if result["success"]:
            if result["exists"]:
                usuario: Usuario = result["usuario"]
                id_perfil = result["id_perfil"]  # Capturar el id_perfil
                self.idU = usuario.id  # Cambiar a idU
                self.inputUsuario.setText(usuario.usuario)  # Asignar el usuario
                self.inputContrasena.setText(usuario.contrasena)  # Asignar la contraseña
                # Cargar el empleado
                self.comboPersona.setCurrentIndex(self.comboPersona.findData(usuario.id_persona))
                self.comboPerfil.setCurrentIndex(self.comboPerfil.findData(id_perfil))  # Usar id_perfil
                
                self._cargar_personas_sin_usuario(usuario.id_persona)
            else:
                dial = DialogoEmergente("Error", "Hubo un error de carga.", "Error")
                dial.exec()
                QTimer.singleShot(0, self.reject)
        else:
            dial = DialogoEmergente("Error", "Hubo un error de carga.", "Error")
            dial.exec()
            QTimer.singleShot(0, self.reject)

    def _accion_usuario(self):
        # Obtener el id de la persona seleccionada
        id_persona = self.comboPersona.currentData()  # Cambiar a id_persona
        # Obtener el id del perfil seleccionado
        id_perfil = self.comboPerfil.currentData()
        
        # Crear el objeto Usuario sin el atributo id_perfil
        usuario = Usuario(
            id=self.idU if self.idU > 0 else None,
            id_persona=id_persona,  # Cambiar a id_persona
            usuario=self.inputUsuario.text(),
            contrasena=self.inputContrasena.text(),
        )

        # Crear el objeto Usuario_Perfil con los datos necesarios
        usuario_perfil = Usuario_Perfil(
            id_perfil=id_perfil,  # Asignar el id_perfil
            id_Usuario=self.idU if self.idU > 0 else None,  # Asignar el id_usuario, si se está actualizando
            id=self.id_usuario_perfil
        )
        
        if self._validar_campos():
            if self.idU > 0:  # Verificar si se está actualizando
                usuario.contrasena = None

                print("Usuario: " + usuario.mostrar() + " y perfil "+ usuario_perfil.mostrar())
                result = self.Uservices.modificarUsuario(usuario, usuario_perfil)  # Cambiar a modificarUsuario
                if result["success"]:
                    dial = DialogoEmergente("Actualización", result["message"], "Check")
                    dial.exec()
                    self.reject()
                else:
                    dial = DialogoEmergente("Error", "Error al actualizar el usuario", "Error")
                    dial.exec()
            else:
                # Llamar al método insertarUsuario y pasar el id_perfil
                result = self.Uservices.insertarUsuario(usuario, id_perfil)  # Cambiar a insertarUsuario
                if result["success"]:
                    print(f"ID Persona: {id_persona}, ID Perfil: {id_perfil}")  # Cambiar a ID Persona
                    dial = DialogoEmergente("Registrar", "Usuario registrado exitosamente", "Check")
                    dial.exec()
                    self.reject()
                else:
                    dial = DialogoEmergente("Error", "Error al registrar el usuario", "Error")
                    dial.exec()

    def __accion_checkbox(self):
        if self.checkVerContrasena.isChecked():
            self.inputContrasena.setEchoMode(QLineEdit.Normal)  # Cambiar a inputContrasena
            Sombrear(self.checkVerContrasena, 30, 0, 5, "green")
        else:
            self.inputContrasena.setEchoMode(QLineEdit.Password)  # Cambiar a inputContrasena
            Sombrear(self.checkVerContrasena, 30, 0, 5)


    