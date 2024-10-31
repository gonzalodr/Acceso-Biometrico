
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from Utils.Utils import *
from UI.DialogoEmergente import *
from services.personaService import *

class formPersona(QDialog):
    update:bool = False
    Pservices = PersonaServices()
    idP = 0
    fotografia = None
    def __init__(self, parent=None, titulo="Registrar persona.",id = None):
        super().__init__(parent)
        self.setObjectName("formPersona")
        self.setMinimumSize(QSize(700,650))
        self.setWindowFlags(Qt.FramelessWindowHint)
        add_Style(archivoQSS="formPersona.css",QObjeto=self)
        
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
        
        """LLenando lado derecho 8 inputs"""
        lblFoto = QLabel(text="Foto. (opcional)")
        self.lblicono = QLabel(text="")
        self.lblicono.setFixedSize(100,100)
        self.btnFoto = QPushButton(text="seleccionar foto")
        self.btnFoto.setMinimumHeight(35)
        self.btnFoto.clicked.connect(self._seleccionar_foto)
        
        layoutFoto = QHBoxLayout()
        layoutFoto.setContentsMargins(0,0,0,0)
        layoutFoto.addWidget(lblFoto)
        layoutFoto.addSpacing(5)
        layoutFoto.addWidget(self.btnFoto)
             
        
        
        lblNombre = QLabel(text="Nombre")   
        self.inputNombre = QLineEdit()
        self.inputNombre.setPlaceholderText("Ingrese su nombre")
        self.inputNombre.installEventFilter(self)
        self.errorNombre =QLabel()
        Sombrear(self.inputNombre,20,0,0)
        
        
        
        lblApellido1 = QLabel(text="Primer apellido")
        self.inputApellido1 = QLineEdit()
        self.inputApellido1.setPlaceholderText("Ingrese su primer apellido")
        self.inputApellido1.installEventFilter(self)
        self.errorApellido1 =QLabel()
        Sombrear(self.inputApellido1,20,0,0)
        
        lblApellido2 = QLabel(text="Segundo apellido")
        self.inputApellido2 = QLineEdit()
        self.inputApellido2.setPlaceholderText("Ingrese su segundo apellido")
        self.inputApellido2.installEventFilter(self)
        self.errorApellido2 =QLabel()
        Sombrear(self.inputApellido2,20,0,0)
        
        lblCedula = QLabel(text="Cedula")
        self.inputCedula = QLineEdit()
        self.inputCedula.setPlaceholderText("Ingrese su cédula")
        self.inputCedula.installEventFilter(self)
        self.inputCedula.editingFinished.connect(self._verificar_cedula)
        self.errorCedula =QLabel()
        Sombrear(self.inputCedula,20,0,0)
        
        layoutForm.addLayout(layoutFoto,0,0)
        layoutForm.addWidget(self.lblicono,1,0)
        layoutForm.addLayout(self._contenedor(lblNombre,self.inputNombre,self.errorNombre),2,0)
        layoutForm.addLayout(self._contenedor(lblApellido1,self.inputApellido1,self.errorApellido1),3,0)
        layoutForm.addLayout(self._contenedor(lblApellido2,self.inputApellido2,self.errorApellido2),4,0)
        layoutForm.addLayout(self._contenedor(lblCedula,self.inputCedula,self.errorCedula),5,0)
        
        """Llenando el lado izquierdo 8 inputs"""
        lblNacim = QLabel(text="Fecha Nacimiento")
        self.inputNacimiento = QDateEdit()
        self.inputNacimiento.setCalendarPopup(True)
        self.inputNacimiento.setDisplayFormat("yyyy-MM-dd")
        self.inputNacimiento.setMaximumDate(QDate.currentDate())
        self.errorNacimiento =QLabel()
        Sombrear(self.inputNacimiento,20,0,0)
        
        lblCorreo = QLabel(text="Correo. Ejemplo:persona@example.com")
        self.inputCorreo = QLineEdit()
        self.inputCorreo.setPlaceholderText("Ingrese su correo electrónico. Ejem: persona@example.com")
        self.inputCorreo.installEventFilter(self)
        self.inputCorreo.editingFinished.connect(self._verificar_correo)
        self.errorCorreo =QLabel()
        Sombrear(self.inputCorreo,20,0,0)
        
        lblEstCivil = QLabel(text="Estado Civil")
        self.inputEstCivil = QComboBox()
        self.inputEstCivil.addItems(["Soltero/a", "Casado/a", "Divorciado/a", "Viudo/a"])
        self.errorEstCivil =QLabel()
        Sombrear(self.inputEstCivil,20,0,0)
        
        lblDirecc = QLabel(text="Direccion")
        self.inputDireccion = QTextEdit()
        self.inputDireccion.setPlaceholderText("Ingrese su dirección completa")
        self.inputDireccion.setMaximumHeight(50)
        self.errorDireccion =QLabel()
        Sombrear(self.inputDireccion,20,0,0)
        
        layoutForm.addLayout(self._contenedor(lblNacim,self.inputNacimiento,self.errorNacimiento),2,1)
        layoutForm.addLayout(self._contenedor(lblCorreo,self.inputCorreo,self.errorCorreo),3,1)
        layoutForm.addLayout(self._contenedor(lblEstCivil,self.inputEstCivil,self.errorEstCivil),4,1)
        layoutForm.addLayout(self._contenedor(lblDirecc,self.inputDireccion,self.errorDireccion),5,1)
        
        
        """Acomodando el resto del layout
            Botones de guardar y cancelar
        """
        
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
        
        boton_box.accepted.connect(self._accion_persona)
        boton_box.rejected.connect(self._cancelar_registro)        

        frame.setLayout(layoutFrame)
        layout = QVBoxLayout()
        layout.setContentsMargins(0,0,0,0)
        layout.addWidget(frame)
        self.setLayout(layout)
        Sombrear(self,30,0,0,"green")
        if id:
            self._obtener_registroId(id)
      
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
    
    def _verificar_correo(self):
        correo = self.inputCorreo.text()
        if correo.strip():
            result = self.Pservices.verificacionCorreo(correo=correo,id=self.idP)
            if not result["success"]:
                self.errorCorreo.setText(result["message"])
                Sombrear(self.inputCorreo,20,0,0,"red")
            else:
                Sombrear(self.inputCorreo,20,0,0)
                self.errorCorreo.setText("")
    
    def _verificar_cedula(self):
        cedula = self.inputCedula.text()
        if cedula.strip():
            result = self.Pservices.validar_cedula(cedula=cedula,id=self.idP)
            if not result["success"]:
                self.errorCedula.setText(result["message"])
                Sombrear(self.inputCedula,20,0,0,"red")   
            else:
                Sombrear(self.inputCedula,20,0,0)
                self.errorCedula.setText("")
                  
    def _seleccionar_foto(self):
        if self.fotografia is None: 
            file_path, _ = QFileDialog.getOpenFileName(
                self,
                "Seleccionar Imagen",
                "",
                "Imágenes (*.png *.jpg *.jpeg)"
            )
            if file_path:
                pixmap = QPixmap(file_path)
                self.lblicono.setPixmap(pixmap.scaled(self.lblicono.size()))
                self.btnFoto.setText("Eliminar foto")
                try:
                    if file_path:
                        with open(file_path, "rb") as file:
                            self.fotografia = file.read()
                except Exception as e:
                    print(f"Error al cargar foto: {e}")
                    self.fotografia = None
            else:
                pass
        else:
            self.lblicono.clear()
            self.btnFoto.setText("Seleccionar foto")
            self.fotografia = None
                 
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
        if self._validar_inputs_sin_con_datos():
            dialEmergente = DialogoEmergente("¿?","¿Estas seguro que que quieres cancelar?","Question",True,True)
            opcion = dialEmergente.exec()
            if opcion == QDialog.Accepted:
                self.reject()
            elif opcion == QDialog.Rejected:
                print("Se rechazó el diálogo.")
        else:
            self.reject()
            
    def _validar_campos(self):
        # Verifica si los campos requeridos están vacíos
        if self._validar_inputs_vacios():
            dialEmergente = DialogoEmergente("Advertencia","Llene todos los campos.","Warnig")
            dialEmergente.exec()
            return False
        else:
            return True
    
    def _validar_inputs_vacios(self):
        vacios:bool = False
            
        if not self.inputNombre.text().strip():
            Sombrear(self.inputNombre,20,0,0,"red")
            vacios = True
        else:
            Sombrear(self.inputNombre,20,0,0)
            
        if not self.inputApellido1.text().strip():
            Sombrear(self.inputApellido1,20,0,0,"red")
            vacios = True
        else:
            Sombrear(self.inputApellido1,20,0,0)
            
        if not self.inputApellido2.text().strip():
            Sombrear(self.inputApellido2,20,0,0,"red")
            vacios = True
        else:
            Sombrear(self.inputApellido2,20,0,0)
            
        if not self. inputCedula.text().strip():
            Sombrear(self.inputCedula,20,0,0,"red")
            vacios = True
        else:
            Sombrear(self.inputCedula,20,0,0)
            
        if not self.inputNacimiento.date().toString("yyyy-MM-dd"):
            Sombrear(self.inputNacimiento,20,0,0,"red")
            vacios = True
        else:
            Sombrear(self.inputNacimiento,20,0,0)
            
        if not self.inputCorreo.text().strip():
            Sombrear(self.inputCorreo,20,0,0,"red") 
            vacios = True
        else:
            Sombrear(self.inputCorreo,20,0,0)
            
        if not self.inputEstCivil.currentText():
            Sombrear(self.inputEstCivil,20,0,0,"red")
            vacios = True
        else:
            Sombrear(self.inputEstCivil,20,0,0)
            
        if not self.inputDireccion.toPlainText().strip():
            Sombrear(self.inputDireccion,20,0,0,"red")
            vacios = True
        else:
            Sombrear(self.inputDireccion,20,0,0)
            
        return vacios
    
    def _validar_inputs_sin_con_datos(self):
        if self.inputNombre.text().strip() or self.inputApellido1.text().strip() or self.inputApellido2.text().strip() or self. inputCedula.text().strip() or self.inputCorreo.text().strip() or self.inputDireccion.toPlainText().strip():
            return True
        else:
            return False
    
    def _obtener_registroId(self, id):
        result = self.Pservices.obtenerPersonaPorId(id)
        if result["success"]:
            if result["data"]:
                persona:Persona = result["data"]
                self.idP = persona.id
                self.fotografia = persona.foto
                self.inputNombre.setText(persona.nombre)
                self.inputApellido1.setText(persona.apellido1)
                self.inputApellido2.setText(persona.apellido2)
                self.inputNacimiento.setDate(QDate.fromString(str(persona.fecha_nacimiento), "yyyy-MM-dd"))
                self.inputCedula.setText(persona.cedula)
                self.inputCorreo.setText(persona.correo)
                self.inputDireccion.setPlainText(persona.direccion)
                self.inputEstCivil.setCurrentText(persona.estado_civil)
                
                self.btnFoto.setText("Eliminar foto " if self.fotografia is not None else "Seleccionar foto")
                if self.fotografia:
                    pixmap = QPixmap()
                    pixmap.loadFromData(self.fotografia)
                    self.lblicono.setPixmap(pixmap.scaled(self.lblicono.size()))
                    self.lblicono.show()
                    
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
    
    def _accion_persona(self):

            
        person:Persona = Persona(
            nombre = self.inputNombre.text(),
            apellido1 = self.inputApellido1.text(),
            apellido2 = self.inputApellido2.text(),
            cedula = self.inputCedula.text(),
            fecha_nacimiento = self.inputNacimiento.date().toString("yyyy-MM-dd"),
            correo = self.inputCorreo.text(),
            estado_civil = self.inputEstCivil.currentText(),
            direccion=self.inputDireccion.toPlainText(),
            id=self.idP,
            foto = self.fotografia
        )
        if self._validar_campos():
            if self.idP > 0:
                result = self.Pservices.modificarPersona(person)
                print(result)
                if result["success"]:
                    dial = DialogoEmergente("Actualización",result["message"],"Check")
                    dial.exec()
                    self.reject()
                else:
                    dial = DialogoEmergente("Erro","Error al actualizar a la persona","Error")
                    dial.exec()
            else:
                result = self.Pservices.insertarPersona(person)
                print(result)
                if result["success"]:
                    dial = DialogoEmergente("Registrar","Persona registrada exitosamente","Check")
                    dial.exec()
                    self.reject()
                else:
                    dial = DialogoEmergente("Erro","Error al registrar a la persona","Error")
                    dial.exec()
        
