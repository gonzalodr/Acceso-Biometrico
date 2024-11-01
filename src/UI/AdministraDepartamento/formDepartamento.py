from PySide6.QtWidgets import *
from PySide6.QtCore import *
from Utils.Utils import *
from UI.DialogoEmergente import *
from services.departamentoService import *

class formDepartamento(QDialog):
    update:bool = False
    Pservices = DepartamentoServices()
    idP = 0
    
    def __init__(self, parent=None, titulo="Registrar Departamento.",id = None):
        
        super().__init__(parent)
        self.setObjectName("formDepartamento")
        self.setMinimumSize(QSize(700,650))
        self.setWindowFlags(Qt.FramelessWindowHint)
        add_Style(archivoQSS="formDepartamento.css",QObjeto=self)
        
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
        layoutForm.setVerticalSpacing(1)
        
        """Crean los labels, inputs y labels de error"""
        lblNombre = QLabel(text="Nombre")   
        self.inputNombre = QLineEdit()
        self.inputNombre.setPlaceholderText("Ingrese su nombre")
        self.inputNombre.installEventFilter(self)
        self.errorNombre =QLabel()
        Sombrear(self.inputNombre,20,0,0)
        
        lblDescripcion = QLabel(text="Descripcion")
        self.inputDescripcion = QLineEdit()
        self.inputDescripcion.setPlaceholderText("Ingrese la descripcion")
        self.inputDescripcion.installEventFilter(self)
        self.errorDescripcion =QLabel()
        Sombrear(self.inputDescripcion,20,0,0)
        
        layoutForm.addLayout(self._contenedor(lblNombre,self.inputNombre,self.errorNombre),0,0)
        layoutForm.addLayout(self._contenedor(lblDescripcion,self.inputDescripcion,self.errorDescripcion),1,0)
        
        boton_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        boton_box.button(QDialogButtonBox.Cancel).setText("Cancelar")
        boton_box.button(QDialogButtonBox.Cancel).setObjectName("btncancelar")
        boton_box.button(QDialogButtonBox.Cancel).setMinimumSize(QSize(100,30))
        
        boton_box.button(QDialogButtonBox.Ok).setText("Registrar" if id == None else "Actualizar")
        boton_box.button(QDialogButtonBox.Ok).setObjectName("btnregistrar")
        boton_box.button(QDialogButtonBox.Ok).setMinimumSize(QSize(100,30))
        Sombrear(boton_box,20,0,5)
        # Centrar los botones
        boton_layout = QHBoxLayout()
        boton_layout.addStretch()
        boton_layout.addWidget(boton_box)
        boton_layout.addStretch()
      
        layoutFrame.addLayout(layoutForm)
        layoutFrame.addLayout(boton_layout)
        
        boton_box.accepted.connect(self._accion_departamento)
        boton_box.rejected.connect(self._cancelar_registro)        

        frame.setLayout(layoutFrame)
        layout = QVBoxLayout()
        layout.setContentsMargins(0,0,0,0)
        layout.addWidget(frame)
        self.setLayout(layout)
        Sombrear(self,30,0,0,"green")
        
         
        """Aqui se revisa si el formulario recibio un id por parametros"""
        if id:
            self._obtener_registroId(id)##carga los inputs con los datos de la consulta obtener por id
            
        """Esto no se toca"""  
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
    
    """Solo lo hice para que al pasar el cursor por un inpunt muestre un mesaje
        no es tan necesario lo pueden dejar a como esta
    """            
    def eventFilter(self, source, event):
        if event.type() == 10:  # Enter (Mouse Enter)
            if isinstance(source, QLineEdit): 
                text = source.placeholderText()
                QToolTip.showText(event.globalPos(),text, source)
        elif event.type() == 11:  # Leave (Mouse Leave)
            if isinstance(source, QLineEdit):
                QToolTip.hideText()
        return super().eventFilter(source, event)
    
    def _cancelar_registro(self):
        
        """Si se encuentra inputs con datos entonces pregunta si esta seguro retirarse"""
        if self._validar_inputs_sin_con_datos():
            dialEmergente = DialogoEmergente("¿?","¿Estas seguro que que quieres cancelar?","Question",True,True)
            opcion = dialEmergente.exec()
            if opcion == QDialog.Accepted:
                self.reject()
            elif opcion == QDialog.Rejected:
                print("Se rechazó el diálogo.")
        else:##si los inputs estan sin datos entonces cierra el formulario de manera normal
            self.reject()##cerrar la ventana
            
            
    """Este metodo se usa para la funcion
        accion persona lo cual se encarga de insertar o actualizar en bd
    """        
    def _validar_campos(self):
        # Verifica si los campos requeridos están vacíos entonces muestra una alerta
        if self._validar_inputs_vacios():
            dialEmergente = DialogoEmergente("Advertencia","Llene todos los campos.","Warning")
            dialEmergente.exec()
            return False
        else:
            return True
        
    """Reviza que los inputs esten llenados antes de insertar
        se usa en la funcion _validar_campos
    """
    def _validar_inputs_vacios(self):
        vacios:bool = False
            
        if not self.inputNombre.text().strip(): ##si no tienes datos, los sombres de rojo
            Sombrear(self.inputNombre,20,0,0,"red")
            vacios = True
        else:
            Sombrear(self.inputNombre,20,0,0) ##de lo contrario los regresa al estado normal
            
        if not self.inputDescripcion.text().strip():
            Sombrear(self.inputDescripcion,20,0,0,"red")
            vacios = True
        else:
            Sombrear(self.inputDescripcion,20,0,0)            
        return vacios
      
    def _validar_inputs_sin_con_datos(self):
        if self.inputNombre.text().strip() or self.inputDescripcion.text().strip():
            return True
        else:
            return False
        
    def _obtener_registroId(self, id):
        result = self.Pservices.obtenerDepartamentoPorId(id)
        if result["success"]:
            if result["data"]:
                departamento:Departamento = result["data"]
                ##guarda ele ide para saber que registro se va a modifcar
                self.idP = departamento.id
                ##llena los inputs
                self.inputNombre.setText(departamento.nombre)
                self.inputDescripcion.setText(departamento.descripcion)
                
            else:
                dial = DialogoEmergente("Error","Hubo un error de carga.","Error")
                dial.exec()
                QTimer.singleShot(0, self.reject)
                return None
        else:
            dial = DialogoEmergente("Error","Hubo un error de carga.","Error")
            dial.exec()
            QTimer.singleShot(0, self.reject)
            return None
        
    def _accion_departamento(self):

        departament:Departamento = Departamento(
            nombre = self.inputNombre.text(),
            descripcion= self.inputDescripcion.text(),
            id=self.idP,
        )
               
        if self.idP > 0:##si el atributo idP es mayor a 0 quiere decir que se va actualizar 
                result = self.Pservices.modificarDepartamento(departament)
                print(result)
                if result["success"]:
                    dial = DialogoEmergente("Actualización",result["message"],"Check")
                    dial.exec()
                    self.reject()
                else:
                    dial = DialogoEmergente("Erro","Error al actualizar departamento","Error")
                    dial.exec()
        else:#de lo contrario lo toma como un crear
                result = self.Pservices.insertarDepartamento(departament)
                print(result)
                if result["success"]:
                    dial = DialogoEmergente("Registrar","Departamento registrado exitosamente","Check")
                    dial.exec()
                    self.reject()
                else:
                    dial = DialogoEmergente("Erro","Error al registrar el departamento","Error")
                    dial.exec()
        
