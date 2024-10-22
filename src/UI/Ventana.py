from PySide6.QtWidgets import *
from PySide6.QtCore import *
from UI.InicioSesionVista import InicioSesion
from UI.VistaPrincipal import MenuPrincipal
##
# Esta clase maneja la conexion de todas las vistas
# En esta clase se estara listando las vistas que se vayan necesitando
# ##
class Ventana(QMainWindow):
    def __init__(self):
        super().__init__()
        ## Tamaño para poder redimencionar
        # self.size= QSize(500, 500)
        self.setMinimumSize(700, 600)
        
        ## Creacion de una lista de vistas
        self.listasVistas = QStackedWidget()
        
        ## Inicio de la sesion
        vista1 = InicioSesion(parent=self)
        self.setCentralWidget(vista1)
        ##Crear la logica del btn iniciar secion 
        
        
        # self.setCentralWidget(vista1)
        self.setWindowTitle("Acceso biometrico")
        
    def accion_btn_iniciar_sesion(self):

        vista2 = MenuPrincipal(parent=self)
        ## se ingresa a la vista
        self.listasVistas.addWidget(vista2)
        self.listasVistas.setCurrentIndex(0) ## mostrar la vista 2
        ##Le indico que todas las vistas seran centradas y acomodada a la ventana
        self.setCentralWidget(self.listasVistas)
            



