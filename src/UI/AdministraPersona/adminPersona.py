from PySide6.QtWidgets import *
from PySide6.QtCore import *
from Utils.Utils import *
from UI.AdministraPersona.formPersona import *
from services.personaService import *
from datetime import datetime

class AdminPersona(QWidget):
    cerrar_adminP = Signal()
    paginaActual = 1
    ultimaPagina = 1
    busqueda = None
    Pservices = PersonaServices()


    def __init__(self, parent= None) -> None:
        super().__init__(parent)
        self.setObjectName("admin")

        add_Style(carpeta="css",archivoQSS="adminPersona.css",QObjeto=self)

        layout = QVBoxLayout();
        layout.setContentsMargins(10,10,10,10)

        frame = QFrame()

        self.layoutFrame = QVBoxLayout()
        self.layoutFrame.setContentsMargins(0,0,0,0)
        self.layoutFrame.setSpacing(0)

        """ 
            Aqui solo cambian el titulo de el widget osea del crud
        """
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
        self.inputBuscar.textChanged.connect(self._cargar_tabla)
        Sombrear(self.inputBuscar,20,0,0)

        self.btnBuscar = QPushButton(text="Buscar")
        self.btnBuscar.setCursor(Qt.PointingHandCursor)
        self.btnBuscar.setFixedSize(minimoTamBtn)
        self.btnBuscar.clicked.connect(self._buscarPersona) ##revicen que el metonod _buscarPersona haga bien su trabajp
        Sombrear(self.btnBuscar,20,0,0)

        self.btnCrear = QPushButton(text="Crear")
        self.btnCrear.setCursor(Qt.PointingHandCursor)
        self.btnCrear.setFixedSize(minimoTamBtn)
        self.btnCrear.setObjectName("crear")
        self.btnCrear.clicked.connect(self._crear_persona) ##esto no se mueve
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
        
        """
            Esto lo deben cambiar cada crean la tabla de acuerdo a la cantidad
            atributos del objeto
            Nota: no debe existir columna de id esto no se debe mostrar nunca
        """
        self.tbPersona = QTableWidget() ##crean el objeto tabla
        if (self.tbPersona.columnCount() < 9):
            self.tbPersona.setColumnCount(9) ##indican la cantidad de columnas.
        ##crean un array de titulos para cada columna    
        header_labels = ["Nombre", "1° Apellido", "2° Apellido", "Cedula", "Correo", "Nacimiento", "Estado civil", "Dirección","Acciones"]
        self.tbPersona.setHorizontalHeaderLabels(header_labels) ##ingreasan el array aqui
        """Esto ya no hace falta momverlo solo cambiar el nombre tbPersona por el nombre que 
            le pusieron a su tabla
        """
        self.tbPersona.horizontalHeader().setFixedHeight(40)
        self.tbPersona.verticalHeader().setVisible(False)
        self.tbPersona.horizontalHeader().setStretchLastSection(True)
        self.tbPersona.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        self.tbPersona.setColumnWidth(8, 220)
        self.tbPersona.horizontalHeader().setSectionsMovable(False)
        self.tbPersona.horizontalHeader().setMinimumSectionSize(50)
        Sombrear(self.tbPersona,30,0,0)


        """de aqui para abajo no se mueve solo asegurese que la tabla se este llamando
            correctamente
        """
        layoutTb = QHBoxLayout()
        layoutTb.setContentsMargins(70,40,70,40)
        layoutTb.addWidget(self.tbPersona)
        self.layoutFrame.addLayout(layoutTb)


        layoutButtom = QHBoxLayout()
        layoutButtom.setAlignment(Qt.AlignCenter)
        layoutButtom.setContentsMargins(10,10,10,40)
        layoutButtom.setSpacing(5)
        """ de aqui para abajo no se modifica nada en teoria"""
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
        self._cargar_tabla() 

    """Esto no se toca"""
    def _cerrar(self):
        self.cerrar_adminP.emit()

    """ lo modifican de acuerdo al nombre de su tabla
        no se modifica mas
    """
    def _mostrar_mensaje_sin_datos(self,mensaje:str):
        #Borra filas en caso de que la conexion se haya ido
        self.tbPersona.setRowCount(0)
        if self.tbPersona.rowCount() == 0:
            # Si la tabla está vacía, agregar una fila con el mensaje "Sin datos"
            self.tbPersona.setRowCount(1)  # Establecer una fila
            item = QTableWidgetItem(mensaje)
            item.setTextAlignment(Qt.AlignCenter)
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.tbPersona.setItem(0, 0, item)

            # Fusionar la celda con el mensaje "Sin datos" en el número de columnas
            if self.tbPersona.columnCount() > 0:  # Asegurarse de que hay columnas
                self.tbPersona.setSpan(0, 0, 1, self.tbPersona.columnCount())

    def _cargar_tabla(self):
        result = self.Pservices.obtenerListaPersonas(pagina=self.paginaActual,tam_pagina=10,tipo_orden="DESC",busqueda=self.busqueda)
        if result["success"]: ##si se hizo la consulta a la bd correctamete de lo contrario se salta el llenado
            listaPersona = result["data"]["listaPersonas"]
            if len(listaPersona) >0:
                paginaActual = result["data"]["pagina_actual"]
                tamPagina = result["data"]["tam_pagina"]
                totalPaginas = result["data"]["total_paginas"]
                totalRegistros = result["data"]["total_registros"]
                #carga los valores de la pagina en teoria quedan igual
                self._actualizar_lblPagina(paginaActual,totalPaginas)
                self._actualizarValoresPaginado(paginaActual,totalPaginas)

                #Limpiamos las filas 
                self.tbPersona.setRowCount(0)
                #recorrer la lista traia de la base de datos.
                for index, persona in enumerate(listaPersona):
                    self.tbPersona.insertRow(index)  # Crea una fila por registro
                    self.tbPersona.setRowHeight(index,45)
                    
                    """"Agregar a tabla de acuerdo a los atributos de su clase
                        usa la funcion addItem_a_tabla()
                    """
                    self.addItem_a_tabla(index,0,persona.nombre)
                    self.addItem_a_tabla(index,1,persona.apellido1)
                    self.addItem_a_tabla(index,2,persona.apellido2)
                    self.addItem_a_tabla(index,3,persona.cedula)
                    self.addItem_a_tabla(index,4,persona.correo)
                    self.addItem_a_tabla(index,5,self._formatear_fecha(str(persona.fecha_nacimiento)))
                    self.addItem_a_tabla(index,6,persona.estado_civil)
                    self.addItem_a_tabla(index,7,persona.direccion)

                    """No cambia"""
                    btnEliminar = QPushButton(text="Eliminar")
                    btnEliminar.clicked.connect(lambda checked, idx=persona.id: self._eliminarRegistro(idx))##cambier solo el persona.id por su objeto.id
                    btnEliminar.setMinimumSize(QSize(80,35))
                    btnEliminar.setMaximumWidth(100)
                    btnEliminar.setStyleSheet("""   QPushButton{background-color:#ff5151;color:white;}
                                                    QPushButton::hover{background-color:#ff0000;color:white;}
                                              """)

                    btnEditar = QPushButton("Editar")
                    btnEditar.clicked.connect(lambda checked, idx = persona.id: self._editar_Persona(idx)) ##cambier solo el persona.id por su objeto, y el nombre de la funcion
                    btnEditar.setMinimumSize(QSize(80,35))
                    btnEditar.setMaximumWidth(100)
                    btnEditar.setStyleSheet(""" QPushButton{background-color:#00b800;color:white;}
                                                QPushButton::hover{background-color:#00a800;color:white;}
                                            """)
                    """No se modifica"""
                    button_widget = QWidget()
                    button_widget.setStyleSheet(u"background-color:transparent;")
                    layout = QHBoxLayout()
                    layout.addWidget(btnEditar)
                    layout.addSpacing(15)
                    layout.addWidget(btnEliminar)
                    button_widget.setLayout(layout)
                    layout.setContentsMargins(10, 0, 10,0)
                    ##el segundo numero indica el numero de columna osea la ultima, varia de acuerdo al bojeto
                    self.tbPersona.horizontalHeader().setSectionResizeMode(8, QHeaderView.Fixed)
                    self.tbPersona.setColumnWidth(8,210)
                    self.tbPersona.setCellWidget(index, 8, button_widget) 
            else:
                self._mostrar_mensaje_sin_datos("No hay registros")
        else:
            self._mostrar_mensaje_sin_datos("Error de conexión")

    """Esto no cambia, el dato debe ser string"""
    def addItem_a_tabla(self,row, colum,dato):
        dato_item = QTableWidgetItem(dato)
        dato_item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)  # No editable
        self.tbPersona.setItem(row, colum, dato_item)

    """No se modifica"""
    def _actualizar_lblPagina(self,numPagina, totalPagina):
        self.lblNumPagina.setText(f"Pagina {numPagina} de {totalPagina} ")

    """En teoria no se modifica"""
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
    """En teoria no se modifica"""
    def _irPrimeraPagina(self):
        self.paginaActual = 1
        self._cargar_tabla()
    
    """En teoria no se modifica"""
    def _irUltimaPagina(self):
        self.paginaActual = self.ultimaPagina
        self._cargar_tabla()
    """En teoria no se modifica"""
    def _irSiguientePagina(self):
        if (self.paginaActual+1) <= self.ultimaPagina:
            self.paginaActual = self.paginaActual+1
            self._cargar_tabla()
    """En teoria no se modifica"""
    def _irAnteriorPagina(self):
        if (self.paginaActual - 1) >= 1:
            self.paginaActual = self.paginaActual-1
            self._cargar_tabla()
    """Lo modifican de acuerdo a su objeto osea el metodo llebe el nombre de su objeto
        ejemplo _buscarDepartamento
        esta funcion esta conectada al botno buscar
        se aseguran que el nombre este igual
    """
    def _buscarPersona(self):
        input_busqueda = self.inputBuscar.text()
        if input_busqueda:
            self.busqueda = input_busqueda
            self._cargar_tabla()
            self.busqueda = None
        else:
            self.paginaActual = 1
            self._cargar_tabla()

    def _formatear_fecha(self,fecha:str):
        año, mes, dia = fecha.split("-")
        mes
        meses = {
            '01': 'enero',
            '02': 'febrero',
            '03': 'marzo',
            '04': 'abril',
            '05': 'mayo',
            '06': 'junio',
            '07': 'julio',
            '08': 'agosto',
            '09': 'septiembre',
            '10': 'octubre',
            '11': 'noviembre',
            '12': 'diciembre'
        }
        mes_nombre = meses[mes]
        return f"{int(dia)} de {mes_nombre} del {año}"

    """Lo modifican de acuerdo a su crud
        aseguresen que se muestre bien los mensajes
    """
    def _eliminarRegistro(self, idx):
            dial = DialogoEmergente("¿?","¿Seguro que quieres eliminar este registro?","Question",True,True)
            if dial.exec() == QDialog.Accepted:##se revisa  si aceptro el dialogo emergente
                result = self.Pservices.eliminarPersona(idx)
                if result["success"]:
                    dial = DialogoEmergente("","Se elimino el registro correctamente.","Check")
                    dial.exec()
                    self._cargar_tabla()
                else:
                    dial = DialogoEmergente("","Hubo un error al eliminar este registro.","Error")
                    dial.exec()
    
    """Modifican nada mas el form osea crean el objeto de su formulario"""
    def _editar_Persona(self,id):
        blur_effect = QGraphicsBlurEffect(self)
        blur_effect.setBlurRadius(10)  # Ajusta el radio de desenfoque según sea necesario
        self.setGraphicsEffect(blur_effect)
        """Aqui crean un omjeto form pasan el titulo y el id"""
        form = formPersona(titulo="Actualizar persona",id=id)
        form.exec()#Levantan la ventana
        
        self._cargar_tabla()#luego de terminar se recarga la tabla
        self.setGraphicsEffect(None)

    def _crear_persona(self):
        blur_effect = QGraphicsBlurEffect(self)
        blur_effect.setBlurRadius(10)  # Ajusta el radio de desenfoque según sea necesario
        self.setGraphicsEffect(blur_effect)
        """Se crean un ombjeto form para crear este no llevara titulo ni id"""
        form = formPersona()
        form.exec() ##se ejecuta
        self._cargar_tabla() ##se recarga la tabla despues de terminar
        self.setGraphicsEffect(None)
        


