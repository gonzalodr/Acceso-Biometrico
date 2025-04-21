from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from Utils.Utils import *
from UI.DialogoEmergente import *
from services.solicitudPermisoService import SolicitudPermisoService
from services.empleadoServices import EmpleadoServices
from datetime import datetime, date
from models.solicitud_permisos import SolicitudPermiso
from settings.logger import logger


class FormSolicitudPermisoAdmin(QDialog):
    def __init__(
        self, parent=None, titulo="Gestionar Solicitud de Permiso", id_solicitud=None
    ):
        super().__init__(parent)
        self.setObjectName("form")
        self.setMinimumSize(QSize(700, 600))
        self.setWindowFlags(Qt.FramelessWindowHint)
        cargar_estilos("claro", "form.css", self)

        self.service = SolicitudPermisoService()
        self.empleado_service = EmpleadoServices()
        self.id_solicitud = id_solicitud  # ID de la solicitud para edición

        # Configuración del frame principal
        frame = QFrame()
        layoutFrame = QVBoxLayout()
        frame.setObjectName("formFrame")
        layoutFrame.setContentsMargins(10, 20, 10, 20)
        layoutFrame.setSpacing(10)

        # Título del formulario
        lblTitulo = QLabel(text=titulo)
        lblTitulo.setObjectName("titulo")
        lblTitulo.setAlignment(Qt.AlignCenter)
        layoutFrame.addWidget(lblTitulo)

        # Layout del formulario
        layoutForm = QGridLayout()
        layoutForm.setContentsMargins(20, 10, 20, 20)
        layoutForm.setHorizontalSpacing(45)
        layoutForm.setVerticalSpacing(1)

        # Elementos del formulario
        # Empleado
        lblEmpleado = QLabel(text="Empleado")
        self.inputEmpleado = QComboBox()
        self.cargar_empleados()  # Cargamos la lista de empleados
        self.errorEmpleado = QLabel()
        Sombrear(self.inputEmpleado, 20, 0, 0)

        # Tipo de Permiso
        lblTipoPermiso = QLabel(text="Tipo de Permiso")
        self.inputTipoPermiso = QComboBox()
        self.inputTipoPermiso.addItems(
            ["Vacaciones", "Enfermedad", "Personal", "Maternidad/Paternidad", "Otro"]
        )
        self.errorTipoPermiso = QLabel()
        Sombrear(self.inputTipoPermiso, 20, 0, 0)

        # Fecha Inicio
        lblFechaInicio = QLabel(text="Fecha Inicio")
        self.inputFechaInicio = QDateEdit()
        self.inputFechaInicio.setDisplayFormat("dd/MM/yyyy")
        self.inputFechaInicio.setDate(QDate.currentDate())
        self.inputFechaInicio.setCalendarPopup(True)
        self.errorFechaInicio = QLabel()
        Sombrear(self.inputFechaInicio, 20, 0, 0)

        # Fecha Fin
        lblFechaFin = QLabel(text="Fecha Fin")
        self.inputFechaFin = QDateEdit()
        self.inputFechaFin.setDisplayFormat("dd/MM/yyyy")
        self.inputFechaFin.setDate(QDate.currentDate())
        self.inputFechaFin.setCalendarPopup(True)
        self.errorFechaFin = QLabel()
        Sombrear(self.inputFechaFin, 20, 0, 0)

        # Estado
        lblEstado = QLabel(text="Estado")
        self.inputEstado = QComboBox()
        self.inputEstado.addItems(["Pendiente", "Aprobado", "Rechazado"])
        self.errorEstado = QLabel()
        Sombrear(self.inputEstado, 20, 0, 0)

        # Descripción
        lblDescripcion = QLabel(text="Descripción")
        self.inputDescripcion = QLineEdit()
        self.inputDescripcion.setPlaceholderText("Ingrese una descripción opcional")
        self.inputDescripcion.setMaximumHeight(50)
        self.errorDescripcion = QLabel()
        Sombrear(self.inputDescripcion, 20, 0, 0)

        # Añadiendo widgets al layout de formulario
        layoutForm.addLayout(
            self._contenedor(lblEmpleado, self.inputEmpleado, self.errorEmpleado), 0, 0
        )
        layoutForm.addLayout(
            self._contenedor(
                lblTipoPermiso, self.inputTipoPermiso, self.errorTipoPermiso
            ),
            1,
            0,
        )
        layoutForm.addLayout(
            self._contenedor(
                lblFechaInicio, self.inputFechaInicio, self.errorFechaInicio
            ),
            2,
            0,
        )
        layoutForm.addLayout(
            self._contenedor(lblFechaFin, self.inputFechaFin, self.errorFechaFin), 3, 0
        )
        layoutForm.addLayout(
            self._contenedor(lblEstado, self.inputEstado, self.errorEstado), 4, 0
        )
        layoutForm.addLayout(
            self._contenedor(
                lblDescripcion, self.inputDescripcion, self.errorDescripcion
            ),
            5,
            0,
        )

        # Botones de acción
        boton_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        boton_box.button(QDialogButtonBox.Cancel).setText("Cancelar")
        boton_box.button(QDialogButtonBox.Cancel).setObjectName("btncancelar")
        boton_box.button(QDialogButtonBox.Cancel).setMinimumSize(QSize(100, 30))

        boton_box.button(QDialogButtonBox.Ok).setText(
            "Registrar" if not id_solicitud else "Actualizar"
        )
        boton_box.button(QDialogButtonBox.Ok).setObjectName("btnregistrar")
        boton_box.button(QDialogButtonBox.Ok).setMinimumSize(QSize(100, 30))

        boton_box.accepted.connect(self.gestionar_solicitud)
        boton_box.rejected.connect(self.reject)

        # Centrar los botones
        boton_layout = QHBoxLayout()
        boton_layout.addStretch()
        boton_layout.addWidget(boton_box)
        boton_layout.addStretch()
        layoutFrame.addLayout(layoutForm)
        layoutFrame.addLayout(boton_layout)

        frame.setLayout(layoutFrame)
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(frame)
        self.setLayout(layout)

        # Cargar datos si se pasa un ID de solicitud
        if id_solicitud:
            """self.cargar_solicitud(id_solicitud)"""

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

    def cargar_empleados(self):
        """Carga la lista de empleados en el combobox"""
        try:
            empleados = self.empleado_service.obtener_empleados()
            for emp in empleados:
                self.inputEmpleado.addItem(
                    f"{emp.nombre} {emp.apellido}", emp.id_empleado
                )
        except Exception as e:
            print(f"Error al cargar empleados: {e}")

    """def cargar_solicitud(self, id_solicitud):
        
        try:
            solicitud = self.service.obtener_solicitud(id_solicitud)
            if solicitud:
                # Buscar y seleccionar el empleado en el combobox
                index = self.inputEmpleado.findData(solicitud.id_empleado)
                if index >= 0:
                    self.inputEmpleado.setCurrentIndex(index)

                self.inputTipoPermiso.setCurrentText(solicitud.tipo)
                self.inputFechaInicio.setDate(
                    QDate.fromString(
                        solicitud.fecha_inicio.strftime("%d/%m/%Y"), "dd/MM/yyyy"
                    )
                )
                self.inputFechaFin.setDate(
                    QDate.fromString(
                        solicitud.fecha_fin.strftime("%d/%m/%Y"), "dd/MM/yyyy"
                    )
                )
                self.inputEstado.setCurrentText(solicitud.estado)
                self.inputDescripcion.setPlainText(solicitud.descripcion)
        except Exception as e:
            print(f"Error al cargar solicitud: {e}")""" ""

    def gestionar_solicitud(self):
        """Gestiona la creación o actualización de una solicitud"""
        # Validaciones básicas
        if self.inputEmpleado.currentIndex() == -1:
            DialogoEmergente("Error", "Debe seleccionar un empleado", "Error").exec()
            return

        if self.inputFechaInicio.date() > self.inputFechaFin.date():
            DialogoEmergente(
                "Error",
                "La fecha de inicio no puede ser posterior a la fecha fin",
                "Error",
            ).exec()
            return

        if len(self.inputDescripcion.text().strip()) < 10:
            DialogoEmergente(
                "Error", "La descripción debe tener al menos 10 caracteres", "Error"
            ).exec()
            return

        # Crear objeto SolicitudPermiso
        solicitud = SolicitudPermiso(
            id_empleado=self.inputEmpleado.currentData(),
            tipo=self.inputTipoPermiso.currentText(),
            fecha_inicio=self.inputFechaInicio.date().toPython(),
            fecha_fin=self.inputFechaFin.date().toPython(),
            descripcion=self.inputDescripcion.text(),
            estado=self.inputEstado.currentText(),
            id_solicitud_permiso=self.id_solicitud if self.id_solicitud else 0,
        )

        # Determinar si es creación o actualización
        if self.id_solicitud:  # Si hay ID, es actualización
            result = self.service.actualizar_solicitud(solicitud)
            if result["success"]:
                DialogoEmergente("Actualización", result["message"], "Check").exec()
                self.accept()
            else:
                DialogoEmergente("Error", result["message"], "Error").exec()
        else:  # Si no hay ID, es creación
            result = self.service.crear_permiso(solicitud)
            if result["success"]:
                DialogoEmergente("Registro", result["message"], "Check").exec()
                self.accept()
            else:
                DialogoEmergente("Error", result["message"], "Error").exec()

    def cargar_empleados(self):
        """
        Método para cargar los empleados en el QComboBox.
        """
        try:
            # Limpia el QComboBox antes de agregar nuevos elementos
            self.inputEmpleado.clear()

            # Obtiene todos los empleados con nombre completo
            resultado = self.empleado_service.obtener_nombre_completo()

            if resultado["success"]:
                empleados = resultado["data"]
                if empleados:  # Si hay empleados
                    for empleado in empleados:
                        self.inputEmpleado.addItem(
                            empleado["nombre_completo"], empleado["id"]
                        )
                else:  # Si no hay empleados
                    dialEmergente = DialogoEmergente(
                        "Advertencia",
                        "No se encontraron empleados registrados.",
                        "Warning",
                        True,
                        False,
                    )
                    dialEmergente.exec()
            else:  # Si hubo un error
                dialEmergente = DialogoEmergente(
                    "Error",
                    resultado["message"],
                    "Error",
                    True,
                    False,
                )
                dialEmergente.exec()

        except Exception as e:
            logger.error(f"Error al cargar empleados: {e}")
            dialEmergente = DialogoEmergente(
                "Error",
                "Error inesperado al cargar empleados",
                "Error",
                True,
                False,
            )
            dialEmergente.exec()
