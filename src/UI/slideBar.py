import sys
from PySide6.QtCore import *
from PySide6.QtWidgets import *
from Utils.Utils import *
from UI.DialogoEmergente import *

class SlideBar(QWidget):
    index_opcion_selecionada = Signal(int)
    senal_abrirConfig = Signal()
    
    def __init__(self,parent= None, listaOpciones=[]):
        """
            Sidebar permite tener un menu de opciones al lado izquierdo de la ventan
            :param parent: Este resive el pariente del objeto
            :param listaBotones: Esta recibe el nombre del btn como el valor numerico
            del la opcion. Tambien debe recibir la ruta del icono o se agregara uno por defecto a cada boton.
        """
        super().__init__(parent=parent)
        self.setObjectName("sidebarWidget")
        self.setMaximumWidth(300)
        self.setMinimumWidth(60)
        self.setFixedWidth(60)
        self.tamano = 60
        ##Añadomos estilos
        cargar_estilos('claro','sidebar.css',self)

        #creamos el layout para contener el frame
        self.layoutSide = QVBoxLayout()
        self.layoutSide.setSpacing(0)
        self.layoutSide.setContentsMargins(0,0,0,0)

        #creamos el frame para el layout de elementos
        self.frame = QFrame()
        #layouto de elementos
        self.layoutFrame = QVBoxLayout()
        self.layoutFrame.setContentsMargins(10,15,0,2)
        self.layoutFrame.setSpacing(0)

        #Conficuramos el icono del usuario
        self.lblUsuario = QLabel(text="User",parent=self)
        self.lblUsuario.setObjectName("iconoUser")
        self.lblUsuario.setMaximumSize(150,150)
        self.lblUsuario.setMinimumSize(150,150)
        self.lblUsuario.setAlignment(Qt.AlignCenter)
        self.lblUsuario.setVisible(False)
        Sombrear(self.lblUsuario,30,0,0)

        #layout para acomodar nuestro icono
        layoutUser = QHBoxLayout()
        layoutUser.setAlignment(Qt.AlignCenter)
        layoutUser.setContentsMargins(0,0,0,0)
        layoutUser.setSpacing(10)
        layoutUser.addWidget(self.lblUsuario)
        layoutUser.setSpacing(10)
        
        self.layoutFrame.addLayout(layoutUser)
        self.layoutFrame.addSpacing(10)
        #grupo de botones
        self.grupoOpciones = QButtonGroup()
        self.grupoOpciones.setExclusive(False)
        
        for opcion in listaOpciones:
            button = QPushButton(text=f"{opcion[1]}")
            
            button.setProperty("index", opcion[0])
            button.setCursor(Qt.PointingHandCursor)
            button.setMaximumHeight(70)
            button.setMinimumHeight(70)
            button.setCheckable(True)
            cargar_icono(button,opcion[2]) 
            self.grupoOpciones.addButton(button)
            self.layoutFrame.addWidget(button)
            
        button = QPushButton(text=f"Conficguracion")
        button.setCursor(Qt.PointingHandCursor)
        button.setMaximumHeight(70)
        button.setMinimumHeight(70)
        cargar_icono(button,'settings.png') 
        # button.clicked.connect(self._abrir_configuracion)
        self.layoutFrame.addWidget(button)

        
        button = QPushButton(text=f"Salir")
        button.setCursor(Qt.PointingHandCursor)
        button.setMaximumHeight(70)
        button.setMinimumHeight(70)
        cargar_icono(button,'exit.png') 
        button.clicked.connect(self._cerrar_App)
        
        self.layoutFrame.addWidget(button)
        """
            Esta señal permite saber que bonton ha sido seleccionado desde ventan principal
        """
        self.grupoOpciones.buttonClicked.connect(self.botton_seleccionado)
       
        self.frame.setLayout(self.layoutFrame)

        # self.layoutSide.addWidget(self.frame)
        # Crear un QScrollArea
        self.scrollArea = QScrollArea(self)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # Solo scroll vertical
        self.scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        self.scrollArea.setWidget(self.frame)
        self.layoutSide.addWidget(self.scrollArea)
        self.setLayout(self.layoutSide)
        Sombrear(self,50,0,0)

    def botton_seleccionado(self,button):
        if not button.isChecked():
            button.setChecked(True)
            return
        for btn in self.grupoOpciones.buttons():
            if btn != button:
                btn.setChecked(False) #Deselecciona el btn
            else:
                self.index_opcion_selecionada.emit(btn.property("index"))

    def _abrir_configuracion(self):
        self.senal_abrirConfig.emit()

    def _cerrar_App(self):
        QApplication.quit()

    def deseleccionar(self):
        for btn in self.grupoOpciones.buttons():
            btn.setChecked(False) #Deselecciona el btn

    def accion_anim(self,btnSidebar):
        if self.tamano == 60:
            self._animacion_abrir()
            cargar_icono_svg(QObjeto=btnSidebar,archivoSVG="arrow-bar-left.svg",Size=QSize(btnSidebar.size().width()-15,btnSidebar.size().height()-15))
        elif self.tamano == 300:
            self._animacion_cerrar()
            cargar_icono_svg(QObjeto=btnSidebar,archivoSVG="arrow-bar-right.svg",Size=QSize(btnSidebar.size().width()-15,btnSidebar.size().height()-15))

    def _animacion_cerrar(self):
        # Crear animación para reducir el ancho
        anim_cerrar = QPropertyAnimation(self, b"maximumWidth",self)
        anim_cerrar.setDuration(500)
        anim_cerrar.setEasingCurve(QEasingCurve.InOutQuad)
        anim_cerrar.setStartValue(self.tamano)
        anim_cerrar.setEndValue(50)
        anim_cerrar.start()
        self.tamano = 60
        self.lblUsuario.setVisible(False)

    def _animacion_abrir(self):
        # Crear animación para aumentar el ancho
        anim_abrir = QPropertyAnimation(self, b"maximumWidth",self)
        anim_abrir.setDuration(500)
        anim_abrir.setEasingCurve(QEasingCurve.InOutQuad)
        anim_abrir.setStartValue(self.tamano)
        anim_abrir.setEndValue(300)
        anim_abrir.start()
        self.tamano = 300
        self.lblUsuario.setVisible(True)
