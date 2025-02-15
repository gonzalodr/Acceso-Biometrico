from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import QIntValidator
from Utils.Utils import *
from services.empleadoServices import EmpleadoServices
from services.usuarioService import UsuarioServices
from services.rolService import RolServices
from services.departamentoService import DepartamentoServices
from services.rolService import RolServices
import re

class formEmpleado(QDialog):
    idEmpleado = None
    fotografia = None
    idUsuario = None
    idPersona = None

    emplServices = EmpleadoServices()
    userServices = UsuarioServices()
    depaServices = DepartamentoServices()
    rolServices  = RolServices()

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
        
        boton_box.button(QDialogButtonBox.Ok).setText("Registrar" if id == None else "Actualizar")
        boton_box.button(QDialogButtonBox.Ok).setObjectName("btnregistrar")
        boton_box.button(QDialogButtonBox.Ok).setMinimumSize(QSize(100,30))
        Sombrear(boton_box,20,0,5)

        layoutFrame.addWidget(boton_box)
        frame.setLayout(layoutFrame)
        self.setLayout(layoutPrin)
        
    '''
    LLenado de layoutContent
    '''
    def llenarLayoutConten(self): 
        #creando widgets para el scrol
        self.widgetIzq = QWidget()
        self.widgetCent = QWidget()
        self.widgetDer = QWidget()

        #creando los layouts
        self.layoutIzq = QVBoxLayout()
        self.layoutCent = QVBoxLayout()
        self.layoutDer = QVBoxLayout()

        #configuracion de los layouts
        self.layoutIzq.setSpacing(20)
        self.layoutCent.setSpacing(20)
        self.layoutDer.setSpacing(20)

        #creando scrolls
        scroll_areaIzq = QScrollArea()
        scroll_areaIzq.setWidgetResizable(True)
        scroll_areaCent= QScrollArea()
        scroll_areaCent.setWidgetResizable(True)
        scroll_areaDer = QScrollArea()
        scroll_areaDer.setWidgetResizable(True)

        self.llenarLayoutIzquierda()
        self.llenarLayoutCentral()
        self.llenarLayoutDerecho()
        
        # Crear los scroll areas
        self.scrollIzq = QScrollArea()
        self.scrollCent = QScrollArea()
        self.scrollDer = QScrollArea()

        # Configurar las scroll areas
        self.scrollIzq.setWidgetResizable(True)
        self.scrollCent.setWidgetResizable(True)
        self.scrollDer.setWidgetResizable(True)

        # Crear widgets contenedores para cada scroll area
        widgetIzq = QWidget()
        widgetCent = QWidget()
        widgetDer = QWidget()

        # Asignar layouts a los widgets contenedores
        widgetIzq.setLayout(self.layoutIzq)
        widgetCent.setLayout(self.layoutCent)
        widgetDer.setLayout(self.layoutDer)
        #agregando nombres
        widgetIzq.setObjectName('contenedor')
        widgetCent.setObjectName('contenedor')
        widgetDer.setObjectName('contenedor')

        # Asignar los widgets a las scroll areas
        self.scrollIzq.setWidget(widgetIzq)
        self.scrollCent.setWidget(widgetCent)
        self.scrollDer.setWidget(widgetDer)

        # Agregar las scroll areas al layout principal
        self.layoutContent.addWidget(self.scrollIzq)
        self.layoutContent.addWidget(self.scrollCent)
        self.layoutContent.addWidget(self.scrollDer)
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
        self.errNombre = QLabel('Error nombre')

        #Apellidos
        self.lblApellidos = QLabel('Apellidos')
        self.inApellidos = QLineEdit()
        self.errApellidos = QLabel('Error apellidos')

        #Cedula
        self.lblCedula = QLabel('Cedula')
        self.inCedula = QLineEdit()
        self.errCedula = QLabel('Error cedula')

        #Fecha de nacimiento
        self.lblNacimiento = QLabel('Nacimiento')
        self.inNacimiento = QDateEdit()
        self.inNacimiento.setCalendarPopup(True)
        self.inNacimiento.setDisplayFormat('yyyy-MM-dd')
        self.inNacimiento.setMaximumDate(QDate.currentDate())
        self.errNacimiento = QLabel('Error nacimiento')

        #Correo
        self.lblCorreo = QLabel('Correo')
        self.inCorreo = QLineEdit()
        self.errCorreo = QLabel('Error correo')

        #cargar layout de telefonos
        self.lblTelefonos = QLabel(text='Telefonos')
        self.layoutTelPrinc = QVBoxLayout()
        self.errTelefono = QLabel(text='Error')
        self.llenarLayoutTelefono()

        #Estado civil
        self.lblEstCivil = QLabel('Estado civil')
        self.inEstCivil = QComboBox()
        self.errEstCivil = QLabel('Error estado civil')
        #Direccion
        self.lblDireccion = QLabel('Direccion')
        self.inDireccion = QTextEdit()
        self.inDireccion.setMaximumHeight(30)
        self.errDireccion = QLabel('Error Direccion')
        
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
    '''
    Llenado de layoutCent
    '''
    def llenarLayoutCentral(self):
        tituloCent = QLabel('Departamento y Rol')
        tituloCent.setObjectName('lblsubtitulos')
        tituloCent.setAlignment(Qt.AlignCenter)

        #Departamento
        self.lblDep = QLabel('Departamento')
        self.inDep = QComboBox()
        self.inDep.addItem('Ninguno', None)
        self.inDep.setMaxVisibleItems(10)
        self.errDep = QLabel('Error Departamento')
        self.llenarComboboxDepa()
        #Departamento
        self.lblRol = QLabel('Rol')
        self.inRol = QComboBox()
        self.inRol.addItem('Ninguno', None)
        self.inRol.setMaxVisibleItems(10)
        self.errRol = QLabel('Error Rol')
        self.llenarComboboxRol()

        self.layoutCent.addWidget(tituloCent)
        self.layoutCent.addLayout(self.contenedor(self.lblDep,self.inDep,self.errDep))
        self.layoutCent.addLayout(self.contenedor(self.lblRol,self.inRol,self.errRol))
        self.layoutCent.setAlignment(Qt.AlignTop) ##Alinea los widgets arriba
    '''
    Llenado de layoutDer
    '''
    def llenarLayoutDerecho(self):
        tituloDer = QLabel('Usuarios')
        tituloDer.setObjectName('lblsubtitulos')
        tituloDer.setAlignment(Qt.AlignCenter)
        self.layoutDer.addWidget(tituloDer)
        self.layoutDer.setAlignment(Qt.AlignTop)
    '''
    Llenado de layoutFoto
    '''
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

        self.layoutFoto.setAlignment(Qt.AlignCenter)
        self.layoutFoto.addWidget(self.foto)
        self.layoutFoto.addWidget(self.btnFoto)
    '''
    Contenedor independiente para cada input
    '''
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
    '''
    llenado de layoutTelefono
    '''
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
    '''
    llenado dinamico de inputs para telefonos
    '''  
    def agregar_nuevo_telefono(self):
        #lblTelefono para cada input telefono
        lblTelefono = QLabel(text='Numero de telefono')

        #input para ingresar el telefono
        inputTelefono = QLineEdit()
        inputTelefono.setPlaceholderText('Ej. 11111111')
        inputTelefono.setValidator(QIntValidator())
        inputTelefono.textChanged.connect(lambda : self.verificar_numero(inputTelefono))

        #input para tipo de contacto
        lblTipo = QLabel(text='Tipo de contacto')

        #input para ingresar el tipo de telefono
        inputTipo = QLineEdit()
        inputTipo.setPlaceholderText('Ej. Telefono fijo')

        #boton para eliminar el telefono
        btnEliminar = QPushButton("Eliminar")
        btnEliminar.setObjectName('eliminar_telefono')
        btnEliminar.setMinimumHeight(30)

        #lblTelefono de error
        lblError = QLabel(text='Error:')
        lblError.setObjectName("lblerror")
        lblError.setMaximumHeight(25)
        lblError.setMinimumHeight(25)
        lblError.setWordWrap(True)

        GLInpTelefonos = QVBoxLayout()
        GLInpTelefonos.setContentsMargins(10,20,10,20)
        GLInpTelefonos.setSpacing(10)
        GLInpTelefonos.addWidget(lblTelefono,0)
        GLInpTelefonos.addWidget(inputTelefono,1)
        GLInpTelefonos.addWidget(lblTipo,2,)
        GLInpTelefonos.addWidget(inputTipo,3)
        GLInpTelefonos.addWidget(lblError,4)
        GLInpTelefonos.addWidget(btnEliminar,5)
       
        btnEliminar.clicked.connect(lambda: self.eliminar_telefono(GLInpTelefonos))
        self.layoutInputTel.addLayout(GLInpTelefonos)
    '''
    eliminado de los inputs dinamicos para los telefonos
    '''
    def eliminar_telefono(self, GLInpTelefonos:QVBoxLayout):
        listWidget = []
        #obtiene la lista de los widgets en el layout a eliminar
        for i in range(6):
            listWidget.append(GLInpTelefonos.itemAt(i).widget())
        #los eliminar uno por uno
        for widget in listWidget:
            GLInpTelefonos.removeWidget(widget)
            if isinstance(widget,QPushButton):
                widget.clicked.disconnect()
            widget.deleteLater()
        #elimina el layout
        self.layoutInputTel.removeItem(GLInpTelefonos)
        GLInpTelefonos.deleteLater()
    '''
    Verificar si el numero es valido
    '''
    def verificar_numero(self, input: QLineEdit):
        numero = input.text()
        if self.es_numero_valido(numero):
            input.setProperty('telValido',True)
        else:
            input.setProperty('telValido',False)
        input.style().polish(input)  

    def es_numero_valido(self, numero: str) -> bool:
        patron = re.compile(r'^[2456789]\d{7}$')
        return bool(patron.match(numero))

    def obtenerTelefonosInputs(self):
        lista =[]
        #obtengo los valores de cada numero ingresado junto con su tipo
        for i in range(self.layoutInputTel.count()):
            item = self.layoutInputTel.itemAt(i).layout()
            if isinstance(item,QVBoxLayout):
                pass
                # numero = item.itemAt(1).widget().text()
                # tipoCont = item.itemAt(3).widget().text()
                # lblError:QLabel = item.itemAt(4).widget()
                # if not numero and not tipoCont:
                #     print('El numero y tipo de contacto esta vacio.')
                #     lblError.setText('El numero y tipo de contacto estan vacios')
                # elif not numero:
                #     print('El numero esta vacio')
                #     lblError.setText('El numero esta vacio')
                # elif not tipoCont:
                #     print('El tipo de contacto esta vacio')
                #     lblError.setText('El tipo de contacto esta vacio')
                
                # print(f'Tel.: {numero}  Tipo: {tipoCont}')
    '''
        Llenado de combobox Rol y departamento
    '''
    def llenarComboboxDepa(self):
        result = self.depaServices.obtenerTodoDepartamento()
        print(result)
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
        print(result)
        if not result['success']:
            self.reject()
            return
        
        if len(result['data']['listaRoles']) == 0:
            self.inDep.setItemText(0,'No hay roles registrados.')
            return

        for rol in result['data']['listaRoles']:
            self.inRol.addItem(rol.nombre, rol.id)
            
    '''
    Logica
    '''
    #Seleccion de foto
    def seleccionarFoto(self):
        if self.fotografia is None:
            self.abrir_seleccion_imagen()
        else:
            self.eliminar_foto()

    def abrir_seleccion_imagen(self):
        dir_defecto = QStandardPaths.writableLocation(QStandardPaths.PicturesLocation)
        file_path, _ = QFileDialog.getOpenFileName(self, "Seleccionar Imagen", dir_defecto, "Imágenes (*.png *.jpg *.jpeg)")
        if file_path:
            self.mostrar_foto(file_path)
            self.btnFoto.setText("Eliminar foto")
            try:
                with open(file_path, "rb") as file:
                    self.fotografia = file.read()
            except Exception as e:
                self.resetear_foto()

    def mostrar_foto(self, file_path):
        self.foto.setPixmap(QPixmap(file_path).scaled(self.foto.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

    def eliminar_foto(self):
        self.resetear_foto()

    def resetear_foto(self):
        cargar_Icono(self.foto, 'userPerson.png')
        self.btnFoto.setText("Seleccionar foto")
        self.fotografia = None

    
    
    
    
#
# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     dialogo = formEmpleado()
#     dialogo.show()
#     sys.exit(app.exec())