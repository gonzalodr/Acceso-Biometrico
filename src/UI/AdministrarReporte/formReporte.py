from PySide6.QtWidgets import *
from PySide6.QtCore import *
from Utils.Utils import *
from UI.DialogoEmergente import *
from services.reporteService import *
from services.empleadoServices import *
from settings.variable import *

class formReporte(QDialog):
    reporteServices =  ReporteServices ()
    empleadoServices = EmpleadoServices()
    idP = 0
    listaEmpleadosID = {}
    
    def __init__(self, parent=None, titulo="Registrar reporte.",id = None):
        super().__init__(parent)
        self.setObjectName("form")
        self.setMinimumSize(QSize(700/2,650/2))
        self.setWindowFlags(Qt.FramelessWindowHint)
        # add_Style(archivoQSS="form.css",QObjeto=self)
        cargar_estilos('claro','form.css',self)


        frame = QFrame()
        layoutFrame = QVBoxLayout()
        frame.setObjectName("formFrame")
        layoutFrame.setContentsMargins(10,20,10,20)
        layoutFrame.setSpacing(10)
        

        lblTitulo = QLabel(text=titulo)
        lblTitulo.setObjectName("titulo")
        lblTitulo.setAlignment(Qt.AlignCenter)
        layoutFrame.addWidget(lblTitulo)
        
        layoutForm = QGridLayout()
        layoutForm.setContentsMargins(20,10,20,20)
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
        lblFecha = QLabel("Fecha de Creación:")
        self.inputFecha = QDateEdit()
        self.inputFecha.setCalendarPopup(True)
        self.inputFecha.setDate(QDate.currentDate())
        self.inputFecha.setMinimumDate(QDate.currentDate())  # Bloquear fechas anteriores
        self.inputFecha.setMaximumDate(QDate.currentDate())  # Bloquear fechas posteriores
        # Acceder al QCalendarWidget asociado al QDateEdit
        self.calendar = self.inputFecha.calendarWidget()
        self.calendar.setMinimumDate(QDate.currentDate())  # Bloquear fechas anteriores
        self.calendar.setMaximumDate(QDate.currentDate())  # Bloquear fechas posterio
        layoutForm.addWidget(lblFecha, 1, 0)
        layoutForm.addWidget(self.inputFecha, 2, 0)
        Sombrear(self.inputFecha, 20, 0, 0)

        # Tipo de reporte
        lblTipo = QLabel(text="Tipo de Reporte:")
        self.inputTipo = QComboBox()
        self.inputTipo.addItems(["Incidencia", "Informe", "Solicitud", "Otro"])  # Tipos de reportes
        self.errorTipo = QLabel(text="")
        Sombrear(self.inputTipo, 20, 0, 0)

        # Contenido del reporte
        lblContenido = QLabel(text="Contenido del Reporte:")
        self.inputContenido = QTextEdit()
        layoutForm.addWidget(lblContenido, 4, 0, 1, 2)
        layoutForm.addWidget(self.inputContenido, 5, 0, 1, 2)
        Sombrear(self.inputContenido, 20, 0, 0)

        layoutForm.addLayout(self._contenedor(lblEmpleado, self.inputEmpleado, self.errorEmpleado), 0, 0)
        layoutForm.addLayout(self._contenedor(lblTipo, self.inputTipo, self.errorTipo), 3, 0)
        
        boton_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        boton_box.button(QDialogButtonBox.Cancel).setText("Cancelar")
        boton_box.button(QDialogButtonBox.Cancel).setObjectName("btncancelar")
        boton_box.button(QDialogButtonBox.Cancel).setMinimumSize(QSize(100,30))

        boton_box.button(QDialogButtonBox.Ok).setText("Registrar" if id == None else "Actualizar")
        boton_box.button(QDialogButtonBox.Ok).setObjectName("btnregistrar")
        boton_box.button(QDialogButtonBox.Ok).setMinimumSize(QSize(100,30))
        Sombrear(boton_box,20,0,5)
        
      #Centrar los botones
        boton_layout = QHBoxLayout()
        boton_layout.addStretch()
        boton_layout.addWidget(boton_box)
        boton_layout.addStretch()
      
        layoutFrame.addLayout(layoutForm)
        layoutFrame.addLayout(boton_layout)
        
        boton_box.accepted.connect(self._accion_reporte)
        boton_box.rejected.connect(self._cancelar_registro)
        
        frame.setLayout(layoutFrame)
        layout = QVBoxLayout()
        layout.setContentsMargins(0,0,0,0)
        layout.addWidget(frame)
        self.setLayout(layout)
        Sombrear(self,30,0,0,"green")  
        
        ##if id:
          #  self._obtener_registroId(id)
        
        layoutFrame.addLayout(layoutForm)  # Agregar formulario al layout principal

        # Definir layout del QDialog
        self.setLayout(layoutFrame)
    
        layoutForm.addLayout(self._contenedor(lblEmpleado,self.inputEmpleado,self.errorEmpleado),0,0)
        #layoutForm.addWidget(self.error,1,0)    
        
        self._cargar_empleados()
        #self._verificar_permiso()
       # self.inputTabla.currentIndexChanged.connect(self._verificar_permiso)
        #self.inputEmpleado.currentIndexChanged.connect(self._verificar_permiso)
            
    def _contenedor(self,label:QLabel,input,label_error:QLabel):
        layout = QVBoxLayout()
        layout.setContentsMargins(0,0,0,0)
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
    
    def _cancelar_registro(self):
        if not self._validar_inputs_vacios():
            dialEmergente = DialogoEmergente("¿Estas seguro que que quieres cancelar?","Question",True,True)
            opcion = dialEmergente.exec()
            if opcion == QDialog.Accepted:
                 self.reject()
            elif opcion == QDialog.Rejected:
                pass
        else:
             self.reject()##cerrar la ventana

    def _cargar_empleados(self):
        result = self.empleadoServices.obtener_todo_empleados()
        if result["success"]:
            listaEmpleados = result["data"]["listaEmpleados"]
            if len(listaEmpleados) > 0:
                for empleado in listaEmpleados:
                    self.inputEmpleado.addItem(str(empleado.id_persona))
                    #self.listaEmpleadosID[empleado.id_persona] = empleado.id
                    self.listaEmpleadosID[str(empleado.id_persona)] = empleado.id  # Usar id_persona 
            else:
                dialEmergente = DialogoEmergente("","Ocurrio un error","Error")
                if dialEmergente.exec() == QDialog.Accepted:
                    self.reject()
        else:
            print(f'\nError:\n{e}\n----------------------\n')
            self.reject()
             
    def _validar_inputs_vacios(self):
         empleado = self.inputEmpleado.currentText().strip()
         fecha = self.inputFecha.date().toString("yyyy-MM-dd").strip()
         tipo = self.inputTipo.currentText().strip()
         contenido = self.inputContenido.toPlainText().strip()

         if not empleado or not fecha or not tipo or not contenido:
            return True  # Hay campos vacíos
         return False  # Todos los campos están llenos
     
     
    def _obtener_registroId(self, id):
        result = self.reporteServices.obtenerReportePorId(id)
        if result["success"]:
            if result["data"]:
                perfil = result["data"]
                self.idP = perfil.id
                self.inputEmpleado.setText(perfil.nombre)
                self.inputFecha.setText(perfil.descripcion)
                self.inputTipo.setText(perfil.nombre)
                self.inputContenido.setText(perfil.descripcion)
                
            else:
                dial = DialogoEmergente("Error", "Hubo un error de carga.", "Error")
                dial.exec()
                QTimer.singleShot(0, self.reject)
        else:
            dial = DialogoEmergente("Error", "Hubo un error de carga.", "Error")
            dial.exec()
            QTimer.singleShot(0, self.reject)
            
    def _accion_reporte(self):       
        reporte : Reporte = Reporte(
            #id_empleado=self.listaEmpleadosID[self.inputEmpleado.currentText()],
            id_empleado=self.listaEmpleadosID[self.inputEmpleado.currentText()],
            fecha_generacion=self.inputFecha.date().toString("yyyy-MM-dd"),
            tipo_reporte=self.inputTipo.currentText(),
            contenido=self.inputContenido.toPlainText(),
            id=self.idP,
        )
        
        if self.idP > 0:
            result = self.reporteServices.modificarReporte(reporte)
            if result["success"]:
                dial = DialogoEmergente("Actualización", result["message"], "Check")
                dial.exec()
                self.reject()
            else:
                dial = DialogoEmergente("Error", "Error al actualizar el perfil", "Error")
                dial.exec()
        else:
            result = self.reporteServices.insertarReporte(reporte)
            if result["success"]:
                dial = DialogoEmergente("Registrar", "Reporte registrado exitosamente", "Check")
                dial.exec()
                self.reject()
            else:
                dial = DialogoEmergente("Error", "Error al registrar el Reporte", "Error")
                dial.exec()