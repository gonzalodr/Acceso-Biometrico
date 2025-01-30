from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from Utils.Utils import *
from models.usuario import *
from services.usuarioService import *
from UI.DialogoEmergente import *
import os

class IniciarSesion(QWidget):
    autenticacion = Signal(Usuario)
    Uservices = UsuarioServices()

    def __init__(self, parent= None):
        super().__init__(parent)
        self.setObjectName("vistaLogin")
        
        #añade estilo a la interfaz
        cargar_estilos('claro','login.css',self)

        frame = QFrame()
        frame.setObjectName("frameFondo")

        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(0,0,0,0)

        self.layoutFrame = QVBoxLayout()
        self.layoutFrame.setSpacing(10)

        lblApp = QLabel(text="ACCESO BIOMETRICO")
        lblApp.setAlignment(Qt.AlignCenter)

        self.layoutFrame.addWidget(lblApp,2)
        self.layoutFrame.addStretch(2)
        self.centrar_frame_login()
        self.layoutFrame.addStretch(1)
        frame.setLayout(self.layoutFrame)
        layout.addWidget(frame)
        self.setLayout(layout)

    def centrar_frame_login(self):
        self.frameLogin = QFrame()
        self.frameLogin.setObjectName("frameLogin")
        # self.frameLogin.setStyleSheet("QFrame{background-color:#FFFFFF;border-radius:15px;}")
        self.frameLogin.setContentsMargins(10,5,10,10)
        Sombrear(self.frameLogin,100,2,2)
        # self.frameLogin.setGraphicsEffect(self._Sombras(self.frameLogin,100,2,2))
        self.frameLogin.setMaximumSize(QSize(350,500))
        self.frameLogin.setMinimumSize(QSize(350,500))

        self.spacing_left = QSpacerItem(1,1, QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.spacing_right = QSpacerItem(1,1, QSizePolicy.Expanding, QSizePolicy.Expanding)

        layoutCuerpo = QHBoxLayout()
        layoutCuerpo.addItem(self.spacing_left)
        layoutCuerpo.addWidget(self.frameLogin)
        layoutCuerpo.addItem(self.spacing_right)

        self.layoutFrame.addLayout(layoutCuerpo,5)
        self.frame_login()

    def frame_login(self):

        lblIcono = QLabel(text="Icono")
        lblIcono.setMaximumHeight(120)
        lblIcono.setAlignment(Qt.AlignCenter)
        cargar_Icono(lblIcono, archivoImg='user.png')

        lblUsurio = QLabel(text="Usuario")
        lblUsurio.setMaximumHeight(40)
        lblUsurio.setAlignment(Qt.AlignCenter)

        lblPass = QLabel(text="Contraseña")
        lblPass.setMaximumHeight(40)
        lblPass.setAlignment(Qt.AlignCenter)

        self.inputUser = QLineEdit()
        self.inputUser.setPlaceholderText("Ingrese su usuario o correo")
        self.inputUser.setMaximumHeight(40)
        self.inputUser.setAlignment(Qt.AlignCenter)
        Sombrear(self.inputUser,15,0,5)

        self.inputPass = QLineEdit()
        self.inputPass.setPlaceholderText("Ingrese su contraseña")
        self.inputPass.setMaximumHeight(40)
        self.inputPass.setAlignment(Qt.AlignCenter)
        self.inputPass.setEchoMode(QLineEdit.Password)
        Sombrear(self.inputPass,15,0,5)

        self.btnIniciarSesion = QPushButton(text="Iniciar sesión")
        self.btnIniciarSesion.setMaximumHeight(50)
        self.btnIniciarSesion.clicked.connect(self.__evento_IniciarSesion)
        Sombrear(self.btnIniciarSesion,30,0,5)

        self.checkVerContrasena = QCheckBox("Mostrar contraseña")
        self.checkVerContrasena.clicked.connect(self.__accion_checkbox)
        Sombrear(self.checkVerContrasena,30,0,5)

        self.lblError = QLabel(text="")
        self.lblError.setObjectName("loginError")
        self.lblError.setAlignment(Qt.AlignCenter)
        self.lblError.setMaximumHeight(30)
        self.lblError.setWordWrap(True)

        layout = QVBoxLayout()
        layout.setContentsMargins(10,1,10,10)
        layout.addWidget(lblIcono,5)
        layout.addWidget(lblUsurio,2)
        layout.addWidget(self.inputUser,1)
        layout.addWidget(lblPass,2)
        layout.addWidget(self.inputPass,1)
        layout.addWidget(self.checkVerContrasena,1)
        layout.addWidget(self.lblError,1)
        layout.addWidget(self.btnIniciarSesion,4)

        self.frameLogin.setLayout(layout)

    def __evento_IniciarSesion(self):
        usuario = self.inputUser.text()
        password = self.inputPass.text()
        if not usuario.strip() or not password.strip():
            self.lblError.setText("Complete los campos para iniciar sesión.")
            if not usuario.strip():
                Sombrear(self.inputUser,15,0,5,"red")
            else:
                Sombrear(self.inputUser,15,0,5)
            if not password.strip():
                Sombrear(self.inputPass,15,0,5,"red")
            else:
                Sombrear(self.inputPass,15,0,5)
        else:
            Sombrear(self.inputUser,15,0,5)
            Sombrear(self.inputPass,15,0,5)
            result = self.Uservices.iniciar_sesion(usuario,password)
            if result["success"]:
                if result["login"]:
                    usuario = result["usuario"]
                    self.inputUser.setText("")
                    self.inputPass.setText("")
                    self.autenticacion.emit(usuario)
                else:
                    self.lblError.setText(result["message"])
            else:
                self.lblError.setText("Error de conexión")

    def __accion_checkbox(self):
        if self.checkVerContrasena.isChecked():
            self.inputPass.setEchoMode(QLineEdit.Normal)
            Sombrear(self.checkVerContrasena,30,0,5,"green")
        else:
            self.inputPass.setEchoMode(QLineEdit.Password)
            Sombrear(self.checkVerContrasena,30,0,5)
