from PySide6.QtWidgets import *
from PySide6.QtCore import *
from Utils.Utils import *
from UI.AdministrarPermisosPerfil.formPerfil import *
from UI.AdministrarPerfil.formPerfil import *
from services.permisosPerfilServices import *
from services.perfilService import *

from settings.config import *

from settings.config import *

from settings.config import *

class AdminPermisosPerfil(QWidget):
    cerrar_adminP = Signal()
    paginaActual = 1
    ultimaPagina = 1
    busqueda = None
    permisoperfilServices = PermisosPerfilServices()
    perfilServices = PerfilServices()

    def __init__(self, parent=None, permiso=None) -> None:
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

        titulo = QLabel(text="Administrar perfiles.")
        titulo.setObjectName("titulo")
        titulo.setMinimumHeight(50)
        titulo.setAlignment(Qt.AlignCenter)
        self.layoutFrame.addWidget(titulo)

        layoutTop = QHBoxLayout()
        layoutTop.setContentsMargins(30, 30, 30, 30)
        layoutTop.setSpacing(5)
        layoutTop.setAlignment(Qt.AlignCenter)
        minimoTamBtn = QSize(120, 40)

        self.inputBuscar = QLineEdit()
        self.inputBuscar.setClearButtonEnabled(True)
        self.inputBuscar.setPlaceholderText("Buscar perfil por nombre.")
        self.inputBuscar.setFixedSize(QSize(500, 30))
        self.inputBuscar.textChanged.connect(self.cargarTablaPerfiles)
        Sombrear(self.inputBuscar, 20, 0, 0)

        ##acomodando botones de arriba en el layout
        layoutTop.addSpacing(25)
        layoutTop.addWidget(self.crearBoton("Cerrar", minimoTamBtn, self.cerrarAdmin))
        layoutTop.addStretch(1)
        layoutTop.addWidget(self.inputBuscar, 2)
        layoutTop.addSpacing(10)
        layoutTop.addWidget(
            self.crearBoton("Buscar", minimoTamBtn, self.buscarPerfiles)
        )
        layoutTop.addStretch(1)
        layoutTop.addWidget(self.crearBoton("Crear", minimoTamBtn, self.crearPerfil))
        layoutTop.addStretch(5)
        self.layoutFrame.addLayout(layoutTop)

        self.tbPermisosPerfil = QTableWidget()  ##crean el objeto tabla
        if self.tbPermisosPerfil.columnCount() < 8:
            self.tbPermisosPerfil.setColumnCount(8)  ##indican la cantidad de columnas.
        ##crean un array de titulos para cada columna
        header_labels = [
            "Perfil",
            "Descripción",
            "Acesso a",
            "Ver",
            "Crear",
            "Editar",
            "Eliminar",
            "Acciones",
        ]
        self.tbPermisosPerfil.setHorizontalHeaderLabels(
            header_labels
        )  ##ingreasan el array aqui
        self.tbPermisosPerfil.horizontalHeader().setFixedHeight(40)
        self.tbPermisosPerfil.verticalHeader().setVisible(False)
        self.tbPermisosPerfil.horizontalHeader().setStretchLastSection(True)
        self.tbPermisosPerfil.horizontalHeader().setSectionsMovable(False)
        self.tbPermisosPerfil.horizontalHeader().setMinimumSectionSize(50)
        self.tbPermisosPerfil.setColumnWidth(7, 305)
        self.tbPermisosPerfil.setSelectionMode(
            QAbstractItemView.SelectionMode.NoSelection
        )
        self.tbPermisosPerfil.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.tbPermisosPerfil.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        Sombrear(self.tbPermisosPerfil, 30, 0, 0)

        layoutTb = QHBoxLayout()
        layoutTb.setContentsMargins(70, 40, 70, 40)
        layoutTb.addWidget(self.tbPermisosPerfil)
        self.layoutFrame.addLayout(layoutTb)

        layoutButtom = QHBoxLayout()
        layoutButtom.setAlignment(Qt.AlignCenter)
        layoutButtom.setContentsMargins(10, 10, 10, 40)
        layoutButtom.setSpacing(5)

        self.lblNumPagina = QLabel(text="Pagina 0 de 0 paginas")
        self.lblNumPagina.setFixedSize(QSize(170, 40))
        self.lblNumPagina.setAlignment(Qt.AlignCenter)

        self.btnPrimerPagina = self.crearBoton(
            "Primer pagina", minimoTamBtn, self._irPrimeraPagina, False
        )
        self.btnAnterior = self.crearBoton(
            "Anterior", minimoTamBtn, self._irAnteriorPagina, False
        )
        self.btnSiguiente = self.crearBoton(
            "Siguiente", minimoTamBtn, self._irSiguientePagina, False
        )
        self.btnUltimaPagina = self.crearBoton(
            "Ultima pagina", minimoTamBtn, self._irUltimaPagina, False
        )

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
        self.cargarTablaPerfiles()

    def crearBoton(
        self,
        text: str,
        fixedSize: QSize,
        functionConnect,
        enable: bool = True,
        cursorType=Qt.PointingHandCursor,
    ) -> QPushButton:
        boton = QPushButton(text)
        boton.setEnabled(enable)
        boton.setFixedSize(fixedSize)
        boton.setCursor(cursorType)
        boton.clicked.connect(functionConnect)
        Sombrear(boton, 20, 0, 0)
        return boton

    def cerrarAdmin(self):
        self.cerrar_adminP.emit()

    def mostrarMensajeTabla(self, mensaje: str):
        self.tbPermisosPerfil.setRowCount(0)
        self.tbPermisosPerfil.setRowCount(1)
        self.addItemTable(0, 0, mensaje)
        self.tbPermisosPerfil.setSpan(0, 0, 1, self.tbPermisosPerfil.columnCount())

    def cargarTablaPerfiles(self):
        result = self.perfilServices.obtenerListaPerfil(
            pagina=self.paginaActual,
            tam_pagina=10,
            tipo_orden="DESC",
            busqueda=self.busqueda,
        )
        if not result["success"]:
            self.mostrarMensajeTabla("Error de conexión.")
            return

        listaPerfiles = result["data"]["listaPerfiles"]
        if len(listaPerfiles) == 0:
            self.mostrarMensajeTabla(
                "No hay registros."
                if self.busqueda is None
                else "No se encontraron registros que coincidan con la busqueda."
            )
            return

        paginaActual = result["data"]["pagina_actual"]
        tamPagina = result["data"]["tam_pagina"]
        totalPaginas = result["data"]["total_paginas"]
        totalRegistros = result["data"]["total_registros"]

        self.actualizarLblPagina(paginaActual, totalPaginas)
        self.actualizarValoresPaginado(paginaActual, totalPaginas)

        self.tbPermisosPerfil.setRowCount(0)
        contadorPerfiles = 0
        for index, perfiles in enumerate(listaPerfiles):
            self.tbPermisosPerfil.insertRow(contadorPerfiles)

            perfil = perfiles["perfil"]
            listPermisos = perfiles["listaPermisos"]

            num_permisos = len(listPermisos) if listPermisos else 1
            print(f"{contadorPerfiles}  and  {num_permisos}")
            self.addItemTable(contadorPerfiles, 0, perfil.nombre)
            self.addItemTable(contadorPerfiles, 1, perfil.descripcion)

            # Insertar el primer permiso en la misma fila
            if not listPermisos:
                self.addItemTable(contadorPerfiles, 2, "Sin accesos registrados.")
                self.tbPermisosPerfil.setSpan(contadorPerfiles, 2, 1, 5)
                self.tbPermisosPerfil.setRowHeight(contadorPerfiles, 50)

            if listPermisos:
                primer_permiso = listPermisos[0]
                self.addItemTable(contadorPerfiles, 2, primer_permiso.tabla)
                self.addItemTable(
                    contadorPerfiles, 3, "Si" if primer_permiso.ver else "No"
                )
                self.addItemTable(
                    contadorPerfiles, 4, "Si" if primer_permiso.crear else "No"
                )
                self.addItemTable(
                    contadorPerfiles, 5, "Si" if primer_permiso.editar else "No"
                )
                self.addItemTable(
                    contadorPerfiles, 6, "Si" if primer_permiso.eliminar else "No"
                )
                self.addItemTable(contadorPerfiles, 7, "")

                # Si hay más permisos, añadir filas adicionales
                for permiso_idx, permiso in enumerate(listPermisos[1:], start=1):
                    row_position = contadorPerfiles + permiso_idx
                    self.tbPermisosPerfil.insertRow(row_position)

                    # Insertar datos del permiso (dejando vacías las columnas 0 (nombre del perfil), 1 (desscripcion) y 7 (acciones))
                    self.addItemTable(row_position, 2, permiso.tabla)
                    self.addItemTable(row_position, 3, "Si" if permiso.ver else "No")
                    self.addItemTable(row_position, 4, "Si" if permiso.crear else "No")
                    self.addItemTable(row_position, 5, "Si" if permiso.editar else "No")
                    self.addItemTable(
                        row_position, 6, "Si" if permiso.eliminar else "No"
                    )
                    self.addItemTable(row_position, 7, "")

                if len(listPermisos) > 1:
                    self.tbPermisosPerfil.setSpan(
                        contadorPerfiles, 0, len(listPermisos), 1
                    )
                    self.tbPermisosPerfil.setSpan(
                        contadorPerfiles, 1, len(listPermisos), 1
                    )
                    self.tbPermisosPerfil.setSpan(
                        contadorPerfiles, 7, len(listPermisos), 1
                    )
                else:
                    self.tbPermisosPerfil.setRowHeight(contadorPerfiles, 50)

            layout = QHBoxLayout()
            layout.addWidget(
                self.crearBtnAccion("Editar", "btneditar", perfil.id, self.editarPerfil)
            )
            layout.addSpacing(15)
            layout.addWidget(
                self.crearBtnAccion(
                    "Eliminar", "btneliminar", perfil.id, self.eliminarPerfil
                )
            )
            layout.setContentsMargins(10, 0, 10, 0)
            button_widget = QWidget()
            button_widget.setFixedWidth(300)
            button_widget.setLayout(layout)
            self.tbPermisosPerfil.setCellWidget(contadorPerfiles, 7, button_widget)

            contadorPerfiles += num_permisos

    def addItemTable(self, row, colum, dato):
        dato_item = QTableWidgetItem(dato)
        dato_item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)  # No editable
        self.tbPermisosPerfil.setItem(row, colum, dato_item)

    def crearBtnAccion(
        self, text: str, objectName: str, id_perfil: int, functionAction
    ):
        boton = QPushButton(text, parent=self.tbPermisosPerfil)
        boton.setObjectName(objectName)
        boton.setMinimumSize(QSize(80, 35))
        boton.setMaximumWidth(100)
        boton.clicked.connect(lambda: functionAction(id_perfil))
        return boton

    def actualizarLblPagina(self, numPagina, totalPagina):
        self.lblNumPagina.setText(f"Pagina {numPagina} de {totalPagina} ")

    def actualizarValoresPaginado(self, paginaActual, totalPaginas):
        self.paginaActual = paginaActual
        self.ultimaPagina = totalPaginas
        self.btnSiguiente.setEnabled(paginaActual < totalPaginas)
        self.btnUltimaPagina.setEnabled(paginaActual < totalPaginas)
        self.btnPrimerPagina.setEnabled(paginaActual > 1)
        self.btnAnterior.setEnabled(paginaActual > 1)

    def _irPrimeraPagina(self):
        self.paginaActual = 1
        self.cargarTablaPerfiles()

    def _irUltimaPagina(self):
        self.paginaActual = self.ultimaPagina
        self.cargarTablaPerfiles()

    def _irSiguientePagina(self):
        if (self.paginaActual + 1) <= self.ultimaPagina:
            self.paginaActual = self.paginaActual + 1
            self.cargarTablaPerfiles()

    def _irAnteriorPagina(self):
        if (self.paginaActual - 1) >= 1:
            self.paginaActual = self.paginaActual - 1
            self.cargarTablaPerfiles()

    def buscarPerfiles(self):
        input_busqueda = self.inputBuscar.text()
        if input_busqueda:
            self.busqueda = input_busqueda
            self.cargarTablaPerfiles()
            self.busqueda = None
        else:
            self.paginaActual = 1
            self.cargarTablaPerfiles()

    def eliminarPerfil(self, id):
        dial = DialogoEmergente(
            "",
            "¿Esta seguro que quieres eliminar este registro?",
            "Question",
            True,
            True,
        )
        if dial.exec() == QDialog.Accepted:
            result = self.perfilServices.eliminarPerfil(id)
            print(result)
            if not result["success"]:
                dial = DialogoEmergente("", result["message"], "Error", True)
                dial.exec()
                return
            dial = DialogoEmergente("", "Se elimino el perfil correctamente.", "Check")
            dial.exec()
            self.cargarTablaPerfiles()

    def editarPerfil(self, id):
        form = FormularioPerfilAccesos(id_perfil=id)
        form.exec()
        self.cargarTablaPerfiles()

    def crearPerfil(self):
        form = FormularioPerfilAccesos()
        form.exec()
        self.cargarTablaPerfiles()
