from PySide6.QtWidgets import *
from PySide6.QtCore import *
from Utils.Utils import *
from services.usuarioService import *

class AdminUsuario(QWidget):
    cerrar_adminU = Signal()
    paginaActual = 1
    ultimaPagina = 1
    busqueda = None
    Uservices = UsuarioServices()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("admin")
        cargar_estilos('claro','admin.css',self)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)

        frame = QFrame()

        self.layoutFrame = QVBoxLayout()
        self.layoutFrame.setContentsMargins(0, 0, 0, 0)
        self.layoutFrame.setSpacing(0)

        titulo = QLabel(text="Administrar Usuarios")
        titulo.setObjectName("titulo")
        titulo.setMinimumHeight(50)
        titulo.setAlignment(Qt.AlignCenter)
        self.layoutFrame.addWidget(titulo)

        layoutTop = QHBoxLayout()
        layoutTop.setContentsMargins(30, 30, 30, 30)
        layoutTop.setSpacing(5)
        layoutTop.setAlignment(Qt.AlignCenter)
        minimoTamBtn = QSize(120, 40)

        self.btnCerrar = QPushButton(text="Cerrar")
        self.btnCerrar.setFixedSize(minimoTamBtn)
        self.btnCerrar.setCursor(Qt.PointingHandCursor)
        self.btnCerrar.clicked.connect(self._cerrar)
        Sombrear(self.btnCerrar, 20, 0, 0)

        # Campo de entrada para buscar Usuarios
        self.inputBuscar = QLineEdit()
        self.inputBuscar.setClearButtonEnabled(True)
        self.inputBuscar.setPlaceholderText("Buscar usuario")
        self.inputBuscar.setFixedSize(QSize(500, 30))
        self.inputBuscar.textChanged.connect(self._cargar_tabla)
        Sombrear(self.inputBuscar, 20, 0, 0)

        self.btnBuscar = QPushButton(text="Buscar")
        self.btnBuscar.setCursor(Qt.PointingHandCursor)
        self.btnBuscar.setFixedSize(minimoTamBtn)
        self.btnBuscar.clicked.connect(self._buscarUsuario)
        Sombrear(self.btnBuscar, 20, 0, 0)

        self.btnCrear = QPushButton(text="Crear")
        self.btnCrear.setCursor(Qt.PointingHandCursor)
        self.btnCrear.setFixedSize(minimoTamBtn)
        self.btnCrear.setObjectName("crear")
        self.btnCrear.clicked.connect(self._crear_Usuario)
        Sombrear(self.btnCrear, 20, 0, 0)

        layoutTop.addSpacing(25)
        layoutTop.addWidget(self.btnCerrar, 1)
        layoutTop.addStretch(1)
        layoutTop.addWidget(self.inputBuscar, 2)
        layoutTop.addSpacing(10)
        layoutTop.addWidget(self.btnBuscar, 2)
        layoutTop.addStretch(1)
        layoutTop.addWidget(self.btnCrear, 2)
        layoutTop.addStretch(5)
        self.layoutFrame.addLayout(layoutTop)

        # Tabla Usuario
        self.tbUsuario = QTableWidget()
        if self.tbUsuario.columnCount() < 3:
            self.tbUsuario.setColumnCount(3)
        header_labels = ["Nombre", "Usuario", "Acciones"]
        self.tbUsuario.setHorizontalHeaderLabels(header_labels)

        self.tbUsuario.horizontalHeader().setFixedHeight(40)
        self.tbUsuario.verticalHeader().setVisible(False)
        self.tbUsuario.horizontalHeader().setStretchLastSection(True)
        self.tbUsuario.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        Sombrear(self.tbUsuario, 30, 0, 0)

        # Layout para la tabla
        layoutTb = QHBoxLayout()
        layoutTb.setContentsMargins(70, 40, 70, 40)
        layoutTb.addWidget(self.tbUsuario)
        self.layoutFrame.addLayout(layoutTb)

        # Layout para los botones de paginación
        layoutButtom = QHBoxLayout()
        layoutButtom.setAlignment(Qt.AlignCenter)
        layoutButtom.setContentsMargins(10, 10, 10, 40)
        layoutButtom.setSpacing(5)
