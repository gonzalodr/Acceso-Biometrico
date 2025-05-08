from PySide6.QtWidgets import *
from PySide6.QtCore import *
from UI.DialogoEmergente import DialogoEmergente
from Utils.Utils import *
from services.usuarioService import *
from UI.AdministrarUsuario.formUsuario import *
from functools import partial

class AdminUsuario(QWidget):
    cerrar_adminU = Signal()
    paginaActual = 1
    ultimaPagina = 1
    busqueda = None
    Uservices = UsuarioServices()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("admin")
        cargar_estilos('claro','admin.css',self)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)

        frame = QFrame()

        self.layoutFrame = QVBoxLayout()
        self.layoutFrame.setContentsMargins(0, 0, 0, 0)
        self.layoutFrame.setSpacing(0)

        titulo = QLabel(text="Administrar Usuarios")
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

        # Campo de entrada para buscar Usuarios
        self.inputBuscar = QLineEdit()
        self.inputBuscar.setClearButtonEnabled(True)
        self.inputBuscar.setPlaceholderText("Buscar usuario")
        self.inputBuscar.setFixedSize(QSize(500, 30))
        self.inputBuscar.textChanged.connect(self._cargar_tabla)
        Sombrear(self.inputBuscar, 20, 0, 0)

        self.btnBuscar = QPushButton(text="Buscar")
        self.btnBuscar.setCursor(Qt.PointingHandCursor)
        self.btnBuscar.setFixedSize(minimoTamBtn)
        self.btnBuscar.clicked.connect(self._buscarUsuario)
        Sombrear(self.btnBuscar, 20, 0, 0)

        self.btnCrear = QPushButton(text="Crear")
        self.btnCrear.setCursor(Qt.PointingHandCursor)
        self.btnCrear.setFixedSize(minimoTamBtn)
        self.btnCrear.clicked.connect(self._crear_usuario)
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

        # Tabla Usuario
        self.tbUsuario = QTableWidget()
        if self.tbUsuario.columnCount() < 4:
            self.tbUsuario.setColumnCount(4)
        header_labels = ["Nombre", "Usuario", "Perfil", "Acciones"]
        self.tbUsuario.setHorizontalHeaderLabels(header_labels)

        self.tbUsuario.horizontalHeader().setFixedHeight(40)
        self.tbUsuario.verticalHeader().setVisible(False)
        self.tbUsuario.horizontalHeader().setStretchLastSection(True)
        self.tbUsuario.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        Sombrear(self.tbUsuario, 30, 0, 0)

        # Layout para la tabla
        layoutTb = QHBoxLayout()
        layoutTb.setContentsMargins(70, 40, 70, 40)
        layoutTb.addWidget(self.tbUsuario)
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

    def _cerrar(self):
        self.cerrar_adminU.emit()

    def _cargar_tabla(self):
        result = self.Uservices.obtenerListaUsuarios(
            pagina=self.paginaActual, tam_pagina=10, busqueda=self.busqueda
        )

        if self.inputBuscar.text() == '':
            self.busqueda = None  # Resetea búsqueda
            self.paginaActual = 1  # Reset a la primera página

        self.tbUsuario.setRowCount(0)  # Limpiar la tabla antes de cargar nuevos datos

        # Verificar si result es None
        if result is None:
            print("Error: No se obtuvo ningún resultado.")
            return  # Salir de la función si no hay resultados

        if result.get("success"):  # Usar get para evitar KeyError
            listaUsuarios = result.get("data", {}).get("listaUsuarios", [])

            if listaUsuarios:
                paginaActual = result["data"]["pagina_actual"]
                totalPaginas = result["data"]["total_paginas"]
                self._actualizar_lblPagina(paginaActual, totalPaginas)
                self._actualizarValoresPaginado(paginaActual, totalPaginas)

                for index, usuario in enumerate(listaUsuarios):
                    self.tbUsuario.insertRow(index)
                    self.tbUsuario.setRowHeight(index, 45)

                    # Nombre completo
                    item_nombre = QTableWidgetItem(usuario["nombre_completo"])
                    item_nombre.setTextAlignment(Qt.AlignCenter)
                    self.tbUsuario.setItem(index, 0, item_nombre)

                    # Usuario
                    item_usuario = QTableWidgetItem(usuario["usuario"])
                    item_usuario.setTextAlignment(Qt.AlignCenter)
                    self.tbUsuario.setItem(index, 1, item_usuario)

                    # Nombre del perfil
                    nombre_perfil = usuario.get("nombre_perfil", "Sin perfil")
                    item_perfil = QTableWidgetItem(nombre_perfil)
                    item_perfil.setTextAlignment(Qt.AlignCenter)
                    self.tbUsuario.setItem(index, 2, item_perfil)

                    # Contenedor para los botones de acción
                    contenedor_botones = QWidget()
                    layout_botones = QHBoxLayout()
                    layout_botones.setContentsMargins(0, 0, 0, 0)
                    layout_botones.setSpacing(5)

                    # Botón Editar
                    btnEditar = QPushButton("Editar")
                    btnEditar.clicked.connect(partial(self._editar_Usuario, usuario["id_usuario"], usuario["id_usuario_perfil"]))
                    btnEditar.setStyleSheet("""
                        QPushButton{background-color:#28A745;color:white;}
                        QPushButton::hover{background-color:#218838;color:white;}
                    """)
                    btnEditar.setMinimumSize(QSize(80, 35))

                    # Botón Eliminar
                    btnEliminar = QPushButton("Eliminar")
                    btnEliminar.clicked.connect(partial(self._eliminarRegistro, usuario["id_usuario"], usuario["id_usuario_perfil"]))
                    btnEliminar.setStyleSheet("""
                        QPushButton{background-color:#DC3545;color:white;}
                        QPushButton::hover{background-color:#C82333;color:white;}
                    """)
                    btnEliminar.setMinimumSize(QSize(80, 35))

                    layout_botones.addWidget(btnEditar)
                    layout_botones.addWidget(btnEliminar)
                    contenedor_botones.setLayout(layout_botones)

                    self.tbUsuario.setCellWidget(index, 3, contenedor_botones)

            else:
                # Mostrar mensaje de "No se encontraron resultados"
                self.tbUsuario.setRowCount(1)
                self.tbUsuario.setItem(0, 0, QTableWidgetItem("No se encontraron resultados."))
                self.tbUsuario.setSpan(0, 0, 1, 4)  # Hacer que el mensaje ocupe varias columnas
                self.tbUsuario.item(0, 0).setTextAlignment(Qt.AlignCenter)

                self._actualizar_lblPagina(0, 0)
                self._actualizarValoresPaginado(0, 0)
        else:
            print("Error al obtener usuarios.")  # Mensaje de depuración
            self.tbUsuario.setRowCount(0)
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

    def _buscarUsuario(self):
        input_busqueda = self.inputBuscar.text()
        if input_busqueda:
            self.busqueda = input_busqueda
            self.paginaActual = 1 
            self._cargar_tabla()
        else:
            self.busqueda = None  
            self.paginaActual = 1  
            self._cargar_tabla() 

    def _eliminarRegistro(self, usuario_id, usuario_perfil_id):
        dial = DialogoEmergente("¿?", "¿Seguro que quieres eliminar este registro?", "Question", True, True)
        if dial.exec() == QDialog.Accepted:
            result = self.Uservices.eliminarUsuario(usuario_id, usuario_perfil_id)
            if result["success"]:
                dial = DialogoEmergente("", "Se eliminó el registro correctamente.", "Check")
                dial.exec()
                self._cargar_tabla()
            else:
                dial = DialogoEmergente("", "Hubo un error al eliminar este registro.", "Error")
                dial.exec()

    def _editar_Usuario(self, id, id_usuario_perfil):
        blur_effect = QGraphicsBlurEffect(self)
        blur_effect.setBlurRadius(10)
        self.setGraphicsEffect(blur_effect)
        
        form = formUsuario(titulo="Actualizar usuario", id=id, id_usuario_perfil=id_usuario_perfil)
        form.exec()
        
        self._cargar_tabla()
        self.setGraphicsEffect(None)

    def _crear_usuario(self):
        blur_effect = QGraphicsBlurEffect(self)
        blur_effect.setBlurRadius(10)
        self.setGraphicsEffect(blur_effect)
        
        form = formUsuario()
        form.exec()
        self._cargar_tabla()
        self.setGraphicsEffect(None)
