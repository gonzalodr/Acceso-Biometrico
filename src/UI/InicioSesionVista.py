from PySide6.QtWidgets import *
from PySide6.QtCore import *
from UI.stilosInterfaz import *
from services.usuarioService import UsuarioServices
from models.usuario import Usuario
from UI.DialogoEmergente import DialogoEmergente

class InicioSesion(QWidget):
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
        self.configurar_login()

    def configurar_encabezado(self):
        self.gridEncabezado = QGridLayout() ## Crea un grid (Matriz) donde se acomodaran los widgets
        self.gridEncabezado.setSpacing(0)   ## Espacio entre widgets es 0
        self.gridEncabezado.setContentsMargins(0,0,0,0) ## El margen osea borders seran 0
        
        #       Alineación horizontal
        # Qt.AlignLeft: Alinea el texto a la izquierda.
        # Qt.AlignRight: Alinea el texto a la derecha.
        # Qt.AlignHCenter: Alinea el texto horizontalmente en el centro.
        # Qt.AlignJustify: Justifica el texto para que ocupe todo el ancho disponible.
        #       Alineación vertical
        # Qt.AlignTop: Alinea el texto en la parte superior.
        # Qt.AlignBottom: Alinea el texto en la parte inferior.
        # Qt.AlignVCenter: Alinea el texto verticalmente en el centro.
        #       Alineación combinada
        # Qt.AlignCenter: Alinea el texto tanto horizontal como verticalmente en el centro.
                
        
        
        ## Nombre del encabezado(Titulo de la pagina)
        self.nombreEncabezado = QLabel()
        self.nombreEncabezado.setStyleSheet("font: 700 24pt \"Segoe UI\";color:#FFFFFF;")
        self.nombreEncabezado.setText("ACCESO BIOMETRICO")
        self.nombreEncabezado.setAlignment(Qt.AlignCenter) ##alineacion del texto en el centro del label
        
        ## Nombre de la vista en la que se ubica(ejemplo: Administracion de empleados)
        self.nombreVista = QLabel()
        self.nombreVista.setText("Inicio de sesión")
        self.nombreVista.setStyleSheet("font: 700 16pt \"Segoe UI\";color:#FFFFFF;")
        self.nombreVista.setAlignment(Qt.AlignCenter)
        
        # QSizePolicy.Fixed: El widget no se puede redimensionar. Tiene un tamaño fijo.
        # QSizePolicy.Minimum: El widget no se reducirá más allá de su tamaño mínimo, pero puede expandirse si hay espacio adicional disponible.
        # QSizePolicy.Maximum: El widget puede reducirse hasta su tamaño mínimo pero no se expandirá más allá de su tamaño actual.
        # QSizePolicy.Preferred: El widget se redimensiona según su tamaño preferido, pero puede expandirse si hay espacio adicional disponible o reducirse hasta su tamaño mínimo si es necesario.
        # QSizePolicy.Expanding: El widget siempre intentará ocupar todo el espacio disponible, expandiéndose lo máximo posible en la dirección especificada.
        # QSizePolicy.MinimumExpanding: El widget tiene un tamaño mínimo, pero si hay espacio adicional disponible, se expandirá como un widget con política de expansión completa.
        # QSizePolicy.Ignored: El tamaño del widget no se tiene en cuenta en absoluto, y el widget se redimensionará para llenar todo el espacio disponible, independientemente de sus restricciones de tamaño.
        
        #Spaciador isquierda y derecha (Expanding: el espacio se expande de acuerdo a la ventana)
        self.espaciolefth_Enc = QSpacerItem(1,1, QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.espacioright_Enc = QSpacerItem(1,1, QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        ##Spaciador arriba y abajo QSpacerItem(tamañoX, tamañoY,QSizeExpanding, QSizeExpanding)
        self.espaciotop_Enc = QSpacerItem(0,10, QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.espaciobottom_Enc = QSpacerItem(0,10, QSizePolicy.Expanding, QSizePolicy.Maximum)
        
        ## Añadir label al gridencabezado
        self.gridEncabezado.addWidget(self.nombreEncabezado,0,1)
        self.gridEncabezado.addWidget(self.nombreVista,1,1)
        ##     0   1   2
        #   0|   | N |   |
        #   1| l | V | r |
        #   2|   | b |   |
        # ##
        ##Añadir espaciadores 
        self.gridEncabezado.addItem(self.espaciolefth_Enc,1,0)
        self.gridEncabezado.addItem(self.espacioright_Enc,1,2)
        self.gridEncabezado.addItem(self.espaciobottom_Enc,2,2)
        self.frameEncabezado.setLayout(self.gridEncabezado) ## se añade el layout al frame encabezado

    ##se acomoda lo que son tablas o demas widgets
    def configurar_cuerpo(self):
        self.gridCuerpo = QGridLayout() ## Crea un grid (Matriz) donde se acomodaran los widgets
        self.gridCuerpo.setSpacing(0)   ## sin espacios entre widgets
        self.gridCuerpo.setContentsMargins(0,0,0,0) ## sin margenes
        
        #Spaciador isquierda y derecha (Expanding: el espacio se expande de acuerdo a la ventana)
        self.espaciolefth_Cuer = QSpacerItem(150,0, QSizePolicy.MinimumExpanding, QSizePolicy.Expanding)
        self.espacioright_Cuer = QSpacerItem(150,0, QSizePolicy.MinimumExpanding, QSizePolicy.Expanding)
        
        ##Spaciador arriba y abajo QSpacerItem(tamañoX, tamañoY,QSizeExpanding, QSizeExpanding)
        self.espaciotop_Cuer = QSpacerItem(0,100, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.espaciobottom_Cuer = QSpacerItem(0,100, QSizePolicy.Expanding, QSizePolicy.Minimum)
        
        
        # # Crear un efecto de sombra
        # shadow_effect = QGraphicsDropShadowEffect()
        # shadow_effect.setBlurRadius(0)  # Radio de desenfoque de la sombra
        # shadow_effect.setXOffset(10)  # Desplazamiento en el eje X
        # shadow_effect.setYOffset(10)  # Desplazamiento en el eje Y
        # shadow_effect.setColor(Qt.black)  # Color de la sombra
        
        self.frameLogin = QFrame()  ## donde iran los inputs del login 
        self.frameLogin.setStyleSheet("background-color:#DDE2FE;border-radius: 30px;")
        # self.frameLogin.setGraphicsEffect(shadow_effect)
        
        self.layoutLogin = QVBoxLayout() ##donde se acomodaran los inputs
        self.layoutLogin.setContentsMargins(2,2,2,2)
        
        ##        0   1  2
        #      0 |  | t|  |         l = espacio derecho left        t = arriba top   
        #      1 |l | F| r|         r = espacio izquierdo right     b = abajo bottom
        #      2 |  | b|  |         f = frame
        # ##
        
        # Añadir los espaciadores y el frame al gridCuerpo
        self.gridCuerpo.addItem(self.espaciotop_Cuer, 0, 1)        # Espaciador arriba
        self.gridCuerpo.addItem(self.espaciolefth_Cuer, 1, 0)      # Espaciador izquierda
        self.gridCuerpo.addWidget(self.frameLogin, 1, 1)           # Frame del login en el centro
        self.gridCuerpo.addItem(self.espacioright_Cuer, 1, 2)      # Espaciador derecha
        self.gridCuerpo.addItem(self.espaciobottom_Cuer, 2, 1)     # Espaciador abajo

        self.framCuerpo.setLayout(self.gridCuerpo) ## se añade al frame cuerpo
        
    def configurar_login(self):
        ## layout de que acomodara los inputs
        self.layoutInputLogin = QVBoxLayout()
        self.layoutInputLogin.setContentsMargins(30,30,30,30)
        self.layoutInputLogin.setSpacing(0)
        
        ##labels Usuario, contraseña y mensaje de error
        self.labelUsuario = QLabel()
        self.labelUsuario.setText("Usuario")
        self.labelUsuario.setAlignment(Qt.AlignCenter)
        self.labelUsuario.setStyleSheet("font: 700 14pt \"Segoe UI\";color:#000000;")
        
        self.labelContrasena = QLabel()
        self.labelContrasena.setText("Contraseña")
        self.labelContrasena.setAlignment(Qt.AlignCenter)
        self.labelContrasena.setStyleSheet("font: 700 14pt \"Segoe UI\";color:#000000;")
        
        self.labelError = QLabel()
        self.labelError.setText("Error")
        self.labelError.setAlignment(Qt.AlignCenter)
        self.labelError.setStyleSheet("font: 700 9pt \"Segoe UI\";color:#D60000;")
        
        ##Inputs contraseña y usuario
        self.inputUsuario = QLineEdit()
        self.inputUsuario.setPlaceholderText("Ingrese su usuario.")
        self.inputUsuario.setStyleSheet(LineEditStyleSheet)
        
        self.inputContrasena = QLineEdit()
        self.inputContrasena.setPlaceholderText("Ingrese su contraseña.")
        self.inputContrasena.setEchoMode(QLineEdit.Password)
        self.inputContrasena.setStyleSheet(LineEditStyleSheet)
        
        ## Boton de iniciar Sesion
        self.botonIniciar = QPushButton()
        self.botonIniciar.setText("Iniciar sesión")
        self.botonIniciar.setStyleSheet("background-color:#ADA2FF")
        self.botonIniciar.setStyleSheet(btnStyleSheet)
        self.botonIniciar.clicked.connect(self.accion_inicio_sesion)
        
        # agregar checkbox
        self.checkVerContrasena = QCheckBox("Mostrar contraseña")
        self.checkVerContrasena.setStyleSheet("font: 700 10pt \"Segoe UI\";color:#000000;")
        self.checkVerContrasena.stateChanged.connect(self.accion_checkbox)
        
        self.espaciotop_Log = QSpacerItem(0,20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.espaciobottom_Log = QSpacerItem(0,20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        
        ## ir agregando los espaciadores los labels con sus respectivos inputs,
        ## y el boton iniciar sesion
        self.layoutInputLogin.addItem(self.espaciotop_Log)
        self.layoutInputLogin.addWidget(self.labelUsuario)
        self.layoutInputLogin.addWidget(self.inputUsuario)
        self.layoutInputLogin.addWidget(self.labelContrasena)
        self.layoutInputLogin.addWidget(self.inputContrasena)
        self.layoutInputLogin.addWidget(self.checkVerContrasena)
        self.layoutInputLogin.addWidget(self.labelError)
        self.layoutInputLogin.addWidget(self.botonIniciar)
        self.layoutInputLogin.addItem(self.espaciobottom_Log)
        
        self.frameLogin.setLayout(self.layoutInputLogin)
      
    def accion_checkbox(self):
        if self.checkVerContrasena.isChecked():
            self.inputContrasena.setEchoMode(QLineEdit.Normal)
        else:
            self.inputContrasena.setEchoMode(QLineEdit.Password)
     
    def accion_inicio_sesion(self):
        usuario = self.inputUsuario.text()
        contrasena = self.inputContrasena.text()
        
        if not usuario.strip() and not contrasena.strip():
            advertencia = DialogoEmergente("¡Advertencia!","¡Ingrese su usuario y contraseña!","Question")
            advertencia.exec()
        else:
            usuario = Usuario(usuario,contrasena)
            servicesUser = UsuarioServices()
            result = servicesUser.inicioSesion(usuario) 
            print()
            print(result)
            print()
            if result["success"]:
                if not result["login"]:
                    self.labelError.setText(result["message"])
            else:
                self.labelError.setText("Error de conexion.")
        
        
        
