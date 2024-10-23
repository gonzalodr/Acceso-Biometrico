from PySide6.QtWidgets import *
from PySide6.QtCore import *
from UI.InicioSesionVista import InicioSesion
from UI.VistaPrincipal import MenuPrincipal
from models.usuario import Usuario
from services.usuarioService import UsuarioServices
from UI.DialogoEmergente import DialogoEmergente
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
        
        # menu = MenuPrincipal(parent=self)
        # self.setCentralWidget(menu)
        
        # ## Inicio de la sesion
        login = InicioSesion(parent=self)
        
        ##Crear la logica del btn iniciar sesion
        login.botonIniciar.clicked.connect(lambda:self.accion_btn_iniciar_sesion(login.inputUsuario.text(),login.inputContrasena.text(),login))
        
        # ##presenta la pantalla
        self.setCentralWidget(login)
        # self.setCentralWidget(vista1)
        self.setWindowTitle("Acceso biometrico")
        
    def accion_btn_iniciar_sesion(self,usuario,contrasena,login):
        # usuario = self.inputUsuario.text()
        # contrasena = self.inputContrasena.text()
        if not usuario.strip() and not contrasena.strip():
            advertencia = DialogoEmergente("¡Advertencia!","¡Ingrese su usuario y contraseña!","Warning")
            advertencia.exec()
        else:
            servicesUser = UsuarioServices()
            result = servicesUser.iniciar_sesion(usuario,contrasena)
            print(result)
            if result["success"]:
                if result["login"]:
                    advertencia = DialogoEmergente("¡Iniciando sesión!",result["message"],"Check")
                    advertencia.exec()
                    ##CARGA TODAS LAS VISTAS              
                    menu = MenuPrincipal(parent=self)
                    ## se ingresa a la vista
                    self.listasVistas.addWidget(menu)
                    ##muestra el menu 
                    self.listasVistas.setCurrentIndex(0) 
                    ##Le indico que todas las vistas seran centradas y acomodada a la ventana
                    self.setCentralWidget(self.listasVistas)
                else:
                    login.labelError.setText(result["message"])
            else:
                login.labelError.setText("Error de conexion")
                
        
        

            



