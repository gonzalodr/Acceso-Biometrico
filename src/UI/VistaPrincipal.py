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
        self.nombreVista.setText("Menu principal")
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

    def configurar_cuerpo(self):
        pass