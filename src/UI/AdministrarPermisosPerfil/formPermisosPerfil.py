
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from Utils.Utils import *
from UI.DialogoEmergente import *
from services.permisosPerfilServices import *
from services.perfilService import *
from settings.variable import *

class formPermiso(QDialog):
    permisosServices = PermisosPerfilServices() 
    perfilServices = PerfilServices()
    idP = 0 
    listaPerfilesID = {} #crea un diccionario de roles con sus ids
    ##constructor
    def __init__(self, parent=None, titulo="Registrar permiso.",id = None):
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
        lblRol = QLabel(text="Seleccionar pefil")   
        self.inputPerfil = QComboBox()
        self.errorPerfil = QLabel(text="")
        
        #permisos para dicha tabla
        lblAcceso = QLabel(text="Acceso a")
        self.inputTabla = QComboBox()
        self.inputTabla.addItems(ACCESO_TABLE.keys())
        self.errorTabla = QLabel(text="")
        
        lblPermisos = QLabel(text="Otorgar los siguientes permisos:")
        
        self.checkVer = QCheckBox("permiso ver")
        self.checkVer.clicked.connect(self._checked_verificacion_ver)
        Sombrear(self.checkVer,30,0,0)
        
        self.checkCrear = QCheckBox("permiso crear")
        self.checkCrear.clicked.connect(self._checked_verificacion)
        Sombrear(self.checkCrear,30,0,0)
        
        self.checkEditar = QCheckBox("permiso editar")
        self.checkEditar.clicked.connect(self._checked_verificacion)
        Sombrear(self.checkEditar,30,0,0)

        self.checkEliminar = QCheckBox("permiso eliminar")
        self.checkEliminar.clicked.connect(self._checked_verificacion)
        Sombrear(self.checkEliminar,30,0,0)

        self.error =QLabel(text="")
        self.error.setObjectName("lblerror")
        self.error.setMaximumHeight(30)
        self.error.setMinimumHeight(30)
        self.error.setWordWrap(True)


        layoutForm.addLayout(self._contenedor(lblRol,self.inputPerfil,self.errorPerfil),0,0)
        layoutForm.addLayout(self._contenedor(lblAcceso,self.inputTabla,self.errorTabla),1,0)
        layoutForm.addWidget(lblPermisos,2,0)
        layoutForm.addWidget(self.checkVer,3,0)
        layoutForm.addWidget(self.checkCrear,4,0)
        layoutForm.addWidget(self.checkEditar,5,0)
        layoutForm.addWidget(self.checkEliminar,6,0)    
        layoutForm.addWidget(self.error,7,0)    
        
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
    
        if id:
            self._obtener_registroId(id)

        self._cargar_perfiles()
        self._verificar_permiso()
        self.inputTabla.currentIndexChanged.connect(self._verificar_permiso)
        self.inputPerfil.currentIndexChanged.connect(self._verificar_permiso)

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

    def _verificar_permiso(self):
            print(self.listaPerfilesID)
            perfilid = self.listaPerfilesID[self.inputPerfil.currentText()]
            tabla = ACCESO_TABLE[self.inputTabla.currentText()]
            result = self.permisosServices.verificar_permiso_perfil_tabla(perfil_id=perfilid, tabla=tabla, id=self.idP)
         
            if result and self.idP == 0:
                self.error.setText(f"El perfil \'{self.inputPerfil.currentText()}\' ya posee el acceso a \'{self.inputTabla.currentText()}\'")
                return False
            else:
                self.error.setText("")
                return True

    def _checked_verificacion_ver(self):
        if not self.checkVer.isChecked():
            self.checkCrear.setChecked(False)
            self.checkEditar.setChecked(False)
            self.checkEliminar.setChecked(False)

    def _checked_verificacion(self):
        if self.checkCrear.isChecked() or self.checkEditar.isChecked() or self.checkEliminar.isChecked():
            self.checkVer.setChecked(True)

    def _cancelar_registro(self):
        if not self._validar_inputs_vacios():
            dialEmergente = DialogoEmergente("¿?","¿Estas seguro que que quieres cancelar?","Question",True,True)
            opcion = dialEmergente.exec()
            if opcion == QDialog.Accepted:
                 self.reject()
            elif opcion == QDialog.Rejected:
                pass
        else:
             self.reject()##cerrar la ventana

    def _cargar_perfiles(self):
        try:
            result = self.perfilServices.obtener_todo_perfiles()
            if result["success"]:
                listaPerfiles = result["data"]["listaPerfiles"]
                if len(listaPerfiles) > 0:
                    for rol in listaPerfiles:
                        self.inputPerfil.addItem(rol.nombre)
                        self.listaPerfilesID[rol.nombre] = rol.id
                else:
                    dialEmergente = DialogoEmergente("","No existen perfiles.","Warning")
                    if dialEmergente.exec() == QDialog.Accepted:
                        self.reject()
            else:
                dialEmergente = DialogoEmergente("","Ocurrio un error","Error")
                if dialEmergente.exec() == QDialog.Accepted:
                    self.reject()
        except Exception as e:
            print(f'\nError:\n{e}\n----------------------\n')
            self.reject()
                      
    def _validar_campos(self):
        if self._validar_inputs_vacios():
            dialEmergente = DialogoEmergente("Advertencia","Debes conceder al menos un permiso.","Warning")
            dialEmergente.exec()
            return False
        else:
            return True

    def _validar_inputs_vacios(self):
        if not self.checkCrear.isChecked() and not self.checkEditar.isChecked() and not self.checkEliminar.isChecked() and not self.checkVer.isChecked():
            return True
        else:
            return False

    def _obtener_registroId(self, id):
        result = self.permisosServices.obtener_permiso_perfil_por_id(id)
        print (result)
        if result["success"]:
            if result["data"]:
                permiso:Permiso_Perfil = result["data"]
                
                dato = self.perfilServices.obtenerPerfilPorId(permiso.perfil_id)
                rol = dato["data"]
                acceso_a = [key for key, value in ACCESO_TABLE.items() if value == permiso.tabla]
                
                
                self.inputPerfil.setCurrentText(rol.nombre)
                self.inputPerfil.setDisabled(True)
                self.inputTabla.setCurrentText(str(acceso_a[0]))
                self.inputTabla.setDisabled(True)
                self.checkVer.setChecked(permiso.ver)
                self.checkCrear.setChecked(permiso.crear)
                self.checkEditar.setChecked(permiso.editar)
                self.checkEliminar.setChecked(permiso.eliminar)
                self.idP = permiso.id
            else:
                dial = DialogoEmergente("Error","Hubo un error de carga.","Error")
                dial.exec()
                QTimer.singleShot(0, self.reject)
                return None
        else:
            dial = DialogoEmergente("Error","Hubo un error al intentar editar.","Error")
            dial.exec()
            QTimer.singleShot(0, self.reject)
            return None 

    def _accion_permiso(self):
        permiso:Permiso_Perfil = Permiso_Perfil(
            perfil_id  = self.listaPerfilesID[self.inputPerfil.currentText()],
            tabla   = ACCESO_TABLE[self.inputTabla.currentText()],
            ver     = self.checkVer.isChecked(),
            crear   = self.checkCrear.isChecked(),
            editar  = self.checkEditar.isChecked(),
            eliminar= self.checkEliminar.isChecked(),
            id      = self.idP
        )
        if not self._verificar_permiso():
            dial = DialogoEmergente("¡Advertencia!",self.error.text(),"Warning")
            dial.exec()
            return

        if self._validar_campos():
            if self.idP > 0:
                result = self.permisosServices.actualizar_permiso_perfil(permiso=permiso)
                if result["success"]:
                    dial = DialogoEmergente("Actualización",result["message"],"Check")
                    dial.exec()
                    self.reject()
                else:
                    dial = DialogoEmergente("Erro","Error al actualizar a el permiso","Error")
                    dial.exec()
            else:
                result = self.permisosServices.insertar_permiso_perfil(permiso=permiso)
                if result["success"]:
                    dial = DialogoEmergente("Registrar","Permiso registrado exitosamente","Check")
                    dial.exec()
                    self.reject()
                else:
                    dial = DialogoEmergente("Erro","Error al registrar a el permiso","Error")
                    dial.exec()