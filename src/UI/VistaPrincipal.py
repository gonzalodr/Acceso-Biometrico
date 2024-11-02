
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from Utils.Utils import *
from UI.slideBar import *
from UI.AdministraPersona.adminPersona import *
from UI.AdministraDepartamento.adminDepartamento import *  # Importa la clase AdminDepartamento
from UI.AdministrarRol.adminRol import *
from models.usuario import *
import sys

class vistaPrincipal(QWidget):
    listaOpciones = [] #numero Index en el stack, el nombre, icono
    usuario:Usuario = None
    
    def __init__(self,usuario:Usuario, parent= None,):
        super().__init__(parent)
        self.usuario = usuario
        self.setObjectName("vistaPrincipal")
        print("Construyendo el objeto")
        """
        add_Style: establece el diseño visual de nuestra ventana
        """
        add_Style("css","ventanaPrincipal.css",self)
        
        """
        frame: Es el frame que le da color a toda la ventana 
        """
        frame = QFrame()
        frame.setObjectName("frameFondoPrincipal")
        frame.setContentsMargins(0,0,0,0)
        
        """
        layoutFrame: Acomoda tanto la seccion de encabezado como la de cuerpo 
        """
        layoutFrame = QVBoxLayout()
        layoutFrame.setContentsMargins(10,10,10,10)
        layoutFrame.setSpacing(10)
        
        """
        frameEncabezado: le da color al encabezado de la ventana
        """
        frameEncabezado = QFrame()
        frameEncabezado.setObjectName("frameEnca")
        frameEncabezado.setContentsMargins(0,0,0,0)
        Sombrear(frameEncabezado,30,0,5)
        
        """
        layoutEncabezado: Acomoda todos los elementos que se mostraran en el encabezado
        """
        layoutEncabezado = QHBoxLayout()
        layoutEncabezado.setSpacing(0)
        layoutEncabezado.setContentsMargins(20,5,20,5)
        
        """
            btnAbrir_SideBar: Este boton nos permitirar abrir y cerrar nuestro sidebar de la ventana
        """
        self.btnAbrir_SideBar = QPushButton(text="")
        self.btnAbrir_SideBar.setCursor(Qt.PointingHandCursor)
        self.btnAbrir_SideBar.setMaximumSize(QSize(45,45))
        cargar_icono_svg(QObjeto=self.btnAbrir_SideBar,archivoSVG="arrow-bar-right.svg",Size=QSize(self.btnAbrir_SideBar.size().width()-15,self.btnAbrir_SideBar.size().height()-15))
        Sombrear(self.btnAbrir_SideBar,20,0,5)
        
        
        """
            lblEncabezado: Mostrara el nombre de nuestra ventana.
        """
        self.lblEncabezado = QLabel(text=f"Bienvenido/a {usuario.usuario}.")
        self.lblEncabezado.setAlignment(Qt.AlignCenter)
        self.lblEncabezado.setMaximumHeight(30)
        # Sombrear(self.lblEncabezado,30,0,5)
        
        """
            lblIconUser: Mostrara la foto de nuestro usuario
        """
        self.lblIconoUser = QLabel(text="User")
        self.lblIconoUser.setObjectName("iconoUser")
        self.lblIconoUser.setMaximumSize(QSize(50,50))
        self.lblIconoUser.setMinimumSize(QSize(50,50))
        self.cargar_imagen_usuario(self.lblIconoUser)
        Sombrear(self.lblIconoUser,30,0,5)
        
        """
            Acomodamos los elementos de nuestra ventana
        """
        layoutEncabezado.addWidget(self.btnAbrir_SideBar,1)
        layoutEncabezado.addStretch(4)
        layoutEncabezado.addWidget(self.lblEncabezado,2)
        layoutEncabezado.addStretch(4)
        layoutEncabezado.addWidget(self.lblIconoUser,1)
        """Agregamos nuestro layout del encabezado a nuestro frame"""
        frameEncabezado.setLayout(layoutEncabezado)
        
        layoutFrame.addWidget(frameEncabezado,1)
        
        """Este layoout es para acomodar los elementos del cuerpo de la ventana"""    
        layoutCuerpo = QHBoxLayout()
        layoutCuerpo.setSpacing(20)
        layoutCuerpo.setContentsMargins(1,10,1,10)
        
        self.stackVistas = QStackedWidget()
        self._llenar_stack_vista()
        
        self.sidebar = SlideBar(listaOpciones=self.listaOpciones)
        self.cargar_imagen_usuario(self.sidebar.lblUsuario)
        self.btnAbrir_SideBar.clicked.connect(lambda click, btn = self.btnAbrir_SideBar:self.sidebar.accion_anim(btnSidebar=btn))

        """Recibimos una señal la cual nos servira para detectar los btn del sidebar"""
        self.sidebar.index_opcion_selecionada.connect(self.seleccion_sidebar)
        
        layoutCuerpo.addWidget(self.sidebar,1)
        layoutCuerpo.addWidget(self.stackVistas,3)
        
        """Agregando sidebar"""
        layoutFrame.addLayout(layoutCuerpo,9)
        
        """Acomodando todo en la ventana"""
        frame.setLayout(layoutFrame)
        layout = QVBoxLayout()
        layout.setContentsMargins(0,0,0,0)
        layout.addWidget(frame)
        self.setLayout(layout)
        
    
    def _llenar_stack_vista(self):
        self.stackVistas.addWidget(self._widget_presentacion())
        """
            Aqui se crean las vistas de acuerdo a los permisos
        """
        if True:
            adminpersona = AdminPersona(parent=self)
            adminpersona.cerrar_adminP.connect(self._salir_crud)
            index =  self.stackVistas.addWidget(adminpersona)
            self.listaOpciones.append((index,"Administrar Persona"))
             
        if True:
            AdminDepart = AdminDepartament(parent=self)
            AdminDepart.cerrar_adminD.connect(self._salir_crud)
            index = self.stackVistas.addWidget(AdminDepart)
            self.listaOpciones.append((index,"Admin. Departamento"))
        if True:
            AdminRol =AdminRol(parent=self)
            AdminRol.cerrar_adminR.connect(self._salir_crud)
            index = self.stackVistas.addWidget(AdminRol)
            self.listaOpciones.append((index,"Admin. Rol"))
        print("LLenando stack")
        print(self.listaOpciones)
        print()
        self.stackVistas.setCurrentIndex(0)
        pass
    
    def _widget_presentacion(self):
        widgetP = QWidget()
        widgetP.setObjectName("widgetDefault")
        
        frame = QFrame()

        layout = QVBoxLayout()
        layout.addWidget(frame)
        lblPresentacion = QLabel(text="Acceso Biometrico")
        lblPresentacion.setAlignment(Qt.AlignCenter)
        Sombrear(lblPresentacion,20,0,0)
        
        layoutP = QVBoxLayout()
        layoutP.setContentsMargins(0,0,0,0)
        layoutP.addWidget(lblPresentacion)
        frame.setLayout(layoutP)
        widgetP.setLayout(layout)
        Sombrear(widgetP,50,0,0)
        return widgetP

    def _salir_crud(self):
        self.sidebar.deseleccionar()
        self.stackVistas.setCurrentIndex(0)
    
    def seleccion_sidebar(self,index):
        print(index)
        self.stackVistas.setCurrentIndex(index)
    
    def cargar_imagen_usuario(self,user,imagen = None):
        try:
            if imagen is not None:
                if not isinstance(imagen, bytes):
                    imagen = bytes(imagen)
                pixmap = QPixmap()
                pixmap.loadFromData(imagen)
                pixmap = pixmap.scaled(user.size(),Qt.KeepAspectRatio, Qt.SmoothTransformation)
                user.setPixmap(pixmap)
            else:
                raise ValueError("La imagen es nulo")
        except Exception as e: 
            if hasattr(user, 'setPixmap'):
                cargar_icono_svg(QObjeto=user, carpeta="iconos", archivoSVG="person-circle.svg")
            else:
                print("El objeto proporcionado no es un QLabel o no tiene el método setPixmap.")