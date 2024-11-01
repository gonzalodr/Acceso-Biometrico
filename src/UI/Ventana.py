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
        # self.setMinimumSize(700, 600)
        # self.tiempo_inactividad = 1 * 10 * 1000  # Ajusta el tiempo de inactividad aquí (en milisegundos)

        # self.temporizador_inactividad = QTimer(self)
        # self.temporizador_inactividad.timeout.connect(self.cerrar_sesion_por_inactividad)

        login = IniciarSesion()
        login.autenticacion.connect(self._autenticacion_login)
        self.setCentralWidget(login)
        self.setWindowTitle("Acceso biometrico")
        
    def _autenticacion_login(self,user:Usuario):
        self.setCentralWidget(None)
        # self.temporizador_inactividad.start(self.tiempo_inactividad) 
        vista = vistaPrincipal(usuario=user)
        self.setCentralWidget(vista)
        
    # def cerrar_sesion_por_inactividad(self):
    #     dial = DialogoEmergente("¡Inactividad!","La sesión se cerrara pronto por inactividad.\n¿Quieres seguir?","Warning",True,True)
    #     temporizador = QTimer()
    #     temporizador.setSingleShot(True) 
    #     temporizador.timeout.connect(dial.reject)
    #     temporizador.start(120000)  
    #     if dial.exec() == QDialog.Accepted:
    #         self.temporizador_inactividad.start(self.tiempo_inactividad)
    #     else:    
    #         self.temporizador_inactividad.stop()
    #         login = IniciarSesion()
    #         login.autenticacion.connect(self._autenticacion_login)
    #         self.setCentralWidget(login)

    # def event(self, event):
    #     if event.type() in (QEvent.MouseButtonPress, QEvent.KeyPress,QEvent.MouseMove, QEvent.FocusIn):
    #         print("Reinicio de temporizador")
    #         self.temporizador_inactividad.start(self.tiempo_inactividad)
    #     return super().event(event)
    
    # def closeEvent(self, event):
    #     dial = DialogoEmergente("¿?","¿Estas seguro que quieres cerrar la aplicación?","Question",True,True)
    #     if dial.exec() == QDialog.Accepted:
    #         event.accept()  # Aceptar el cierre de la ventana
    #     else:
    #         event.ignore() 

                
        
        

            



