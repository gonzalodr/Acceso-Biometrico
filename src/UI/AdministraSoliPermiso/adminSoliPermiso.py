from PySide6.QtWidgets import *
from PySide6.QtCore import *
from Utils.Utils import *
from UI.DialogoEmergente import DialogoEmergente
from services.solicitudPermisoService import SolicitudPermisoService
from datetime import datetime
from UI.AdministraSoliPermiso.formSoliPermiso import FormSolicitudPermisoAdmin


class AdminSoliPermiso(QWidget):
    cerrar_admin_soli_permiso = Signal()
    paginaActual = 1
    ultimaPagina = 1
    busqueda = None
    permiso_service = SolicitudPermisoService()

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("admin")
        cargar_estilos("claro", "admin.css", self)

        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)

        frame = QFrame()
        self.layoutFrame = QVBoxLayout()
        self.layoutFrame.setContentsMargins(0, 0, 0, 0)
        self.layoutFrame.setSpacing(0)

        # Título
        titulo = QLabel(text="Solicitudes de Permisos")
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
        self.inputBuscar.setPlaceholderText("Buscar por empleado o tipo de permiso")
        self.inputBuscar.setFixedSize(QSize(500, 30))
        # self.inputBuscar.textChanged.connect(self._cargar_tabla)
        Sombrear(self.inputBuscar, 20, 0, 0)

        self.btnBuscar = QPushButton(text="Buscar")
        self.btnBuscar.setCursor(Qt.PointingHandCursor)
        self.btnBuscar.setFixedSize(minimoTamBtn)
        self.btnBuscar.clicked.connect(self._buscarPermisos)
        Sombrear(self.btnBuscar, 20, 0, 0)

        self.btnCrear = QPushButton(text="Crear")
        self.btnCrear.setCursor(Qt.PointingHandCursor)
        self.btnCrear.setFixedSize(minimoTamBtn)
        self.btnCrear.setObjectName("crear")
        self.btnCrear.clicked.connect(self._crear_permiso)
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

        # Tabla de permisos
        self.tbPermisos = QTableWidget()
        if self.tbPermisos.columnCount() < 8:
            self.tbPermisos.setColumnCount(7)

        header_labels = [
            "Empleado",
            "Tipo Permiso",
            "Fecha Inicio",
            "Fecha Fin",
            "Descripción",
            "Estado",
            "Acciones",
        ]
        self.tbPermisos.setHorizontalHeaderLabels(header_labels)

        self.tbPermisos.horizontalHeader().setFixedHeight(40)
        self.tbPermisos.verticalHeader().setVisible(False)
        self.tbPermisos.horizontalHeader().setStretchLastSection(True)
        self.tbPermisos.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        Sombrear(self.tbPermisos, 30, 0, 0)

        layoutTb = QHBoxLayout()
        layoutTb.setContentsMargins(70, 40, 70, 40)
        layoutTb.addWidget(self.tbPermisos)
        self.layoutFrame.addLayout(layoutTb)

        # Botones de paginación (igual que en AdminHorario)
        layoutButtom = QHBoxLayout()
        layoutButtom.setAlignment(Qt.AlignCenter)
        layoutButtom.setContentsMargins(10, 10, 10, 40)
        layoutButtom.setSpacing(5)

        # ... (Mantén el mismo código de paginación que en AdminHorario)

        self.layoutFrame.addLayout(layoutButtom)
        frame.setLayout(self.layoutFrame)
        layout.addWidget(frame)
        self.setLayout(layout)
        Sombrear(self, 30, 0, 0)
        # self._cargar_tabla()

    def _cerrar(self):
        self.cerrar_admin_soli_permiso.emit()

    def _mostrar_mensaje_sin_datos(self, mensaje: str):
        self.tbPermisos.setRowCount(0)
        if self.tbPermisos.rowCount() == 0:
            self.tbPermisos.setRowCount(1)
            item = QTableWidgetItem(mensaje)
            item.setTextAlignment(Qt.AlignCenter)
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.tbPermisos.setItem(0, 0, item)
            if self.tbPermisos.columnCount() > 0:
                self.tbPermisos.setSpan(0, 0, 1, self.tbPermisos.columnCount())

    """def _cargar_tabla(self):
        self.tbPermisos.setRowCount(0)
        result = self.permiso_service.obtener_lista_permisos(
            pagina=self.paginaActual,
            tam_pagina=10,
            busqueda=self.busqueda,
        )

        if result["success"]:
            lista_permisos = result["data"]["lista_permisos"]
            if lista_permisos:
                paginaActual = result["data"]["pagina_actual"]
                totalPaginas = result["data"]["total_paginas"]
                self._actualizar_lblPagina(paginaActual, totalPaginas)
                self._actualizarValoresPaginado(paginaActual, totalPaginas)

                self.tbPermisos.setRowCount(0)

                for index, permiso in enumerate(lista_permisos):
                    self.tbPermisos.insertRow(index)
                    self.tbPermisos.setRowHeight(index, 45)

                    # Calcular días de diferencia
                    fecha_inicio = datetime.strptime(
                        permiso["fecha_inicio"], "%Y-%m-%d"
                    ).date()
                    fecha_fin = datetime.strptime(
                        permiso["fecha_fin"], "%Y-%m-%d"
                    ).date()
                    dias = (fecha_fin - fecha_inicio).days + 1

                    self.addItem_a_tabla(
                        index,
                        0,
                        f"{permiso['nombre_empleado']} {permiso['apellido_empleado']}",
                    )
                    self.addItem_a_tabla(index, 1, permiso["tipo"])
                    self.addItem_a_tabla(index, 2, permiso["fecha_inicio"])
                    self.addItem_a_tabla(index, 3, permiso["fecha_fin"])
                    self.addItem_a_tabla(index, 4, str(dias))
                    self.addItem_a_tabla(index, 5, permiso["descripcion"])
                    self.addItem_a_tabla(index, 6, permiso["estado"])
                    self._agregar_acciones(index, permiso["id"])
            else:
                self._mostrar_mensaje_sin_datos("No hay registros")
        else:
            self._mostrar_mensaje_sin_datos("Error de conexión")"""

    def addItem_a_tabla(self, row, colum, dato):
        dato_item = QTableWidgetItem(str(dato))
        dato_item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.tbPermisos.setItem(row, colum, dato_item)

    def _agregar_acciones(self, index, permiso_id):
        btnEliminar = QPushButton(text="Eliminar")
        btnEliminar.clicked.connect(
            lambda checked, idx=permiso_id: self._eliminarRegistro(idx)
        )
        btnEliminar.setMinimumSize(QSize(80, 35))
        btnEliminar.setMaximumWidth(100)
        btnEliminar.setStyleSheet(
            "QPushButton{background-color:#ff5151;color:white;} QPushButton::hover{background-color:#ff0000;color:white;}"
        )

        btnEditar = QPushButton("Editar")
        btnEditar.clicked.connect(
            lambda checked, idx=permiso_id: self._editar_permiso(idx)
        )
        btnEditar.setMinimumSize(QSize(80, 35))
        btnEditar.setMaximumWidth(100)
        btnEditar.setStyleSheet(
            "QPushButton{background-color:#00b800;color:white;} QPushButton::hover{background-color:#00a800;color:white;}"
        )

        btnAprobar = QPushButton("Aprobar")
        btnAprobar.clicked.connect(
            lambda checked, idx=permiso_id: self._cambiar_estado(idx, "Aprobado")
        )
        btnAprobar.setMinimumSize(QSize(80, 35))
        btnAprobar.setMaximumWidth(100)
        btnAprobar.setStyleSheet(
            "QPushButton{background-color:#0078d7;color:white;} QPushButton::hover{background-color:#006cbe;color:white;}"
        )

        button_widget = QWidget()
        layout = QHBoxLayout(button_widget)
        layout.addWidget(btnEditar)
        layout.addSpacing(5)
        layout.addWidget(btnAprobar)
        layout.addSpacing(5)
        layout.addWidget(btnEliminar)
        layout.setContentsMargins(10, 0, 10, 0)
        self.tbPermisos.setCellWidget(index, 7, button_widget)

    """def _cambiar_estado(self, id_permiso, estado):
        dial = DialogoEmergente(
            "Confirmación", f"¿Cambiar estado a {estado}?", "Question", True, True
        )
        if dial.exec() == QDialog.Accepted:
            result = self.permiso_service.cambiar_estado(id_permiso, estado)
            mensaje = (
                f"Estado cambiado a {estado} correctamente."
                if result["success"]
                else "Hubo un error al cambiar el estado."
            )
            DialogoEmergente(
                "", mensaje, "Check" if result["success"] else "Error"
            ).exec()
            self._cargar_tabla()"""

    # ... (Mantén los mismos métodos de paginación que en AdminHorario)

    def _buscarPermisos(self):
        input_busqueda = self.inputBuscar.text()
        self.busqueda = input_busqueda if input_busqueda else None
        self.paginaActual = 1
        # self._cargar_tabla()

    def _eliminarRegistro(self, idx):
        dial = DialogoEmergente(
            "¿?", "¿Seguro que quieres eliminar este registro?", "Question", True, True
        )
        if dial.exec() == QDialog.Accepted:
            result = self.permiso_service.eliminar_permiso(idx)
            mensaje = (
                "Se eliminó el registro correctamente."
                if result["success"]
                else "Hubo un error al eliminar este registro."
            )
            DialogoEmergente(
                "", mensaje, "Check" if result["success"] else "Error"
            ).exec()
            # self._cargar_tabla()

    def _crear_permiso(self):
        # blur_effect = QGraphicsBlurEffect(self)
        ##blur_effect.setBlurRadius(10)
        ##self.setGraphicsEffect(blur_effect)

        form = FormSolicitudPermisoAdmin()
        if form.exec() == QDialog.Accepted:
            # self._cargar_tabla()
            self.setGraphicsEffect(None)

    def _editar_permiso(self, id):
        form = FormSolicitudPermisoAdmin(titulo="Editar Solicitud", id_solicitud=id)
        form.exec()
        # self._cargar_tabla()

    def _eliminarRegistro(self, id_solicitud: int):
        """
        Maneja la eliminación de una solicitud con confirmación

        Args:
            id_solicitud (int): ID de la solicitud a eliminar
        """
        dial = DialogoEmergente(
            "Confirmación",
            "¿Estás seguro de eliminar esta solicitud de permiso?",
            "Question",
            True,
            True,
        )

        if dial.exec() == QDialog.Accepted:
            resultado = self.permiso_service.eliminar_permiso(id_solicitud)

            mensaje = resultado["message"]
            icono = "Check" if resultado["success"] else "Error"

            DialogoEmergente("Resultado", mensaje, icono, True, False).exec()

            # self._cargar_tabla()  # Refrescar la tabla
