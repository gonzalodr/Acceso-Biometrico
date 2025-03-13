from PySide6.QtWidgets import *
from PySide6.QtCore import *
from Utils.Utils import *
from services.justificacionService import *

class AdminJustificacion(QWidget):
    cerrar_adminJ = Signal()
    
    paginaActual = 1
    ultimaPagina = 1
    busqueda = None
    Pservices = JustificacionServices()
    
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("admin")
        
        cargar_estilos('claro', 'admin.css', self)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
    
        frame = QFrame()
    
        self.layoutFrame = QVBoxLayout()
        self.layoutFrame.setContentsMargins(0, 0, 0, 0)
        self.layoutFrame.setSpacing(0)
    
        titulo = QLabel(text="Administrar justificaciones")
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
        
        self.inputBuscar = QLineEdit()
        self.inputBuscar.setClearButtonEnabled(True)
        self.inputBuscar.setPlaceholderText("Buscar justificación por motivo o descripción.")
        self.inputBuscar.setFixedSize(QSize(500, 30))
        self.inputBuscar.textChanged.connect(self._cargar_tabla)
        Sombrear(self.inputBuscar, 20, 0, 0)
        
        self.btnBuscar = QPushButton(text="Buscar")
        self.btnBuscar.setCursor(Qt.PointingHandCursor)
        self.btnBuscar.setFixedSize(minimoTamBtn)
        self.btnBuscar.clicked.connect(self._buscarJustificacion)
        Sombrear(self.btnBuscar, 20, 0, 0)
        
        self.btnCrear = QPushButton(text="Crear")
        self.btnCrear.setCursor(Qt.PointingHandCursor)
        self.btnCrear.setFixedSize(minimoTamBtn)
        self.btnCrear.clicked.connect(self._crear_justificacion)
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
        
        # Tabla Justificaciones
        self.tbJustificacion = QTableWidget()
        if (self.tbJustificacion.columnCount() < 3):
            self.tbJustificacion.setColumnCount(3)
        header_labels = ["Motivo", "Descripción", "Acciones"]
        self.tbJustificacion.setHorizontalHeaderLabels(header_labels)
        
        self.tbJustificacion.horizontalHeader().setFixedHeight(40)
        self.tbJustificacion.verticalHeader().setVisible(False)
        self.tbJustificacion.horizontalHeader().setStretchLastSection(True)
        self.tbJustificacion.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        Sombrear(self.tbJustificacion, 30, 0, 0)
        
        # Layout para la tabla
        layoutTb = QHBoxLayout()
        layoutTb.setContentsMargins(70, 40, 70, 40)
        layoutTb.addWidget(self.tbJustificacion)
        self.layoutFrame.addLayout(layoutTb)

        # Layout para los botones de paginación
        layoutButtom = QHBoxLayout()
        layoutButtom.setAlignment(Qt.AlignCenter)
        layoutButtom.setContentsMargins(10, 10, 10, 40)
        layoutButtom.setSpacing(5)
        
        self.btnPrimerPagina = QPushButton(text="Primera Página")
        self.btnPrimerPagina.setFixedSize(minimoTamBtn)
        self.btnPrimerPagina.setEnabled(False)
        self.btnPrimerPagina.clicked.connect(self._irPrimeraPagina)
        Sombrear(self.btnPrimerPagina, 20, 0, 0)
        
        self.btnAnterior = QPushButton(text="Anterior")
        self.btnAnterior.setEnabled(False)
        self.btnAnterior.setFixedSize(minimoTamBtn)
        self.btnAnterior.clicked.connect(self._irAnteriorPagina)
        Sombrear(self.btnAnterior, 20, 0, 0)
        
        self.lblNumPagina = QLabel(text="Página 0 de 0 páginas")
        self.lblNumPagina.setFixedSize(QSize(170, 40))
        self.lblNumPagina.setAlignment(Qt.AlignCenter)
        
        self.btnSiguiente = QPushButton(text="Siguiente")
        self.btnSiguiente.setEnabled(False)
        self.btnSiguiente.setFixedSize(minimoTamBtn)
        self.btnSiguiente.clicked.connect(self._irSiguientePagina)
        Sombrear(self.btnSiguiente, 20, 0, 0)
        
        self.btnUltimaPagina = QPushButton(text="Última Página")
        self.btnUltimaPagina.setEnabled(False)
        self.btnUltimaPagina.setFixedSize(minimoTamBtn)
        self.btnUltimaPagina.clicked.connect(self._irUltimaPagina)
        Sombrear(self.btnUltimaPagina, 20, 0, 0)
        
        layoutButtom.addWidget(self.btnPrimerPagina)
        layoutButtom.addSpacing(10)
        layoutButtom.addWidget(self.btnAnterior)
        layoutButtom.addSpacing(10)
        layoutButtom.addWidget(self.lblNumPagina)
        layoutButtom.addSpacing(10)
        layoutButtom.addWidget(self.btnSiguiente)
        layoutButtom.addSpacing(10)
        layoutButtom.addWidget(self.btnUltimaPagina)

        self.layoutFrame.addLayout(layoutButtom)
        frame.setLayout(self.layoutFrame)
        layout.addWidget(frame)
        self.setLayout(layout)
        Sombrear(self, 30, 0, 0)
        self._cargar_tabla()
        
    def _cerrar(self):
        self.cerrar_adminJ.emit()
             
    def _mostrar_mensaje_sin_datos(self):
        self.tbJustificacion.setRowCount(0)
        if self.tbJustificacion.rowCount() == 0:
            self.tbJustificacion.setRowCount(1)
            item = QTableWidgetItem("Sin datos")
            item.setTextAlignment(Qt.AlignCenter)
            self.tbJustificacion.setItem(0, 0, item)
            for col in range(1, self.tbJustificacion.columnCount()):
                self.tbJustificacion.setItem(0, col, QTableWidgetItem(""))
            self.tbJustificacion.setSpan(0, 0, 1, self.tbJustificacion.columnCount())
                
    def _cargar_tabla(self):
        result = self.Pservices.obtenerListaJustificacion(pagina=self.paginaActual, tam_pagina=10, tipo_orden="DESC", busqueda=self.busqueda)
        if result["success"]:
            listaJustificaciones = result["data"]["listaJustificaciones"]
            if len(listaJustificaciones) > 0:
                paginaActual = result["data"]["pagina_actual"]
                tamPagina = result["data"]["tam_pagina"]
                totalPaginas = result["data"]["total_paginas"]
                totalRegistros = result["data"]["total_registros"]
                self._actualizar_lblPagina(paginaActual, totalPaginas)
                self._actualizarValoresPaginado(paginaActual, totalPaginas)
                
                self.tbJustificacion.setRowCount(0)
                for index, justificacion in enumerate(listaJustificaciones):
                    self.tbJustificacion.insertRow(index)
                    self.tbJustificacion.setRowHeight(index, 45)
                    
                    self.addItem_a_tabla(index, 0, justificacion.motivo)
                    self.addItem_a_tabla(index, 1, justificacion.descripcion)

                    btnEliminar = QPushButton("Eliminar")
                    btnEliminar.clicked.connect(lambda checked, idx=justificacion.id_justificacion: self._eliminarRegistro(idx))
                    btnEliminar.setMinimumSize(QSize(80, 35))
                    btnEliminar.setStyleSheet("""   QPushButton{background-color:#ff5151;color:white;}
                                                    QPushButton::hover{background-color:#ff0000;color:white;}
                                              """)
                    
                    btnEditar = QPushButton("Editar")
                    btnEditar.clicked.connect(lambda checked, idx=justificacion.id_justificacion: self._editar_Justificacion(idx))
                    btnEditar.setMinimumSize(QSize(80, 35))
                    btnEditar.setStyleSheet(""" QPushButton{background-color:#00b800;color:white;}
                                                QPushButton::hover{background-color:#00a800;color:white;}
                                            """)

                    button_widget = QWidget()
                    button_widget.setStyleSheet(u"background-color:transparent;")
                    layout = QHBoxLayout()
                    layout.addWidget(btnEditar)
                    layout.addSpacing(15)
                    layout.addWidget(btnEliminar)
                    button_widget.setLayout(layout)
                    layout.setContentsMargins(10, 0, 10, 0)

                    self.tbJustificacion.setCellWidget(index, 2, button_widget)
            else:
                self._mostrar_mensaje_sin_datos()
        else:
            self._mostrar_mensaje_sin_datos()

    def addItem_a_tabla(self, row, colum, dato):
        dato_item = QTableWidgetItem(dato)
        dato_item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.tbJustificacion.setItem(row, colum, dato_item)

    