from PySide6.QtWidgets import *
from PySide6.QtCore import *
from Utils.Utils import *
from UI.AdministrarPerfil.formPerfil import *
from services.perfilService import *

class AdminPerfil(QWidget):
    cerrar_adminP = Signal()
    paginaActual = 1
    ultimaPagina = 1
    busqueda = None
    Pservices = PerfilServices()
    
    def __init__(self, parent = None):
        super().__init__(parent)
        self.setObjectName("admin")
        cargar_estilos('claro', 'admin.css', self)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        
        frame = QFrame()
        
        self.layoutFrame = QVBoxLayout()
        self.layoutFrame.setContentsMargins(0, 0, 0, 0)
        self.layoutFrame.setSpacing(0)
        
        titulo = QLabel(text="Administrar Perfiles")
        titulo.setObjectName("titulo")  
        titulo.setMinimumHeight(50)
        titulo.setAlignment(Qt.AlignCenter)
        self.layoutFrame.addWidget(titulo)
        
        layoutTop = QHBoxLayout()
        layoutTop.setContentsMargins (30, 30, 30, 30)
        layoutTop.setSpacing(5)
        layoutTop.setAlignment(Qt.AlignCenter)
        minimoTamBtn = QSize(120, 40)
        
        self.btnCerrar = QPushButton(text="Cerrar")
        self.btnCerrar.setFixedSize(minimoTamBtn)
        self.btnCerrar.setCursor(Qt.PointingHandCursor)
        self.btnCerrar.clicked.connect(self._cerrar)
        Sombrear(self.btnCerrar, 20, 0, 0)
        
        
        # Campo de entrada para buscar Perfil
        self.inputBuscar = QLineEdit()
        self.inputBuscar.setClearButtonEnabled(True)
        self.inputBuscar.setPlaceholderText("Buscar perfil por nombre o descripción.")
        self.inputBuscar.setFixedSize(QSize(500, 30))
        self.inputBuscar.textChanged.connect(self._cargar_tabla)
        Sombrear(self.inputBuscar, 20, 0, 0)

        self.btnBuscar = QPushButton(text="Buscar")
        self.btnBuscar.setCursor(Qt.PointingHandCursor)
        self.btnBuscar.setFixedSize(minimoTamBtn)
        self.btnBuscar.clicked.connect(self._buscarPerfil)
        Sombrear(self.btnBuscar, 20, 0, 0)

        self.btnCrear = QPushButton(text="Crear")
        self.btnCrear.setCursor(Qt.PointingHandCursor)
        self.btnCrear.setFixedSize(minimoTamBtn)
        self.btnCrear.setObjectName("crear")
        self.btnCrear.clicked.connect(self._crear_perfil)
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
        
         # Tabla Rol
        self.tbPerfil = QTableWidget()
        if self.tbPerfil.columnCount() < 3:
            self.tbPerfil.setColumnCount(3)
        header_labels = ["Nombre", "Descripción", "Acciones"]
        self.tbPerfil.setHorizontalHeaderLabels(header_labels)

        self.tbPerfil.horizontalHeader().setFixedHeight(40)
        self.tbPerfil.verticalHeader().setVisible(False)
        self.tbPerfil.horizontalHeader().setStretchLastSection(True)
        self.tbPerfil.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        Sombrear(self.tbPerfil, 30, 0, 0)

        # Layout para la tabla
        layoutTb = QHBoxLayout()
        layoutTb.setContentsMargins(70, 40, 70, 40)
        layoutTb.addWidget(self.tbPerfil)
        self.layoutFrame.addLayout(layoutTb)

        # Layout para los botones de paginación
        layoutButtom = QHBoxLayout()
        layoutButtom.setAlignment(Qt.AlignCenter)
        layoutButtom.setContentsMargins(10, 10, 10, 40)
        layoutButtom.setSpacing(5)

        # Botón para ir a la primera página
        self.btnPrimerPagina = QPushButton(text="Primera Página.")
        self.btnPrimerPagina.setFixedSize(minimoTamBtn)
        self.btnPrimerPagina.setCursor(Qt.PointingHandCursor)
        self.btnPrimerPagina.setEnabled(False)
        self.btnPrimerPagina.clicked.connect(self._irPrimeraPagina)
        Sombrear(self.btnPrimerPagina, 20, 0, 0)

        # Botón para ir a la página anterior
        self.btnAnterior = QPushButton(text="Anterior")
        self.btnAnterior.setEnabled(False)
        self.btnAnterior.setCursor(Qt.PointingHandCursor)
        self.btnAnterior.setFixedSize(minimoTamBtn)
        self.btnAnterior.clicked.connect(self._irAnteriorPagina)
        Sombrear(self.btnAnterior, 20, 0, 0)

        # Etiqueta para mostrar el número de la página actual
        self.lblNumPagina = QLabel(text="Página 0 de 0 páginas")
        self.lblNumPagina.setFixedSize(QSize(170, 40))
        self.lblNumPagina.setAlignment(Qt.AlignCenter)

        # Botón para ir a la página siguiente
        self.btnSiguiente = QPushButton(text="Siguiente")
        self.btnSiguiente.setCursor(Qt.PointingHandCursor)
        self.btnSiguiente.setEnabled(False)
        self.btnSiguiente.setFixedSize(minimoTamBtn)
        self.btnSiguiente.clicked.connect(self._irSiguientePagina)
        Sombrear(self.btnSiguiente, 20, 0, 0)
        
         # Botón para ir a la última página
        self.btnUltimaPagina = QPushButton(text="Última Página.")
        self.btnUltimaPagina.setCursor(Qt.PointingHandCursor)
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
        self.cerrar_adminP.emit()
        
    def _mostrar_mensaje_sin_datos(self):
        # Si la tabla está vacía, agregar una fila con el mensaje "Sin datos"
        self.tbPerfil.setRowCount(0)
        if self.tbPerfil.rowCount() == 0:
            self.tbPerfil.setRowCount(1)
            item = QTableWidgetItem("Sin datos")
            item.setTextAlignment(Qt.AlignCenter)
            self.tbPerfil.setItem(0, 0, item)
            for col in range(1, self.tbPerfil.columnCount()):
                self.tbPerfil.setItem(0, col, QTableWidgetItem(""))  # Celdas vacías
            self.tbPerfil.setSpan(0, 0, 1, self.tbPerfil.columnCount())
            
    def _cargar_tabla(self):
        result = self.Pservices.obtenerListaPerfil(pagina=self.paginaActual, tam_pagina=10, tipo_orden="DESC", busqueda=self.busqueda)
        if result["success"]:
            listaPerfil = result["data"]["listaPerfiles"]
            if len(listaPerfil) > 0:
                paginaActual = result["data"]["pagina_actual"]
                tamPagina = result["data"]["tam_pagina"]
                totalPaginas = result["data"]["total_paginas"]
                totalRegistros = result["data"]["total_registros"]
                
                self._actualizar_lblPagina(paginaActual, totalPaginas)
                self._actualizarValoresPaginado(paginaActual, totalPaginas)
                
                self.tbPerfil.setRowCount(0)
                for index, perfil in enumerate(listaPerfil):
                    self.tbPerfil.insertRow(index)
                    self.tbPerfil.setRowHeight(index, 45)

                    self.addItem_a_tabla(index, 0, perfil.nombre)
                    self.addItem_a_tabla(index, 1, perfil.descripcion)

                    # Botones para editar y eliminar
                    btnEliminar = QPushButton("Eliminar")
                    btnEliminar.clicked.connect(lambda checked, idx=perfil.id: self._eliminarRegistro(idx))
                    btnEliminar.setMinimumSize(QSize(80, 35))
                    btnEliminar.setStyleSheet("""   QPushButton{background-color:#ff5151;color:white;}
                                                    QPushButton::hover{background-color:#ff0000;color:white;}
                                              """)

                    btnEditar = QPushButton("Editar")
                    btnEditar.clicked.connect(lambda checked, idx=perfil.id: self._editar_Perfil(idx))
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
                    layout.setContentsMargins(10, 0, 10,0)

                    self.tbPerfil.setCellWidget(index, 2, button_widget)
            else:
                self._mostrar_mensaje_sin_datos()
        else:
            self._mostrar_mensaje_sin_datos()
            
    def addItem_a_tabla(self,row, colum,dato):
        dato_item = QTableWidgetItem(dato)
        dato_item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)  # No editable
        self.tbPerfil.setItem(row, colum, dato_item)

    def _actualizar_lblPagina(self, paginaActual, totalPaginas):
        self.lblNumPagina.setText(f"Página {paginaActual} de {totalPaginas} páginas.")

    def _actualizarValoresPaginado(self, paginaActual, totalPaginas):
        self.paginaActual = paginaActual
        self.ultimaPagina = totalPaginas
        self.btnSiguiente.setEnabled(paginaActual < totalPaginas)
        self.btnUltimaPagina.setEnabled(paginaActual < totalPaginas)
        self.btnPrimerPagina.setEnabled(paginaActual > 1)
        self.btnAnterior.setEnabled(paginaActual > 1)

    def _buscarPerfil(self):
        self.busqueda = self.inputBuscar.text()
        self.paginaActual = 1
        self._cargar_tabla()
        
    def _crear_perfil(self):
        blur_effect = QGraphicsBlurEffect(self)
        blur_effect.setBlurRadius(10)
        self.setGraphicsEffect(blur_effect)
        perfil_form = formPerfil()
        perfil_form.exec()
        self._cargar_tabla()
        self.setGraphicsEffect(None)

    def _eliminarRegistro(self, id_perfil):
        dial = DialogoEmergente("¿?","¿Seguro que quieres eliminar este registro?","Question",True,True)
        if dial.exec() == QDialog.Accepted:
                result = self.Pservices.eliminarPerfil(id_perfil)
                if result["success"]:
                    dial = DialogoEmergente("","Se elimino el registro correctamente.","Check")
                    dial.exec()
                    self._cargar_tabla()
                else:
                    dial = DialogoEmergente("","Hubo un error al eliminar este registro.","Error")
                    dial.exec()
                    
                    
    def _editar_Perfil(self, id_perfil):
        blur_effect = QGraphicsBlurEffect(self)
        blur_effect.setBlurRadius(10)
        self.setGraphicsEffect(blur_effect)
        perfil_form = formPerfil(id=id_perfil)
        perfil_form.exec()
        self._cargar_tabla()
        self._cargar_tabla()
        self.setGraphicsEffect(None)

    def _irPrimeraPagina(self):
        self.paginaActual = 1
        self._cargar_tabla()

    def _irAnteriorPagina(self):
        if self.paginaActual > 1:
            self.paginaActual -= 1
            self._cargar_tabla()

    def _irSiguientePagina(self):
        if self.paginaActual < self.ultimaPagina:
            self.paginaActual += 1
            self._cargar_tabla()

    def _irUltimaPagina(self):
        self.paginaActual = self.ultimaPagina
        self._cargar_tabla()
