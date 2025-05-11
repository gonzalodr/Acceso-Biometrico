from PySide6.QtWidgets import *
from PySide6.QtCore import *
from Utils.Utils import *
from UI.DialogoEmergente import *
from services.asistenciaService import *
from services.empleadoServices import *
from settings.config import *

class formAsistencia(QDialog):
    update: bool = False
    asistenciaServices = AsistenciaServices()
    empleadoServices = EmpleadoServices()
    idP = 0
    listaEmpleadosID = {}

    def __init__(self, parent=None, titulo="Registrar asistencia.", id=None):
        super().__init__(parent)
        self.setObjectName("form")
        self.setMinimumSize(QSize(700 / 2, 650 / 2))
        self.setWindowFlags(Qt.FramelessWindowHint)
        # add_Style(archivoQSS="form.css",QObjeto=self)
        cargar_estilos("claro", "form.css", self)

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
        layoutForm.setVerticalSpacing(5)

        """ 
            Aqui cargar el combo box de registros
        """
        lblEmpleado = QLabel(text="Seleccionar Empleado:")
        self.inputEmpleado = QComboBox()
        self.errorEmpleado = QLabel(text="")
        Sombrear(self.inputEmpleado, 20, 0, 0)

        # Fecha de creación
        lblFecha = QLabel("Fecha:")
        self.inputFecha = QDateEdit()
        self.inputFecha.setCalendarPopup(True)
        self.inputFecha.setDate(QDate.currentDate())

        if id is None:  # Crear nuevo reporte
            self.inputFecha.setMinimumDate(
                QDate.currentDate()
            )  # Bloquear fechas anteriores
            self.inputFecha.setMaximumDate(
                QDate.currentDate()
            )  # Bloquear fechas posteriores
        else:  # Editar reporte
            self.inputFecha.setMinimumDate(
                QDate(2000, 1, 1)
            )  # Permitir fechas de hace años
            self.inputFecha.setMaximumDate(
                QDate.currentDate()
            )  # Bloquear fechas futuras

        # Acceder al QCalendarWidget asociado al QDateEdit
        self.calendar = self.inputFecha.calendarWidget()
        self.calendar.setMinimumDate(
            self.inputFecha.minimumDate()
        )  # Bloquear fechas anteriores
        self.calendar.setMaximumDate(
            self.inputFecha.maximumDate()
        )  # Bloquear fechas posteriores
        layoutForm.addWidget(lblFecha, 1, 0)
        layoutForm.addWidget(self.inputFecha, 2, 0)
        Sombrear(self.inputFecha, 20, 0, 0)

        # Tipo de reporte
        lblEstado = QLabel(text="Estado Asistencia:")
        self.inputEstado = QComboBox()
        self.inputEstado.addItems(["Presente", "Ausente", "Tarde"])  # Tipos de reportes
        self.errorEstado = QLabel(text="")
        Sombrear(self.inputEstado, 20, 0, 0)

        layoutForm.addLayout(
            self._contenedor(lblEmpleado, self.inputEmpleado, self.errorEmpleado), 0, 0
        )
        layoutForm.addLayout(
            self._contenedor(lblEstado, self.inputEstado, self.errorEstado), 3, 0
        )

        boton_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        boton_box.button(QDialogButtonBox.Cancel).setText("Cancelar")
        boton_box.button(QDialogButtonBox.Cancel).setObjectName("btncancelar")
        boton_box.button(QDialogButtonBox.Cancel).setMinimumSize(QSize(100, 30))

        boton_box.button(QDialogButtonBox.Ok).setText(
            "Registrar" if id == None else "Actualizar"
        )
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

        boton_box.accepted.connect(self._accion_asistencia)
        boton_box.rejected.connect(self._cancelar_registro)

        frame.setLayout(layoutFrame)
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(frame)
        self.setLayout(layout)
        Sombrear(self, 30, 0, 0, "green")

        if id:
            self._obtener_registroId(id)

        layoutFrame.addLayout(layoutForm)  # Agregar formulario al layout principal

        # Definir layout del QDialog
        self.setLayout(layoutFrame)

        layoutForm.addLayout(
            self._contenedor(lblEmpleado, self.inputEmpleado, self.errorEmpleado), 0, 0
        )
        # layoutForm.addWidget(self.error,1,0)

        self._cargar_empleados()
        # self._verificar_permiso()

    # self.inputTabla.currentIndexChanged.connect(self._verificar_permiso)
    # self.inputEmpleado.currentIndexChanged.connect(self._verificar_permiso)

    def _contenedor(self, label: QLabel, input, label_error: QLabel):
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

    def eventFilter(self, source, event):
        if event.type() == 10:  # Enter (Mouse Enter)
            if isinstance(source, QLineEdit):
                text = source.placeholderText()
                QToolTip.showText(event.globalPos(), text, source)
        elif event.type() == 11:  # Leave (Mouse Leave)
            if isinstance(source, QLineEdit):
                QToolTip.hideText()
        return super().eventFilter(source, event)

    # def _cancelar_registro(self):
    #    if not self._validar_inputs_vacios():
    #       dialEmergente = DialogoEmergente("¿Estas seguro que  quieres cancelar?","Question",True,True)
    #      opcion = dialEmergente.exec()
    #     if opcion == QDialog.Accepted:
    #         self.reject()
    #   elif opcion == QDialog.Rejected:
    #      pass
    # else:
    #    self.reject()##cerrar la ventana

    # def _cancelar_registro(self):
#     if not self._validar_inputs_vacios():
#         # Mostrar un diálogo emergente de confirmación
#         dialEmergente = QMessageBox()
#         dialEmergente.setIcon(QMessageBox.Question)
#         dialEmergente.setText("¿Estás seguro que quieres cancelar?")
#         dialEmergente.setWindowTitle("Confirmar cancelación")

#         # Personalizar los botones para que digan "Sí" y "No"
#         boton_si = dialEmergente.addButton("Sí", QMessageBox.YesRole)
#         boton_no = dialEmergente.addButton("No", QMessageBox.NoRole)

#         # Aplicar estilos para cambiar el fondo a blanco
#         dialEmergente.setStyleSheet(
#             """
#             QMessageBox {
#                 background-color: white;
#             }
#             QMessageBox QLabel {
#                 color: black; /* Cambiar el color del texto si es necesario */
#             }
#             QMessageBox QPushButton {
#                 background-color: #f0f0f0; /* Color de fondo del botón */
#                 color: black; /* Color del texto del botón */
#                 border: 1px solid #ccc; /* Borde del botón */
#                 padding: 5px 10px; /* Espaciado interno del botón */
#             }
#             QMessageBox QPushButton:hover {
#                 background-color: #d0d0d0; /* Color de fondo al pasar el mouse */
#             }
#             QMessageBox QPushButton:pressed {
#                 background-color: #a0a0a0; /* Color de fondo al presionar el botón */
#             }
#         """
#         )

#         # Obtener la respuesta del usuario
#         dialEmergente.exec()

#         # Si el usuario elige "Sí", cerrar la ventana
#         if dialEmergente.clickedButton() == boton_si:
#             self.reject()
#         # Si el usuario elige "No", no hacer nada
#         elif dialEmergente.clickedButton() == boton_no:
#             pass
#     else:
#         # Si los inputs están vacíos, cerrar la ventana directamente
#         self.reject()

    def _cancelar_registro(self):
        dialEmergente = DialogoEmergente(
            "Confirmación",
            "¿Estás seguro de que quieres cancelar?",
            "Confirmation",
            True,
            True,
        )
        opcion = dialEmergente.exec()

        if opcion == QDialog.Accepted:
            self.reject() 
            
            
    def _cargar_empleados(self):
        result = self.empleadoServices.obtener_todo_empleados()
        if result["success"]:
            listaEmpleados = result["data"]["listaEmpleados"]
            if len(listaEmpleados) > 0:
                for empleado in listaEmpleados:
                    
                    self.inputEmpleado.addItem(
                        empleado.nombre_persona
                        )
                    # self.listaEmpleadosID[empleado.id_persona] = empleado.id
                    self.listaEmpleadosID[empleado.nombre_persona] = (
                        empleado.id
                    )  # Usar id_persona
            else:
                dialEmergente = DialogoEmergente("", "Ocurrio un error", "Error")
                if dialEmergente.exec() == QDialog.Accepted:
                    self.reject()
        else:
            print(f"\nError:\n{e}\n----------------------\n")
            self.reject()

    def _validar_inputs_vacios(self):
        empleado = self.inputEmpleado.currentText().strip()
        fecha = self.inputFecha.date().toString("yyyy-MM-dd").strip()
        estado = self.inputEstado.currentText().strip()

        if not empleado or not fecha or not estado:
            return True  # Hay campos vacíos
        return False  # Todos los campos están llenos

    def _obtener_registroId(self, id):
        result = self.asistenciaServices.obtenerAsistenciaPorId(id)
        if result["success"]:
            if result["data"]:
                asistencia: Asistencia = result["data"]
                self.idP = asistencia.id
                self.inputEmpleado.setCurrentText(asistencia.nombre_persona)
                # Convertir fecha a QDate antes de asignarla
                fecha_qt = QDate(
                    asistencia.fecha.year, asistencia.fecha.month, asistencia.fecha.day
                )
                self.inputFecha.setDate(fecha_qt)
                # Restringir la fecha máxima a hoy
                self.inputFecha.setMaximumDate(QDate.currentDate())

                self.inputEstado.setCurrentText(asistencia.estado_asistencia)

            else:
                dial = DialogoEmergente("Error", "Hubo un error de carga.", "Error")
                dial.exec()
                QTimer.singleShot(0, self.reject)
        else:
            dial = DialogoEmergente("Error", "Hubo un error de carga.", "Error")
            dial.exec()
            QTimer.singleShot(0, self.reject)

    def _accion_asistencia(self):
        asistencia: Asistencia = Asistencia(
            # id_empleado=self.listaEmpleadosID[self.inputEmpleado.currentText()],
            id_empleado=self.listaEmpleadosID[self.inputEmpleado.currentText()],
            fecha=self.inputFecha.date().toString("yyyy-MM-dd"),
            estado_asistencia=self.inputEstado.currentText(),
            id=self.idP,
        )

        if (
            self.idP and self.idP > 0
        ):  # Verifica que self.idP no sea None y sea mayor a 0
            result = self.asistenciaServices.modificarAsistencia(asistencia)
            mensaje = (
                "Actualización"
                if result["success"]
                else "Error al actualizar el perfil"
            )
        else:
            result = self.asistenciaServices.insertarAsistencia(asistencia)
            mensaje = (
                "Reporte registrado exitosamente"
                if result["success"]
                else "Error al registrar el Reporte"
            )

        icono = "Check" if result["success"] else "Error"
        dial = DialogoEmergente(
            mensaje, result["message"] if result["success"] else "Error", icono
        )
        dial.exec()

        if result["success"]:
            self.reject()  # Cierra el diálogo solo si la operación fue exitosa
