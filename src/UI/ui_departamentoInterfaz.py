# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'departamentoInterfaz.ui'
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################


import sys
from services.departamentoService import DepartamentoServices
from UI.stilosInterfaz import (btnStyleSheet,btnEliminarStyleSheet,LineEditStyleSheet,
                               tableStyleSheet,mesboxStyleSheet,
                               btnDisableStyleSheet,
                               form_styleSheet)
from models.departamento import Departamento


from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QGridLayout, QHBoxLayout,
    QHeaderView, QLabel, QLineEdit, QPushButton,
    QSizePolicy, QSpacerItem, QTableWidget, QTableWidgetItem,
    QVBoxLayout, QWidget, QMessageBox)
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QDialog,
    QLabel, QLineEdit, QDateEdit, QComboBox, QTextEdit, QFormLayout, QDialogButtonBox, QFrame, QMessageBox
)

class Ui_departamentoInterfaz(object):
    paginaActual = 1
    ultimaPagina = 1
    Pservices = DepartamentoServices()
        
    def setupUi(self, departamentoInterfaz):
        if not departamentoInterfaz.objectName():
             departamentoInterfaz.setObjectName(u"departamentoInterfaz")
        departamentoInterfaz.resize(1200, 800)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(departamentoInterfaz.sizePolicy().hasHeightForWidth())
        departamentoInterfaz.setSizePolicy(sizePolicy)
        departamentoInterfaz.setMinimumSize(QSize(600, 400))
        departamentoInterfaz.setMaximumSize(QSize(1200, 800))
        departamentoInterfaz.setStyleSheet("background-color:#FFFFFF; color: #000000;")

        
        self.verticalLayoutWidget = QWidget(departamentoInterfaz)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(0, 0, 1201, 791))
        self.vLayoutPagina = QVBoxLayout(self.verticalLayoutWidget)
        self.vLayoutPagina.setSpacing(0)
        self.vLayoutPagina.setObjectName(u"vLayoutPagina")
        self.vLayoutPagina.setContentsMargins(0, 0, 0, 0)
        self.gridLayoutEncabezado = QGridLayout()
        self.gridLayoutEncabezado.setObjectName(u"gridLayoutEncabezado")
        
        self.frameEncabezado = QFrame(self.verticalLayoutWidget)
        self.frameEncabezado.setObjectName(u"frameEncabezado")
        sizePolicy.setHeightForWidth(self.frameEncabezado.sizePolicy().hasHeightForWidth())
        self.frameEncabezado.setSizePolicy(sizePolicy)
        self.frameEncabezado.setStyleSheet(u"background-color:#0300D1;")
        self.frameEncabezado.setFrameShape(QFrame.Shape.StyledPanel)
        self.frameEncabezado.setFrameShadow(QFrame.Shadow.Raised)

        self.gridLayoutWidget = QWidget(self.frameEncabezado)
        self.gridLayoutWidget.setObjectName(u"gridLayoutWidget")
        self.gridLayoutWidget.setGeometry(QRect(0, 0, 1201, 111))
        self.gridLayoutEncabezado_2 = QGridLayout(self.gridLayoutWidget)
        self.gridLayoutEncabezado_2.setSpacing(0)
        self.gridLayoutEncabezado_2.setObjectName(u"gridLayoutEncabezado_2")
        self.gridLayoutEncabezado_2.setContentsMargins(0, 0, 0, 0)
    
        # Botón de configuración
        self.btnConfigPag = QPushButton(self.gridLayoutWidget)
        self.btnConfigPag.setObjectName(u"btnConfigPag")
        sizePolicy.setHeightForWidth(self.btnConfigPag.sizePolicy().hasHeightForWidth())
        self.btnConfigPag.setSizePolicy(sizePolicy)
        self.gridLayoutEncabezado_2.addWidget(self.btnConfigPag, 1, 2, 1, 1)

    # Avatar del usuario
        self.label_3 = QLabel(self.gridLayoutWidget)
        self.label_3.setObjectName(u"label_3")
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        self.gridLayoutEncabezado_2.addWidget(self.label_3, 0, 2, 1, 1)

        # Nombre de la página actual
        self.lblNombrePagina = QLabel(self.gridLayoutWidget)
        self.lblNombrePagina.setObjectName(u"lblNombrePagina")
        self.lblNombrePagina.setStyleSheet(u"font: 700 16pt 'Segoe UI'; color: #FFFFFF;")
        self.lblNombrePagina.setIndent(10)
        self.gridLayoutEncabezado_2.addWidget(self.lblNombrePagina, 1, 0, 1, 1)

        # Título de la aplicación
        self.label = QLabel(self.gridLayoutWidget)
        self.label.setObjectName(u"label")
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setStyleSheet(u"font: 700 24pt 'Segoe UI'; color:#FFFFFF;")
        self.label.setIndent(10)
        self.gridLayoutEncabezado_2.addWidget(self.label, 0, 0, 1, 1)


        # Espaciadores para el encabezado
        self.horizontalSpacer_8 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.gridLayoutEncabezado_2.addItem(self.horizontalSpacer_8, 0, 1, 1, 1)
        
        self.horizontalSpacer_9 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.gridLayoutEncabezado_2.addItem(self.horizontalSpacer_9, 1, 1, 1, 1)

        # Configuración de estiramiento para las filas y columnas
        self.gridLayoutEncabezado_2.setRowStretch(0, 2)
        self.gridLayoutEncabezado_2.setRowStretch(1, 1)
        self.gridLayoutEncabezado_2.setColumnStretch(0, 6)
        self.gridLayoutEncabezado_2.setColumnStretch(1, 1)
        self.gridLayoutEncabezado_2.setColumnStretch(2, 1)
        self.gridLayoutEncabezado.addWidget(self.frameEncabezado, 0, 0, 1, 1)
        self.vLayoutPagina.addLayout(self.gridLayoutEncabezado)

        #Creando el cuerpo de la ventana
        self.vLayoutCuerpo = QVBoxLayout()
        self.vLayoutCuerpo.setObjectName(u"vLayoutCuerpo")

        #Creando el frame para el cuerpo
        self.frameCuerpo = QFrame(self.verticalLayoutWidget)
        self.frameCuerpo.setObjectName(u"frameCuerpo")
        self.frameCuerpo.setStyleSheet(u"background-color:rgb(255, 255, 255)")
        self.frameCuerpo.setFrameShape(QFrame.Shape.StyledPanel)
        self.frameCuerpo.setFrameShadow(QFrame.Shadow.Raised)

        #Añadiendo el frameCuerpo al layout principal
        self.verticalLayoutWidget_2 = QWidget(self.frameCuerpo)
        self.verticalLayoutWidget_2.setObjectName(u"verticalLayoutWidget_2")
        self.verticalLayoutWidget_2.setGeometry(QRect(-1, 39, 1201, 641))

        self.vLayoutCuerpo_3 = QVBoxLayout(self.verticalLayoutWidget_2)
        self.vLayoutCuerpo_3.setSpacing(0)
        self.vLayoutCuerpo_3.setObjectName(u"vLayoutCuerpo_3")
        self.vLayoutCuerpo_3.setContentsMargins(0, 0, 0, 0)
        self.hLayoutCuerpo = QHBoxLayout()
        self.hLayoutCuerpo.setSpacing(0)
        self.hLayoutCuerpo.setObjectName(u"hLayoutCuerpo")
        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.hLayoutCuerpo.addItem(self.horizontalSpacer_3)

        self.btnRegresarMenu = QPushButton(self.verticalLayoutWidget_2)
        self.btnRegresarMenu.setObjectName(u"btnRegresarMenu")
        self.btnRegresarMenu.setStyleSheet(btnStyleSheet)
        self.hLayoutCuerpo.addWidget(self.btnRegresarMenu)
        
        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.hLayoutCuerpo.addItem(self.horizontalSpacer_4)

        self.InputBusqueda = QLineEdit(self.verticalLayoutWidget_2)
        self.InputBusqueda.setObjectName(u"InputBusqueda")
        self.InputBusqueda.setStyleSheet(LineEditStyleSheet)
        self.InputBusqueda.setClearButtonEnabled(True)
        self.hLayoutCuerpo.addWidget(self.InputBusqueda)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.hLayoutCuerpo.addItem(self.horizontalSpacer_5)

        self.btnBuscar = QPushButton(self.verticalLayoutWidget_2)
        self.btnBuscar.setObjectName(u"btnBuscar")
        self.btnBuscar.setStyleSheet(btnStyleSheet)
        self.hLayoutCuerpo.addWidget(self.btnBuscar)

        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.hLayoutCuerpo.addItem(self.horizontalSpacer_7)
        
        self.btnCrearDepartamento = QPushButton(self.verticalLayoutWidget_2)
        self.btnCrearDepartamento.setObjectName(u"btnCrearDepartamento")
        self.btnCrearDepartamento.setStyleSheet(btnStyleSheet)
        self.hLayoutCuerpo.addWidget(self.btnCrearDepartamento)
        
        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.hLayoutCuerpo.addItem(self.horizontalSpacer_6)

        self.hLayoutCuerpo.setStretch(1, 1)
        self.hLayoutCuerpo.setStretch(2, 2)
        self.hLayoutCuerpo.setStretch(3, 4)
        self.hLayoutCuerpo.setStretch(5, 1)
        self.hLayoutCuerpo.setStretch(6, 1)
        self.hLayoutCuerpo.setStretch(7, 1)
        self.hLayoutCuerpo.setStretch(8, 1)
        self.vLayoutCuerpo_3.addLayout(self.hLayoutCuerpo)

        self.gridLayoutCuerpo_3 = QGridLayout()
        self.gridLayoutCuerpo_3.setSpacing(0)
        self.gridLayoutCuerpo_3.setObjectName(u"gridLayoutCuerpo_3")
        
        
        self.tbDepartamento = QTableWidget(self.verticalLayoutWidget_2)
        if self.tbDepartamento.columnCount() < 3:
            self.tbDepartamento.setColumnCount(3)
# Definir los nombres de las cabeceras directamente
        header_labels = ["Nombre", "Descripción", "Acciones"]
        self.tbDepartamento.setHorizontalHeaderLabels(header_labels)
        self.tbDepartamento.setAlternatingRowColors(True)

        self.tbDepartamento.setObjectName(u"tbDepartamento")
        self.tbDepartamento.setStyleSheet(tableStyleSheet)
        self.tbDepartamento.horizontalHeader().setCascadingSectionResizes(True)
        self.tbDepartamento.horizontalHeader().setHighlightSections(True)
        self.tbDepartamento.horizontalHeader().setStretchLastSection(True)
        self.tbDepartamento.verticalHeader().setVisible(False)
        self.tbDepartamento.verticalHeader().setHighlightSections(False)
        self.gridLayoutCuerpo_3.addWidget(self.tbDepartamento, 1, 1, 1, 1)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        self.gridLayoutCuerpo_3.addItem(self.verticalSpacer_2, 4, 1, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        self.gridLayoutCuerpo_3.addItem(self.verticalSpacer, 0, 1, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.gridLayoutCuerpo_3.addItem(self.horizontalSpacer_2, 1, 2, 1, 1)

        self.gdLvLayoutCuerpo = QHBoxLayout()
        self.gdLvLayoutCuerpo.setObjectName(u"gdLvLayoutCuerpo")
        self.horizontalSpacer_10 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.gdLvLayoutCuerpo.addItem(self.horizontalSpacer_10)

        self.btnPrimerPagina = QPushButton(self.verticalLayoutWidget_2)
        self.btnPrimerPagina.setObjectName(u"btnPrimerPagina")
        self.btnPrimerPagina.setStyleSheet(btnStyleSheet)
        self.gdLvLayoutCuerpo.addWidget(self.btnPrimerPagina)

        self.horizontalSpacer_11 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.gdLvLayoutCuerpo.addItem(self.horizontalSpacer_11)

        self.btnAnterior = QPushButton(self.verticalLayoutWidget_2)
        self.btnAnterior.setObjectName(u"btnAnterior")
        self.btnAnterior.setStyleSheet(btnStyleSheet)
        self.gdLvLayoutCuerpo.addWidget(self.btnAnterior)

        self.horizontalSpacer_12 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.gdLvLayoutCuerpo.addItem(self.horizontalSpacer_12)

        self.lblNumeroPagina = QLabel(self.verticalLayoutWidget_2)
        self.lblNumeroPagina.setObjectName(u"lblNumeroPagina")
        self.lblNumeroPagina.setStyleSheet(u"color:rgb(0, 0, 255);font: 700 9pt \"Segoe UI\";")
        self.gdLvLayoutCuerpo.addWidget(self.lblNumeroPagina)

        self.horizontalSpacer_13 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.gdLvLayoutCuerpo.addItem(self.horizontalSpacer_13)

        self.btnSiguiente = QPushButton(self.verticalLayoutWidget_2)
        self.btnSiguiente.setObjectName(u"btnSiguiente")
        self.btnSiguiente.setStyleSheet(btnStyleSheet)
        self.gdLvLayoutCuerpo.addWidget(self.btnSiguiente)

        self.horizontalSpacer_15 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.gdLvLayoutCuerpo.addItem(self.horizontalSpacer_15)

        self.btnUltimaPagina = QPushButton(self.verticalLayoutWidget_2)
        self.btnUltimaPagina.setObjectName(u"btnUltimaPagina")
        self.btnUltimaPagina.setStyleSheet(btnStyleSheet)
        self.gdLvLayoutCuerpo.addWidget(self.btnUltimaPagina)

        self.horizontalSpacer_14 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.gdLvLayoutCuerpo.addItem(self.horizontalSpacer_14)

        self.gdLvLayoutCuerpo.setStretch(0, 3)
        self.gdLvLayoutCuerpo.setStretch(10, 3)
        self.gridLayoutCuerpo_3.addLayout(self.gdLvLayoutCuerpo, 3, 1, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.gridLayoutCuerpo_3.addItem(self.horizontalSpacer, 1, 0, 1, 1)

        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        self.gridLayoutCuerpo_3.addItem(self.verticalSpacer_3, 2, 1, 1, 1)

        self.gridLayoutCuerpo_3.setRowStretch(0, 1)
        self.gridLayoutCuerpo_3.setRowStretch(1, 7)
        self.gridLayoutCuerpo_3.setRowStretch(2, 1)
        self.gridLayoutCuerpo_3.setRowStretch(3, 1)
        self.gridLayoutCuerpo_3.setColumnStretch(0, 1)
        self.gridLayoutCuerpo_3.setColumnStretch(1, 8)
        self.gridLayoutCuerpo_3.setColumnStretch(2, 1)

        #Ordenar crear el layout de cuerpo
        self.vLayoutCuerpo_3.addLayout(self.gridLayoutCuerpo_3)
        self.vLayoutCuerpo_3.setStretch(0, 1)
        self.vLayoutCuerpo_3.setStretch(1, 7)
        self.vLayoutCuerpo.addWidget(self.frameCuerpo)
        self.vLayoutPagina.addLayout(self.vLayoutCuerpo)

        self.vLayoutPagina.setStretch(0, 1)
        self.vLayoutPagina.setStretch(1, 6)
        
        # Botones
        self.btnBuscar.clicked.connect(self.buscarDepartamento)
        self.btnAnterior.clicked.connect(self.irAnteriorPagina)
        self.btnSiguiente.clicked.connect(self.irSiguientePagina)
        self.btnUltimaPagina.clicked.connect(self.irUltimaPagina)
        self.btnPrimerPagina.clicked.connect(self.irPrimeraPagina)
        self.btnCrearDepartamento.clicked.connect(self.abrir_formulario_modal)
        self.llenarTabla()

        self.retranslateUi(departamentoInterfaz)
        QMetaObject.connectSlotsByName(departamentoInterfaz)
# setupUi

    def llenarTabla(self):
        Dservices = DepartamentoServices()
        resultado = Dservices.obtenerListaDepartamento(self.paginaActual,10,"Id","DESC")
        if resultado["success"]:
            listaDepartamento = resultado["data"]["listaDepartamentos"]
            paginaActual = resultado["data"]["pagina_actual"]
            tamPagina = resultado["data"]["tam_pagina"]
            totalPaginas = resultado["data"]["total_paginas"]
            totalRegistros = resultado["data"]["total_registros"]

            self.actualizarLabelPaginas(paginaActual,totalPaginas)
            self.ActualizarValoresPaginado(paginaActual,totalPaginas)

        # Limpiamos las filas
            self.tbDepartamento.setRowCount(0) 

        for index, departamento in enumerate(listaDepartamento):
            self.tbDepartamento.insertRow(index)  # Crea una fila por registro
            self.tbDepartamento.setRowHeight(index,45)

            self.addItem_a_tabla(index,0,departamento.nombre)
            self.addItem_a_tabla(index,1,departamento.descripcion)
            
            # Colocación de botones de eliminación y edición
            btnEliminar = QPushButton("Eliminar")
            btnEliminar.setStyleSheet(btnEliminarStyleSheet)
            btnEliminar.clicked.connect(lambda checked, idx=departamento.id: self.eliminarRegistro(idx))
            btnEliminar.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Fixed)

            btnEditar = QPushButton("Editar")
            btnEditar.setStyleSheet(btnStyleSheet)
            btnEditar.clicked.connect(lambda checked, fila=index,idx = departamento.id: self.editar_Departamento(fila,idx))
            btnEditar.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
            button_widget = QWidget()
            button_widget.setStyleSheet(u"background-color:transparent;")
            button_widget.setFixedSize(140,40) 
            layout = QHBoxLayout(button_widget)
            layout.addWidget(btnEditar)
            layout.addWidget(btnEliminar)
            layout.setAlignment(Qt.AlignCenter)  # Centrar el botón
            layout.setContentsMargins(0, 0, 0, 0)  # Quitar márgenes
            self.tbDepartamento.setCellWidget(index, 2, button_widget)

    def addItem_a_tabla(self, row, column, dato):
        dato_item = QTableWidgetItem(dato)
        dato_item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)  # No editable
        self.tbDepartamento.setItem(row, column, dato_item)

    def actualizarLabelPaginas(self, numPagina, totalPagina):
        self.lblNumeroPagina.setText(f"Pagina {numPagina} de {totalPagina}")

    def ActualizarValoresPaginado(self, paginaActual=1, totalPaginas=1):
        self.paginaActual = paginaActual
        self.ultimaPagina = totalPaginas
    # Configuración de botones de paginación
        if totalPaginas == 1:
            self.btnAnterior.setEnabled(False)
            self.btnAnterior.setStyleSheet(btnDisableStyleSheet)

            self.btnSiguiente.setEnabled(False)
            self.btnSiguiente.setStyleSheet(btnDisableStyleSheet)

            self.btnUltimaPagina.setEnabled(False)
            self.btnUltimaPagina.setStyleSheet(btnDisableStyleSheet)

            self.btnPrimerPagina.setEnabled(False)
            self.btnPrimerPagina.setStyleSheet(btnDisableStyleSheet)
        
        elif paginaActual == 1:
            self.btnAnterior.setEnabled(False)
            self.btnAnterior.setStyleSheet(btnDisableStyleSheet)
        
            self.btnPrimerPagina.setEnabled(False)
            self.btnPrimerPagina.setStyleSheet(btnDisableStyleSheet)
        
            self.btnSiguiente.setEnabled(True)
            self.btnSiguiente.setStyleSheet(btnStyleSheet)
        
            self.btnUltimaPagina.setEnabled(True)
            self.btnUltimaPagina.setStyleSheet(btnStyleSheet)
        
        elif paginaActual == totalPaginas:
            self.btnAnterior.setEnabled(True)
            self.btnAnterior.setStyleSheet(btnStyleSheet)
        
            self.btnPrimerPagina.setEnabled(True)
            self.btnPrimerPagina.setStyleSheet(btnStyleSheet)
        
            self.btnSiguiente.setEnabled(False)
            self.btnSiguiente.setStyleSheet(btnDisableStyleSheet)
        
            self.btnUltimaPagina.setEnabled(False)
            self.btnUltimaPagina.setStyleSheet(btnDisableStyleSheet)
        
        else:
            self.btnAnterior.setEnabled(True)
            self.btnAnterior.setStyleSheet(btnStyleSheet)
        
            self.btnPrimerPagina.setEnabled(True)
            self.btnPrimerPagina.setStyleSheet(btnStyleSheet)
        
            self.btnSiguiente.setEnabled(True)
            self.btnSiguiente.setStyleSheet(btnStyleSheet)
        
            self.btnUltimaPagina.setEnabled(True)
            self.btnUltimaPagina.setStyleSheet(btnStyleSheet)

    def irPrimeraPagina(self):
        self.paginaActual = 1
        self.llenarTabla()
    
    def irUltimaPagina(self):
        self.paginaActual = self.ultimaPagina
        self.llenarTabla()
        
    def irSiguientePagina(self):
         if (self.paginaActual + 1) <= self.ultimaPagina:
            self.paginaActual += 1
            self.llenarTabla()
    
    def irAnteriorPagina(self):
         if (self.paginaActual - 1) >= 1:
          self.paginaActual -= 1
         self.llenarTabla()
    
    def buscarDepartamento(self):
        input_busqueda = self.InputBusqueda.text()
        if input_busqueda:
            print("Texto: " + input_busqueda)
        else:
            MessageBox = QMessageBox()
            MessageBox.setWindowTitle("Advertencia de búsqueda")
            MessageBox.setText("Debes ingresar algún texto para poder realizar la búsqueda.")
            btn_ok = MessageBox.addButton(QMessageBox.Ok)
            MessageBox.setIcon(QMessageBox.Icon.Warning)
            MessageBox.setStyleSheet(mesboxStyleSheet)
            btn_ok.setStyleSheet(btnStyleSheet)
            response = MessageBox.exec()
            if response == QMessageBox.Ok:
                print("El usuario presionó OK")

    def eliminarRegistro(self, id):
        MessageBox = QMessageBox()
        MessageBox.setWindowTitle("Confirmar eliminación")
        MessageBox.setText("¿Estás seguro que quieres eliminar este departamento?")
        btn_ok = MessageBox.addButton(QMessageBox.Ok)
        btn_cancel = MessageBox.addButton(QMessageBox.Cancel)
        MessageBox.setIcon(QMessageBox.Icon.Question)
        MessageBox.setStyleSheet(mesboxStyleSheet)
        btn_ok.setStyleSheet(btnStyleSheet)
        btn_cancel.setStyleSheet(btnEliminarStyleSheet)
        btn_ok.setText("Sí")
        btn_cancel.setText("No")
        response = MessageBox.exec()
        if response == QMessageBox.Ok:
            Pservices = DepartamentoServices()
            result = Pservices.eliminarDepartamento(id)
        if result["success"]:
            MessageBox = QMessageBox()
            MessageBox.setWindowTitle("Confirmación de eliminación")
            MessageBox.setText("Departamento eliminado.")
            btn_ok = MessageBox.addButton(QMessageBox.Ok)
            MessageBox.setIcon(QMessageBox.Icon.Information)
            MessageBox.setStyleSheet(mesboxStyleSheet)
            btn_ok.setStyleSheet(btnStyleSheet)
            response = MessageBox.exec()
            if response == QMessageBox.Ok:
                self.paginaActual = 1
                self.llenarTabla()

    def crear_formulario_dialogo(self, lista=None):
        dialogo = QDialog(self)
        dialogo.setWindowTitle("Registrar Departamento")
        dialogo.setFixedSize(450, 300)
        dialogo.setStyleSheet(form_styleSheet)
    
        frame = QFrame(dialogo)
        form_layout = QFormLayout(frame)

        inputNombre = QLineEdit()
        inputNombre.setPlaceholderText("Ingrese el nombre del departamento")
        inputDescripcion = QTextEdit()
        inputDescripcion.setPlaceholderText("Ingrese la descripción del departamento")
        inputDescripcion.setFixedHeight(50)
    
        if lista:
            inputNombre.setText(lista["nombre"])
            inputDescripcion.setPlainText(lista["descripcion"])

        form_layout.addRow(QLabel("Nombre:"), inputNombre)
        form_layout.addRow(QLabel("Descripción:"), inputDescripcion)

        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.button(QDialogButtonBox.Ok).setStyleSheet(btnStyleSheet)
        button_box.button(QDialogButtonBox.Cancel).setStyleSheet(btnEliminarStyleSheet)
        button_box.button(QDialogButtonBox.Ok).setText("Guardar")
    
        button_box.accepted.connect(lambda: self.validar_campos(dialogo, inputNombre.text().strip(), inputDescripcion.toPlainText().strip()))
        button_box.rejected.connect(dialogo.reject)
    
        main_layout = QVBoxLayout()
        main_layout.addWidget(frame)
        main_layout.addWidget(button_box)
        dialogo.setLayout(main_layout)
    
        return dialogo, inputNombre, inputDescripcion

    def validar_campos(self, dialogo, inputNombre, inputDescripcion):
        if not inputNombre or not inputDescripcion:
            MessageBox = QMessageBox()
            MessageBox.setWindowTitle("Campos vacíos")
            MessageBox.setText("Por favor, complete todos los campos.")
            btn_ok = MessageBox.addButton(QMessageBox.Ok)
            MessageBox.setIcon(QMessageBox.Icon.Warning)
            MessageBox.setStyleSheet(mesboxStyleSheet)
            btn_ok.setStyleSheet(btnStyleSheet)
            MessageBox.exec()
        else:
            dialogo.accept()

    def abrir_formulario_modal(self):
        dialogo, inputNombre, inputDescripcion = self.crear_formulario_dialogo()
        if dialogo.exec_() == QDialog.Accepted:
            nombre = inputNombre.text()
            descripcion = inputDescripcion.toPlainText()
        
            departamento = Departamento(nombre, descripcion)
            result = self.Pservices.insertarDepartamento(departamento)
            if result["success"]:
                MessageBox = QMessageBox()
                MessageBox.setWindowTitle("Éxito")
                MessageBox.setText("El departamento se guardó correctamente.")
                btn_ok = MessageBox.addButton(QMessageBox.Ok)
                MessageBox.setIcon(QMessageBox.Icon.Information)
                MessageBox.setStyleSheet(mesboxStyleSheet)
                btn_ok.setStyleSheet(btnStyleSheet)
                MessageBox.exec()
                self.llenarTabla()
            else:
                MessageBox = QMessageBox()
                MessageBox.setWindowTitle("Error")
                MessageBox.setText("Error al guardar el departamento.")
                btn_ok = MessageBox.addButton(QMessageBox.Ok)
                MessageBox.setIcon(QMessageBox.Icon.Critical)
                MessageBox.setStyleSheet(mesboxStyleSheet)
                btn_ok.setStyleSheet(btnStyleSheet)
                MessageBox.exec()

    def editar_Departamento(self, fila, id):
        lista = self.obtenerDatosDeTabla(fila)
        dialogo, inputNombre, inputDescripcion = self.crear_formulario_dialogo(lista)
        if dialogo.exec_() == QDialog.Accepted:
            nombre = inputNombre.text()
            descripcion = inputDescripcion.toPlainText()
        
            departamento = Departamento(nombre, descripcion, id)
            result = self.Pservices.modificarDepartamento(departamento)
            if result["success"]:
                MessageBox = QMessageBox()
                MessageBox.setWindowTitle("Éxito")
                MessageBox.setText("Se guardó la nueva información correctamente.")
                btn_ok = MessageBox.addButton(QMessageBox.Ok)
                MessageBox.setIcon(QMessageBox.Icon.Information)
                MessageBox.setStyleSheet(mesboxStyleSheet)
                btn_ok.setStyleSheet(btnStyleSheet)
                response = MessageBox.exec()
                self.llenarTabla()
            else:
                MessageBox = QMessageBox()
                MessageBox.setWindowTitle("Error")
                MessageBox.setText("Error al guardar la nueva información del departamento.")
                btn_ok = MessageBox.addButton(QMessageBox.Ok)
                MessageBox.setIcon(QMessageBox.Icon.Critical)
                MessageBox.setStyleSheet(mesboxStyleSheet)
                btn_ok.setStyleSheet(btnStyleSheet)
                response = MessageBox.exec()

    def obtenerDatosDeTabla(self, fila):
        lista = {}
        lista["nombre"] = self.tbDepartamento.item(fila, 0).text()
        lista["descripcion"] = self.tbDepartamento.item(fila, 1).text()
        return lista

    def retranslateUi(self, departamentoInterfaz):
        departamentoInterfaz.setWindowTitle(QCoreApplication.translate("departamentoInterfaz", "Administración de Departamentos", None))
        self.btnConfigPag.setText(QCoreApplication.translate("departamentoInterfaz", "Configuración", None))
        self.label_3.setText(QCoreApplication.translate("departamentoInterfaz", "Avatar", None))
        self.lblNombrePagina.setText(QCoreApplication.translate("departamentoInterfaz", "Administración de Departamentos", None))
        self.label.setText(QCoreApplication.translate("departamentoInterfaz", "Acceso Biométrico de Empleados", None))
        self.btnRegresarMenu.setText(QCoreApplication.translate("departamentoInterfaz", "Menú", None))
        self.InputBusqueda.setPlaceholderText(QCoreApplication.translate("departamentoInterfaz", "Ingrese texto para buscar.", None))
        self.btnBuscar.setText(QCoreApplication.translate("departamentoInterfaz", "Buscar", None))
        self.btnCrearDepartamento.setText(QCoreApplication.translate("departamentoInterfaz", "Crear Departamento", None))
        self.btnPrimerPagina.setText(QCoreApplication.translate("departamentoInterfaz", "Primera Página", None))
        self.btnAnterior.setText(QCoreApplication.translate("departamentoInterfaz", "Anterior", None))
        self.btnSiguiente.setText(QCoreApplication.translate("departamentoInterfaz", "Siguiente", None))
        self.btnUltimaPagina.setText(QCoreApplication.translate("departamentoInterfaz", "Última Página", None))
