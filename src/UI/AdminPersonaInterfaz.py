from PySide6.QtWidgets import *
from PySide6.QtCore import *
from stilosInterfaz import *
from DialogoEmergente import *
import sys

class AdminPersona(QWidget):
    senal_cambio_ventana = Signal(int)
    blur_efecto = False
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
        self.frameEncabezado.setStyleSheet("background-color:#BCB9FF;")

        ##Cuerpo de la pagina
        self.framCuerpo = QFrame()
        self.framCuerpo.setStyleSheet("background-color:#FFFFFF;border-radius:20px")

        ## Pie de la pagina
        self.framePiePagina = QFrame()
        self.framePiePagina.setStyleSheet("background-color:#BCB9FF")

        ##Agregar encabezado, cuerpo y pie de pagina
        self.root_layout.addWidget(self.frameEncabezado,15)
        self.root_layout.addWidget(self.framCuerpo, 80)
        self.root_layout.addWidget(self.framePiePagina,5)
        self.setLayout(self.root_layout)

        self.configurar_encabezado()
        self.configurar_cuerpo()
        self.configurar_sombras()

    def configurar_encabezado(self):
        self.gridEncabezado = QGridLayout() ## Crea un grid (Matriz) donde se acomodaran los widgets
        self.gridEncabezado.setSpacing(0)   ## Espacio entre widgets es 0
        self.gridEncabezado.setContentsMargins(0,0,0,0) ## El margen osea borders seran 0

        ## Nombre del encabezado(Titulo de la pagina)
        self.nombreEncabezado = QLabel()
        self.nombreEncabezado.setStyleSheet("font: 700 24pt \"Segoe UI\";color:#000000;")
        self.nombreEncabezado.setText("ACCESO BIOMETRICO")
        self.nombreEncabezado.setAlignment(Qt.AlignCenter) ##alineacion del texto en el centro del label

        ## Nombre de la vista en la que se ubica(ejemplo: Administracion de empleados)
        self.nombreVista = QLabel()
        self.nombreVista.setText("Admin Persona")
        self.nombreVista.setStyleSheet("font: 700 16pt \"Segoe UI\";color:#000000;")
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
        self.layoutCuerpo = QGridLayout()
        self.layoutCuerpo.setSpacing(0)
        self.layoutCuerpo.setContentsMargins(5,5,5,5)
        ##layout de los botones de busqueda, creacion
        self.layoutBtnTop = QHBoxLayout()
        self.layoutBtnTop.setSpacing(2)
        self.layoutBtnTop.setContentsMargins(0,0,0,5)
        ##layout para los botones de abajo paginacion
        self.layoutBtnButtom = QHBoxLayout()
        self.layoutBtnButtom.setSpacing(2)
        self.layoutBtnButtom.setContentsMargins(2,3,2,3)
        #crea el input de busqueda los botones de crear y buscar
        self.configurar_widgets()
        #acomodando los botones de arriba
        self.layoutBtnTop.addStretch(1)
        self.layoutBtnTop.addWidget(self.InputBusqueda,5)
        self.layoutBtnTop.addStretch(1)
        self.layoutBtnTop.addWidget(self.btnBuscar,2)
        self.layoutBtnTop.addStretch(2)
        self.layoutBtnTop.addWidget(self.btnCrear,2)
        
        #acomodando los botones de abajo
        self.layoutBtnButtom.addStretch(1)
        self.layoutBtnButtom.addWidget(self.btnPrimeraPagina,2)
        self.layoutBtnButtom.addStretch(1)
        self.layoutBtnButtom.addWidget(self.btnAnterior,2)
        self.layoutBtnButtom.addStretch(1)
        self.layoutBtnButtom.addWidget(self.lblPagina,1)
        self.layoutBtnButtom.addStretch(1)
        self.layoutBtnButtom.addWidget(self.btnSiguiente,2)
        self.layoutBtnButtom.addStretch(1)
        self.layoutBtnButtom.addWidget(self.btnUltimaPagina,2)
        self.layoutBtnButtom.addStretch(1)


        #tabla
        self.tbPersona = QTableWidget()
        if (self.tbPersona.columnCount() < 9):
            self.tbPersona.setColumnCount(9)
        header_labels = ["Nombre", "1° Apellido", "2° Apellido", "Cedula", "Correo", "Nacimiento", "Estado civil", "Dirección","Acciones"]
        self.tbPersona.setHorizontalHeaderLabels(header_labels)
        self.tbPersona.verticalHeader().setVisible(False)
        self.tbPersona.horizontalHeader().setStretchLastSection(True)
        self.tbPersona.setStyleSheet(tableStyleSheet)
        self.tbPersona.setMaximumSize(QSize(1100,350))
        self.tbPersona.setMinimumSize(QSize(500,350))
        self.tbPersona.setSizePolicy(QSizePolicy.Preferred,QSizePolicy.Preferred)

        #Spaciador isquierda y derecha (Expanding: el espacio se expande de acuerdo a la ventana)
        self.espaciolefth_Cuer = QSpacerItem(250,0, QSizePolicy.Maximum, QSizePolicy.Expanding)
        self.espacioright_Cuer = QSpacerItem(250,0, QSizePolicy.Maximum, QSizePolicy.Expanding)

        ##Spaciador arriba y abajo QSpacerItem(tamañoX, tamañoY,QSizeExpanding, QSizeExpanding)
        self.espaciotop_Cuer = QSpacerItem(0,50, QSizePolicy.Expanding, QSizePolicy.Maximum)
        self.espaciobottom_Cuer = QSpacerItem(0,100, QSizePolicy.Expanding, QSizePolicy.Maximum)

        self.layoutCuerpo.addLayout(self.layoutBtnTop,1,1)
        self.layoutCuerpo.addWidget(self.tbPersona,2,1)
        self.layoutCuerpo.addLayout(self.layoutBtnButtom,3,1)
        
        self.layoutCuerpo.addItem(self.espaciotop_Cuer,0,1)
        self.layoutCuerpo.addItem(self.espaciobottom_Cuer,3,1)
        
        self.layoutCuerpo.addItem(self.espaciolefth_Cuer,2,0)
        self.layoutCuerpo.addItem(self.espacioright_Cuer,2,2)
        
        self.framCuerpo.setLayout(self.layoutCuerpo)

    def configurar_sombras(self):
        self.btnPrimeraPagina.setGraphicsEffect(self._sombras_sombras(self.btnPrimeraPagina,30))
        self.btnAnterior.setGraphicsEffect(self._sombras_sombras(self.btnAnterior,30))
        self.btnSiguiente.setGraphicsEffect(self._sombras_sombras(self.btnSiguiente,30))
        self.btnUltimaPagina.setGraphicsEffect(self._sombras_sombras(self.btnUltimaPagina,30))
    
        self.InputBusqueda.setGraphicsEffect(self._sombras_sombras( self.InputBusqueda,30))
        self.btnBuscar.setGraphicsEffect(self._sombras_sombras(self.btnBuscar,30))
        self.btnCrear.setGraphicsEffect(self._sombras_sombras(self.btnCrear,30))
        self.tbPersona.setGraphicsEffect(self._sombras_sombras(self.tbPersona,70))  
        
    def _sombras_sombras(self,objeto,blurRadius=10):
        sombras = QGraphicsDropShadowEffect(objeto)
        sombras.setBlurRadius(blurRadius)
        sombras.setXOffset(0)
        sombras.setYOffset(0)
        return sombras
    
    def configurar_widgets(self):
        #linea de busquda
        self.InputBusqueda = QLineEdit()
        self.InputBusqueda.setStyleSheet(LineEditStyleSheet)
        self.InputBusqueda.setClearButtonEnabled(True)
        #boton buscar
        self.btnBuscar =QPushButton(text="Buscar")
        self.btnBuscar.setStyleSheet(btnStyleSheet)
        self.btnBuscar.clicked.connect(self.abrir_dialogo)
        #boton crear
        self.btnCrear = QPushButton(text="Crear")
        self.btnCrear.setStyleSheet(btnStyleSheet)
        #paginacion
        self.btnAnterior = QPushButton(text="Anterior")
        self.btnAnterior.setStyleSheet(btnStyleSheet)
        self.btnSiguiente = QPushButton(text="Siguiente")
        self.btnSiguiente.setStyleSheet(btnStyleSheet)
        # self.btnSiguiente.setMaximumSize(150,40)
        self.btnPrimeraPagina = QPushButton(text="Primera")
        self.btnPrimeraPagina.setStyleSheet(btnStyleSheet)
        # self.btnPrimeraPagina.setMaximumSize(150,40)
        self.btnUltimaPagina = QPushButton(text="Ultima pagina")
        self.btnUltimaPagina.setStyleSheet(btnStyleSheet)

        self.lblPagina = QLabel(text="Pagina 0 de 0")
        self.lblPagina.setStyleSheet("background-color:transparent;")
        self.lblPagina.setAlignment( Qt.AlignCenter)
        
    def abrir_dialogo(self):
        pass
              
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = AdminPersona()
    ventana.setWindowTitle("Administración de Personas")
    ventana.resize(800, 600)  # Ajusta el tamaño de la ventana según tus necesidades
    ventana.show()
    sys.exit(app.exec())
