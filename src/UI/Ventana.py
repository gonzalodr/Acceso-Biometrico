from PySide6.QtWidgets import *
from PySide6.QtCore import *
from models.usuario import Usuario
from UI.inicioSesion import *
from UI.VistaPrincipal import *
from UI.DialogoEmergente import *


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
        login = IniciarSesion()
        login.autenticacion.connect(self._autenticacion_login)
        self.setCentralWidget(login)
        self.setWindowTitle("Acceso biometrico")
        
    def _autenticacion_login(self,user:Usuario):
        vista = vistaPrincipal(usuario=user)
        self.setCentralWidget(vista)
    
    def closeEvent(self, event):
        dial = DialogoEmergente("¿?","¿Estas seguro que quieres cerrar la aplicación?","Question",True,True)
        if dial.exec() == QDialog.Accepted:
            event.accept()  # Aceptar el cierre de la ventana
        else:
            event.ignore() 

                
        
        

            



