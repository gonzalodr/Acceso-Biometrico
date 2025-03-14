from PySide6.QtWidgets import *
from PySide6.QtCore import *
from Utils.Utils import *
from UI.DialogoEmergente import *
from services.perfilService import *

class formPerfil(QDialog):
    update: bool = False
    Pservices = PerfilServices()
    idP= 0
    
    def __init__(self, parent = None, titulo= "Registrar Perfil", id =None):
        super().__init__(parent)
        self.setObjectName("form")
        self.setMinimumSize(QSize(400, 350))
        self.setWindowFlags(Qt.FramelessWindowHint)
        cargar_estilos('claro','form.css',self)
        
        frame = QFrame()
        layoutFrame = QVBoxLayout()
        frame.setObjectName("formFrame")
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

        # Crear los labels, inputs y labels de error
        lblNombre = QLabel(text="Nombre")
        self.inputNombre = QLineEdit()
        self.inputNombre.setPlaceholderText("Ingrese el nombre del perfil")
        self.inputNombre.installEventFilter(self)
        self.errorNombre = QLabel()
        Sombrear(self.inputNombre, 20, 0, 0)

        lblDescripcion = QLabel(text="Descripción")
        self.inputDescripcion = QLineEdit()
        self.inputDescripcion.setPlaceholderText("Ingrese la descripción")
        self.inputDescripcion.installEventFilter(self)
        self.errorDescripcion = QLabel()
        Sombrear(self.inputDescripcion, 20, 0, 0)
        
        layoutForm.addLayout(self._contenedor(lblNombre, self.inputNombre, self.errorNombre), 0, 0)
        layoutForm.addLayout(self._contenedor(lblDescripcion, self.inputDescripcion, self.errorDescripcion), 1, 0)

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

        boton_box.accepted.connect(self._accion_perfil)
        boton_box.rejected.connect(self._cancelar_registro)
        
        frame.setLayout(layoutFrame)
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(frame)
        self.setLayout(layout)
        Sombrear(self, 30, 0, 0, "green")

        # Revisar si el formulario recibió un id por parámetros
        if id:
            self._obtener_registroId(id)
    
    def _contenedor(self, label: QLabel, input: QLineEdit, label_error: QLabel):
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)

        label_error.setObjectName("lblError")
        label_error.setMaximumHeight(25)
        label_error.setMinimumHeight(25)
        label_error.setWordWrap(True)

        layout.addWidget(label)
        layout.addWidget(input)
        layout.addWidget(label_error)
        return layout

    def eventFilter(self, source, event):
        if event.type() == 10:  # Enter (Mouse Enter)
            if isinstance(source, QLineEdit):
                text = source.placeholderText()
                QToolTip.showText(event.globalPos(), text, source)
        elif event.type() == 11:  # Leave (Mouse Leave)
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
        return True

    def _validar_inputs_vacios(self):
        vacios = False
        if not self.inputNombre.text().strip():
            Sombrear(self.inputNombre, 20, 0, 0, "red")
            vacios = True
        else:
            Sombrear(self.inputNombre, 20, 0, 0)

        if not self.inputDescripcion.text().strip():
            Sombrear(self.inputDescripcion, 20, 0, 0, "red")
            vacios = True
        else:
            Sombrear(self.inputDescripcion, 20, 0, 0)

        return vacios

    def _validar_inputs_sin_con_datos(self):
        return bool(self.inputNombre.text().strip() or self.inputDescripcion.text().strip())
    
    def _obtener_registroId(self, id):
        result = self.Pservices.obtenerPerfilPorId(id)
        if result["success"]:
            if result["data"]:
                perfil = result["data"]
                self.idP = perfil.id
                self.inputNombre.setText(perfil.nombre)
                self.inputDescripcion.setText(perfil.descripcion)
            else:
                dial = DialogoEmergente("Error", "Hubo un error de carga.", "Error")
                dial.exec()
                QTimer.singleShot(0, self.reject)
        else:
            dial = DialogoEmergente("Error", "Hubo un error de carga.", "Error")
            dial.exec()
            QTimer.singleShot(0, self.reject)

    def _accion_perfil(self):
        perfil = Perfil(
            nombre=self.inputNombre.text(),
            descripcion=self.inputDescripcion.text(),
            id=self.idP,
        )
        if self._validar_campos():
            if self.idP > 0:
                result = self.Pservices.modificarPerfil(perfil)
                if result["success"]:
                    dial = DialogoEmergente("Actualización", result["message"], "Check")
                    dial.exec()
                    self.reject()
                else:
                    dial = DialogoEmergente("Error", "Error al actualizar el perfil", "Error")
                    dial.exec()
            else:
                result = self.Pservices.insertarPerfil(perfil)
                if result["success"]:
                    dial = DialogoEmergente("Registrar", "Perfil registrado exitosamente", "Check")
                    dial.exec()
                    self.reject()
                else:
                    dial = DialogoEmergente("Error", "Error al registrar el Perfil", "Error")
                    dial.exec()