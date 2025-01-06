from PySide6.QtWidgets import *
from PySide6.QtCore import *
from Utils.Utils import *
# from UI.DialogoEmergente import *
import sys

class formEmpleado(QDialog):
    idEmpleado = None
    fotografia = None

    def __init__(self, parent = None, titulo = 'Registrar empleado', id_empleado = None):
        super().__init__(parent)
        self.setObjectName('form')
        self.setMinimumSize(QSize(1050,700))
        # self.setWindowFlags(Qt.FramelessWindowHint)
        cargar_estilos('claro','formEm.css',self)
        
        layoutPrin =QVBoxLayout()
        frame = QFrame()
        frame.setObjectName('formFrame')
        #asignando el frame al layout principal
        layoutPrin.addWidget(frame)

        ## layoutFrame
        layoutFrame = QVBoxLayout()
        lbltitulo = QLabel(titulo)
        lbltitulo.setObjectName('lbltitulo')
        lbltitulo.setAlignment(Qt.AlignCenter)
        lbltitulo.setMinimumHeight(40)
        layoutFrame.addWidget(lbltitulo)

        ## layoutContent
        self.layoutContent = QHBoxLayout()

        self._llenar_layoutConten()

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
    def _llenar_layoutConten(self): 
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
        #margenes
        # self.layoutIzq.setContentsMargins(15,20,15,0)
        # self.layoutCent.setContentsMargins(15,20,15,0)
        # self.layoutDer.setContentsMargins(15,20,15,0)

        #creando scrolls
        scroll_areaIzq = QScrollArea()
        scroll_areaIzq.setWidgetResizable(True)
        scroll_areaCent= QScrollArea()
        scroll_areaCent.setWidgetResizable(True)
        scroll_areaDer = QScrollArea()
        scroll_areaDer.setWidgetResizable(True)

        self._llenar_layoutIzq()
        self._llenar_layoutCent()
        self._llenar_layoutDer()
        
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
    def _llenar_layoutIzq(self):
        tituloIzq = QLabel('Datos Personales')
        tituloIzq.setObjectName('lblsubtitulos')
        tituloIzq.setAlignment(Qt.AlignCenter)

        self.layoutFoto = QVBoxLayout()
        self._llenar_LayoutFoto()
        #Creando Label, Input y label de error
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
        self.layoutIzq.addLayout(self._contenedor(self.lblNombre,self.inNombre,self.errNombre))
        self.layoutIzq.addLayout(self._contenedor(self.lblApellidos,self.inApellidos,self.errApellidos))
        self.layoutIzq.addLayout(self._contenedor(self.lblCedula,self.inCedula,self.errCedula))
        self.layoutIzq.addLayout(self._contenedor(self.lblNacimiento,self.inNacimiento,self.errNacimiento))
        self.layoutIzq.addLayout(self._contenedor(self.lblCorreo,self.inCorreo,self.errCorreo))
        self.layoutIzq.addLayout(self._contenedor(self.lblEstCivil,self.inEstCivil,self.errEstCivil))
        self.layoutIzq.addLayout(self._contenedor(self.lblDireccion,self.inDireccion,self.errDireccion))
    '''
    Llenado de layoutCent
    '''
    def _llenar_layoutCent(self):
        tituloCent = QLabel('Departamento y Rol')
        tituloCent.setObjectName('lblsubtitulos')
        tituloCent.setAlignment(Qt.AlignCenter)

        #Departamento
        self.lblDep = QLabel('Departamento')
        self.inDep = QComboBox()
        self.errDep = QLabel('Error Departamento')
        #Departamento
        self.lblRol = QLabel('Rol')
        self.inRol = QComboBox()
        self.errRol = QLabel('Error Rol')

        self.layoutCent.addWidget(tituloCent)
        self.layoutCent.addLayout(self._contenedor(self.lblDep,self.inDep,self.errDep))
        self.layoutCent.addLayout(self._contenedor(self.lblRol,self.inRol,self.errRol))
        self.layoutCent.setAlignment(Qt.AlignTop) ##Alinea los widgets arriba
    '''
    Llenado de layoutDer
    '''
    def _llenar_layoutDer(self):
        tituloDer = QLabel('Usuarios')
        tituloDer.setObjectName('lblsubtitulos')
        tituloDer.setAlignment(Qt.AlignCenter)
        self.layoutDer.addWidget(tituloDer)
        self.layoutDer.setAlignment(Qt.AlignTop)
    '''
    Llenado de layoutFoto
    '''
    def _llenar_LayoutFoto(self):
        self.foto = QLabel()
        self.foto.setObjectName('foto')
        self.foto.setFixedSize(250,250)
        self.foto.setAlignment(Qt.AlignCenter)
        self.foto.setStyleSheet('#foto{border-radius:10;border: 1px solid black;}')
        cargar_Icono(self.foto,'userPerson.png')

        self.btnFoto = QPushButton(text='Seleccionar foto')
        self.btnFoto.setObjectName('select_foto')
        self.btnFoto.setFixedHeight(40)
        self.btnFoto.clicked.connect(self._seleccionar_foto)

        self.layoutFoto.setAlignment(Qt.AlignCenter)
        self.layoutFoto.addWidget(self.foto)
        self.layoutFoto.addWidget(self.btnFoto)
    '''
    Contenedor independiente para cada input
    '''
    def _contenedor(self,label:QLabel,input,label_error:QLabel)->QVBoxLayout:
        layout = QVBoxLayout()
        layout.setContentsMargins(10,5,10,0)
        layout.setSpacing(0)
        
        label_error.setObjectName("lblerror")
        label_error.setMaximumHeight(25)
        label_error.setMinimumHeight(25)
        label_error.setWordWrap(True)
        
        layout.addWidget(label)
        layout.addSpacing(5)
        layout.addWidget(input)
        layout.addWidget(label_error)
        return layout
    '''
    Logica
    '''
    #Seleccion de foto
    def _seleccionar_foto(self):
        if self.fotografia is None: 
            dir_defecto = QStandardPaths.writableLocation(QStandardPaths.PicturesLocation)
            file_path, _ = QFileDialog.getOpenFileName(self,"Seleccionar Imagen",dir_defecto,"Imágenes (*.png *.jpg *.jpeg)")
            if file_path:
                self.foto.setPixmap(QPixmap(file_path).scaled(self.foto.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
                self.btnFoto.setText("Eliminar foto")
                try:
                    with open(file_path, "rb") as file:
                        self.fotografia = file.read()
                except Exception as e:
                    cargar_Icono(self.foto,'userPerson.png')
                    self.btnFoto.setText("Seleccionar foto")
                    self.fotografia = None
        else:
            cargar_Icono(self.foto,'userPerson.png')
            self.btnFoto.setText("Seleccionar foto")
            self.fotografia = None


if __name__ == '__main__':
    app = QApplication(sys.argv)
    dialogo = formEmpleado()
    dialogo.show()
    sys.exit(app.exec())