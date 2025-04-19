from datetime import datetime
from PySide6.QtWidgets import *
from PySide6.QtCore import QDate
from Utils.Utils import cargar_estilos
from services.empleadoServices import EmpleadoServices

class GenerarReporte(QDialog):
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Generar Reporte")

        # Layout principal
        layout = QVBoxLayout()

        cargar_estilos('claro','formReporte.css',self)
        
        # Grupo para selección de empleado
        groupEmpleado = QGroupBox("Selección de Empleado")
        layoutEmpleado = QVBoxLayout()
        
        self.cmbEmpleado = QComboBox()
        self.cmbEmpleado.addItem("Todos los empleados",None)
        
        layoutEmpleado.addWidget(self.cmbEmpleado)
        groupEmpleado.setLayout(layoutEmpleado)
        layout.addWidget(groupEmpleado)
        
        # Grupo para tipo de reporte
        groupTipoReporte = QGroupBox("Tipo de Reporte")
        layoutTipoReporte = QVBoxLayout()
        
        self.checkJustificacion = QCheckBox("Justificaciones")
        self.checkAsistencia    = QCheckBox("Asistencias")
        self.checkPermiso       = QCheckBox("Permisos")
        self.checkTodo          = QCheckBox("Todo")
        self.checkTodo.stateChanged.connect(self.SeleccionTodoTipoReporte)
        
        layoutTipoReporte.addWidget(self.checkJustificacion)
        layoutTipoReporte.addWidget(self.checkAsistencia)
        layoutTipoReporte.addWidget(self.checkPermiso)
        layoutTipoReporte.addWidget(self.checkTodo)
        groupTipoReporte.setLayout(layoutTipoReporte)
        layout.addWidget(groupTipoReporte)
        
        # Grupo para rango de fechas
        groupRangoFecha = QGroupBox("Rango de Fechas (Opcional)")
        layoutRangoFecha = QHBoxLayout()
        
        self.checkRangoFecha = QCheckBox("Aplicar rango de fechas")
        self.checkRangoFecha.stateChanged.connect(self.SeleccionRangoFecha)
        
        self.fechaInicio = QDateEdit(QDate.currentDate())
        self.fechaInicio.setEnabled(False)
        self.fechaFin = QDateEdit(QDate.currentDate())
        self.fechaFin.setEnabled(False)


        self.fechaInicio.editingFinished.connect(self.validarFechaInicio)
        self.fechaFin.editingFinished.connect(self.validarFechaFin)
        
        layoutRangoFecha.addWidget(self.checkRangoFecha)
        layoutRangoFecha.addWidget(QLabel("Desde:"))
        layoutRangoFecha.addWidget(self.fechaInicio)
        layoutRangoFecha.addWidget(QLabel("Hasta:"))
        layoutRangoFecha.addWidget(self.fechaFin)
        groupRangoFecha.setLayout(layoutRangoFecha)
        layout.addWidget(groupRangoFecha)
        
        # Grupo para nombre y ubicación del archivo
        groupArchivo = QGroupBox("Opciones de Archivo")
        layoutArchivo = QVBoxLayout()
        
        # Nombre del archivo
        layoutNombreArchivo = QHBoxLayout()
        layoutNombreArchivo.addWidget(QLabel("Nombre del archivo:"))
        self.inputNombreArchivo = QLineEdit()
        self.inputNombreArchivo.setPlaceholderText("Dejar en blanco para nombre generado automáticamente")
        layoutNombreArchivo.addWidget(self.inputNombreArchivo)
        layoutArchivo.addLayout(layoutNombreArchivo)
        
        # Tipo de archivo
        layoutTipoArchivo = QHBoxLayout()
        layoutTipoArchivo.addWidget(QLabel("Tipo de archivo:"))
        self.cmbTipoArchivo = QComboBox()
        self.cmbTipoArchivo.addItems(["PDF", "DOCX", "CSV"])
        layoutTipoArchivo.addWidget(self.cmbTipoArchivo)
        layoutArchivo.addLayout(layoutTipoArchivo)
        
        # Ruta de guardado
        layoutRuta = QHBoxLayout()
        self.inputRuta = QLineEdit()
        self.inputRuta.setPlaceholderText("Seleccione una ruta para guardar el reporte")
        btnBuscarRuta = QPushButton("Examinar...")
        btnBuscarRuta.setMinimumSize(50, 20)

        btnBuscarRuta.clicked.connect(self.BuscarRuta)
        layoutRuta.addWidget(self.inputRuta)
        layoutRuta.addWidget(btnBuscarRuta)
        layoutArchivo.addLayout(layoutRuta)
        
        groupArchivo.setLayout(layoutArchivo)
        layout.addWidget(groupArchivo)
        
        # Botones de acción
        layoutBotones = QHBoxLayout()
        self.btnGenerar = QPushButton("Generar Reporte")
        self.btnCancelar = QPushButton("Cancelar")
        self.btnCancelar.clicked.connect(self.reject)
        
        layoutBotones.addWidget(self.btnGenerar)
        layoutBotones.addWidget(self.btnCancelar)
        layout.addLayout(layoutBotones)
        self.setLayout(layout)
        
    def validarFechaInicio(self):
        fechaInicio = self.fechaInicio.date().toString('yyyy-MM-dd')
        fechaFin    = self.fechaFin.date().toString('yyyy-MM-dd')

        if fechaInicio > fechaFin:
            self.fechaInicio.setDate(self.fechaFin.date()) 

    def validarFechaFin(self):
        fechaInicio = self.fechaInicio.date().toString('yyyy-MM-dd')
        fechaFin    = self.fechaFin.date().toString('yyyy-MM-dd')

        if fechaInicio > fechaFin:
            self.fechaFin.setDate(self.fechaInicio.date()) 

    def SeleccionTodoTipoReporte(self, state):
        """Activa/desactiva todos los checkboxes de tipo de reporte"""
        checked = state == 2  # 2 representa "checked" en Qt
        self.checkJustificacion.setChecked(checked)
        self.checkAsistencia.setChecked(checked)
        self.checkPermiso.setChecked(checked)
        
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
            
    def obtenerDatosReporte(self):
        """Recopila todos los datos ingresados en el formulario"""
        data = {
            "empleado": self.cmbEmpleado.currentText(),
            "tipoReporte": {
                "justificacion": self.checkJustificacion.isChecked(),
                "asistencia": self.checkAsistencia.isChecked(),
                "permisos": self.checkPermiso.isChecked(),
                "todo": self.checkTodo.isChecked()
            },
            "rangofecha": self.checkRangoFecha.isChecked(),
            "fechaInicio": self.fechaInicio.date().toString("yyyy-MM-dd"),
            "fechaFin": self.fechaFin.date().toString("yyyy-MM-dd"),
            "nombreReporte": self.inputNombreArchivo.text() or f"reporte-{datetime.now().strftime('%Y-%m-%d-%H-%M')}",
            "tipoArchivo": self.cmbTipoArchivo.currentText().lower(),
            "ruta": self.inputRuta.text()
        }
        
        return data