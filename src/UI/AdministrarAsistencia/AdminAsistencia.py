from PySide6.QtWidgets import QMessageBox
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from Utils.Utils import *
from UI.AdministrarAsistencia.formAsistencia import *
from services.asistenciaService import *
from services.empleadoServices import *
import locale
from datetime import datetime

from settings.config import *

from settings.config import *

class AdminAsistencia(QWidget):
    cerrar_adminA = Signal()
    paginaActual = 1
    ultimaPagina = 1
    busqueda = None
    asistenciaServices = AsistenciaServices()
    empleadoServices = EmpleadoServices()

    def __init__(self, parent=None, permiso = None) -> None:
        super().__init__(parent)
        self.setObjectName("admin")
        self.permisoUsuario = permiso

        cargar_estilos("claro", "admin.css", self)

        # layout = QBoxLayout()
        layout = QBoxLayout(QBoxLayout.TopToBottom)
        layout.setContentsMargins(10, 10, 10, 10)

        frame = QFrame()
        self.layoutFrame = QVBoxLayout()
        self.layoutFrame.setContentsMargins(0, 0, 0, 0)
        self.layoutFrame.setSpacing(0)

        titulo = QLabel(text="Administrar asistencias")
        titulo.setObjectName("titulo")
        titulo.setMinimumHeight(50)
        titulo.setAlignment(Qt.AlignCenter)
        self.layoutFrame.addWidget(titulo)

        layoutTop = QHBoxLayout()
        layoutTop.setContentsMargins(30, 30, 30, 30)
        layoutTop.setSpacing(5)
        layoutTop.setAlignment(Qt.AlignCenter)
        minimoTamBtn = QSize(120, 40)

        ##botones de arriba
        self.btnCerrar = QPushButton(text="Cerrar")
        self.btnCerrar.setFixedSize(minimoTamBtn)
        self.btnCerrar.setCursor(Qt.PointingHandCursor)
        self.btnCerrar.clicked.connect(self._cerrar)
        Sombrear(self.btnCerrar, 20, 0, 0)

        self.inputBuscar = QLineEdit()
        self.inputBuscar.setClearButtonEnabled(True)
        self.inputBuscar.setPlaceholderText("Buscar asistencia por empleado.")
        self.inputBuscar.setFixedSize(QSize(500, 30))
        self.inputBuscar.textChanged.connect(self._cargar_tabla)
        Sombrear(self.inputBuscar, 20, 0, 0)

        self.btnBuscar = QPushButton(text="Buscar")
        self.btnBuscar.setCursor(Qt.PointingHandCursor)
        self.btnBuscar.setFixedSize(minimoTamBtn)
        self.btnBuscar.clicked.connect(
            self._buscarEmpleado
        )  ##revicen que el metonod _buscarPermisos haga bien su trabajp
        Sombrear(self.btnBuscar, 20, 0, 0)

        self.btnCrear = QPushButton(text="Crear")
        self.btnCrear.setCursor(Qt.PointingHandCursor)
        self.btnCrear.setFixedSize(minimoTamBtn)
        self.btnCrear.setObjectName("crear")
        self.btnCrear.clicked.connect(self._crear_asistencia)  ##esto no se mueve
        Sombrear(self.btnCrear, 20, 0, 0)
        
        self.btnActualizar = QPushButton(text="Actualizar")
        self.btnActualizar.setCursor(Qt.PointingHandCursor)
        self.btnActualizar.setFixedSize(minimoTamBtn)
        self.btnActualizar.setObjectName("crear")
        self.btnActualizar.clicked.connect(self.actualizarAsistencias)  ##esto no se mueve
        Sombrear(self.btnActualizar, 20, 0, 0)

        ##acomodando botones de arriba en el layout
        layoutTop.addSpacing(25)
        layoutTop.addWidget(self.btnCerrar, 1)
        layoutTop.addStretch(1)
        layoutTop.addWidget(self.inputBuscar, 2)
        layoutTop.addSpacing(10)
        layoutTop.addWidget(self.btnBuscar, 2)
        layoutTop.addStretch(1)
        layoutTop.addWidget(self.btnCrear, 2)
        layoutTop.addStretch(1)
        layoutTop.addWidget(self.btnActualizar, 2)
        layoutTop.addStretch(5)
        self.layoutFrame.addLayout(layoutTop)

        # Tabla Rol
        self.tbAsistencia = QTableWidget()  # Crea la tabla para mostrar los perfiles
        if self.tbAsistencia.columnCount() < 4:  # Si la tabla no tiene 3 columnas
            self.tbAsistencia.setColumnCount(4)  # Establece 3 columnas
        header_labels = ["Empleado", "Fecha", "Estado Asistencia", "Acciones"]
        self.tbAsistencia.setHorizontalHeaderLabels(header_labels)

        self.tbAsistencia.horizontalHeader().setFixedHeight(
            40
        )  # Establece una altura fija para los encabezados
        self.tbAsistencia.verticalHeader().setVisible(
            False
        )  # Oculta los encabezados verticales
        self.tbAsistencia.horizontalHeader().setStretchLastSection(
            True
        )  # Hace que la última sección de la tabla se estire
        self.tbAsistencia.setSelectionMode(
            QAbstractItemView.SelectionMode.NoSelection
        )  # Deshabilita la selección de filas
        Sombrear(self.tbAsistencia, 30, 0, 0)

        # Layout para la tabla
        layoutTb = QHBoxLayout()
        layoutTb.setContentsMargins(70, 40, 70, 40)
        layoutTb.addWidget(self.tbAsistencia)
        self.layoutFrame.addLayout(layoutTb)

        # Layout para los botones de paginación
        layoutButtom = (
            QHBoxLayout()
        )  # Crea un layout horizontal para los botones de paginación
        layoutButtom.setAlignment(Qt.AlignCenter)  # Centra los botones en el layout
        layoutButtom.setContentsMargins(
            10, 10, 10, 40
        )  # Establece márgenes alrededor de los botones
        layoutButtom.setSpacing(5)  # Define el espacio entre los botones

        # Botón para ir a la primera página
        self.btnPrimerPagina = QPushButton(text="Primera Página.")
        self.btnPrimerPagina.setFixedSize(minimoTamBtn)
        self.btnPrimerPagina.setCursor(
            Qt.PointingHandCursor
        )  # Cambia el cursor al pasar sobre el botón
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

        self.layoutFrame.addLayout(
            layoutButtom
        )  # Añadir el layout de los botones al layout principal
        frame.setLayout(self.layoutFrame)  # Establecer el layout del frame principal
        layout.addWidget(frame)  # Añadir el frame al layout principal
        self.setLayout(layout)  # Establecer el layout del widget
        Sombrear(self, 30, 0, 0)
        self._cargar_tabla()

    def _cerrar(self):
        # Emitir una señal para cerrar la ventana
        self.cerrar_adminA.emit()

    def _mostrar_mensaje_sin_datos(self):
        # Si la tabla está vacía, agregar una fila con el mensaje "Sin datos"
        self.tbAsistencia.setRowCount(0)
        if self.tbAsistencia.rowCount() == 0:  # Si no hay filas
            self.tbAsistencia.setRowCount(
                1
            )  # Establecer una fila para mostrar el mensaje
            item = QTableWidgetItem("Sin datos")
            item.setTextAlignment(Qt.AlignCenter)
            self.tbAsistencia.setItem(
                0, 0, item
            )  # Establecer el item en la primera celda
            for col in range(1, self.tbAsistencia.columnCount()):
                self.tbAsistencia.setItem(0, col, QTableWidgetItem(""))  # Celdas vacías
            self.tbAsistencia.setSpan(
                0, 0, 1, self.tbAsistencia.columnCount()
            )  # Hacer que el mensaje ocupe toda la f

    def _cargar_tabla(self):
        # Método para cargar los datos en la tabla
        result = self.asistenciaServices.obtenerListaAsistencia(
            pagina=self.paginaActual,
            tam_pagina=10,
            tipo_orden="DESC",
            busqueda=self.busqueda,
        )
        if result["success"]:
            listaAsistencias = result["data"][
                "listaAsistencias"
            ]  # Obtener la lista de perfiles
            if len(listaAsistencias) > 0:
                paginaActual = result["data"]["pagina_actual"]
                tamPagina = result["data"]["tam_pagina"]
                totalPaginas = result["data"]["total_paginas"]
                totalRegistros = result["data"]["total_registros"]

                self._actualizar_lblPagina(paginaActual, totalPaginas)
                self._actualizarValoresPaginado(paginaActual, totalPaginas)

                self.tbAsistencia.setRowCount(0)
                print("🔍 Datos recibidos en _cargar_tabla:")
                for asistencia in listaAsistencias:
                    print(
                        f"- Nombre: {asistencia['nombre_empleado']}, Fecha: {asistencia['asistencia'].fecha}, Estado: {asistencia['asistencia'].estado_asistencia}"
                    )
                for index, asistencia in enumerate(
                    listaAsistencias
                ):  # Iterar sobre la lista de perfiles
                    self.tbAsistencia.insertRow(
                        index
                    )  # Insertar una nueva fila en la tabla
                    self.tbAsistencia.setRowHeight(
                        index, 45
                    )  # Establecer la altura de la fila

                    # Agregar los datos del perfil a la tabla
                    
                    self.addItem_a_tabla(index, 0, str(asistencia["nombre_empleado"]))
                    self.addItem_a_tabla(index, 1, asistencia["asistencia"].fecha.strftime("%Y-%m-%d"))  # Formatear fecha
                    self.addItem_a_tabla(index, 2, asistencia["asistencia"].estado_asistencia)  # Agregar el nombre del perfil a la columna 0

                    # Botones para editar y eliminar
                    btnEliminar = QPushButton("Eliminar")
                    btnEliminar.clicked.connect(
                        lambda checked, idx=asistencia[
                            "asistencia"
                        ].id: self._eliminarRegistro(idx)
                    )
                    btnEliminar.setMinimumSize(
                        QSize(80, 35)
                    )  # Establecer el tamaño mínimo del botón
                    btnEliminar.setStyleSheet(
                        """   QPushButton{background-color:#ff5151;color:white;}
                                                    QPushButton::hover{background-color:#ff0000;color:white;}
                                              """
                    )  # Estilo del botón

                    btnEditar = QPushButton("Editar")
                    btnEditar.clicked.connect(
                        lambda checked, idx=asistencia[
                            "asistencia"
                        ].id: self._editar_Asistencia(idx)
                    )
                    btnEditar.setMinimumSize(QSize(80, 35))
                    btnEditar.setStyleSheet(
                        """ QPushButton{background-color:#00b800;color:white;}
                                                QPushButton::hover{background-color:#00a800;color:white;}
                                            """
                    )

                    button_widget = QWidget()
                    button_widget.setStyleSheet("background-color:transparent;")
                    layout = QHBoxLayout()
                    layout.addWidget(btnEditar)
                    layout.addSpacing(15)
                    layout.addWidget(btnEliminar)
                    button_widget.setLayout(layout)
                    layout.setContentsMargins(10, 0, 10, 0)

                    self.tbAsistencia.setCellWidget(index, 3, button_widget)
            else:
                self._mostrar_mensaje_sin_datos()
        else:
            self._mostrar_mensaje_sin_datos()

    def addItem_a_tabla(self, row, colum, dato):
        dato_item = QTableWidgetItem(dato)
        dato_item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)  # No editable
        self.tbAsistencia.setItem(row, colum, dato_item)

    def _actualizar_lblPagina(self, paginaActual, totalPaginas):
        self.lblNumPagina.setText(f"Página {paginaActual} de {totalPaginas} páginas.")

    def _actualizarValoresPaginado(self, paginaActual, totalPaginas):
        self.paginaActual = paginaActual
        self.ultimaPagina = totalPaginas
        self.btnSiguiente.setEnabled(paginaActual < totalPaginas)
        self.btnUltimaPagina.setEnabled(paginaActual < totalPaginas)
        self.btnPrimerPagina.setEnabled(paginaActual > 1)
        self.btnAnterior.setEnabled(paginaActual > 1)

    def _buscarEmpleado(self):
        self.busqueda = self.inputBuscar.text()
        self.paginaActual = 1
        self._cargar_tabla()

    def _crear_asistencia(self):
        blur_effect = QGraphicsBlurEffect(self)
        blur_effect.setBlurRadius(10)
        self.setGraphicsEffect(blur_effect)
        asistencia_form = formAsistencia()
        asistencia_form.exec()
        self._cargar_tabla()
        self.setGraphicsEffect(None)

    def _eliminarRegistro(self, id_asistencia):
        dial = DialogoEmergente(
            "¿Seguro que quieres eliminar este registro?", "Question", True, True
        )
        if dial.exec() == QDialog.Accepted:
            result = self.asistenciaServices.eliminarAsistencia(id_asistencia)
            if result["success"]:
                dial = DialogoEmergente(
                    "", "Se elimino el registro correctamente.", "Check"
                )
                dial.exec()
                self._cargar_tabla()
            else:
                dial = DialogoEmergente(
                    "", "Hubo un error al eliminar este registro.", "Error"
                )
                dial.exec()

    def _editar_Asistencia(self, id_asistencia):
        blur_effect = QGraphicsBlurEffect(self)
        blur_effect.setBlurRadius(10)
        self.setGraphicsEffect(blur_effect)  # Aplicar efecto de desenfoque
        asistencia_form = formAsistencia(
            id=id_asistencia
        )  # Abrir el formulario de edición
        asistencia_form.exec()
        self._cargar_tabla()
        self._cargar_tabla()
        self.setGraphicsEffect(None)  # Quitar el efecto de desenfoque

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
        
    def actualizarAsistencias(self):
        result = self.asistenciaServices.registrarAsistenciaEmpleado()
        print(result)
        self._cargar_tabla()