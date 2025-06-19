from PySide6.QtWidgets import *
from PySide6.QtCore import *
from Utils.Utils import cargar_estilos, Sombrear, format_Fecha
from UI.AdministrarEmpleado.formEmpleado import formEmpleado
from UI.AdministrarEmpleado.imformacionEmpleado import informacionEmpleado
from UI.DialogoEmergente import DialogoEmergente
from services.empleadoServices import EmpleadoServices
from services.huellaService import HuellaService
from services.ZKService        import ZKServices 
from models.persona import Persona
from datetime import datetime

class AdminEmpleado(QWidget):
    signalCerrar = Signal()
    paginaActual = 1
    ultimaPagina = 1
    busqueda = None
    EmpServices = EmpleadoServices()
    HueServices = HuellaService()


    def __init__(self, parent= None, permiso= None) -> None:
        super().__init__(parent)
        self.setObjectName("admin")
        self.permisoUsuario = permiso
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

       
        self.inputBuscar = QLineEdit()
        self.inputBuscar.setClearButtonEnabled(True)
        self.inputBuscar.setPlaceholderText("Buscar persona por nombre, apellidos, cedula o correo.")
        self.inputBuscar.setFixedSize(QSize(500,30))
        self.inputBuscar.textChanged.connect(self.cargarTabla)
        Sombrear(self.inputBuscar,20,0,0)
        
        minimoTamBtn = QSize(120,40)
        ##acomodando botones de arriba en el layout
        layoutTop.addSpacing(25)
        layoutTop.addWidget(self.crearBoton("Cerrar",minimoTamBtn,self.cerrarAdminEmpleado))
        layoutTop.addStretch(1)
        layoutTop.addWidget(self.inputBuscar,2)
        layoutTop.addSpacing(10)
        layoutTop.addWidget(self.crearBoton("Buscar",minimoTamBtn,self.buscarPersona))
        layoutTop.addStretch(1)
        layoutTop.addWidget(self.crearBoton("Crear",minimoTamBtn,self.crearEmpleado))
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
        self.tbPersona.setColumnWidth(6, 305)  # La columna 6 tendrá un ancho fijo de 150 píxeles
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

        #label para mostrar la cantidad y el numero de pagina en el que se ubica
        self.lblNumPagina = QLabel(text="Pagina 0 de 0 paginas")
        self.lblNumPagina.setFixedSize(QSize(170,40))
        self.lblNumPagina.setAlignment(Qt.AlignCenter)

        #crear Botones de navegacion
        self.btnPrimerPagina= self.crearBoton("Primer pagina",minimoTamBtn,self._irPrimeraPagina,False)
        self.btnAnterior    = self.crearBoton("Anterior",minimoTamBtn,self._irAnteriorPagina,False)
        self.btnSiguiente   = self.crearBoton("Siguiente",minimoTamBtn,self._irSiguientePagina,False)
        self.btnUltimaPagina= self.crearBoton("Ultima pagina",minimoTamBtn,self._irUltimaPagina,False)
        
        #acomoda los botones del layout
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

    def crearBoton(self,text:str,fixedSize:QSize, functionConnect,enable:bool = True,cursorType=Qt.PointingHandCursor)->QPushButton:
        boton = QPushButton(text)
        boton.setEnabled(enable)
        boton.setFixedSize(fixedSize)
        boton.setCursor(cursorType)
        boton.clicked.connect(functionConnect)
        Sombrear(boton,20,0,0)
        return boton

    def cerrarAdminEmpleado(self):
        self.signalCerrar.emit()

    def mensajeEstadoTabla(self,mensaje:str):
        self.tbPersona.setRowCount(0)
        self.tbPersona.setRowCount(1) 
        self.addItemTable(0,0,mensaje)
        self.tbPersona.setSpan(0, 0, 1, self.tbPersona.columnCount())

    def cargarTabla(self): 
        result = self.EmpServices.listar_empleados(pagina=self.paginaActual,tam_pagina=10,tipo_orden="DESC",busqueda=self.busqueda)
        if not result["success"]:
            self.mensajeEstadoTabla("Error de conexión.")
            return
        
        listaPersona = result["data"]["listaPersonas"]
        if len(listaPersona) == 0:
            self.mensajeEstadoTabla("No hay registros." if self.busqueda is None else "No se encontraron registros que coincidan con la busqueda.")  
            return 

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
            self.tbPersona.insertRow(index)
            self.tbPersona.setRowHeight(index,45)

            id_empleado     = data['id_empleado']
            persona:Persona = data['persona']

            self.addItemTable(index,0,f'{persona.nombre} {persona.apellidos}')
            self.addItemTable(index,1,persona.cedula)
            self.addItemTable(index,2,persona.correo)
            self.addItemTable(index,3,format_Fecha(str(persona.fecha_nacimiento)))
            self.addItemTable(index,4,persona.estado_civil)
            self.addItemTable(index,5,persona.direccion)

            #contenedor de los botones.
            layout = QHBoxLayout()
            layout.addWidget(self.crearBtnAccion('Mas info','btnInfo',id_empleado,self.verMasInformacion))
            layout.addSpacing(15)
            layout.addWidget(self.crearBtnAccion('Editar','btneditar',id_empleado,self.editarEmpleado))
            layout.addSpacing(15)
            layout.addWidget(self.crearBtnAccion('Eliminar','btneliminar',id_empleado,self.eliminarEmpleado))
            layout.setContentsMargins(10, 0, 10,0)
            #widget para el layout de los botones.
            button_widget = QWidget()
            button_widget.setFixedWidth(300)
            button_widget.setLayout(layout)
            self.tbPersona.setCellWidget(index, 6, button_widget) 
    
    def addItemTable(self,row, colum,dato):
        dato_item = QTableWidgetItem(dato)
        dato_item.setTextAlignment(Qt.AlignCenter)
        dato_item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)  # No editable
        self.tbPersona.setItem(row, colum, dato_item)

    def crearBtnAccion(self,text:str,objectName:str,id_empleado:int,functionAction):
        boton = QPushButton(text,parent=self.tbPersona)
        boton.setObjectName(objectName)
        boton.setMinimumSize(QSize(80,35))
        boton.setMaximumWidth(100)
        boton.clicked.connect(lambda: functionAction(id_empleado))
        return boton

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
        print(f'\n\neliminar id {id_empleado}\n\n')
        inf = informacionEmpleado(id_empleado)
        inf.exec()

<<<<<<< HEAD

    def obtenerHuella(self, id_empleado: int):
        result = self.HueServices.buscar_huellas_por_empleado(id_empleado)

        if not result["success"]:
            dial = DialogoEmergente("", "Error al obtener la huella del empleado.", "Error", True)
            dial.exec()
            return None

        if result["exists"]:
            return result["id_huella"]  # Retorna el ID de la huella
        else:
            return None

<<<<<<< HEAD
    def eliminarEmpleado(self, id_empleado: int, nombre_completo: str):
        texto = f"Se eliminarán todos los datos asociados a este empleado."
=======
    def eliminarEmpleado(self, id_empleado:int):
        texto = "Se eliminaran todos los datos asociados a este empleado."
>>>>>>> parent of 373e4d9 (17-5-2025 (Todos))
=======
    def eliminarEmpleado(self, id_empleado: int):
        texto = "Se eliminarán todos los datos asociados a este empleado."
>>>>>>> parent of bc060e5 (Correcciones)
        texto += "\n¿Quieres eliminar este empleado?"
        dial = DialogoEmergente("¡Advertencia!", texto, "Warning", True, True)

        if dial.exec() == QDialog.Accepted:
            # Obtener la huella del empleado antes de eliminarlo
            id_huella = self.obtenerHuella(id_empleado)
<<<<<<< HEAD
                        # Si el empleado fue eliminado, eliminar su huella si existe prueba
            if id_huella is not None:
                result_huella = self.HueServices.eliminarHuella(id_huella)
                if not result_huella['success']:
                    dial = DialogoEmergente("", "Empleado eliminado, pero no se pudo eliminar la huella.", "Error", True)
                    dial.exec()
=======
>>>>>>> parent of bc060e5 (Correcciones)
            zk_service = ZKServices()
            zk_service.eliminar_huella(id_huella)


            # Eliminar al empleado
            result = self.EmpServices.eliminar_empleado(id_empleado)

            if not result['success']:
                dial = DialogoEmergente("", result['message'], "Error", True)
                dial.exec()
                return

            # Si el empleado fue eliminado, eliminar su huella si existe
            if id_huella is not None:

                result_huella = self.HueServices.eliminarHuella(id_huella)
                if not result_huella['success']:
                    dial = DialogoEmergente("", "Empleado eliminado, pero no se pudo eliminar la huella.", "Error", True)
                    dial.exec()

            # Confirmación final
            dial = DialogoEmergente("", result['message'], "Check", True)
            dial.exec()

        self.cargarTabla()
    
    def editarEmpleado(self,id_empleado:int):
        print(f'\n\nEditar id {id_empleado}\n\n')
        form = formEmpleado(titulo='Editar empleado',id_empleado = id_empleado)
        form.finished.connect(form.deleteLater)
        form.exec()
        self.cargarTabla()

    def crearEmpleado(self):
        form = formEmpleado()
        form.finished.connect(form.deleteLater)
        form.exec()
        self.cargarTabla()