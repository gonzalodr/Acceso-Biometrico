from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import QIntValidator
from Utils.Utils import *

from models.persona import Persona
from models.justificacion import Justificacion
from models.asistencia import Asistencia  # Asegúrate de importar la clase Asistencia
from services.empleadoServices import EmpleadoServices
from services.justificacionService import JustificacionServices
from services.asistenciaService import AsistenciaServices  # Asegúrate de importar el servicio de asistencias
from UI.DialogoEmergente import DialogoEmergente
from datetime import date

import re

class formJustificacion(QDialog):
    update: bool = False
    Pservices = JustificacionServices()
    Pempleado = EmpleadoServices()
    Pasistencia = AsistenciaServices()  # Instancia del servicio de asistencias
    idJ = 0

    def __init__(self, parent=None, titulo="Registrar Justificación", id=None):
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

        # Crear los labels, inputs y labels de error
        lblMotivo = QLabel(text="Motivo")
        self.inputMotivo = QLineEdit()
        self.inputMotivo.setPlaceholderText("Ingrese el motivo")
        self.inputMotivo.installEventFilter(self)
        self.errorMotivo = QLabel()
        Sombrear(self.inputMotivo, 20, 0, 0)

        lblDescripcion = QLabel(text="Descripción")
        self.inputDescripcion = QLineEdit()
        self.inputDescripcion.setPlaceholderText("Ingrese la descripción")
        self.inputDescripcion.installEventFilter(self)
        self.errorDescripcion = QLabel()
        Sombrear(self.inputDescripcion, 20, 0, 0)

        # Crear el ComboBox para seleccionar el empleado
        lblEmpleado = QLabel(text="Empleado")
        self.comboEmpleado = QComboBox()
        self.comboEmpleado.setPlaceholderText("Seleccione un empleado")
        self.errorEmpleado = QLabel()
        Sombrear(self.comboEmpleado, 20, 0, 0)

        # Crear el ComboBox oculto para las asistencias
        lblAsistencia = QLabel(text="Asistencia")
        self.comboAsistencia = QComboBox()
        self.comboAsistencia.setPlaceholderText("Seleccione una asistencia")
        self.comboAsistencia.setVisible(False)  # Ocultar inicialmente
        self.errorAsistencia = QLabel()
        Sombrear(self.comboAsistencia, 20, 0, 0)

        # Label para mostrar mensaje si no hay asistencias
        self.lblNoAsistencias = QLabel("Este empleado no tiene asistencias injustificadas")
        self.lblNoAsistencias.setVisible(False)  # Ocultar inicialmente

        layoutForm.addLayout(self._contenedor(lblEmpleado, self.comboEmpleado, self.errorEmpleado), 2, 0)
        layoutForm.addLayout(self._contenedor(lblAsistencia, self.comboAsistencia, self.errorAsistencia), 3, 0)
        layoutForm.addWidget(self.lblNoAsistencias, 4, 0, 1, 2)  # Añadir el label al layout
        layoutForm.addLayout(self._contenedor(lblMotivo, self.inputMotivo, self.errorMotivo), 0, 0)
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

        boton_box.accepted.connect(self._accion_justificacion)
        boton_box.rejected.connect(self._cancelar_registro)

        frame.setLayout(layoutFrame)
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(frame)
        self.setLayout(layout)

        # Cargar empleados después de inicializar todos los widgets
        self._cargar_empleados()

        # Conectar la señal de cambio del ComboBox de empleados
        self.comboEmpleado.currentIndexChanged.connect(self._actualizar_asistencias)

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
    
    def _cargar_empleados(self):
        result = self.Pempleado.listar_empleados()  
        if result["success"]:
            for empleado in result["data"]["listaPersonas"]:
                # Asegúrate de que empleado['persona'] sea una instancia de Persona
                if isinstance(empleado['persona'], Persona):
                    # Accede a los atributos de la clase Persona
                    self.comboEmpleado.addItem(f"{empleado['persona'].nombre} {empleado['persona'].apellidos}", empleado['id_empleado'])
                else:
                    print("Error: empleado['persona'] no es una instancia de Persona")
        else:
            dial = DialogoEmergente("Error", "No se pudieron cargar los empleados.", "Error")
            dial.exec()

    def _actualizar_asistencias(self):
        # Limpiar el ComboBox de asistencias
        self.comboAsistencia.clear()
        self.comboAsistencia.setVisible(False)  # Ocultar el ComboBox de asistencias inicialmente
        self.lblNoAsistencias.setVisible(False)  # Ocultar el mensaje de no asistencias

        # Obtener el id del empleado seleccionado
        id_empleado = self.comboEmpleado.currentData()
        if id_empleado:
            # Cargar asistencias no justificadas para el empleado seleccionado
            result = self.Pasistencia.obtenerAsistenciaPorEmpleado(id_empleado)
            if result["success"]:
                asistencias = result["data"]
                if asistencias:
                    for asistencia in asistencias:
                        self.comboAsistencia.addItem(asistencia.fecha.strftime("%Y-%m-%d"), asistencia.id_asistencia)
                    self.comboAsistencia.setVisible(True)  # Mostrar el ComboBox si hay asistencias
                else:
                    # Si no hay asistencias, mostrar el mensaje
                    self.lblNoAsistencias.setVisible(True)
                    self.comboAsistencia.setVisible(False)  # Asegurarse de que el ComboBox de asistencias esté oculto
            else:
                dial = DialogoEmergente("Error", "No se pudieron cargar las asistencias.", "Error")
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
        if not self.comboAsistencia.currentData():  # Verifica si hay una asistencia seleccionada
            Sombrear(self.comboAsistencia, 20, 0, 0, "red")
            return False
        return True

    def _validar_inputs_vacios(self):
        vacios = False

        if not self.inputMotivo.text().strip():
            Sombrear(self.inputMotivo, 20, 0, 0, "red")
            vacios = True
        else:
            Sombrear(self.inputMotivo, 20, 0, 0)

        if not self.inputDescripcion.text().strip():
            Sombrear(self.inputDescripcion, 20, 0, 0, "red")
            vacios = True
        else:
            Sombrear(self.inputDescripcion, 20, 0, 0)

        if not self.comboEmpleado.currentData():  # Verifica si no hay empleado seleccionado
            Sombrear(self.comboEmpleado, 20, 0, 0, "red")
            vacios = True
        else:
            Sombrear(self.comboEmpleado, 20, 0, 0)

        if not self.comboAsistencia.currentData():  # Verifica si no hay empleado seleccionado
            Sombrear(self.comboEmpleado, 20, 0, 0, "red")
            vacios = True
        else:
            Sombrear(self.comboEmpleado, 20, 0, 0)

        return vacios

    def _validar_inputs_sin_con_datos(self):
        return self.inputMotivo.text().strip() or self.inputDescripcion.text().strip()

    def _obtener_registroId(self, id):
        result = self.Pservices.obtenerJustificacionPorId(id)
        if result["success"]:
            if result["data"]:
                justificacion: Justificacion = result["data"]
                self.idJ = justificacion.id_justificacion
                self.inputMotivo.setText(justificacion.motivo)
                self.inputDescripcion.setText(justificacion.descripcion)
            else:
                dial = DialogoEmergente("Error", "Hubo un error de carga.", "Error")
                dial.exec()
                QTimer.singleShot(0, self.reject)
        else:
            dial = DialogoEmergente("Error", "Hubo un error de carga.", "Error")
            dial.exec()
            QTimer.singleShot(0, self.reject)

    def _accion_justificacion(self):
        id_empleado = self.comboEmpleado.currentData()
        justificacion = Justificacion(
            id_empleado=id_empleado,  # Cambia esto según tu lógica
            id_asistencia=self.comboAsistencia.currentData(),  # Obtener el id de asistencia seleccionado
            fecha=date.today(),
            motivo=self.inputMotivo.text(),
            descripcion=self.inputDescripcion.text(),
            id_justificacion=self.idJ,
        )
        if self._validar_campos():
            if self.idJ > 0:
                result = self.Pservices.modificarJustificacion(justificacion)
                if result["success"]:
                    dial = DialogoEmergente("Actualización", result["message"], "Check")
                    dial.exec()
                    self.reject()
                else:
                    dial = DialogoEmergente("Error", "Error al actualizar justificación", "Error")
                    dial.exec()
            else:
                result = self.Pservices.insertarJustificacion(justificacion)
                if result["success"]:
                    dial = DialogoEmergente("Registrar", "Justificación registrada exitosamente", "Check")
                    dial.exec()
                    self.reject()
                else:
                    dial = DialogoEmergente("Error", "Error al registrar la justificación", "Error")
                    dial.exec()