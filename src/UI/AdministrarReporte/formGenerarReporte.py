from datetime import datetime
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import QDate
from Utils.Utils import cargar_estilos
from services.empleadoServices import EmpleadoServices
from services.reporteService import ReporteServices
from services.departamentoService import DepartamentoServices
from services.rolService import RolServices

from UI.DialogoEmergente import DialogoEmergente
import os


class GenerarReporte(QDialog):
    reporteServices = ReporteServices()
    rolServices = RolServices()
    depaServices = DepartamentoServices()
    empleServices = EmpleadoServices()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Generar Reporte")

        # Layout principal
        self.layout = QVBoxLayout()

        cargar_estilos("claro", "formReporte.css", self)

        self.grupoSeleccionEmpleado()
        self.grupoSeleccionarDempartamentoRol()
        self.grupoTipoReporte()
        self.grupoRangoFechas()
        self.grupoGenerarReporte()

        self.cargarComboboxEmpleados()
        self.cargarComboboxDepartamento()
        self.cargarComboboxRol()

        # Botones de acción
        boton_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        boton_box.button(QDialogButtonBox.Cancel).setText("Cancelar")
        boton_box.button(QDialogButtonBox.Cancel).setObjectName("btncancelar")
        boton_box.button(QDialogButtonBox.Cancel).setMinimumSize(150, 30)

        boton_box.button(QDialogButtonBox.Ok).setText("Generar")
        boton_box.button(QDialogButtonBox.Ok).setObjectName("btngenerar")
        boton_box.button(QDialogButtonBox.Ok).setMinimumSize(150, 30)

        boton_box.accepted.connect(self.generaReporte)
        boton_box.rejected.connect(self.reject)

        # Centrar los botones
        boton_layout = QHBoxLayout()
        boton_layout.addStretch()
        boton_layout.addWidget(boton_box)
        boton_layout.addStretch()

        self.layout.addLayout(boton_layout)
        self.setLayout(self.layout)

    def cerrarForm(self):
        print("cerrando form")
        self.reject()
        
    def grupoSeleccionEmpleado(self):
        groupEmpleado = QGroupBox("Selección de Empleado")
        layoutEmpleado = QVBoxLayout()

        self.cmbEmpleado = QComboBox()
        self.cmbEmpleado.addItem("Todos los empleados", None)

        layoutEmpleado.addWidget(self.cmbEmpleado)
        groupEmpleado.setLayout(layoutEmpleado)
        self.layout.addWidget(groupEmpleado)

    def grupoSeleccionarDempartamentoRol(self):
        groupDepaRol = QGroupBox("Departamento y rol")
        layoutDepaRol = QVBoxLayout()

        self.cmbDepartamento = QComboBox()
        self.cmbRol = QComboBox()

        self.cmbDepartamento.addItem("Todos", None)
        self.cmbRol.addItem("Todos", None)

        layoutDepaRol.addWidget(QLabel("Seleccionar departamento"))
        layoutDepaRol.addWidget(self.cmbDepartamento)

        layoutDepaRol.addWidget(QLabel("Seleccionar rol"))
        layoutDepaRol.addWidget(self.cmbRol)

        groupDepaRol.setLayout(layoutDepaRol)
        self.layout.addWidget(groupDepaRol)

    def grupoTipoReporte(self):
        # Grupo para tipo de reporte
        groupTipoReporte = QGroupBox("Tipo de Reporte")
        layoutTipoReporte = QVBoxLayout()

        self.checkJustificacion = QCheckBox("Justificaciones")
        self.checkAsistencia = QCheckBox("Asistencias")
        self.checkPermiso = QCheckBox("Permisos")
        self.checkTodo = QCheckBox("Todo")

        # conexiones de los checks
        self.checkJustificacion.clicked.connect(self.seleccionTipoReporte)
        self.checkAsistencia.clicked.connect(self.seleccionTipoReporte)
        self.checkPermiso.clicked.connect(self.seleccionTipoReporte)
        self.checkTodo.clicked.connect(self.SeleccionTodoTipoReporte)

        layoutTipoReporte.addWidget(self.checkJustificacion)
        layoutTipoReporte.addWidget(self.checkAsistencia)
        layoutTipoReporte.addWidget(self.checkPermiso)
        layoutTipoReporte.addWidget(self.checkTodo)
        groupTipoReporte.setLayout(layoutTipoReporte)
        self.layout.addWidget(groupTipoReporte)

    def grupoRangoFechas(self):
        groupRangoFecha = QGroupBox("Rango de Fechas (Opcional)")
        layoutRangoFecha = QHBoxLayout()

        self.checkRangoFecha = QCheckBox("Aplicar rango de fechas")

        self.fechaInicio = QDateEdit(QDate.currentDate())
        self.fechaFin = QDateEdit(QDate.currentDate())

        self.fechaInicio.setEnabled(False)
        self.fechaFin.setEnabled(False)
        # conexiones
        self.checkRangoFecha.stateChanged.connect(self.SeleccionRangoFecha)
        self.fechaInicio.editingFinished.connect(self.validarFechaInicio)
        self.fechaFin.editingFinished.connect(self.validarFechaFin)

        layoutRangoFecha.addWidget(self.checkRangoFecha)
        layoutRangoFecha.addWidget(QLabel("Desde:"))
        layoutRangoFecha.addWidget(self.fechaInicio)
        layoutRangoFecha.addWidget(QLabel("Hasta:"))
        layoutRangoFecha.addWidget(self.fechaFin)
        groupRangoFecha.setLayout(layoutRangoFecha)
        self.layout.addWidget(groupRangoFecha)

    def grupoGenerarReporte(self):
        # Grupo para nombre y ubicación del archivo
        groupArchivo = QGroupBox("Opciones de Archivo")
        layoutArchivo = QVBoxLayout()

        # Nombre del archivo
        layoutNombreArchivo = QHBoxLayout()
        layoutNombreArchivo.addWidget(QLabel("Nombre del archivo:"))
        self.inputNombreArchivo = QLineEdit()
        self.inputNombreArchivo.setPlaceholderText(
            "Dejar en blanco para nombre generado automáticamente"
        )
        layoutNombreArchivo.addWidget(self.inputNombreArchivo)
        layoutArchivo.addLayout(layoutNombreArchivo)

        # Tipo de archivo
        layoutTipoArchivo = QHBoxLayout()
        layoutTipoArchivo.addWidget(QLabel("Tipo de archivo:"))
        self.cmbTipoArchivo = QComboBox()

        self.cmbTipoArchivo.addItem("PDF", "pdf")
        self.cmbTipoArchivo.addItem("DOCX", "docx")
        self.cmbTipoArchivo.addItem("CSV", "csv")

        layoutTipoArchivo.addWidget(self.cmbTipoArchivo)
        layoutArchivo.addLayout(layoutTipoArchivo)

        # Ruta de guardado
        layoutRuta = QHBoxLayout()
        self.inputRuta = QLineEdit()
        self.inputRuta.setPlaceholderText("Seleccione una ruta para guardar el reporte")
        btnBuscarRuta = QPushButton("Examinar...")
        btnBuscarRuta.setObjectName("btnexaminar")
        btnBuscarRuta.setMinimumSize(150, 30)

        btnBuscarRuta.clicked.connect(self.BuscarRuta)
        layoutRuta.addWidget(self.inputRuta)
        layoutRuta.addWidget(btnBuscarRuta)
        layoutArchivo.addLayout(layoutRuta)

        groupArchivo.setLayout(layoutArchivo)
        self.layout.addWidget(groupArchivo)

    def cargarComboboxDepartamento(self):
        result = self.depaServices.obtenerTodoDepartamento()
        if not result["success"]:
            dial = DialogoEmergente("", "Ocurrio un error de conexion.", "Error", True)
            dial.exec()
            self.reject()
            return

        departamentos = result["listaDepa"]
        if len(departamentos) == 0:
            dial = DialogoEmergente("", "No existen departamentos.", "Error", True)
            dial.exec()
            return

        for depa in departamentos:
            self.cmbDepartamento.addItem(depa.nombre, depa.id)

    def cargarComboboxRol(self):
        result = self.rolServices.obtener_todo_roles()

        if not result["success"]:
            dial = DialogoEmergente("", "Ocurrio un error de conexion.", "Error", True)
            dial.exec()
            self.reject()
            return

        roles = result["data"]["listaRoles"]
        if len(roles) == 0:
            dial = DialogoEmergente("", "No existen roles.", "Error", True)
            dial.exec()
            return

        for rol in roles:
            self.cmbRol.addItem(rol.nombre, rol.id)

    def cargarComboboxEmpleados(self):
        result = self.empleServices.list_empleados_todos()
        if not result["success"]:
            dial = DialogoEmergente("", "Ocurrio un error de conexion.", "Error", True)
            dial.exec()
            self.reject()
            return

        empleados = result["listaEmpleados"]
        if len(empleados) == 0:
            dial = DialogoEmergente("", "No existen empleados.", "Error", True)
            dial.exec()
            return

        for datos in empleados:
            id_empleado = datos["id_empleado"]
            persona = datos["persona"]
            self.cmbEmpleado.addItem(
                f"{persona.nombre +' '+persona.apellidos} - {persona.cedula}",
                id_empleado,
            )

    def validarFechaInicio(self):
        fechaInicio = self.fechaInicio.date().toString("yyyy-MM-dd")
        fechaFin = self.fechaFin.date().toString("yyyy-MM-dd")

        if fechaInicio > fechaFin:
            self.fechaInicio.setDate(self.fechaFin.date())

    def validarFechaFin(self):
        fechaInicio = self.fechaInicio.date().toString("yyyy-MM-dd")
        fechaFin = self.fechaFin.date().toString("yyyy-MM-dd")

        if fechaInicio > fechaFin:
            self.fechaFin.setDate(self.fechaInicio.date())

    def SeleccionTodoTipoReporte(self):
        """Activa/desactiva todos los checkboxes de tipo de reporte"""
        checked = self.checkTodo.isChecked()

        self.checkJustificacion.setChecked(checked)
        self.checkAsistencia.setChecked(checked)
        self.checkPermiso.setChecked(checked)

    def seleccionTipoReporte(self):
        asistencias = self.checkAsistencia.isChecked()
        justificacion = self.checkJustificacion.isChecked()
        permiso = self.checkPermiso.isChecked()
        if asistencias and justificacion and permiso:
            self.checkTodo.setChecked(True)
            return
        self.checkTodo.setChecked(False)

    def SeleccionRangoFecha(self, state):
        """Activa/desactiva los date edits según el checkbox"""
        enabled = state == 2
        self.fechaInicio.setEnabled(enabled)
        self.fechaFin.setEnabled(enabled)

    def BuscarRuta(self):
        """Abre el diálogo para seleccionar la ruta de guardado"""
        path = QFileDialog.getExistingDirectory(self, "Seleccionar directorio")
        if path:
            self.inputRuta.setText(path)

    def validarTiposReportes(self):
        asistencias = self.checkAsistencia.isChecked()
        justificacion = self.checkJustificacion.isChecked()
        permiso = self.checkPermiso.isChecked()
        todo = self.checkTodo.isChecked()
        if not asistencias and not justificacion and not permiso and not todo:
            return False
        return True

    def obtenerDatosReporte(self):
        # empleado seleccionado
        empleado = self.cmbEmpleado.currentData()

        # empleado seleccionar departamento o rol
        departamento = self.cmbDepartamento.currentData()
        rol = self.cmbRol.currentData()

        # tipo de reportes seleccionados
        asistencias = self.checkAsistencia.isChecked()
        justificacion = self.checkJustificacion.isChecked()
        permiso = self.checkPermiso.isChecked()
        todo = self.checkTodo.isChecked()

        # rango de fechas seleccionadas
        fechaIncio = (
            self.fechaInicio.date().toString("yyyy-MM-dd")
            if self.checkRangoFecha.isChecked()
            else None
        )
        fechaFin = (
            self.fechaFin.date().toString("yyyy-MM-dd")
            if self.checkRangoFecha.isChecked()
            else None
        )

        # datos del archivo reporte
        nombre = (
            self.inputNombreArchivo.text()
            or f"reporte-{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}"
        )
        extencion = self.cmbTipoArchivo.currentData()
        ruta = self.inputRuta.text()

        # mostrar el nombre predeterminado
        self.inputNombreArchivo.setText(nombre)

        tipoReporte = []

        if asistencias:
            tipoReporte.append("justificacion")

        if justificacion:
            tipoReporte.append("asistencias")

        if permiso:
            tipoReporte.append("permisos")

        return {
            "nombre_reporte": nombre,
            "extencion": extencion,
            "ruta": ruta,
            "tipoReporte": tipoReporte,
            "id_departamento": departamento,
            "id_rol": rol,
            "id_empleado": empleado,
            "rangoFechas": [fechaIncio, fechaFin] if fechaIncio and fechaFin else None,
        }

    def generaReporte(self):

        datos = self.obtenerDatosReporte()
        print(datos)
        # Se valida que el tipo de archivo seleccionado sea valido o soportado
        if datos["extencion"] not in ["pdf", "docx", "csv"]:
            dial = DialogoEmergente(
                "",
                "El tipo de archivo seleccionado no es válido.",
                "Error",
                True,
                False,
            )
            dial.exec()
            return

        # se valida antes de generar reporte
        if not self.validarTiposReportes():
            dial = DialogoEmergente(
                "", f"Debes seleccionar el tipo de reporte.", "Error", True, False
            )
            dial.exec()
            return
        # se valida que la ruta sea seleccionada
        if not datos["ruta"]:
            dial = DialogoEmergente(
                "",
                "Debes seleccionar una ruta para guardar el reporte.",
                "Error",
                True,
                False,
            )
            dial.exec()
            return

        if not os.path.exists(datos["ruta"]):
            dial = DialogoEmergente(
                "",
                f"La ruta '{datos['ruta']}' para guardar el documento no existe.",
                "Error",
                True,
                False,
            )
            dial.exec()
            return

        if os.path.isfile(
            os.path.join(
                datos["ruta"], f"{datos['nombre_reporte']}.{datos['extencion']}"
            )
        ):
            dial = DialogoEmergente(
                "",
                f"Ya existe un documento en la misma ruta con el mismo nombre y formato: '{os.path.join(datos['ruta'], f'{datos['nombre_reporte']}.{datos['extencion']}')}'",
                "Error",
                True,
                False,
            )
            dial.exec()
            return

        # genera reporte
        resultado = self.reporteServices.crear_reporte(**datos)
        if resultado["success"]:
            dial = DialogoEmergente(
                "", "Se genero el reporte correctamente.", "Check", True, False
            )
            dial.exec()
            self.reject()
            return

        if not resultado["success"]:
            dial = DialogoEmergente("", resultado["message"], "Error", True, False)
            dial.exec()
            return
