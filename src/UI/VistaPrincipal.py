from PySide6.QtWidgets import *
from PySide6.QtCore import *
import sys

class MenuPrincipal(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        ## layout principal
        self.root_layout = QVBoxLayout()
        self.root_layout.setSpacing(0)
        self.root_layout.setContentsMargins(0,0,0,0)#ajusta el margen(bordes laterales)#000587
        
        ##Encabezado de la pagina
        self.frameEncabezado = QFrame()
        self.frameEncabezado.setStyleSheet("background-color:#000A94;")
        
        ##Cuerpo de la pagina
        self.framCuerpo = QFrame()
        self.framCuerpo.setStyleSheet("background-color:#F0F2FF;")
        
        ## Pie de la pagina
        self.framePiePagina = QFrame()
        self.framePiePagina.setStyleSheet("background-color:#000A94")
        
        ##Agregar encabezado, cuerpo y pie de pagina
        self.root_layout.addWidget(self.frameEncabezado,15)
        self.root_layout.addWidget(self.framCuerpo, 80)
        self.root_layout.addWidget(self.framePiePagina,5)
        self.setLayout(self.root_layout)
        
        self.configurar_encabezado()
        self.configurar_cuerpo()
        
    def configurar_encabezado(self):
        self.gridEncabezado = QGridLayout() ## Crea un grid (Matriz) donde se acomodaran los widgets
        self.gridEncabezado.setSpacing(0)   ## Espacio entre widgets es 0
        self.gridEncabezado.setContentsMargins(0,0,0,0) ## El margen osea borders seran 0
        
        ## Nombre del encabezado(Titulo de la pagina)
        self.nombreEncabezado = QLabel()
        self.nombreEncabezado.setStyleSheet("font: 700 24pt \"Segoe UI\";color:#FFFFFF;")
        self.nombreEncabezado.setText("ACCESO BIOMETRICO")
        self.nombreEncabezado.setAlignment(Qt.AlignCenter) ##alineacion del texto en el centro del label
        
        ## Nombre de la vista en la que se ubica(ejemplo: Administracion de empleados)
        self.nombreVista = QLabel()
        self.nombreVista.setText("Menu principal")
        self.nombreVista.setStyleSheet("font: 700 16pt \"Segoe UI\";color:#FFFFFF;")
        self.nombreVista.setAlignment(Qt.AlignCenter)
        
        #Spaciador isquierda y derecha (Expanding: el espacio se expande de acuerdo a la ventana)
        self.espaciolefth_Enc = QSpacerItem(1,1, QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.espacioright_Enc = QSpacerItem(1,1, QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        ##Spaciador arriba y abajo QSpacerItem(tamañoX, tamañoY,QSizeExpanding, QSizeExpanding)
        self.espaciotop_Enc = QSpacerItem(0,10, QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.espaciobottom_Enc = QSpacerItem(0,10, QSizePolicy.Expanding, QSizePolicy.Maximum)
        
        ## Añadir label al gridencabezado
        self.gridEncabezado.addWidget(self.nombreEncabezado,0,1)
        self.gridEncabezado.addWidget(self.nombreVista,1,1)

        ##Añadir espaciadores 
        self.gridEncabezado.addItem(self.espaciolefth_Enc,1,0)
        self.gridEncabezado.addItem(self.espacioright_Enc,1,2)
        self.gridEncabezado.addItem(self.espaciobottom_Enc,2,2)
        self.frameEncabezado.setLayout(self.gridEncabezado) ## se añade el layout al frame encabezado

    def configurar_cuerpo(self):
        #cuerpo colocacion de las opciones
        self.gridlayoutCuerpo = QGridLayout()
        self.gridlayoutCuerpo.setSpacing(10)
        self.gridlayoutCuerpo.setContentsMargins(20,20,20,20)
        
        self.frameAdminPersona = QFrame()
        self.frameAdminPersona.setStyleSheet("background-color:#000000")
        self.frameAdminPersona.mouseDoubleClickEvent = self.frame_double_click
        
        self.frameAminDepartamento = QFrame()
        self.frameAminDepartamento.setStyleSheet("background-color:#000000")
        
        self.gridlayoutCuerpo.addWidget(self.frameAdminPersona,1,1)
        self.framCuerpo.setLayout(self.gridlayoutCuerpo)
        
    def frame_double_click(self,event):
        if event.button() == Qt.LeftButton:
            print("Frame doble clickeado")