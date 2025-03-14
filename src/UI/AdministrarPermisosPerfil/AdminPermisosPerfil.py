from PySide6.QtWidgets import QMessageBox
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from Utils.Utils import *
from UI.AdministrarPermisosPerfil.formPermisosPerfil import *
from UI.AdministrarPerfil.formPerfil import *
from services.permisosPerfilServices import *
from services.perfilService import *
from services.perfilService import *
from settings.variable import *

class AdminPermisosPerfil(QWidget):
    cerrar_adminP = Signal()
    paginaActual = 1
    ultimaPagina = 1
    busqueda = None
    permisoperfilServices = PermisosPerfilServices()
    perfilServices = PerfilServices()
  #  """
    def __init__(self, parent= None) -> None:
        super().__init__(parent)
        self.setObjectName("admin")
    
        cargar_estilos('claro','admin.css',self)
    
        #layout = QBoxLayout()
        layout = QBoxLayout(QBoxLayout.TopToBottom)
        layout.setContentsMargins(10,10,10,10)
    
        frame = QFrame()
        self.layoutFrame = QVBoxLayout()
        self.layoutFrame.setContentsMargins(0,0,0,0)
        self.layoutFrame.setSpacing(0)
    
        titulo = QLabel(text="Administrar permisos de perfil")
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
        self.inputBuscar.setPlaceholderText("Buscar persona por nombre.")
        self.inputBuscar.setFixedSize(QSize(500,30))
        self.inputBuscar.textChanged.connect(self._cargar_tabla)
        Sombrear(self.inputBuscar,20,0,0)
        
        self.btnBuscar = QPushButton(text="Buscar")
        self.btnBuscar.setCursor(Qt.PointingHandCursor)
        self.btnBuscar.setFixedSize(minimoTamBtn)
        self.btnBuscar.clicked.connect(self._buscarPermisos) ##revicen que el metonod _buscarPermisos haga bien su trabajp
        Sombrear(self.btnBuscar,20,0,0)

        self.btnCrear = QPushButton(text="Crear")
        self.btnCrear.setCursor(Qt.PointingHandCursor)
        self.btnCrear.setFixedSize(minimoTamBtn)
        self.btnCrear.setObjectName("crear")
        self.btnCrear.clicked.connect(self._crear_permisos) ##esto no se mueve
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
        
        
        
        #    Esto lo deben cambiar cada crean la tabla de acuerdo a la cantidad
         #   atributos del objeto
          #  Nota: no debe existir columna de id esto no se debe mostrar nunca
        
        self.tbPermisosPerfil = QTableWidget() ##crean el objeto tabla
        if (self.tbPermisosPerfil.columnCount() < 7):
            self.tbPermisosPerfil.setColumnCount(7) ##indican la cantidad de columnas.
        ##crean un array de titulos para cada columna    
        header_labels = ["Perfil", "Acesso a", "Ver", "Crear", "Editar", "Eliminar","Acciones"]
        self.tbPermisosPerfil.setHorizontalHeaderLabels(header_labels) ##ingreasan el array aqui
        self.tbPermisosPerfil.horizontalHeader().setFixedHeight(40)
        self.tbPermisosPerfil.verticalHeader().setVisible(False)
        self.tbPermisosPerfil.horizontalHeader().setStretchLastSection(True)
        self.tbPermisosPerfil.horizontalHeader().setSectionsMovable(False)
        self.tbPermisosPerfil.horizontalHeader().setMinimumSectionSize(50)
        self.tbPermisosPerfil.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        Sombrear(self.tbPermisosPerfil,30,0,0)


        #de aqui para abajo no se mueve solo asegurese que la tabla se este llamando correctamente
        
        layoutTb = QHBoxLayout()
        layoutTb.setContentsMargins(70,40,70,40)
        layoutTb.addWidget(self.tbPermisosPerfil)
        self.layoutFrame.addLayout(layoutTb)
        
        
        layoutButtom = QHBoxLayout()
        layoutButtom.setAlignment(Qt.AlignCenter)
        layoutButtom.setContentsMargins(10,10,10,40)
        layoutButtom.setSpacing(5)
        # de aqui para abajo no se modifica nada en teoria
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

    def _cerrar(self):
        self.cerrar_adminP.emit()
        
    def _mostrar_mensaje_sin_datos(self,mensaje:str):
        #Borra filas en caso de que la conexion se haya ido
        self.tbPermisosPerfil.setRowCount(0)
        if self.tbPermisosPerfil.rowCount() == 0:
            # Si la tabla está vacía, agregar una fila con el mensaje "Sin datos"
            self.tbPermisosPerfil.setRowCount(1)  # Establecer una fila
            item = QTableWidgetItem(mensaje)
            item.setTextAlignment(Qt.AlignCenter)
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.tbPermisosPerfil.setItem(0, 0, item)

            # Fusionar la celda con el mensaje "Sin datos" en el número de columnas
            if self.tbPermisosPerfil.columnCount() > 0:  # Asegurarse de que hay columnas
                self.tbPermisosPerfil.setSpan(0, 0, 1, self.tbPermisosPerfil.columnCount())
               # """
    def _crear_boton(self, texto, estilo, funcion, idx):
        btn = QPushButton(texto)
        btn.clicked.connect(lambda checked, idx=idx: funcion(idx))
        btn.setMinimumSize(QSize(80, 35))
        btn.setMaximumWidth(100)
        btn.setStyleSheet(estilo)
        return btn

    def _cargar_tabla(self):
        result = self.permisoperfilServices.listar_permisos_perfil(pagina=self.paginaActual, tam_pagina=10, tipo_orden="DESC", busqueda=self.busqueda)
        
        
        
        if result["success"]:
            listaPermisos = result["data"]["listaPermisosPerfil"]
            if len(listaPermisos) > 0:
                paginaActual = result["data"]["pagina_actual"]
                tamPagina = result["data"]["tam_pagina"]
                totalPaginas = result["data"]["total_paginas"]
                totalRegistros = result["data"]["total_registros"]
                self._actualizar_lblPagina(paginaActual, totalPaginas)
                self._actualizarValoresPaginado(paginaActual, totalPaginas)

                self.tbPermisosPerfil.setRowCount(0)
                for index, permisos in enumerate(listaPermisos):
                    self.tbPermisosPerfil.insertRow(index)
                    self.tbPermisosPerfil.setRowHeight(index, 45)

                    dato = self.perfilServices.obtenerPerfilPorId(permisos.perfil_id)
                    perfil = dato["data"]
                    acceso_a = [key for key, value in ACCESO_TABLE.items() if value == permisos.tabla]

                    self.addItem_a_tabla(index, 0, str(perfil.nombre))
                    if acceso_a:
                        self.addItem_a_tabla(index, 1, str(acceso_a[0]))
                    else:
                        print(f"Advertencia: `acceso_a` está vacío para el índice {index}")
                        self.addItem_a_tabla(index, 1, "N/A")

                    self.addItem_a_tabla(index, 2, ("Si" if permisos.ver else "No"))
                    self.addItem_a_tabla(index, 3, ("Si" if permisos.crear else "No"))
                    self.addItem_a_tabla(index, 4, ("Si" if permisos.editar else "No"))
                    self.addItem_a_tabla(index, 5, ("Si" if permisos.eliminar else "No"))

                    btnEliminar = self._crear_boton("Eliminar", """QPushButton{background-color:#ff5151;color:white;} QPushButton::hover{background-color:#ff0000;color:white;}""", self._eliminarRegistro, permisos.id)
                    btnEditar = self._crear_boton("Editar", """QPushButton{background-color:#00b800;color:white;} QPushButton::hover{background-color:#00a800;color:white;}""", self._editar_permiso, permisos.id)

                    button_widget = QWidget()
                    button_widget.setStyleSheet(u"background-color:transparent;")
                    layout = QHBoxLayout()
                    layout.addWidget(btnEditar)
                    layout.addSpacing(15)
                    layout.addWidget(btnEliminar)
                    button_widget.setLayout(layout)
                    layout.setContentsMargins(10, 0, 10, 0)
                    self.tbPermisosPerfil.setCellWidget(index, 6, button_widget)
            else:
                self._mostrar_mensaje_sin_datos("No hay registros")
        else:
            self._mostrar_mensaje_sin_datos("Error de conexión")

        
    def addItem_a_tabla(self,row, colum,dato):
        dato_item = QTableWidgetItem(dato)
        dato_item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)  # No editable
        self.tbPermisosPerfil.setItem(row, colum, dato_item)

    def _actualizar_lblPagina(self,numPagina, totalPagina):
        self.lblNumPagina.setText(f"Pagina {numPagina} de {totalPagina} ")

    def _actualizarValoresPaginado(self,paginaActual,totalPaginas):
        self.paginaActual = paginaActual
        self.ultimaPagina = totalPaginas
        self.btnSiguiente.setEnabled(paginaActual < totalPaginas)
        self.btnUltimaPagina.setEnabled(paginaActual < totalPaginas)
        self.btnPrimerPagina.setEnabled(paginaActual > 1)
        self.btnAnterior.setEnabled(paginaActual > 1)

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
 
    def _buscarPermisos(self):
        input_busqueda = self.inputBuscar.text()
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
                result = self.permisoperfilServices.eliminar_permiso_perfil(idx)
                if result["success"]:
                    dial = DialogoEmergente("","Se elimino el registro correctamente.","Check")
                    dial.exec()
                    self._cargar_tabla()
                else:
                    dial = DialogoEmergente("","Hubo un error al eliminar este registro.","Error")
                    dial.exec()
    
    def _editar_permiso(self,id):
        blur_effect = QGraphicsBlurEffect(self)
        blur_effect.setBlurRadius(10)
        self.setGraphicsEffect(blur_effect)
        form = formPermiso(titulo="Actualizar permiso",id=id)
        form.exec()
        self._cargar_tabla()
        self.setGraphicsEffect(None)

    def _crear_permiso(self):
        blur_effect = QGraphicsBlurEffect(self)
        blur_effect.setBlurRadius(10)
        self.setGraphicsEffect(blur_effect)
        form = formPermiso()
        form.exec()
        self._cargar_tabla() 
        self.setGraphicsEffect(None)
        
    def _crear_perfil(self):
    # Lógica para crear un perfil
        blur_effect = QGraphicsBlurEffect(self)
        blur_effect.setBlurRadius(10)
        self.setGraphicsEffect(blur_effect)
        form = formPerfil()
        form.exec()
        self.setGraphicsEffect(None)
        
        
    def _crear_permisos(self):
     # Crear un QMessageBox personalizado
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Crear")
        msg_box.setText("¿Qué desea crear?")
    # Agregar botones personalizados
        btn_perfil = msg_box.addButton("Crear perfil", QMessageBox.ActionRole)
        btn_permiso = msg_box.addButton("Crear permiso", QMessageBox.ActionRole)
        btn_cancelar = msg_box.addButton("Cancelar", QMessageBox.RejectRole)
        # Estilos para el QMessageBox
        
        estilo_msg_box = """
            QMessageBox {
                background-color: #f0f0f0; /* Color de fondo */
                border: 2px solid #4CAF50; /* Borde */
                border-radius: 10px; /* Bordes redondeados */
                padding: 20px; /* Espaciado interno */
            }
            QMessageBox QLabel {
                color: #333333; /* Color del texto */
                font-size: 16px; /* Tamaño de la fuente */
                font-weight: bold; /* Negrita */
            }
        """
   # Aplicar estilos a los botones
        estilo_botones = """
            QPushButton {
                background-color: #4CAF50; /* Color de fondo */
                color: white; /* Color del texto */
                border-radius: 5px; /* Bordes redondeados */
                padding: 10px 20px; /* Espaciado interno */
                font-size: 14px; /* Tamaño de la fuente */
                font-weight: bold; /* Negrita */
            }
            QPushButton:hover {
                background-color: #45a049; /* Color de fondo al pasar el mouse */
            }
            QPushButton:pressed {
                background-color: #3d8b40; /* Color de fondo al hacer clic */
            }
        """
    
    # Estilo específico para el botón de cancelar
        estilo_cancelar = """
            QPushButton {
                background-color: #f44336; /* Color de fondo */
                color: white; /* Color del texto */
                border-radius: 5px; /* Bordes redondeados */
                padding: 10px 20px; /* Espaciado interno */
                font-size: 14px; /* Tamaño de la fuente */
                font-weight: bold; /* Negrita */
            }
            QPushButton:hover {
                background-color: #e53935; /* Color de fondo al pasar el mouse */
            }
            QPushButton:pressed {
                background-color: #c62828; /* Color de fondo al hacer clic */
            }
        """
    
    # Aplicar estilos a los botones
        msg_box.setStyleSheet(estilo_msg_box)
        btn_perfil.setStyleSheet(estilo_botones)
        btn_permiso.setStyleSheet(estilo_botones)
        btn_cancelar.setStyleSheet(estilo_cancelar)
    # Mostrar el cuadro de diálogo
        msg_box.exec()
    
    # Verificar qué botón se presionó
        if msg_box.clickedButton() == btn_perfil:
            self._crear_perfil()  # Método para crear un perfil
        elif msg_box.clickedButton() == btn_permiso:
                self._crear_permiso()  # Método para crear un permiso
        elif msg_box.clickedButton() == btn_cancelar:
            return  # No hacer nada si se cancela
         
   