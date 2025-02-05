from PySide6.QtWidgets import *
from PySide6.QtCore import *
from Utils.Utils import *
from UI.AdministraPersona.formPersona import *
from services.empleadoServices import EmpleadoServices
from datetime import datetime

class AdminEmpleado(QWidget):
    cerrar_adminEmpleado = Signal()
    paginaActual = 1
    ultimaPagina = 1
    busqueda = None
    EmpServices = EmpleadoServices()


    def __init__(self, parent= None) -> None:
        super().__init__(parent)
        self.setObjectName("admin")

        cargar_estilos('claro','admin.css',self)

        layout = QVBoxLayout()
        layout.setContentsMargins(10,10,10,10)

        frame = QFrame()

        self.layoutFrame = QVBoxLayout()
        self.layoutFrame.setContentsMargins(0,0,0,0)
        self.layoutFrame.setSpacing(0)

        titulo = QLabel(text="Administrar personas")
        titulo.setObjectName("titulo")
        titulo.setMinimumHeight(50)
        titulo.setAlignment(Qt.AlignCenter)
        self.layoutFrame.addWidget(titulo)
        
        layoutTop = QHBoxLayout()
        layoutTop.setContentsMargins(30,30,30,30)
        layoutTop.setSpacing(5)
        layoutTop.setAlignment(Qt.AlignCenter)
        minimoTamBtn = QSize(120,40)

        ##botones de arriba
        self.btnCerrar = QPushButton(text="Cerrar");
        self.btnCerrar.setFixedSize(minimoTamBtn)
        self.btnCerrar.setCursor(Qt.PointingHandCursor)
        self.btnCerrar.clicked.connect(self._cerrar)
        Sombrear(self.btnCerrar,20,0,0)

        self.inputBuscar = QLineEdit()
        self.inputBuscar.setClearButtonEnabled(True)
        self.inputBuscar.setPlaceholderText("Buscar persona por nombre, apellidos, cedula o correo.")
        self.inputBuscar.setFixedSize(QSize(500,30))
        self.inputBuscar.textChanged.connect(self.cargarTabla)
        Sombrear(self.inputBuscar,20,0,0)

        self.btnBuscar = QPushButton(text="Buscar")
        self.btnBuscar.setCursor(Qt.PointingHandCursor)
        self.btnBuscar.setFixedSize(minimoTamBtn)
        self.btnBuscar.clicked.connect(self.buscarPersona) 
        Sombrear(self.btnBuscar,20,0,0)

        self.btnCrear = QPushButton(text="Crear")
        self.btnCrear.setCursor(Qt.PointingHandCursor)
        self.btnCrear.setFixedSize(minimoTamBtn)
        self.btnCrear.setObjectName("crear")
        self.btnCrear.clicked.connect(self.crearEmpleado) ##esto no se mueve
        Sombrear(self.btnCrear,20,0,0)

        ##acomodando botones de arriba en el layout
        layoutTop.addSpacing(25)
        layoutTop.addWidget(self.btnCerrar,1)
        layoutTop.addStretch(1)
        layoutTop.addWidget(self.inputBuscar,2)
        layoutTop.addSpacing(10)
        layoutTop.addWidget(self.btnBuscar,2)
        layoutTop.addStretch(1)
        layoutTop.addWidget(self.btnCrear,2)
        layoutTop.addStretch(5)
        self.layoutFrame.addLayout(layoutTop)
        
        ##crean el objeto tabla
        self.tbPersona = QTableWidget() 
        if (self.tbPersona.columnCount() < 7):
            self.tbPersona.setColumnCount(7) ##indican la cantidad de columnas.
        ##crean un array de titulos para cada columna    
        header_labels = ["Nombre", "Cedula", "Correo", "Nacimiento", "Estado civil", "Dirección","Acciones"]
        self.tbPersona.setHorizontalHeaderLabels(header_labels) ##ingresan el array aquí
        self.tbPersona.horizontalHeader().setFixedHeight(40)
        self.tbPersona.verticalHeader().setVisible(False)
        self.tbPersona.horizontalHeader().setStretchLastSection(True)
        self.tbPersona.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        # self.tbPersona.setColumnWidth(8, 220)
        self.tbPersona.setColumnWidth(6, 305)  # La columna 3 tendrá un ancho fijo de 150 píxeles

        self.tbPersona.horizontalHeader().setSectionsMovable(False)
        self.tbPersona.horizontalHeader().setMinimumSectionSize(50)
        self.tbPersona.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.tbPersona.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        Sombrear(self.tbPersona,30,0,0)

        layoutTb = QHBoxLayout()
        layoutTb.setContentsMargins(70,40,70,40)
        layoutTb.addWidget(self.tbPersona)
        self.layoutFrame.addLayout(layoutTb)


        layoutButtom = QHBoxLayout()
        layoutButtom.setAlignment(Qt.AlignCenter)
        layoutButtom.setContentsMargins(10,10,10,40)
        layoutButtom.setSpacing(5)

        self.btnPrimerPagina = QPushButton(text="Primera Pagina.")
        self.btnPrimerPagina.setFixedSize(minimoTamBtn)
        self.btnPrimerPagina.setCursor(Qt.PointingHandCursor)
        self.btnPrimerPagina.setEnabled(False)
        self.btnPrimerPagina.clicked.connect(self._irPrimeraPagina)
        Sombrear(self.btnPrimerPagina,20,0,0)

        self.btnAnterior = QPushButton(text="Anterior")
        self.btnAnterior.setEnabled(False)
        self.btnAnterior.setCursor(Qt.PointingHandCursor)
        self.btnAnterior.setFixedSize(minimoTamBtn)
        self.btnAnterior.clicked.connect(self._irAnteriorPagina)
        Sombrear(self.btnAnterior,20,0,0)

        self.lblNumPagina = QLabel(text="Pagina 0 de 0 paginas")
        self.lblNumPagina.setFixedSize(QSize(170,40))
        self.lblNumPagina.setAlignment(Qt.AlignCenter)


        self.btnSiguiente = QPushButton(text="Siguiente")
        self.btnSiguiente.setCursor(Qt.PointingHandCursor)
        self.btnSiguiente.setEnabled(False)
        self.btnSiguiente.setFixedSize(minimoTamBtn)
        self.btnSiguiente.clicked.connect(self._irSiguientePagina)
        Sombrear(self.btnSiguiente,20,0,0)

        self.btnUltimaPagina = QPushButton(text="Ultima Pagina")
        self.btnUltimaPagina.setCursor(Qt.PointingHandCursor)
        self.btnUltimaPagina.setEnabled(False)
        self.btnUltimaPagina.setFixedSize(minimoTamBtn)
        self.btnUltimaPagina.clicked.connect(self._irUltimaPagina)
        Sombrear(self.btnUltimaPagina,20,0,0)

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
        self.cargarTabla() 

    def _cerrar(self):
        self.cerrar_adminEmpleado.emit()

    def mensajeEstadoTabla(self,mensaje:str):
        self.tbPersona.setRowCount(0)
        if self.tbPersona.rowCount() == 0:
            # Si la tabla está vacía, agregar una fila con el mensaje
            self.tbPersona.setRowCount(1)  # Establecer una fila
            self.addItem_a_tabla(0,0,mensaje)
            # Fusionar la celda con el mensaje "Sin datos" en el número de columnas
            if self.tbPersona.columnCount() > 0:
                self.tbPersona.setSpan(0, 0, 1, self.tbPersona.columnCount())

    def cargarTabla(self):
        result = self.EmpServices.listar_empleados(pagina=self.paginaActual,tam_pagina=10,tipo_orden="DESC",busqueda=self.busqueda)
        
        if result["success"]:
            listaPersona = result["data"]["listaPersonas"]
            if len(listaPersona) >0:
                paginaActual    = result["data"]["pagina_actual"]
                tamPagina       = result["data"]["tam_pagina"]
                totalPaginas    = result["data"]["total_paginas"]
                totalRegistros  = result["data"]["total_registros"]

                #carga los valores de la pagina.
                self.actualizarLabelPagina(paginaActual,totalPaginas)
                self.actualizarBtnPagina(paginaActual,totalPaginas)

                #Limpiamos filas para cada ocasion que se recarga la tabla
                self.tbPersona.setRowCount(0)

                for index, data in enumerate(listaPersona):
                    self.tbPersona.insertRow(index)  # Crea una fila por registro
                    self.tbPersona.setRowHeight(index,45)
                    #obteniendo el id empleado y el id empleado
                    id_empleado = data['id_empleado']
                    persona:Persona = data['persona']

                    self.addItem_a_tabla(index,0,f'{persona.nombre} {persona.apellidos}')
                    self.addItem_a_tabla(index,1,persona.cedula)
                    self.addItem_a_tabla(index,2,persona.correo)
                    self.addItem_a_tabla(index,3,format_Fecha(str(persona.fecha_nacimiento)))
                    self.addItem_a_tabla(index,4,persona.estado_civil)
                    self.addItem_a_tabla(index,5,persona.direccion)

                    #Agregando los botones de las acciones que se pueden realizar
                    #boton mas informacion, boton editar, boton eliminar.
                    btnInfo = QPushButton(text="Más Info.",parent=self.tbPersona)
                    btnInfo.setObjectName('btnInfo')
                    btnInfo.setMinimumSize(QSize(80,35))
                    btnInfo.setMaximumWidth(100)
                    btnInfo.clicked.connect(lambda checked, idx=persona.id: self.eliminarEmpleado(idx))
                           
                    btnEliminar = QPushButton(text="Eliminar",parent=self.tbPersona)
                    btnEliminar.setObjectName('btneliminar')
                    btnEliminar.setMinimumSize(QSize(80,35))
                    btnEliminar.setMaximumWidth(100)
                    btnEliminar.clicked.connect(lambda checked, idx=persona.id: self.eliminarEmpleado(idx))

                    btnEditar = QPushButton("Editar",parent=self.tbPersona)
                    btnEditar.setObjectName('btneditar')
                    btnEditar.setMinimumSize(QSize(80,35))
                    btnEditar.setMaximumWidth(100)
                    btnEditar.clicked.connect(lambda checked, idx = persona.id: self.editarEmpleado(idx))
                    
                    #contenedor de los botones.
                    layout = QHBoxLayout()
                    layout.addWidget(btnInfo)
                    layout.addSpacing(15)
                    layout.addWidget(btnEditar)
                    layout.addSpacing(15)
                    layout.addWidget(btnEliminar)
                    layout.setContentsMargins(10, 0, 10,0)
                    #widget para el layout de los botones.
                    button_widget = QWidget()
                    button_widget.setFixedWidth(300)
                    button_widget.setLayout(layout)
    
                    self.tbPersona.setCellWidget(index, 6, button_widget) 
            else:
                self.mensajeEstadoTabla("No hay registros.")
        else:
            self.mensajeEstadoTabla("Error de conexión.")

    def addItem_a_tabla(self,row, colum,dato):
        dato_item = QTableWidgetItem(dato)
        dato_item.setTextAlignment(Qt.AlignCenter)
        dato_item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)  # No editable
        self.tbPersona.setItem(row, colum, dato_item)
##resto del codigo..
    def actualizarLabelPagina(self,numPagina, totalPagina):
        self.lblNumPagina.setText(f"Pagina {numPagina} de {totalPagina} ")

    def actualizarBtnPagina(self,paginaActual,totalPaginas):
        self.paginaActual = paginaActual
        self.ultimaPagina = totalPaginas
        self.btnSiguiente.setEnabled(paginaActual < totalPaginas)
        self.btnUltimaPagina.setEnabled(paginaActual < totalPaginas)
        self.btnPrimerPagina.setEnabled(paginaActual > 1)
        self.btnAnterior.setEnabled(paginaActual > 1)

    def _irPrimeraPagina(self):
        self.paginaActual = 1
        self.cargarTabla()
    
    def _irUltimaPagina(self):
        self.paginaActual = self.ultimaPagina
        self.cargarTabla()

    def _irSiguientePagina(self):
        if (self.paginaActual+1) <= self.ultimaPagina:
            self.paginaActual = self.paginaActual+1
            self.cargarTabla()

    def _irAnteriorPagina(self):
        if (self.paginaActual - 1) >= 1:
            self.paginaActual = self.paginaActual-1
            self.cargarTabla()

    def buscarPersona(self):
        input_busqueda = self.inputBuscar.text()
        if input_busqueda:
            self.busqueda = input_busqueda
            self.cargarTabla()
            self.busqueda = None
        else:
            self.paginaActual = 1
            self.cargarTabla()

    def verMasInformacion(self, id_empleado:int):
        pass

    def eliminarEmpleado(self, idx):
        pass

    def editarEmpleado(self,id):
        blur_effect = QGraphicsBlurEffect(self)
        blur_effect.setBlurRadius(10)  # Ajusta el radio de desenfoque según sea necesario
        self.setGraphicsEffect(blur_effect)

        self.cargarTabla()#luego de terminar se recarga la tabla
        self.setGraphicsEffect(None)

    def crearEmpleado(self):
        blur_effect = QGraphicsBlurEffect(self)
        blur_effect.setBlurRadius(10)  # Ajusta el radio de desenfoque según sea necesario
        
        self.cargarTabla() ##se recarga la tabla despues de terminar
        self.setGraphicsEffect(None)
        