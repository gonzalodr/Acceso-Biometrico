
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from Utils.Utils import *
from UI.DialogoEmergente import *
from services.permisosRolServices import *
from services.rolService import *
from settings.variable import *

class formPermiso(QDialog):
    update:bool = False 
    permisosServices = PermisosRolServices() 
    idP = 0 
    fotografia = None
    ##constructor
    def __init__(self, parent=None, titulo="Registrar permiso.",id = None):
        super().__init__(parent)
        self.setObjectName("form")
        self.setMinimumSize(QSize(700/2,650/2))
        self.setWindowFlags(Qt.FramelessWindowHint)
        add_Style(archivoQSS="form.css",QObjeto=self)
        
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

        """ 
            Aqui cargar el combo box de registros
        """
        lblRol = QLabel(text="Seleccionar rol")   
        self.inputRol = QComboBox()
        self.errorRol = QLabel(text="")
        
        
        #permisos para dicha tabla
        lblAcceso = QLabel(text="Acceso a")
        self.inputTabla = QComboBox()
        self.inputTabla.addItems(ACCESO_TABLE.keys())
        self.errorTabla = QLabel(text="")
        
        self.checkVer = QCheckBox("permiso ver")
        Sombrear(self.checkVer,30,0,5)
        
        self.checkCrear = QCheckBox("permiso crear")
        Sombrear(self.checkCrear,30,0,5)
        
        self.checkEditar = QCheckBox("permiso editar")
        Sombrear(self.checkEditar,30,0,5)

        self.checkEliminar = QCheckBox("permiso eliminar")
        Sombrear(self.checkEliminar,30,0,5)

        layoutForm.addLayout(self._contenedor(lblRol,self.inputRol,self.errorRol),0,0)
        layoutForm.addLayout(self._contenedor(lblAcceso,self.inputTabla,self.errorTabla),1,0)
        layoutForm.addWidget(self.checkVer,2,0)
        layoutForm.addWidget(self.checkCrear,3,0)
        layoutForm.addWidget(self.checkEditar,4,0)
        layoutForm.addWidget(self.checkEliminar,5,0)        
        
        
        
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
        
        boton_box.accepted.connect(self._accion_permiso)
        boton_box.rejected.connect(self._cancelar_registro)        

        frame.setLayout(layoutFrame)
        layout = QVBoxLayout()
        layout.setContentsMargins(0,0,0,0)
        layout.addWidget(frame)
        self.setLayout(layout)
        Sombrear(self,30,0,0,"green")
        
        """Aqui se revisa si el formulario recibio un id por parametros"""
        if id:
            self._obtener_registroId(id)

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
        # if self._validar_inputs_sin_con_datos():
        #     dialEmergente = DialogoEmergente("¿?","¿Estas seguro que que quieres cancelar?","Question",True,True)
        #     opcion = dialEmergente.exec()
        #     if opcion == QDialog.Accepted:
        #         self.reject()
        #     elif opcion == QDialog.Rejected:
        #         print("Se rechazó el diálogo.")
        # else:##si los inputs estan sin datos entonces cierra el formulario de manera normal
        #     self.reject()##cerrar la ventana
        pass
                
    def _validar_campos(self):
        # Verifica si los campos requeridos están vacíos entonces muestra una alerta
        # if self._validar_inputs_vacios():
        #     dialEmergente = DialogoEmergente("Advertencia","Llene todos los campos.","Warning")
        #     dialEmergente.exec()
        #     return False
        # else:
        #     return True
        pass

    def _validar_inputs_vacios(self):
        # vacios:bool = False
            
        # if not self.inputNombre.text().strip(): ##si no tienes datos, los sombres de rojo
        #     Sombrear(self.inputNombre,20,0,0,"red")
        #     vacios = True
        # else:
        #     Sombrear(self.inputNombre,20,0,0) ##de lo contrario los regresa al estado normal
            
        # if not self.inputApellido1.text().strip():
        #     Sombrear(self.inputApellido1,20,0,0,"red")
        #     vacios = True
        # else:
        #     Sombrear(self.inputApellido1,20,0,0)
            
        # if not self.inputApellido2.text().strip():
        #     Sombrear(self.inputApellido2,20,0,0,"red")
        #     vacios = True
        # else:
        #     Sombrear(self.inputApellido2,20,0,0)
            
        # if not self. inputCedula.text().strip():
        #     Sombrear(self.inputCedula,20,0,0,"red")
        #     vacios = True
        # else:
        #     Sombrear(self.inputCedula,20,0,0)
            
        # if not self.inputNacimiento.date().toString("yyyy-MM-dd"):
        #     Sombrear(self.inputNacimiento,20,0,0,"red")
        #     vacios = True
        # else:
        #     Sombrear(self.inputNacimiento,20,0,0)
            
        # if not self.inputCorreo.text().strip():
        #     Sombrear(self.inputCorreo,20,0,0,"red") 
        #     vacios = True
        # else:
        #     Sombrear(self.inputCorreo,20,0,0)
            
        # if not self.inputEstCivil.currentText():
        #     Sombrear(self.inputEstCivil,20,0,0,"red")
        #     vacios = True
        # else:
        #     Sombrear(self.inputEstCivil,20,0,0)
            
        # if not self.inputDireccion.toPlainText().strip():
        #     Sombrear(self.inputDireccion,20,0,0,"red")
        #     vacios = True
        # else:
        #     Sombrear(self.inputDireccion,20,0,0)
        # return vacios
        pass



    def _validar_inputs_sin_con_datos(self):
        # if self.inputNombre.text().strip() or self.inputApellido1.text().strip() or self.inputApellido2.text().strip() or self. inputCedula.text().strip() or self.inputCorreo.text().strip() or self.inputDireccion.toPlainText().strip():
        #     return True
        # else:
        #     return False
        pass
    def _obtener_registroId(self, id):
        # result = self.permisosServices.obtenerPersonaPorId(id)
        # if result["success"]:
        #     if result["data"]:
        #         persona:Persona = result["data"]
        #         ##guarda ele ide para saber que registro se va a modifcar
        #         self.idP = persona.id
        #         ##llena los inputs
        #         self.fotografia = persona.foto
        #         self.inputNombre.setText(persona.nombre)
        #         self.inputApellido1.setText(persona.apellido1)
        #         self.inputApellido2.setText(persona.apellido2)
        #         self.inputNacimiento.setDate(QDate.fromString(str(persona.fecha_nacimiento), "yyyy-MM-dd"))
        #         self.inputCedula.setText(persona.cedula)
        #         self.inputCorreo.setText(persona.correo)
        #         self.inputDireccion.setPlainText(persona.direccion)
        #         self.inputEstCivil.setCurrentText(persona.estado_civil)
                
        #         self.btnFoto.setText("Eliminar foto " if self.fotografia is not None else "Seleccionar foto")
        #         if self.fotografia:
        #             pixmap = QPixmap()
        #             pixmap.loadFromData(self.fotografia)
        #             self.lblicono.setPixmap(pixmap.scaled(self.lblicono.size()))
        #             self.lblicono.show()
                    
        #     else:
        #         dial = DialogoEmergente("Error","Hubo un error de carga.","Error")
        #         dial.exec()
        #         QTimer.singleShot(0, self.reject)
        #         return None
        # else:
        #     dial = DialogoEmergente("Error","Hubo un error de carga.","Error")
        #     dial.exec()
        #     QTimer.singleShot(0, self.reject)
        #     return None
        pass
    def _accion_permiso(self):

        # person:Persona = Persona(
        #     nombre = self.inputNombre.text(),
        #     apellido1 = self.inputApellido1.text(),
        #     apellido2 = self.inputApellido2.text(),
        #     cedula = self.inputCedula.text(),
        #     fecha_nacimiento = self.inputNacimiento.date().toString("yyyy-MM-dd"),
        #     correo = self.inputCorreo.text(),
        #     estado_civil = self.inputEstCivil.currentText(),
        #     direccion=self.inputDireccion.toPlainText(),
        #     id=self.idP,
        #     foto = self.fotografia
        # )
        # if self._validar_campos():##valida si todos los campos necesarios estan llenos
        #     result = self.permisosServices.verificacionCorreo(correo=self.inputCorreo.text(),id=self.idP)
        #     if not result["success"]:
        #         self.errorCorreo.setText(result["message"])
        #         Sombrear(self.inputCorreo,20,0,0,"red")
        #         return
        #     result = self.permisosServices.validar_cedula(cedula=self.inputCedula.text(),id=self.idP)
        #     if not result["success"]:
        #         self.errorCedula.setText(result["message"])
        #         Sombrear(self.inputCedula,20,0,0,"red")
        #         return
               
        #     if self.idP > 0:##si el atributo idP es mayor a 0 quiere decir que se va actualizar 
        #         result = self.permisosServices.modificarPersona(person)
        #         if result["success"]:
        #             dial = DialogoEmergente("Actualización",result["message"],"Check")
        #             dial.exec()
        #             self.reject()
        #         else:
        #             dial = DialogoEmergente("Erro","Error al actualizar a la persona","Error")
        #             dial.exec()
        #     else:#de lo contrario lo toma como un crear
        #         result = self.permisosServices.insertarPersona(person)
        #         if result["success"]:
        #             dial = DialogoEmergente("Registrar","Persona registrada exitosamente","Check")
        #             dial.exec()
        #             self.reject()
        #         else:
        #             dial = DialogoEmergente("Erro","Error al registrar a la persona","Error")
        #             dial.exec()
        pass
