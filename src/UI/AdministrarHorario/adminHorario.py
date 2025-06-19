from PySide6.QtWidgets import *
from PySide6.QtCore import *
from Utils.Utils import *
from UI.AdministrarHorario.formHorario import *
from services.horarioService import *
from datetime import datetime


class AdminHorario(QWidget):
    cerrar_adminH = Signal()
    paginaActual = 1
    ultimaPagina = 1
    busqueda = None
    Hservices = HorarioService()

    def __init__(self, parent=None,permiso = None) -> None:
        super().__init__(parent)
        self.permisoUsuario = permiso
        
        self.setObjectName("admin")

        # add_Style(carpeta="css", archivoQSS="adminHorario.css", QObjeto=self)
        cargar_estilos("claro", "admin.css", self)

        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)

        frame = QFrame()
        self.layoutFrame = QVBoxLayout()
        self.layoutFrame.setContentsMargins(0, 0, 0, 0)
        self.layoutFrame.setSpacing(0)

        # Título
        titulo = QLabel(text="Administrar Horarios")
        titulo.setObjectName("titulo")
        titulo.setMinimumHeight(50)
        titulo.setAlignment(Qt.AlignCenter)
        self.layoutFrame.addWidget(titulo)

        layoutTop = QHBoxLayout()
        layoutTop.setContentsMargins(30, 30, 30, 30)
        layoutTop.setSpacing(5)
        layoutTop.setAlignment(Qt.AlignCenter)
        minimoTamBtn = QSize(130, 50)

        # Botones superiores
        self.btnCerrar = QPushButton(text="Cerrar")
        self.btnCerrar.setFixedSize(minimoTamBtn)
        self.btnCerrar.setCursor(Qt.PointingHandCursor)
        self.btnCerrar.clicked.connect(self._cerrar)
        Sombrear(self.btnCerrar, 20, 0, 0)

        self.inputBuscar = QLineEdit()
        self.inputBuscar.setClearButtonEnabled(True)
        self.inputBuscar.setPlaceholderText(
            "Buscar horario por días o tipo de jornada."
        )
        self.inputBuscar.setFixedSize(QSize(500, 30))
        self.inputBuscar.textChanged.connect(self._cargar_tabla)
        Sombrear(self.inputBuscar, 20, 0, 0)

        self.btnBuscar = QPushButton(text="Buscar")
        self.btnBuscar.setCursor(Qt.PointingHandCursor)
        self.btnBuscar.setFixedSize(minimoTamBtn)
        self.btnBuscar.clicked.connect(self._buscarHorario)
        Sombrear(self.btnBuscar, 20, 0, 0)

        self.btnCrear = QPushButton(text="Crear")
        self.btnCrear.setCursor(Qt.PointingHandCursor)
        self.btnCrear.setFixedSize(minimoTamBtn)
        self.btnCrear.setObjectName("crear")
        self.btnCrear.clicked.connect(self._crear_horario)
        Sombrear(self.btnCrear, 20, 0, 0)

        # Agregar botones superiores
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

        # Tabla de horarios
        self.tbHorario = QTableWidget()
        if self.tbHorario.columnCount() < 8:
            self.tbHorario.setColumnCount(8)

        header_labels = [
            "Horario",
            "Rol",
            "Días",
            "Joranada",
            "Hora Inicio",
            "Hora Fin",
            "Descripción",
            "Acciones",
        ]
        self.tbHorario.setHorizontalHeaderLabels(header_labels)

        self.tbHorario.horizontalHeader().setFixedHeight(40)
        self.tbHorario.verticalHeader().setVisible(False)
        self.tbHorario.horizontalHeader().setStretchLastSection(True)
        self.tbHorario.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        Sombrear(self.tbHorario, 30, 0, 0)

        layoutTb = QHBoxLayout()
        layoutTb.setContentsMargins(70, 40, 70, 40)
        layoutTb.addWidget(self.tbHorario)
        self.layoutFrame.addLayout(layoutTb)

        # Botones de paginación
        layoutButtom = QHBoxLayout()
        layoutButtom.setAlignment(Qt.AlignCenter)
        layoutButtom.setContentsMargins(10, 10, 10, 40)
        layoutButtom.setSpacing(5)
        self.btnPrimerPagina = QPushButton(text="Primera Pagina")
        self.btnPrimerPagina.setFixedSize(minimoTamBtn)
        self.btnPrimerPagina.setCursor(Qt.PointingHandCursor)
        self.btnPrimerPagina.setEnabled(False)
        self.btnPrimerPagina.clicked.connect(self._irPrimeraPagina)
        Sombrear(self.btnPrimerPagina, 20, 0, 0)

        self.btnAnterior = QPushButton(text="Anterior")
        self.btnAnterior.setEnabled(False)
        self.btnAnterior.setCursor(Qt.PointingHandCursor)
        self.btnAnterior.setFixedSize(minimoTamBtn)
        self.btnAnterior.clicked.connect(self._irAnteriorPagina)
        Sombrear(self.btnAnterior, 20, 0, 0)

        self.lblNumPagina = QLabel(text="Pagina 0 de 0 paginas")
        self.lblNumPagina.setFixedSize(QSize(170, 40))
        self.lblNumPagina.setAlignment(Qt.AlignCenter)

        self.btnSiguiente = QPushButton(text="Siguiente")
        self.btnSiguiente.setCursor(Qt.PointingHandCursor)
        self.btnSiguiente.setEnabled(False)
        self.btnSiguiente.setFixedSize(minimoTamBtn)
        self.btnSiguiente.clicked.connect(self._irSiguientePagina)
        Sombrear(self.btnSiguiente, 20, 0, 0)

        self.btnUltimaPagina = QPushButton(text="Ultima Pagina")
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
        self.cerrar_adminH.emit()

    def _mostrar_mensaje_sin_datos(self, mensaje: str):
        self.tbHorario.setRowCount(0)
        if self.tbHorario.rowCount() == 0:
            self.tbHorario.setRowCount(1)
            item = QTableWidgetItem(mensaje)
            item.setTextAlignment(Qt.AlignCenter)
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.tbHorario.setItem(0, 0, item)
            if self.tbHorario.columnCount() > 0:
                self.tbHorario.setSpan(0, 0, 1, self.tbHorario.columnCount())

    def _cargar_tabla(self):

        self.tbHorario.setRowCount(0)
        result = self.Hservices.obtenerListaHorarios(
            pagina=self.paginaActual,
            tam_pagina=10,
            tipo_orden="DESC",
            busqueda=self.busqueda,
        )
        if result["success"]:
            listaHorarios = result["data"]["listaHorarios"]
            if listaHorarios:
                paginaActual = result["data"]["pagina_actual"]
                totalPaginas = result["data"]["total_paginas"]
                self._actualizar_lblPagina(paginaActual, totalPaginas)
                self._actualizarValoresPaginado(paginaActual, totalPaginas)

                self.tbHorario.setRowCount(0)

                for index, horario in enumerate(listaHorarios):
                    self.tbHorario.insertRow(index)
                    self.tbHorario.setRowHeight(index, 45)

                    # Convertir hora_inicio y hora_fin a cadenas de texto (si es necesario)
                    hora_inicio_str = str(horario["hora_inicio"])
                    hora_fin_str = str(horario["hora_fin"])

                    # Agrega los datos a la tabla
                    self.addItem_a_tabla(index, 0, horario["nombre_horario"])
                    self.addItem_a_tabla(index, 1, horario.get("nombre_rol", "Sin rol"))
                    self.addItem_a_tabla(index, 2, horario["dias_semanales"])
                    self.addItem_a_tabla(index, 3, horario["tipo_jornada"])
                    self.addItem_a_tabla(index, 4, hora_inicio_str)
                    self.addItem_a_tabla(index, 5, hora_fin_str)
                    self.addItem_a_tabla(index, 6, horario["descripcion"])
                    self._agregar_acciones(index, horario["id"])
            else:
                self._mostrar_mensaje_sin_datos("No hay registros")
        else:
            self._mostrar_mensaje_sin_datos("Error de conexión")

    def addItem_a_tabla(self, row, colum, dato):
        dato_item = QTableWidgetItem(dato)
        dato_item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.tbHorario.setItem(row, colum, dato_item)

    def _agregar_acciones(self, index, horario_id):
        btnEliminar = QPushButton(text="Eliminar")
        btnEliminar.clicked.connect(
            lambda checked, idx=horario_id: self._eliminarRegistro(idx)
        )
        btnEliminar.setMinimumSize(QSize(80, 35))
        btnEliminar.setMaximumWidth(100)
        btnEliminar.setStyleSheet(
            "QPushButton{background-color:#ff5151;color:white;} QPushButton::hover{background-color:#ff0000;color:white;}"
        )

        btnEditar = QPushButton("Editar")
        btnEditar.clicked.connect(
            lambda checked, idx=horario_id: self._editar_horario(idx)
        )
        btnEditar.setMinimumSize(QSize(80, 35))
        btnEditar.setMaximumWidth(100)
        btnEditar.setStyleSheet(
            "QPushButton{background-color:#00b800;color:white;} QPushButton::hover{background-color:#00a800;color:white;}"
        )

        button_widget = QWidget()
        layout = QHBoxLayout(button_widget)
        layout.addWidget(btnEditar)
        layout.addSpacing(15)
        layout.addWidget(btnEliminar)
        layout.setContentsMargins(10, 0, 10, 0)
        self.tbHorario.setCellWidget(index, 7, button_widget)

    def _actualizar_lblPagina(self, numPagina, totalPagina):
        self.lblNumPagina.setText(f"Pagina {numPagina} de {totalPagina} ")

    def _actualizarValoresPaginado(self, paginaActual, totalPaginas):
        self.paginaActual = paginaActual
        self.ultimaPagina = totalPaginas
        self.btnPrimerPagina.setEnabled(paginaActual > 1)
        self.btnAnterior.setEnabled(paginaActual > 1)
        self.btnSiguiente.setEnabled(paginaActual < totalPaginas)
        self.btnUltimaPagina.setEnabled(paginaActual < totalPaginas)

    def _irPrimeraPagina(self):
        self.paginaActual = 1
        self._cargar_tabla()

    def _irUltimaPagina(self):
        self.paginaActual = self.ultimaPagina
        self._cargar_tabla()

    def _irSiguientePagina(self):
        if self.paginaActual < self.ultimaPagina:
            self.paginaActual += 1
            self._cargar_tabla()

    def _irAnteriorPagina(self):
        if self.paginaActual > 1:
            self.paginaActual -= 1
            self._cargar_tabla()

    def _buscarHorario(self):
        input_busqueda = self.inputBuscar.text()
        self.busqueda = input_busqueda if input_busqueda else None
        self.paginaActual = 1
        self._cargar_tabla()

    def _eliminarRegistro(self, idx):
        dial = DialogoEmergente(
            "¿?", "¿Seguro que quieres eliminar este registro?", "Question", True, True
        )
        if dial.exec() == QDialog.Accepted:
            result = self.Hservices.eliminarHorario(idx)
            mensaje = (
                "Se eliminó el registro correctamente."
                if result["success"]
                else "Hubo un error al eliminar este registro."
            )
            DialogoEmergente(
                "", mensaje, "Check" if result["success"] else "Error"
            ).exec()
            self._cargar_tabla()

    def _crear_horario(self):
        blur_effect = QGraphicsBlurEffect(self)
        blur_effect.setBlurRadius(10)
        self.setGraphicsEffect(blur_effect)

        form = formHorario()
        if (
            form.exec() == QDialog.Accepted
        ):  # Verifica si el formulario se cerró correctamente
            self._cargar_tabla()
        self.setGraphicsEffect(None)

    def _editar_horario(self, id):
        form = formHorario(titulo="Actualizar Horario", id=id)
        form.exec()
        self._cargar_tabla()
