from PySide6.QtWidgets import QMessageBox
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from Utils.Utils import *
from UI.AdministrarReporte.formReporte import *
from UI.AdministrarReporte.formGenerarReporte import GenerarReporte
from services.reporteService import *
from services.empleadoServices import *
from settings.logger import logger
from settings.config import *

class AdminReporte(QWidget):
    signalCerrar = Signal()
    paginaActual = 1
    ultimaPagina = 1
    busqueda = None
    reporteServices = ReporteServices()
    empleadoServices = EmpleadoServices()
<<<<<<< HEAD

    def __init__(self, parent=None, permiso = None) -> None:
        super().__init__(parent)
        self.setObjectName("admin")
        self.permisoUsuario = permiso

        cargar_estilos("claro", "admin.css", self)

        # layout = QBoxLayout()
=======
    
    def __init__(self, parent= None) -> None:
        super().__init__(parent)
        self.setObjectName("admin")
    
        cargar_estilos('claro','admin.css',self)
    
        #layout = QBoxLayout()
>>>>>>> parent of 543debc (Merge branch 'main' into Gonzalo)
        layout = QBoxLayout(QBoxLayout.TopToBottom)
        layout.setContentsMargins(10,10,10,10)
    
        frame = QFrame()
        self.layoutFrame = QVBoxLayout()
        self.layoutFrame.setContentsMargins(0,0,0,0)
        self.layoutFrame.setSpacing(0)
    
        titulo = QLabel(text="Administrar reportes")
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
        self.inputBuscar = QLineEdit()
        self.inputBuscar.setClearButtonEnabled(True)
        self.inputBuscar.setPlaceholderText("Buscar reporte.")
        self.inputBuscar.setFixedSize(QSize(500,30))
        self.inputBuscar.textChanged.connect(self.cargarTabla)
        Sombrear(self.inputBuscar,20,0,0)

        ##acomodando botones de arriba en el layout
        layoutTop.addSpacing(25)
        layoutTop.addWidget(self.crearBoton('Cerrar',minimoTamBtn,self.cerrarAdminReporte))
        layoutTop.addStretch(1)
        layoutTop.addWidget(self.inputBuscar,2)
        layoutTop.addSpacing(10)
        layoutTop.addWidget(self.crearBoton('Buscar',minimoTamBtn,self.buscarRegistro))
        layoutTop.addStretch(1)
        layoutTop.addWidget(self.crearBoton('Generar Reporte',minimoTamBtn,self.crearReporte))
        layoutTop.addStretch(5)
        self.layoutFrame.addLayout(layoutTop)
        
        
         # Tabla Rol
        self.tbReporte = QTableWidget()# Crea la tabla para mostrar los perfiles
        if self.tbReporte.columnCount() < 5:# Si la tabla no tiene 3 columnas
            self.tbReporte.setColumnCount(5)# Establece 3 columnas
        header_labels = ["Empleado", "Fecha Generación", "Tipo Reporte", "Contenido", "Acciones"]
        self.tbReporte.setHorizontalHeaderLabels(header_labels)
        self.tbReporte.horizontalHeader().setFixedHeight(40) # Establece una altura fija para los encabezados
        self.tbReporte.verticalHeader().setVisible(False)# Oculta los encabezados verticales
        self.tbReporte.horizontalHeader().setStretchLastSection(True) # Hace que la última sección de la tabla se estire
        self.tbReporte.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)# Deshabilita la selección de filas
        Sombrear(self.tbReporte, 30, 0, 0)

        # Layout para la tabla
        layoutTb = QHBoxLayout()
        layoutTb.setContentsMargins(70, 40, 70, 40)
        layoutTb.addWidget(self.tbReporte)
        self.layoutFrame.addLayout(layoutTb)

        # Layout para los botones de paginación
        layoutButtom = QHBoxLayout()  # Crea un layout horizontal para los botones de paginación
        layoutButtom.setAlignment(Qt.AlignCenter)  # Centra los botones en el layout
        layoutButtom.setContentsMargins(10, 10, 10, 40)  # Establece márgenes alrededor de los botones
        layoutButtom.setSpacing(5)  # Define el espacio entre los botones

        # Etiqueta para mostrar el número de la página actual
        self.lblNumPagina = QLabel(text="Página 0 de 0 páginas")
        self.lblNumPagina.setFixedSize(QSize(170, 40))
        self.lblNumPagina.setAlignment(Qt.AlignCenter)
   
        self.btnPrimerPagina= self.crearBoton("Primer pagina",minimoTamBtn,self._irPrimeraPagina,False)
        self.btnAnterior    = self.crearBoton("Anterior",minimoTamBtn,self._irAnteriorPagina,False)
        self.btnSiguiente   = self.crearBoton("Siguiente",minimoTamBtn,self._irSiguientePagina,False)
        self.btnUltimaPagina= self.crearBoton("Ultima pagina",minimoTamBtn,self._irUltimaPagina,False)
        
        layoutButtom.addWidget(self.btnPrimerPagina)
        layoutButtom.addSpacing(10)
        layoutButtom.addWidget(self.btnAnterior)
        layoutButtom.addSpacing(10)
        layoutButtom.addWidget(self.lblNumPagina)
        layoutButtom.addSpacing(10)
        layoutButtom.addWidget(self.btnSiguiente)
        layoutButtom.addSpacing(10)
        layoutButtom.addWidget(self.btnUltimaPagina)


        self.layoutFrame.addLayout(layoutButtom)# Añadir el layout de los botones al layout principal
        frame.setLayout(self.layoutFrame) # Establecer el layout del frame principal
        layout.addWidget(frame) # Añadir el frame al layout principal
        self.setLayout(layout)# Establecer el layout del widget
        Sombrear(self, 30, 0, 0)
        self.cargarTabla()

    def crearBoton(self,text:str,fixedSize:QSize, functionConnect,enable:bool = True,cursorType=Qt.PointingHandCursor)->QPushButton:
        boton = QPushButton(text)
        boton.setEnabled(enable)
        boton.setFixedSize(fixedSize)
        boton.setCursor(cursorType)
        boton.clicked.connect(functionConnect)
        Sombrear(boton,20,0,0)
        return boton
    
    def cerrarAdminReporte(self):
         # Emitir una señal para cerrar la ventana
        self.signalCerrar.emit()
        
    def mensajeEstadoTabla(self, mensaje:str):
        self.tbReporte.setRowCount(0)
        self.tbReporte.setRowCount(1) 
        self.addItemTable(0,0,mensaje)
        self.tbReporte.setSpan(0, 0, 1, self.tbReporte.columnCount())# Hacer que el mensaje ocupe toda la f
            
    def cargarTabla(self):
         # Método para cargar los datos en la tabla
        result = self.reporteServices.obtenerListaReporte(pagina=self.paginaActual, tam_pagina=10, tipo_orden="DESC", busqueda=self.busqueda)
        if not result["success"]:
            self.mensajeEstadoTabla('Error de conexion.')
            return
        
        listaReporte = result["data"]["listaReportes"]
        if len(listaReporte) == 0:
            self.mensajeEstadoTabla('No se encontraron registros que coincidan con la busqueda.' if self.busqueda else 'No hay registros.')
            return

        paginaActual    = result["data"]["pagina_actual"]
        tamPagina       = result["data"]["tam_pagina"]
        totalPaginas    = result["data"]["total_paginas"]
        totalRegistros  = result["data"]["total_registros"]
                
        self.actualizarLabelPagina(paginaActual, totalPaginas)
        self.actualizarBtnPagina(paginaActual, totalPaginas)
        
        self.tbReporte.setRowCount(0)
        for index, reporte in enumerate(listaReporte):  # Iterar sobre la lista de perfiles
            self.tbReporte.insertRow(index)# Insertar una nueva fila en la tabla
            self.tbReporte.setRowHeight(index, 45) # Establecer la altura de la fila
            # Agregar los datos del perfil a la tabla
            self.addItemTable(index, 0, str(reporte['nombre_empleado'])) 
            self.addItemTable(index, 1, format_Fecha(reporte["reporte"].fecha_generacion))
            self.addItemTable(index, 2, reporte["reporte"].tipo_reporte)
            self.addItemTable(index, 3, reporte["reporte"].contenido)

            layout = QHBoxLayout()
            layout.addWidget(self.crearBtnAccion('Editar','btneditar',reporte["reporte"].id,self.editarReporte))
            layout.addSpacing(15)
            layout.addWidget(self.crearBtnAccion('Eliminar','btneliminar',reporte["reporte"].id,self._eliminarRegistro))

            button_widget = QWidget()
            button_widget.setLayout(layout)
            layout.setContentsMargins(10, 0, 10,0)
            self.tbReporte.setCellWidget(index, 4, button_widget)
            
    def crearBtnAccion(self,text:str,objectName:str,id_empleado:int,functionAction):
        boton = QPushButton(text,parent=self.tbReporte)
        boton.setObjectName(objectName)
        boton.setMinimumSize(QSize(80,35))
        boton.setMaximumWidth(100)
        boton.clicked.connect(lambda: functionAction(id_empleado))
        return boton
    
    def addItemTable(self,row, colum,dato):
        dato_item = QTableWidgetItem(dato)
        dato_item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)  # No editable
        self.tbReporte.setItem(row, colum, dato_item)

    def actualizarLabelPagina(self, paginaActual, totalPaginas):
        self.lblNumPagina.setText(f"Página {paginaActual} de {totalPaginas} páginas.")

    def actualizarBtnPagina(self, paginaActual, totalPaginas):
        self.paginaActual = paginaActual
        self.ultimaPagina = totalPaginas
        self.btnSiguiente.setEnabled(paginaActual < totalPaginas)
        self.btnUltimaPagina.setEnabled(paginaActual < totalPaginas)
        self.btnPrimerPagina.setEnabled(paginaActual > 1)
        self.btnAnterior.setEnabled(paginaActual > 1)

    def buscarRegistro(self):
        input_busqueda = self.inputBuscar.text()
        if input_busqueda:
            self.busqueda = input_busqueda
            self.cargarTabla()
            self.busqueda = None
        else:
            self.paginaActual = 1
            self.cargarTabla()
        
    def crearReporte(self):
        reporteForm = GenerarReporte()
        reporteForm.exec()
        # reporte_form = formReporte()
        # reporte_form.exec()
        self.cargarTabla()

    def _eliminarRegistro(self, id_reporte):
        dial = DialogoEmergente(
            title="Confirmación",
            message="¿Seguro que quieres eliminar este registro?",
            Icono="Question",
            show_accept_button=True,
            show_cancel_button=True
        )
        if dial.exec() == QDialog.Accepted:
                result = self.reporteServices.eliminarReporte(id_reporte)
                if result["success"]:
                    dial = DialogoEmergente("","Se elimino el registro correctamente.","Check")
                    dial.exec()
                    self.cargarTabla()
                else:
                    dial = DialogoEmergente("","Hubo un error al eliminar este registro.","Error")
                    dial.exec()
                    
                    
    def editarReporte(self, id_reporte):
        reporte_form = formReporte(id=id_reporte)# Abrir el formulario de edición
        reporte_form.exec()
        self.cargarTabla()

    def _irPrimeraPagina(self):
        self.paginaActual = 1
        self.cargarTabla()

    def _irAnteriorPagina(self):
        if self.paginaActual > 1:
            self.paginaActual -= 1
            self.cargarTabla()

    def _irSiguientePagina(self):
        if self.paginaActual < self.ultimaPagina:
            self.paginaActual += 1
            self.cargarTabla()

    def _irUltimaPagina(self):
        self.paginaActual = self.ultimaPagina
        self.cargarTabla()
