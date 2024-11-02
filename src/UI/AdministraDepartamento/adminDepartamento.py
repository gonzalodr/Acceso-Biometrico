from PySide6.QtWidgets import *
from PySide6.QtCore import *
from Utils.Utils import *
from UI.AdministraDepartamento.formDepartamento import *
from services.departamentoService import *

class AdminDepartament(QWidget):
    cerrar_adminD = Signal()
    
    paginaActual = 1
    ultimaPagina = 1
    busqueda = None
    Pservices = DepartamentoServices()
    
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("admin")
    
        add_Style(carpeta="css", archivoQSS="adminDepartamento.css", QObjeto=self)
    
        layout = QVBoxLayout();
        layout.setContentsMargins(10, 10, 10, 10)
    
        frame = QFrame()
    
        self.layoutFrame = QVBoxLayout()
        self.layoutFrame.setContentsMargins(0, 0, 0, 0)
        self.layoutFrame.setSpacing(0)
    
        titulo = QLabel(text="Administrar departamentos")
        titulo.setObjectName("titulo")
        titulo.setMinimumHeight(50)
        titulo.setAlignment(Qt.AlignCenter)
        self.layoutFrame.addWidget(titulo)
        
        layoutTop = QHBoxLayout()
        layoutTop.setContentsMargins(30, 30, 30, 30)  # Establecemos márgenes
        layoutTop.setSpacing(5)  # Establecemos espaciado entre widgets
        layoutTop.setAlignment(Qt.AlignCenter)  # Centramos los elementos
        minimoTamBtn = QSize(120, 40)
        
        self.btnCerrar = QPushButton(text="Cerrar")
        self.btnCerrar.setFixedSize(minimoTamBtn)  # Establecemos tamaño fijo
        self.btnCerrar.setCursor(Qt.PointingHandCursor)  # Cambiamos el cursor al pasar por encima
        self.btnCerrar.clicked.connect(self._cerrar)  # Conectamos la señal de clic al método _cerrar
        Sombrear(self.btnCerrar, 20, 0, 0)  # Aplicamos efecto de sombreado
        
        # Campo de entrada para buscar Departamento
        self.inputBuscar = QLineEdit()
        self.inputBuscar.setClearButtonEnabled(True)  # Activamos el botón de limpiar
        self.inputBuscar.setPlaceholderText("Buscar departamento por nombre o descripción.")  # Texto de marcador
        self.inputBuscar.setFixedSize(QSize(500, 30))  # Establecemos tamaño fijo
        self.inputBuscar.textChanged.connect(self._cargar_tabla)
        Sombrear(self.inputBuscar, 20, 0, 0)  # Aplicamos efecto de sombreado
        
        
        self.btnBuscar = QPushButton(text="Buscar")  # Botón para buscar
        self.btnBuscar.setCursor(Qt.PointingHandCursor)  # Cambiamos el cursor al pasar por encima
        self.btnBuscar.setFixedSize(minimoTamBtn)  # Establecemos tamaño fijo
        self.btnBuscar.clicked.connect(self._buscarDepartamento)  # Conectamos la señal de clic al método _buscarDepartamento
        Sombrear(self.btnBuscar, 20, 0, 0)  # Aplicamos efecto de sombreado
        
        self.btnCrear = QPushButton(text="Crear")
        self.btnCrear.setCursor(Qt.PointingHandCursor)
        self.btnCrear.setFixedSize(minimoTamBtn)
        self.btnCrear.setObjectName("crear")
        self.btnCrear.clicked.connect(self._crear_departamento)
        Sombrear(self.btnCrear, 20, 0, 0)
        
         ## Agregamos los botones al layout de la parte superior
        layoutTop.addSpacing(25)  # Espaciado inicial
        layoutTop.addWidget(self.btnCerrar, 1)  # Agregamos el botón de cerrar
        layoutTop.addStretch(1)  # Espacio flexible
        layoutTop.addWidget(self.inputBuscar, 2)  # Agregamos el campo de búsqueda
        layoutTop.addSpacing(10)  # Espaciado entre el campo y el botón de búsqueda
        layoutTop.addWidget(self.btnBuscar, 2)  # Agregamos el botón de búsqueda
        layoutTop.addStretch(1)  # Espacio flexible
        layoutTop.addWidget(self.btnCrear, 2)  # Agregamos el botón de crear
        layoutTop.addStretch(5)  # Espacio flexible
        self.layoutFrame.addLayout(layoutTop)  # Agregamos el layout de botones al layout principal
        
        #Tabla Departamento
        self.tbDepartamento = QTableWidget()
        if (self.tbDepartamento.columnCount() < 3):
            self.tbDepartamento.setColumnCount(3)
        header_labels = ["Nombre", "Descripcion", "Accciones"]
        self.tbDepartamento.setHorizontalHeaderLabels(header_labels)
        
        self.tbDepartamento.horizontalHeader().setFixedHeight(40)
        self.tbDepartamento.verticalHeader().setVisible(False)
        self.tbDepartamento.horizontalHeader().setStretchLastSection(True)
        self.tbDepartamento.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        Sombrear(self.tbDepartamento, 30, 0, 0)
        
        # Layout para la tabla
        layoutTb = QHBoxLayout()
        layoutTb.setContentsMargins(70, 40, 70, 40)  # Establecemos márgenes del layout
        layoutTb.addWidget(self.tbDepartamento)  # Agregamos la tabla al layout
        self.layoutFrame.addLayout(layoutTb)  # Agregamos el layout de la tabla al layout principal

        # Layout para los botones de paginación
        layoutButtom = QHBoxLayout()
        layoutButtom.setAlignment(Qt.AlignCenter)  # Centramos los botones
        layoutButtom.setContentsMargins(10, 10, 10, 40)  # Establecemos márgenes
        layoutButtom.setSpacing(5)  # Establecemos espaciado entre botones
        
         # Botón para ir a la primera página
        self.btnPrimerPagina = QPushButton(text="Primera Pagina.")
        self.btnPrimerPagina.setFixedSize(minimoTamBtn)  # Establecemos tamaño fijo
        self.btnPrimerPagina.setCursor(Qt.PointingHandCursor)  # Cambiamos el cursor al pasar por encima
        self.btnPrimerPagina.setEnabled(False)  # Deshabilitamos el botón inicialmente
        self.btnPrimerPagina.clicked.connect(self._irPrimeraPagina)  # Conectamos la señal de clic al método _irPrimeraPagina
        Sombrear(self.btnPrimerPagina, 20, 0, 0)  # Aplicamos efecto de sombreado
        
         # Botón para ir a la página anterior
        self.btnAnterior = QPushButton(text="Anterior")
        self.btnAnterior.setEnabled(False)  # Deshabilitamos el botón inicialmente
        self.btnAnterior.setCursor(Qt.PointingHandCursor)  # Cambiamos el cursor al pasar por encima
        self.btnAnterior.setFixedSize(minimoTamBtn)  # Establecemos tamaño fijo
        self.btnAnterior.clicked.connect(self._irAnteriorPagina)  # Conectamos la señal de clic al método _irAnteriorPagina
        Sombrear(self.btnAnterior, 20, 0, 0)  # Aplicamos efecto de sombreado
        
         # Etiqueta para mostrar el número de la página actual
        self.lblNumPagina = QLabel(text="Pagina 0 de 0 paginas")
        self.lblNumPagina.setFixedSize(QSize(170, 40))  # Establecemos tamaño fijo
        self.lblNumPagina.setAlignment(Qt.AlignCenter)  # Centramos el texto

             # Botón para ir a la página siguiente
        self.btnSiguiente = QPushButton(text="Siguiente")
        self.btnSiguiente.setCursor(Qt.PointingHandCursor)  # Cambiamos el cursor al pasar por encima
        self.btnSiguiente.setEnabled(False)  # Deshabilitamos el botón inicialmente
        self.btnSiguiente.setFixedSize(minimoTamBtn)  # Establecemos tamaño fijo
        self.btnSiguiente.clicked.connect(self._irSiguientePagina)  # Conectamos la señal de clic al método _irSiguientePagina
        Sombrear(self.btnSiguiente, 20, 0, 0)  # Aplicamos efecto de sombreado
        
        # Botón para ir a la última página
        self.btnUltimaPagina = QPushButton(text="Última Pagina.")
        self.btnUltimaPagina.setCursor(Qt.PointingHandCursor)  # Cambiamos el cursor al pasar por encima
        self.btnUltimaPagina.setEnabled(False)  # Deshabilitamos el botón inicialmente
        self.btnUltimaPagina.setFixedSize(minimoTamBtn)  # Establecemos tamaño fijo
        self.btnUltimaPagina.clicked.connect(self._irUltimaPagina)  # Conectamos la señal de clic al método _irUltimaPagina
        Sombrear(self.btnUltimaPagina, 20, 0, 0)  # Aplicamos efecto de sombreado
        
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
        Sombrear(self,30,0,0)
        self._cargar_tabla()
        
    def _cerrar(self):
             self.cerrar_adminD.emit()
             
    def _mostrar_mensaje_sin_datos(self):
        # Si la tabla está vacía, agregar una fila con el mensaje "Sin datos"
        #Limpiamos las filas 
            self.tbDepartamento.setRowCount(0)
            if self.tbDepartamento.rowCount() == 0:
                self.tbDepartamento.setRowCount(1)
                item = QTableWidgetItem("Sin datos")
                item.setTextAlignment(Qt.AlignCenter)
                self.tbDepartamento.setItem(0, 0, item)
                # Deshabilitar la edición de la celda y ocultar las celdas adicionales
                for col in range(1, self.tbDepartamento.columnCount()):
                    self.tbDepartamento.setItem(0, col, QTableWidgetItem(""))  # Celdas vacías
                self.tbDepartamento.setSpan(0,0,1,self.tbDepartamento.columnCount())
                
    def _cargar_tabla(self):
        result = self.Pservices.obtenerListaDepartamento(pagina=self.paginaActual, tam_pagina=10, tipo_orden="DESC", busqueda=self.busqueda)
        if result["success"]:
            listaDepartamento = result["data"]["listaDepartamentos"]
            if len(listaDepartamento) > 0:
                paginaActual = result["data"]["pagina_actual"]
                tamPagina = result["data"]["tam_pagina"]
                totalPaginas = result["data"]["total_paginas"]
                totalRegistros = result["data"]["total_registros"]
                 #carga los valores de la pagina en teoria quedan igual
                self._actualizar_lblPagina(paginaActual,totalPaginas)
                self._actualizarValoresPaginado(paginaActual,totalPaginas)
                
                # Limpia la tabla antes de cargar los nuevos datos
                self.tbDepartamento.setRowCount(0)
                # Llenado de la tabla con los datos recibidos
                for index, departamento in enumerate(listaDepartamento):
                    self.tbDepartamento.insertRow(index)
                    self.tbDepartamento.setRowHeight(index, 45)
                    
                    
                    self.addItem_a_tabla(index, 0, departamento.nombre)
                    self.addItem_a_tabla(index, 1, departamento.descripcion)

                    # Botones para editar y eliminar
                    btnEliminar = QPushButton("Eliminar")
                    btnEliminar.clicked.connect(lambda checked, idx=departamento.id: self._eliminarRegistro(idx))
                    btnEliminar.setMinimumSize(QSize(80,35))
                    btnEliminar.setStyleSheet("""   QPushButton{background-color:#ff5151;color:white;}
                                                    QPushButton::hover{background-color:#ff0000;color:white;}
                                              """)
                    
                    btnEditar = QPushButton("Editar")
                    btnEditar.clicked.connect(lambda checked, idx=departamento.id: self._editar_Departamento(idx))
                    btnEditar.setMinimumSize(QSize(80,35))
                    btnEditar.setStyleSheet(""" QPushButton{background-color:#00b800;color:white;}
                                                QPushButton::hover{background-color:#00a800;color:white;}
                                            """)

                    # Crear un contenedor para los botones
                    button_widget = QWidget()
                    button_widget.setStyleSheet(u"background-color:transparent;")
                    layout = QHBoxLayout()
                    layout.addWidget(btnEditar)
                    layout.addSpacing(15)
                    layout.addWidget(btnEliminar)
                    button_widget.setLayout(layout)
                    layout.setContentsMargins(10, 0, 10,0)

                    # Añadir el contenedor de botones a la última columna de la fila actual
                    self.tbDepartamento.setCellWidget(index, 2, button_widget)
            else:
                self._mostrar_mensaje_sin_datos()
        else:
            self._mostrar_mensaje_sin_datos()

    def addItem_a_tabla(self,row, colum,dato):
        dato_item = QTableWidgetItem(dato)
        dato_item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)  # No editable
        self.tbDepartamento.setItem(row, colum, dato_item)

    def _actualizar_lblPagina(self,numPagina, totalPagina):
        self.lblNumPagina.setText(f"Pagina {numPagina} de {totalPagina} ")

    def _actualizarValoresPaginado(self,paginaActual,totalPaginas):
        self.paginaActual = paginaActual
        self.ultimaPagina = totalPaginas
        ## Valores necesarios para las paginacion:
        if totalPaginas <= 1:
            self.btnPrimerPagina.setEnabled(False)
            self.btnAnterior.setEnabled(False)
            self.btnSiguiente.setEnabled(False)
            self.btnUltimaPagina.setEnabled(False)
        elif paginaActual == 1:
            self.btnPrimerPagina.setEnabled(False)
            self.btnAnterior.setEnabled(False)
            self.btnSiguiente.setEnabled(True)
            self.btnUltimaPagina.setEnabled(True)
        elif paginaActual == totalPaginas:
            self.btnPrimerPagina.setEnabled(True)
            self.btnAnterior.setEnabled(True)
            self.btnSiguiente.setEnabled(False)
            self.btnUltimaPagina.setEnabled(False)
        else:
            self.btnPrimerPagina.setEnabled(True)
            self.btnAnterior.setEnabled(True)
            self.btnSiguiente.setEnabled(True)
            self.btnUltimaPagina.setEnabled(True)

    def _irPrimeraPagina(self):
        self.paginaActual = 1
        self._cargar_tabla()

    def _irUltimaPagina(self):
        self.paginaActual = self.ultimaPagina
        self._cargar_tabla()

    def _irSiguientePagina(self):
        if (self.paginaActual+1) <= self.ultimaPagina:
            self.paginaActual = self.paginaActual+1
            self._cargar_tabla()

    def _irAnteriorPagina(self):
        if (self.paginaActual - 1) >= 1:
            self.paginaActual = self.paginaActual-1
            self._cargar_tabla()

    def _buscarDepartamento(self):
        input_busqueda = self.inputBuscar.text();
        if input_busqueda:
            self.busqueda = input_busqueda
            self._cargar_tabla()
            self.busqueda = None
        else:
            self.paginaActual = 1
            self._cargar_tabla()

    def _eliminarRegistro(self, idx):
            dial = DialogoEmergente("¿?","¿Seguro que quieres eliminar este registro?","Question",True,True)
            if dial.exec() == QDialog.Accepted:
                result = self.Pservices.eliminarDepartamento(idx)
                if result["success"]:
                    dial = DialogoEmergente("","Se elimino el registro correctamente.","Check")
                    dial.exec()
                    self._cargar_tabla()
                else:
                    dial = DialogoEmergente("","Hubo un error al eliminar este registro.","Error")
                    dial.exec()

    def _editar_Departamento(self,id):
        blur_effect = QGraphicsBlurEffect(self)
        blur_effect.setBlurRadius(10)  # Ajusta el radio de desenfoque según sea necesario
        self.setGraphicsEffect(blur_effect)
        
        form = formDepartamento(titulo="Actualizar departamento",id=id)
        form.exec()
        
        self._cargar_tabla()
        self.setGraphicsEffect(None)

    def _crear_departamento(self):
        blur_effect = QGraphicsBlurEffect(self)
        blur_effect.setBlurRadius(10)  # Ajusta el radio de desenfoque según sea necesario
        self.setGraphicsEffect(blur_effect)
        
        form = formDepartamento()
        form.exec()
        self._cargar_tabla()
        self.setGraphicsEffect(None)
        