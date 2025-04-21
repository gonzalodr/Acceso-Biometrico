from PySide6.QtWidgets import *
from PySide6.QtCore import *
from Utils.Utils import *
from UI.AdministrarJustificacion.formJustificacion import *
from services.justificacionService import *
from functools import partial
from .infoJustificacion import InfoJustificacion
import locale
from datetime import datetime

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

        locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')

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
        if (self.tbJustificacion.columnCount() < 6):
            self.tbJustificacion.setColumnCount(6)  # Se añaden 2 columnas más
        header_labels = ["Motivo", "Descripción", "Empleado", "Asistencia", "Fecha Realizada", "Acciones"]
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

    def mostrar_info_justificacion(self, column, idx):
        if column == 5:  
            resultado = self.Pservices.obtenerJustificacionPorId(idx)  

            if resultado["success"] and resultado["exists"]:
                justificacion = resultado["justificacion"]  
                nombre_empleado = resultado["nombre_completo_empleado"]  
                fecha_asistencia = resultado["fecha_asistencia"] 
                

                dialog = InfoJustificacion(justificacion, nombre_empleado, fecha_asistencia, self)
                dialog.exec_()
            else:
                QMessageBox.warning(self, "Error", "No se encontró la justificación.")

    def _cerrar(self):
        self.cerrar_adminJ.emit()

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
                    
                    # Motivo
                    item_motivo = QTableWidgetItem(justificacion["motivo"])
                    item_motivo.setTextAlignment(Qt.AlignCenter)  
                    self.tbJustificacion.setItem(index, 0, item_motivo)

                    # Descripción
                    item_descripcion = QTableWidgetItem(justificacion["descripcion"])
                    item_descripcion.setTextAlignment(Qt.AlignCenter)  
                    self.tbJustificacion.setItem(index, 1, item_descripcion)

                    # Nombre del empleado
                    item_nombre_empleado = QTableWidgetItem(justificacion["nombre_completo_empleado"])
                    item_nombre_empleado.setTextAlignment(Qt.AlignCenter) 
                    self.tbJustificacion.setItem(index, 2, item_nombre_empleado)

                    # Fecha de asistencia
                    fecha_Asistencia = justificacion["fecha_asistencia"]
                    fecha_str = fecha_Asistencia.strftime("%d de %B del %Y")  # Cambiado a %d
                    dia = int(fecha_str.split(" ")[0])  # Convertir el día a entero para eliminar ceros a la izquierda
                    fecha_str = f"{dia} de {fecha_Asistencia.strftime('%B')} del {fecha_Asistencia.strftime('%Y')}"
                    item_fecha_Asistencia = QTableWidgetItem(fecha_str)
                    item_fecha_Asistencia.setTextAlignment(Qt.AlignCenter) 
                    self.tbJustificacion.setItem(index, 3, item_fecha_Asistencia)

                    # Fecha realizado
                    fecha_Realizado = justificacion["fecha_realizado"]
                    fecha_str = fecha_Realizado.strftime("%d de %B del %Y")  # Cambiado a %d
                    dia = int(fecha_str.split(" ")[0])  # Convertir el día a entero para eliminar ceros a la izquierda
                    fecha_str = f"{dia} de {fecha_Realizado.strftime('%B')} del {fecha_Realizado.strftime('%Y')}"
                    item_fecha_Realizado = QTableWidgetItem(fecha_str)
                    item_fecha_Realizado.setTextAlignment(Qt.AlignCenter)
                    self.tbJustificacion.setItem(index, 4, item_fecha_Realizado)

                    # Creación de un contenedor para los botones
                    contenedor_botones = QWidget()
                    layout_botones = QHBoxLayout()
                    layout_botones.setContentsMargins(0, 0, 0, 0)
                    layout_botones.setSpacing(5)

                    # Botón Más info
                    btnInfo = QPushButton("Más info")
                    btnInfo.clicked.connect(partial(self.mostrar_info_justificacion, 5, justificacion["id_justificacion"]))  # Cambia el índice según tu tabla
                    btnInfo.setStyleSheet("""
                        QPushButton{background-color:#D4D600;color:white;}  /* Yellow */
                        QPushButton::hover{background-color:#FFEA00;color:white;}
                    """)
                    btnInfo.setMinimumSize(QSize(80, 35))
                    
                    # Botón Editar
                    btnEditar = QPushButton("Editar")
                    btnEditar.clicked.connect(partial(self._editar_Justificacion, justificacion["id_justificacion"]))
                    btnEditar.setStyleSheet("""
                        QPushButton{background-color:#28A745;color:white;}  /* Green */
                        QPushButton::hover{background-color:#218838;color:white;}
                    """)
                    btnEditar.setMinimumSize(QSize(80, 35))

                    # Botón Eliminar
                    btnEliminar = QPushButton("Eliminar")
                    btnEliminar.clicked.connect(partial(self._eliminarRegistro, justificacion["id_justificacion"]))
                    btnEliminar.setStyleSheet("""
                        QPushButton{background-color:#DC3545;color:white;}  /* Red */
                        QPushButton::hover{background-color:#A71D2A;color:white;}
                    """)
                    btnEliminar.setMinimumSize(QSize(80, 35))

                    # Agregar botones al layout
                    layout_botones.addWidget(btnInfo)
                    layout_botones.addWidget(btnEditar)
                    layout_botones.addWidget(btnEliminar)


                    contenedor_botones.setLayout(layout_botones)


                    self.tbJustificacion.setCellWidget(index, 5, contenedor_botones)

            else:
                print("No se encontraron justificaciones.")  # Mensaje de depuración
                self.tbJustificacion.setRowCount(0)
                self._actualizar_lblPagina(0, 0)
                self._actualizarValoresPaginado(0, 0)
        else:
            print("Error al obtener justificaciones.")  # Mensaje de depuración
            self.tbJustificacion.setRowCount(0)
            self._actualizar_lblPagina(0, 0)
            self._actualizarValoresPaginado(0, 0)

    def _actualizar_lblPagina(self, numPagina, totalPagina):
        self.lblNumPagina.setText(f"Página {numPagina} de {totalPagina}")

    def _actualizarValoresPaginado(self, paginaActual, totalPaginas):
        self.paginaActual = paginaActual
        self.ultimaPagina = totalPaginas
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
        if (self.paginaActual + 1) <= self.ultimaPagina:
            self.paginaActual += 1
            self._cargar_tabla()

    def _irAnteriorPagina(self):
        if (self.paginaActual - 1) >= 1:
            self.paginaActual -= 1
            self._cargar_tabla()

    def _buscarJustificacion(self):
        input_busqueda = self.inputBuscar.text()
        if input_busqueda:
            self.busqueda = input_busqueda
            self._cargar_tabla()
            self.busqueda = None
        else:
            self.paginaActual = 1
            self._cargar_tabla()

    def _eliminarRegistro(self, idx):
        dial = DialogoEmergente("¿?", "¿Seguro que quieres eliminar este registro?", "Question", True, True)
        if dial.exec() == QDialog.Accepted:
            result = self.Pservices.eliminarJustificacion(idx)
            if result["success"]:
                dial = DialogoEmergente("", "Se eliminó el registro correctamente.", "Check")
                dial.exec()
                self._cargar_tabla()
            else:
                dial = DialogoEmergente("", "Hubo un error al eliminar este registro.", "Error")
                dial.exec()

    def _editar_Justificacion(self, id):
        blur_effect = QGraphicsBlurEffect(self)
        blur_effect.setBlurRadius(10)
        self.setGraphicsEffect(blur_effect)
        
        form = formJustificacion(titulo="Actualizar justificación", id=id)
        form.exec()
        
        self._cargar_tabla()
        self.setGraphicsEffect(None)

    def _crear_justificacion(self):
        blur_effect = QGraphicsBlurEffect(self)
        blur_effect.setBlurRadius(10)
        self.setGraphicsEffect(blur_effect)
        
        form = formJustificacion()
        form.exec()
        self._cargar_tabla()
        self.setGraphicsEffect(None)