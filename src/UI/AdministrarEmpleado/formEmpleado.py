from PySide6.QtWidgets  import *
from PySide6.QtCore     import *
from PySide6.QtGui      import QIntValidator,QStandardItemModel
from Utils.Utils        import *
from functools          import partial

from services.empleadoServices  import EmpleadoServices
from services.rolService        import RolServices
from services.departamentoService import DepartamentoServices
from services.personaService    import PersonaServices
from services.rolService        import RolServices
from services.perfilService     import PerfilServices
from services.telefonoServices  import TelefonoServices
from services.ZKService        import ZKServices 
from settings.logger         import logger
from UI.DialogoEmergente import DialogoEmergente


from models.persona     import Persona
from models.telefono    import Telefono
from settings.config    import ZKTECA_CONFIG

from datetime import datetime
import time
import re

class formEmpleado(QDialog):
    idEmpleado  = None
    fotografia  = None
    idPersona   = None

    emplServices = EmpleadoServices()
    depaServices = DepartamentoServices()
    rolServices  = RolServices()
    perServices  = PersonaServices()
    perfilServices = PerfilServices()
    telServices  = TelefonoServices()

    def __init__(self, parent = None, titulo = 'Registrar empleado', id_empleado = None):
        super().__init__(parent)
        self.setObjectName('form')
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setMinimumSize(QSize(1050,700))
        
        cargar_estilos('claro','formEm.css',self)
        
        layoutPrin =QVBoxLayout()
        layoutPrin.setContentsMargins(0,0,0,0)
        frame = QFrame()
        frame.setObjectName('formFrame')
        #asignando el frame al layout principal
        layoutPrin.addWidget(frame)

        ## layoutFrame
        layoutFrame = QVBoxLayout()
        layoutFrame.setContentsMargins(10,10,10,10)

        lbltitulo = QLabel(titulo)
        lbltitulo.setObjectName('lbltitulo')
        lbltitulo.setAlignment(Qt.AlignCenter)
        lbltitulo.setMinimumHeight(40)
        layoutFrame.addWidget(lbltitulo)

        ## layoutContent
        self.layoutContent = QHBoxLayout()

        self.llenarLayoutConten()

        layoutFrame.addLayout(self.layoutContent)

        boton_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        boton_box.button(QDialogButtonBox.Cancel).setText("Cancelar")
        boton_box.button(QDialogButtonBox.Cancel).setObjectName("btncancelar")
        boton_box.button(QDialogButtonBox.Cancel).setMinimumSize(QSize(100,30))
        boton_box.button(QDialogButtonBox.Cancel).clicked.connect(self.cerrarForm)
        
        boton_box.button(QDialogButtonBox.Ok).setText("Registrar" if id_empleado == None else "Actualizar")
        boton_box.button(QDialogButtonBox.Ok).setObjectName("btnregistrar")
        boton_box.button(QDialogButtonBox.Ok).setMinimumSize(QSize(100,30))
        boton_box.button(QDialogButtonBox.Ok).clicked.connect(self.registrarDatos)
        Sombrear(boton_box,20,0,5)

        if id_empleado:
            self.idEmpleado = id_empleado
            self.precargarFormulario() 

        layoutFrame.addWidget(boton_box)
        frame.setLayout(layoutFrame)
        self.setLayout(layoutPrin)   
    
    '''
    LLenado de layoutContent
    '''
    def llenarLayoutConten(self): 
        #creando widgets para el scrol
        self.widgetIzq = QWidget()

        #creando los layouts
        self.layoutIzq = QVBoxLayout()


        #configuracion de los layouts
        self.layoutIzq.setSpacing(20)



        #creando scrolls
        scroll_areaIzq = QScrollArea()
        scroll_areaIzq.setWidgetResizable(True)


        self.llenarLayoutIzquierda()

        
        # Crear los scroll areas
        self.scrollIzq = QScrollArea()


        # Configurar las scroll areas
        self.scrollIzq.setWidgetResizable(True)


        # Crear widgets contenedores para cada scroll area
        widgetIzq = QWidget()

        # Asignar layouts a los widgets contenedores
        widgetIzq.setLayout(self.layoutIzq)

        #agregando nombres
        widgetIzq.setObjectName('contenedor')


        # Asignar los widgets a las scroll areas
        self.scrollIzq.setWidget(widgetIzq)



        # Agregar las scroll areas al layout principal
        self.layoutContent.addWidget(self.scrollIzq)

    '''
    Llenado de layoutIzq
    '''
    def llenarLayoutIzquierda(self):
        tituloIzq = QLabel('Datos Personales')
        tituloIzq.setObjectName('lblsubtitulos')
        tituloIzq.setAlignment(Qt.AlignCenter)

        self.layoutFoto = QVBoxLayout()
        self.llenarLayoutFoto()
        #Creando lblTelefono, Input y lblTelefono de error
        #Nombre
        self.lblNombre = QLabel('Nombre')
        self.inNombre = QLineEdit()
        self.errNombre = QLabel()

        #Apellidos
        self.lblApellidos = QLabel('Apellidos')
        self.inApellidos = QLineEdit()
        self.errApellidos = QLabel()

        #Cedula
        self.lblCedula = QLabel('Cedula')
        self.inCedula = QLineEdit()
        self.inCedula.editingFinished.connect(self.validar_cedula)
        self.errCedula = QLabel()

        #Fecha de nacimiento
        self.lblNacimiento = QLabel('Nacimiento')
        self.inNacimiento = QDateEdit()
        self.inNacimiento.setCalendarPopup(True)
        self.inNacimiento.setDisplayFormat('yyyy-MM-dd')
        self.inNacimiento.setMaximumDate(QDate.currentDate())
        self.errNacimiento = QLabel()

        #Correo
        self.lblCorreo = QLabel('Correo')
        self.inCorreo = QLineEdit()
        self.inCorreo.editingFinished.connect(self.validar_correo)
        self.errCorreo = QLabel()

        #cargar layout de telefonos
        self.lblTelefonos = QLabel(text='Telefonos')
        self.layoutTelPrinc = QVBoxLayout()
        self.errTelefono = QLabel()
        self.llenarLayoutTelefono()

        #Estado civil
        self.lblEstCivil = QLabel('Estado civil')
        self.inEstCivil = QComboBox()
        self.inEstCivil.addItems(["Soltero/a", "Casado/a", "Divorciado/a", "Viudo/a"])
        self.errEstCivil = QLabel('Error estado civil')
        #Direccion
        self.lblDireccion = QLabel('Direccion')
        self.inDireccion = QTextEdit()
        self.inDireccion.setMaximumHeight(30)
        self.errDireccion = QLabel()

        #Departamento
        self.lblDep = QLabel('Departamento')
        self.inDep = QComboBox()
        self.inDep.addItem('Ninguno', None)
        self.inDep.setMaxVisibleItems(10)
        self.errDep = QLabel()
        self.llenarComboboxDepa()
        #Departamento
        self.lblRol = QLabel('Rol')
        self.inRol = QComboBox()
        self.inRol.addItem('Ninguno', None)
        self.inRol.setMaxVisibleItems(10)
        self.errRol = QLabel()
        self.llenarComboboxRol()
        
        # Botón para registrar huella - CAMBIO IMPORTANTE
        #self.btnRegistrarHuella = QPushButton('Registrar huella')
        #self.btnRegistrarHuella.setObjectName('btnHuella')
        #self.btnRegistrarHuella.setMinimumHeight(40)
        #self.btnRegistrarHuella.setStyleSheet("""
        #QPushButton {
         #   background-color: #4CAF50;
          #  color: white;
           # border: none;
            #border-radius: 5px;
            #padding: 8px;
            #font-size: 14px;
        #}
        #QPushButton:hover {
         #   background-color: #45a049;
        #}
    #""")
     #   self.btnRegistrarHuella.clicked.connect(self.registrar_huella)
    
    # Layout contenedor para el botón (para mejor espaciado)
       # layoutHuella = QVBoxLayout()
       # layoutHuella.setContentsMargins(10, 10, 10, 10)
       # layoutHuella.addWidget(self.btnRegistrarHuella)  
        #asignando al layoutIzq
        self.layoutIzq.addWidget(tituloIzq)
        self.layoutIzq.addLayout(self.layoutFoto)
        self.layoutIzq.addLayout(self.contenedor(self.lblNombre,self.inNombre,self.errNombre))
        self.layoutIzq.addLayout(self.contenedor(self.lblApellidos,self.inApellidos,self.errApellidos))
        self.layoutIzq.addLayout(self.contenedor(self.lblCedula,self.inCedula,self.errCedula))
        self.layoutIzq.addLayout(self.contenedor(self.lblNacimiento,self.inNacimiento,self.errNacimiento))
        self.layoutIzq.addLayout(self.contenedor(self.lblCorreo,self.inCorreo,self.errCorreo))
        self.layoutIzq.addLayout(self.contenedor(self.lblTelefonos,self.layoutTelPrinc,self.errTelefono))
        self.layoutIzq.addLayout(self.contenedor(self.lblEstCivil,self.inEstCivil,self.errEstCivil))
        self.layoutIzq.addLayout(self.contenedor(self.lblDireccion,self.inDireccion,self.errDireccion))
        self.layoutIzq.addLayout(self.contenedor(self.lblDep,self.inDep,self.errDep))
        self.layoutIzq.addLayout(self.contenedor(self.lblRol,self.inRol,self.errRol))
        #self.layoutIzq.addLayout(layoutHuella)  
    
    #layout para la foto
    def llenarLayoutFoto(self):
        self.foto = QLabel()
        self.foto.setObjectName('foto')
        self.foto.setFixedSize(250,250)
        self.foto.setAlignment(Qt.AlignCenter)
        self.foto.setStyleSheet('#foto{border-radius:10;border: 1px solid black;}')
        cargar_Icono(self.foto,'userPerson.png')

        self.btnFoto = QPushButton(text='Seleccionar foto')
        self.btnFoto.setObjectName('select_foto')
        self.btnFoto.setFixedHeight(40)
        self.btnFoto.clicked.connect(self.seleccionarFoto)

        self.errFoto = QLabel()
        self.errFoto.setObjectName("lblerror")
        self.errFoto.setMaximumHeight(25)
        self.errFoto.setMinimumHeight(25)
        self.errFoto.setWordWrap(True)

        self.layoutFoto.setAlignment(Qt.AlignCenter)
        self.layoutFoto.addWidget(self.foto)
        self.layoutFoto.addWidget(self.btnFoto)
        self.layoutFoto.addWidget(self.errFoto)
    #contenedor para cada input
    def contenedor(self,lblTelefono:QLabel,input,label_error:QLabel)->QVBoxLayout:
        layout = QVBoxLayout()
        layout.setContentsMargins(10,5,10,0)
        layout.setSpacing(0)
        
        label_error.setObjectName("lblerror")
        label_error.setMaximumHeight(25)
        label_error.setMinimumHeight(25)
        label_error.setWordWrap(True)
        
        layout.addWidget(lblTelefono)
        layout.addSpacing(5)
        layout.addLayout(input) if isinstance(input,QVBoxLayout) else layout.addWidget(input)
        layout.addWidget(label_error)
        return layout
    #layout donde se maneja los telefonos
    def llenarLayoutTelefono(self):
        #boton para agregar telefono
        btnAgregarTel = QPushButton(text='Agregar telefono.')
        btnAgregarTel.setObjectName('btn_AgregarTel')
        btnAgregarTel.setMinimumHeight(40)
        btnAgregarTel.clicked.connect(self.agregar_nuevo_telefono)

        self.layoutInputTel = QVBoxLayout()
        #asignando los valores alos layouts
        self.layoutTelPrinc.addWidget(btnAgregarTel)
        self.layoutTelPrinc.addLayout(self.layoutInputTel)

    #agregado de telefono
    def agregar_nuevo_telefono(self, telefono:Telefono=None):
        #lblTelefono para cada input telefono
        lblTelefono = QLabel(text='Numero de telefono')
        #input para ingresar el telefono
        inputTelefono = QLineEdit()
        inputTelefono.setPlaceholderText('Ejemplo: 11111111')
        inputTelefono.setValidator(QIntValidator())
        inputTelefono.textChanged.connect(lambda : self.verificarNumero(inputTelefono))

        #input para tipo de contacto
        lblTipo = QLabel(text='Tipo de contacto')

        #input para ingresar el tipo de telefono
        inputTipo = QLineEdit()
        inputTipo.setPlaceholderText('Ejemplo: Telefono fijo')

        #boton para eliminar el telefono
        btnEliminar = QPushButton("Eliminar")
        btnEliminar.setObjectName('eliminar_telefono')
        btnEliminar.setMinimumHeight(30)
        

        #lblTelefono de error
        lblError = QLabel()
        lblError.setObjectName("lblerror")
        lblError.setMaximumHeight(25)
        lblError.setMinimumHeight(25)
        lblError.setWordWrap(True)

        layoutInputsTelefonos = QVBoxLayout()

        if telefono:##cargar datos de los telefonos
            inputTelefono.setText(telefono.numero)
            inputTipo.setText(telefono.tipo)
            layoutInputsTelefonos.setProperty('id_telefono',telefono.id)
            inputTelefono.setEnabled(False)
            inputTipo.setEnabled(False)
            btnEliminar.clicked.connect(lambda _,id_telefono = telefono.id: self.eliminar_telefono(layoutInputsTelefonos, id_telefono))
        else:
            btnEliminar.clicked.connect(lambda : self.eliminar_telefono(layoutInputsTelefonos))

        layoutInputsTelefonos.setContentsMargins(10,20,10,20)
        layoutInputsTelefonos.setSpacing(10)
        layoutInputsTelefonos.addWidget(lblTelefono,0)
        layoutInputsTelefonos.addWidget(inputTelefono,1)
        layoutInputsTelefonos.addWidget(lblTipo,2,)
        layoutInputsTelefonos.addWidget(inputTipo,3)
        layoutInputsTelefonos.addWidget(lblError,4)
        layoutInputsTelefonos.addWidget(btnEliminar,5)
        self.layoutInputTel.addLayout(layoutInputsTelefonos)
    
    #eliminado de telefono
    def eliminar_telefono(self, layoutInputsTelefonos:QVBoxLayout, id_telefono:int = None):
        if id_telefono:
            text = "Este numero de telefono ya se encuentrar registrado en la plataforma.\n"
            text+= "¿Quieres eliminarlo?"
            dial = DialogoEmergente("",text,'Warning',True,True)
            if dial.exec() == QDialog.Accepted:
                result = self.telServices.eliminar_telefono(id_telefono)
                if not result['success']:
                    dial = DialogoEmergente('',result['message'],'Error',True)
                    dial.exec()
                    return
                
                dial = DialogoEmergente('',result['message'],'Check',True)
                dial.exec()
            else:
                return

        self.eliminacionLayout(layoutInputsTelefonos)
        self.layoutInputTel.removeItem(layoutInputsTelefonos)
        layoutInputsTelefonos.deleteLater()

    
    def llenarComboboxDepa(self):
        result = self.depaServices.obtenerTodoDepartamento()

        if not result['success']:
            self.reject()
            return
        
        if len(result['listaDepa']) == 0:
            self.inDep.setItemText(0,'No hay departamentos registrados.')
            return

        for depa in result['listaDepa']:
            self.inDep.addItem(depa.nombre,depa.id)
            
    def llenarComboboxRol(self):
        result = self.rolServices.obtener_todo_roles()
        if not result['success']:
            self.reject()
            return
        
        if len(result['data']['listaRoles']) == 0:
            self.inRol.setItemText(0,'No hay roles registrados.')
            return

        for rol in result['data']['listaRoles']:
            self.inRol.addItem(rol.nombre, rol.id)

    
    



    def mostrarContrasena(self,input:QLineEdit):
        if input.echoMode() == QLineEdit.Password:
            input.setEchoMode(QLineEdit.Normal)
        else:
            input.setEchoMode(QLineEdit.Password)

    #eliminacion de layout y sus elementos
    def eliminacionLayout(self,layout:QVBoxLayout | QHBoxLayout):
        while layout.count():
            item = layout.takeAt(0)  # Tomar el primer item del layout
            if item.widget():                   #eliminacion de widgets
                widget = item.widget()
                layout.removeWidget(widget)
                widget.deleteLater()
            elif item.layout():                 #eliminacion de layout
                sub_layout = item.layout()
                self.eliminacionLayout(sub_layout)
                layout.removeItem(item)
                sub_layout.deleteLater()
            elif item.spacerItem():             #eliminacion de spacing
                spacer = item.spacerItem()
                layout.removeItem(item) 

    def actualizacionArbolPerfil(self,idperfil,model):
       pass
    """
    Metodos de validaciones de datos e inputs.
    """
    #verificacion del telefono
    def verificarNumero(self, input: QLineEdit):
        numero = input.text()
        if self.numeroTelefonoValido(numero):
            input.setProperty('telValido',True)
            input.style().polish(input)  
            return True
        else:
            input.setProperty('telValido',False)
            input.style().polish(input)  
            return False
        
    
    #verificacion del telefono sea 8 digitos y empiece con 2,4,5,6,7,8,9
    def numeroTelefonoValido(self, numero: str) -> bool:
        patron = re.compile(r'^[2456789]\d{7}$')
        return bool(patron.match(numero))
    
    """
    Fin metodos de validaciones de datos e inputs
    """
    #cerrado de telefono
    def cerrarForm(self):
        if self.validar_datos_personales():
            dialogo = DialogoEmergente('','¿Estas seguro que quieres cancelar?','Question',True,True)
            if dialogo.exec() == QDialog.Accepted:
                self.reject()
                return
        self.reject()
    '''
    Logica
    '''
    #extraer todos los datos.
    def extraerDatosEmpleados(self):
        #datos de la persona
        persona = Persona(
            nombre          = self.inNombre.text(),
            apellidos       = self.inApellidos.text(),
            cedula          = self.inCedula.text(),
            fecha_nacimiento = self.inNacimiento.text(),
            correo          = self.inCorreo.text(),
            estado_civil    = self.inEstCivil.currentText(),
            direccion       = self.inDireccion.toPlainText(),
            id              = self.idPersona,
            foto            = self.fotografia
        )

        listaTelefonos  = self.extraerTelefonos()

        datos = {
            'persona'       : persona,
            'listaTelefonos': listaTelefonos,
            'id_departamento':self.inDep.currentData(),
            'id_rol'        : self.inRol.currentData(),
        }

        return datos

    #extraer los telefonos
    def extraerTelefonos(self):
        listaTelefonos = []
        #obtengo los valores de cada numero ingresado junto con su tipo
        for i in range(self.layoutInputTel.count()):
            item = self.layoutInputTel.itemAt(i).layout()
            if isinstance(item,QVBoxLayout):
                id          = item.property('id_telefono')
                numero      = item.itemAt(1).widget().text()
                tipoCont    = item.itemAt(3).widget().text()
                if numero.strip() and tipoCont.strip():
                    telefono = Telefono(
                        numero        = numero,
                        tipo_contacto = tipoCont,
                        id            = id
                    )
                    listaTelefonos.append(telefono)
        return listaTelefonos

 
    

    #precargando formulario en caso de que se este actualizando
    def precargarFormulario(self):
        result = self.emplServices.obtener_empleado_por_id(self.idEmpleado)
        if not result['success']:
            dial = DialogoEmergente('','Ocurrio un error al precargar los datos de los empleados.\nError: '+result['message'],'Error',True,False)
            dial.exec()
            self.reject()

        datos   = result.get('empleado')
        persona:Persona = datos.get('persona')  #objeto Persona
        dictRolEmp = datos.get('rolEmpleado')   #diccionario
        departamen = datos.get('departamento')  #int
        listaTelef = datos.get('listaTelefonos')#telefonos del 

        self.idPersona = persona.id
        self.fotografia = persona.foto

        self.btnFoto.setText("Eliminar foto " if self.fotografia is not None else "Seleccionar foto")
        if self.fotografia:
            pixmap = QPixmap()
            pixmap.loadFromData(self.fotografia)
            # Escalar la imagen manteniendo la relación de aspecto y la calidad
            scaled_pixmap = pixmap.scaled(self.foto.size(),Qt.KeepAspectRatio,Qt.SmoothTransformation)
            # Establecer la imagen escalada en el QLabel
            self.foto.setPixmap(scaled_pixmap)
            self.foto.setAlignment(Qt.AlignCenter)  # Centrar la imagen en el QLabel
            self.foto.show()

        self.inNombre.setText(persona.nombre)
        self.inApellidos.setText(persona.apellidos)
        self.inNacimiento.setDate(QDate.fromString(str(persona.fecha_nacimiento), "yyyy-MM-dd"))
        self.inCedula.setText(persona.cedula)
        self.inCorreo.setText(persona.correo)
        self.inDireccion.setPlainText(persona.direccion)
        self.inEstCivil.setCurrentText(persona.estado_civil)

        if listaTelef:
            for telefono in listaTelef:
                self.agregar_nuevo_telefono(telefono)
        
        ##cargar departamento y rol
        index = self.inDep.findData(departamen)
        self.inDep.setCurrentIndex(index if index >= 0 else -1)


        if dictRolEmp:
            index = self.inRol.findData(dictRolEmp.get('id_rol'))
            self.inRol.setCurrentIndex(index if index >= 0 else None)



    #validar cedula 
    def validar_cedula(self):
        cedula = self.inCedula.text()
        self.errCedula.clear()
        if cedula.strip():
            result = self.perServices.validar_cedula(cedula,self.idPersona)
            if not result['success']:
                self.errCedula.setText(result['message'])
                return False
            return True
    
    def validar_correo(self):
        correo = self.inCorreo.text()
        self.errCorreo.clear()
        if correo:
            result = self.perServices.verificacionCorreo(correo, self.idPersona)
          
            if not result['success']:
                self.errCorreo.setText(result['message'])
                return False
            return True
        else:
            self.errCorreo.setText("El correo es obligatorio.")
            return False
    
        
    #validar numeros de telefonos
    def validar_listaTelefonos(self):
        valido = True
        numeros_telefonicos = []  # Lista para almacenar los números de teléfono y verificar duplicados

        for i in range(self.layoutInputTel.count()):
            item = self.layoutInputTel.itemAt(i).layout()
            if isinstance(item, QVBoxLayout):
                numero              = item.itemAt(1).widget().text().strip()
                tipoCont            = item.itemAt(3).widget().text().strip()
                lblError: QLabel    = item.itemAt(4).widget()


                if numero or tipoCont:
                    if not numero:
                        lblError.setText('Debes agregar un número telefónico.')
                        valido = False
                    elif not tipoCont:
                        lblError.setText('Debes agregar el tipo de contacto.')
                        valido = False
                    else:
                        # Verificar duplicados en la lista
                        if numero in numeros_telefonicos:
                            lblError.setText('Este número de teléfono está duplicado en la lista.')
                            valido = False
                        else:
                            numeros_telefonicos.append(numero)
                            # Verificar en la base de datos si no hay duplicados y los campos están llenos
                            id_telefono = item.property('id_telefono')
                            result = self.telServices.verificar_telefono(numero, id_telefono)
                            if not result['success']:
                                lblError.setText('Ocurrió un error al validar el número de teléfono.')
                                valido = False
                            elif not result['isValid']:
                                lblError.setText('Este número de teléfono ya se encuentra registrado.')
                                valido = False
                            else:
                                lblError.setText('')  # Limpiar el mensaje de error si todo está bien

        return valido
    


    #validar datos personales
    def validar_datos_personales(self):
        datos_validos = True

        # Limpiar mensajes de error antes de validar
        self.errNombre.clear()
        self.errApellidos.clear()
        self.errCedula.clear()
        self.errNacimiento.clear()
        self.errCorreo.clear()
        self.errTelefono.clear()
        self.errEstCivil.clear()
        self.errDireccion.clear()

        # Validar Nombre
        if not self.inNombre.text().strip():
            self.errNombre.setText("El nombre es obligatorio.")
            datos_validos = False

        # Validar Apellidos
        if not self.inApellidos.text().strip():
            self.errApellidos.setText("Los apellidos son obligatorios.")
            datos_validos = False

        # Validar Cédula
        if not self.inCedula.text().strip():
            self.errCedula.setText("La cédula es obligatoria.")
            datos_validos = False

        # Validar Fecha de Nacimiento
        if not self.inNacimiento.date().isValid():
            self.errNacimiento.setText("Debes seleccionar una fecha válida.")
            datos_validos = False

        # Validar Correo
        if not self.inCorreo.text().strip():
            self.errCorreo.setText("El correo es obligatorio.")
            datos_validos = False

        # Validar que haya al menos un teléfono agregado
        if self.layoutInputTel.count() == 0:
            self.errTelefono.setText("Debes agregar al menos un número de teléfono.")
            datos_validos = False

        # Validar Estado Civil (Debe seleccionar uno, aunque ya tiene opciones por defecto)
        if self.inEstCivil.currentIndex() == -1:
            self.errEstCivil.setText("Debes seleccionar un estado civil válido.")
            datos_validos = False

        # Validar Dirección
        if not self.inDireccion.toPlainText().strip():
            self.errDireccion.setText("La dirección es obligatoria.")
            datos_validos = False

        return datos_validos

    #Seleccion de foto
    def seleccionarFoto(self):
        self.errFoto.clear()
        if self.fotografia:
            self.resetear_foto()
        else:
            dir_defecto = QStandardPaths.writableLocation(QStandardPaths.PicturesLocation)
            file_path, _ = QFileDialog.getOpenFileName(self, "Seleccionar Imagen", dir_defecto, "Imágenes (*.png *.jpg *.jpeg)")
            if file_path:
                max_size_mb = 14  # Tamaño máximo en MB
                file_info = QFileInfo(file_path)
                file_size_mb = file_info.size() / (1024 * 1024)  # Convertir bytes a MB
                if file_size_mb <= max_size_mb:
                    # Mostrar la foto y leer los datos binarios
                    self.mostrar_foto(file_path)
                    self.btnFoto.setText("Eliminar foto")
                    try:
                        with open(file_path, "rb") as file:
                            self.fotografia = file.read()
                    except Exception as e:
                        self.errFoto.setText(f"Error al leer el archivo: {e}")
                        self.resetear_foto()
                else:
                    self.errFoto.setText(f"El archivo seleccionado supera el tamaño máximo permitido de {max_size_mb} MB.")
    
    def mostrar_foto(self, file_path):
        self.foto.setPixmap(QPixmap(file_path).scaled(self.foto.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))


    def resetear_foto(self):
        cargar_Icono(self.foto, 'userPerson.png')
        self.btnFoto.setText("Seleccionar foto")
        self.fotografia = None
        
    """def registrar_huella(self):
        #Maneja el registro de huella usando solo el nombre
        try:
            # Validar que se ingresó el nombre
            nombre = self.inNombre.text().strip()
            if not nombre:
                self.errNombre.setText("El nombre es obligatorio")
                DialogoEmergente(
                    'Datos incompletos',
                    'Debe ingresar el nombre del empleado',
                    'Warning',
                    True
                ).exec()
                return

            # Mostrar diálogo de espera
            dialogo_espera = DialogoEmergente(
                'Registro de Huella',
                'Preparando dispositivo...\n\nPor favor espere',
                'Info',
                False
            )
            dialogo_espera.show()
            QApplication.processEvents()

            # Llamar al servicio simplificado que genera el ID automáticamente
            zk_service = ZKServices()
            resultado = zk_service.registrar_empleado_simple(nombre)

            # Cerrar diálogo de espera
            dialogo_espera.close()

            # Mostrar resultados
            if resultado['success']:
                if resultado['huella_registrada']:
                    DialogoEmergente(
                        'Registro Exitoso',
                        f'Empleado registrado:\n\nNombre: {nombre}\nID: {resultado["user_id"]}',
                        'Check',
                        True
                    ).exec()
                else:
                    DialogoEmergente(
                        'Registro Parcial',
                        f'Usuario registrado pero sin huella:\n\nNombre: {nombre}',
                        'Warning',
                        True
                    ).exec()
            else:
                raise Exception(resultado['message'])

        except Exception as e:
            DialogoEmergente(
                'Error',
                f'Error durante el registro:\n\n{str(e)}',
                'Error',
                True
            ).exec()
    """

            
            
            
            
    """def registrarDatos(self):
        if not self.validar_datos_personales():
            dial = DialogoEmergente('','Asegurece de llenar todos los datos personales','Error',True)
            dial.exec()
            return

        if not self.validar_cedula():
            dial = DialogoEmergente('','Asegurece de que la cedula sea correcta.','Error',True)
            dial.exec()
            return
        
        if not self.validar_correo():
            dial = DialogoEmergente('','Asegurece de que el correo sea correcto.','Error',True)
            dial.exec()
            return
        
        if not self.validar_listaTelefonos():
            dial = DialogoEmergente('','Los numeros de telefonos no son validos o se encuentran duplicados.','Error',True)
            dial.exec()
            return
        
        if not self.validar_usuario():
            dial = DialogoEmergente('','Asegurese que los datos del usuario sean correctos.','Error',True)
            dial.exec()
            return

        datos = self.extraerDatosEmpleados()
        if len(datos['listaTelefonos']) == 0:
            dial = DialogoEmergente('','Debes añadir minimo un numero telefonico.','Error',True)
            dial.exec()
            return
        
        if self.idEmpleado:
            result = self.emplServices.actualizar_empleado(self.idEmpleado,datos)
            if not result['success']:
                dial = DialogoEmergente('','Ocurrio un error al actualizar el empleado.\nError: '+result['message'],'Error',True)
                dial.exec()
                return
            dial = DialogoEmergente('',result['message'],'Check',True)
            dial.exec()
            self.reject()
        else:
            result = self.emplServices.crear_empleado(datos)
            if not result['success']:
                dial = DialogoEmergente('','Ocurrio un error al registrar el empleado.\nError: '+result['message'],'Error',True)
                dial.exec()
                return
            
            dial = DialogoEmergente('',result['message'],'Check',True)
            dial.exec()
            self.reject()
    
    """
    
    def registrarDatos(self):
        """Maneja el registro completo del empleado incluyendo huella digital"""
        try:
            # 1. Validar todos los campos obligatorios
            if not self.validar_datos_personales():
                DialogoEmergente('', 'Complete todos los campos obligatorios', 'Error', True).exec()
                return

            # 2. Extraer datos del formulario
            datos = self.extraerDatosEmpleados()
            
            # 3. Mostrar diálogo de confirmación
            confirmacion = DialogoEmergente(
                'Confirmar Registro',
                '¿Desea registrar al empleado y capturar su huella digital?',
                'Question',
                True,
                True
            )
            
            if confirmacion.exec() != QDialog.Accepted:
                return

            # 4. Mostrar diálogo de progreso (sin intentar modificar lblMensaje)
            dialogo_progreso = DialogoEmergente(
                'Procesando Registro',
                'Guardando datos del empleado...',
                'Info',
                False
            )
            dialogo_progreso.show()
            QApplication.processEvents()

            # 5. Registrar datos básicos en la base de datos
            if self.idEmpleado:
                resultado_db = self.emplServices.actualizar_empleado(self.idEmpleado, datos)
            else:
                resultado_db = self.emplServices.crear_empleado(datos)

            if not resultado_db['success']:
                dialogo_progreso.close()
                DialogoEmergente('', f"Error en registro: {resultado_db['message']}", 'Error', True).exec()
                return
            
            if is_device_reachable(ZKTECA_CONFIG["host"], ZKTECA_CONFIG["port"]):
                print("conectado")
            else:
                print("desconectado")
        
            
            # 6. Crear nuevo diálogo para captura de huella (evitando modificar lblMensaje)
            dialogo_progreso.close()
            dialogo_huella = DialogoEmergente(
                'Captura de Huella',
                'Por favor, coloque el dedo en el lector biométrico...',
                'Info',
                False
            )
            dialogo_huella.show()
            QApplication.processEvents()

            # 7. Registrar huella digital
            zk_service = ZKServices()
            nombre_completo = datos['persona'].nombre  # Solo el nombre, sin apellidos


            
            resultado_huella = zk_service.registrar_empleado_simple(nombre_completo, self.emplServices.obtener_id_empleado())

            # 8. Manejar resultados
            dialogo_huella.close()
            
            if not resultado_huella['success']:
                DialogoEmergente(
                    'Error en Huella',
                    f"Empleado registrado pero error en huella: {resultado_huella['message']}",
                    'Error',
                    True
                ).exec()
            elif resultado_huella.get('huella_registrada', False):
                DialogoEmergente(
                    'Registro Exitoso',
                    'Empleado registrado con huella digital correctamente',
                    'Check',
                    True
                ).exec()
                self.reject()
            else:
                DialogoEmergente(
                    'Registro Parcial',
                    'Empleado registrado pero no se capturó huella digital',
                    'Warning',
                    True
                ).exec()
                self.reject()

        except Exception as e:
            if 'dialogo_progreso' in locals():
                dialogo_progreso.close()
            if 'dialogo_huella' in locals():
                dialogo_huella.close()
            logger.error(f"Error en registro completo: {str(e)}")
            DialogoEmergente(
                'Error',
                f'Ocurrió un error inesperado:\n\n{str(e)}',
                'Error',
                True
            ).exec()


   