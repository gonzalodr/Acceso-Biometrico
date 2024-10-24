# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'personaInterfazpakdMI.ui'
##
## Created by: Qt User Interface Compiler version 6.7.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################
import sys
from services.personaService import PersonaServices
from UI.stilosInterfaz import (btnStyleSheet,btnEliminarStyleSheet,LineEditStyleSheet,
                               tableStyleSheet,mesboxStyleSheet,
                               btnDisableStyleSheet,
                               form_styleSheet)
from models.persona import Persona


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

class Ui_personaInterfaz(object):
    paginaActual = 1
    ultimaPagina = 1
    busqueda = None
    Pservices = PersonaServices()
    
    def setupUi(self, personaInterfaz):
        if not personaInterfaz.objectName():
            personaInterfaz.setObjectName(u"personaInterfaz")
        personaInterfaz.resize(1200, 800)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(personaInterfaz.sizePolicy().hasHeightForWidth())
        personaInterfaz.setSizePolicy(sizePolicy)
        personaInterfaz.setMinimumSize(QSize(600, 400))
        personaInterfaz.setMaximumSize(QSize(1200, 800))
        personaInterfaz.setStyleSheet(u"background-color:#FFFFFF;")

        self.verticalLayoutWidget = QWidget(personaInterfaz)
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

        #Boton de configuracion de la pagina
        self.btnConfigPag = QPushButton(self.gridLayoutWidget)
        self.btnConfigPag.setObjectName(u"btnConfigPag")
        sizePolicy.setHeightForWidth(self.btnConfigPag.sizePolicy().hasHeightForWidth())
        self.btnConfigPag.setSizePolicy(sizePolicy)
        self.gridLayoutEncabezado_2.addWidget(self.btnConfigPag, 1, 2, 1, 1)

        #Avatar del usuario
        self.label_3 = QLabel(self.gridLayoutWidget)
        self.label_3.setObjectName(u"label_3")
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        self.gridLayoutEncabezado_2.addWidget(self.label_3, 0, 2, 1, 1)

        #Encabezado de la pagina nombre de la pagina en la que se ubica
        self.lblNombrePagina = QLabel(self.gridLayoutWidget)
        self.lblNombrePagina.setObjectName(u"lblNombrePagina")
        self.lblNombrePagina.setStyleSheet(u"font: 700 16pt \"Segoe UI\";color: #FFFFFF")
        self.lblNombrePagina.setIndent(10)
        self.gridLayoutEncabezado_2.addWidget(self.lblNombrePagina, 1, 0,1,1)

        #Nombre de la pagina nombre de la aplicacion
        self.label = QLabel(self.gridLayoutWidget)
        self.label.setObjectName(u"label")
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setStyleSheet(u"font: 700 24pt \"Segoe UI\";color:#FFFFFF;")
        self.label.setIndent(10)
        self.gridLayoutEncabezado_2.addWidget(self.label, 0, 0, 1, 1)


        #Espaciadores entre los labels del encabezados y el avatar y boton de configuracion
        self.horizontalSpacer_8 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.gridLayoutEncabezado_2.addItem(self.horizontalSpacer_8, 0, 1, 1, 1)

        self.horizontalSpacer_9 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.gridLayoutEncabezado_2.addItem(self.horizontalSpacer_9, 1, 1, 1, 1)

        #Configuracion de tamaños de los elementos, labels del encabezado, avatar y btnConfig
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

        self.btnCrearPersona = QPushButton(self.verticalLayoutWidget_2)
        self.btnCrearPersona.setObjectName(u"btnCrearPersona")
        self.btnCrearPersona.setStyleSheet(btnStyleSheet)
        self.hLayoutCuerpo.addWidget(self.btnCrearPersona)

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


        self.tbPersona = QTableWidget(self.verticalLayoutWidget_2)
        if (self.tbPersona.columnCount() < 9):
            self.tbPersona.setColumnCount(9)
        # Definir los nombres de las cabeceras directamente
        header_labels = ["Nombre", "1° Apellido", "2° Apellido", "Cedula", "Correo", "Nacimiento", "Estado civil", "Dirección","Acciones"]
        self.tbPersona.setHorizontalHeaderLabels(header_labels)
        self.tbPersona.setAlternatingRowColors(True)
        
        self.tbPersona.setObjectName(u"tbPersona")
        self.tbPersona.setStyleSheet(tableStyleSheet)
        self.tbPersona.horizontalHeader().setCascadingSectionResizes(True)
        self.tbPersona.horizontalHeader().setHighlightSections(True)
        self.tbPersona.horizontalHeader().setStretchLastSection(True)
        self.tbPersona.verticalHeader().setVisible(False)
        self.tbPersona.verticalHeader().setHighlightSections(False)
        self.gridLayoutCuerpo_3.addWidget(self.tbPersona, 1, 1, 1,1)

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

        ## Botones
        self.btnBuscar.clicked.connect(self.buscarPersona)
        self.btnAnterior.clicked.connect(self.irAnteriorPagina)
        self.btnSiguiente.clicked.connect(self.irSiguientePagina)
        self.btnUltimaPagina.clicked.connect(self.irUltimaPagina)
        self.btnPrimerPagina.clicked.connect(self.irPrimeraPagina)
        self.btnCrearPersona.clicked.connect(self.abrir_formulario_modal)
        self.llenarTabla()

        self.retranslateUi(personaInterfaz)
        QMetaObject.connectSlotsByName(personaInterfaz)
    # setupUi

    def llenarTabla(self):
        Pservices = PersonaServices()
        resultado = Pservices.obtenerListaPersonas(self.paginaActual,10,tipo_orden="DESC",busqueda = self.busqueda)
        if resultado["success"]:
            listaPersona = resultado["data"]["listaPersonas"]
            paginaActual = resultado["data"]["pagina_actual"]
            tamPagina = resultado["data"]["tam_pagina"]
            totalPaginas = resultado["data"]["total_paginas"]
            totalRegistros = resultado["data"]["total_registros"]
            
            self.actualizarLabelPaginas(paginaActual,totalPaginas)
            self.ActualizarValoresPaginado(paginaActual,totalPaginas)
            
            #Limpiamos las filas 
            self.tbPersona.setRowCount(0) 
            
            for index, persona in enumerate(listaPersona):
                self.tbPersona.insertRow(index)  # Crea una fila por registro
                self.tbPersona.setRowHeight(index,45)
                
                self.addItem_a_tabla(index,0,persona.nombre)
                self.addItem_a_tabla(index,1,persona.apellido1)
                self.addItem_a_tabla(index,2,persona.apellido2)
                self.addItem_a_tabla(index,3,persona.cedula)
                self.addItem_a_tabla(index,4,persona.correo)
                self.addItem_a_tabla(index,5,str(persona.fecha_nacimiento))         
                self.addItem_a_tabla(index,6,persona.estado_civil)  
                self.addItem_a_tabla(index,7,persona.direccion)
                
                #Colocacion de botones de eliminacion y edicion
                btnEliminar = QPushButton("Eliminar")
                btnEliminar.setStyleSheet(btnEliminarStyleSheet)
                btnEliminar.clicked.connect(lambda checked, idx=persona.id: self.eliminarRegistro(idx))
                btnEliminar.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Fixed)
                
                btnEditar = QPushButton("Editar")
                btnEditar.setStyleSheet(btnStyleSheet)
                btnEditar.clicked.connect(lambda checked, fila=index,idx = persona.id: self.editar_Persona(fila,idx))
                btnEditar.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
                button_widget = QWidget()
                button_widget.setStyleSheet(u"background-color:transparent;")
                button_widget.setFixedSize(140,40) 
                layout = QHBoxLayout(button_widget)
                layout.addWidget(btnEditar)
                layout.addWidget(btnEliminar)
                layout.setAlignment(Qt.AlignCenter)  # Centrar el botón
                layout.setContentsMargins(0, 0, 0, 0)  # Quitar márgenes
                self.tbPersona.setCellWidget(index, 8, button_widget) 
        
    def addItem_a_tabla(self,row, colum,dato):
        dato_item = QTableWidgetItem(dato)
        dato_item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)  # No editable
        self.tbPersona.setItem(row, colum, dato_item)
        
    def actualizarLabelPaginas(self,numPagina, totalPagina):
        self.lblNumeroPagina.setText(f"Pagina {numPagina} de {totalPagina} ")

    def ActualizarValoresPaginado(self,paginaActual = 1, totalPaginas = 1):
        self.paginaActual = paginaActual
        self.ultimaPagina = totalPaginas
        ## Valores necesarios para las paginacion:
        if totalPaginas <= 1:
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
        if (self.paginaActual+1) <= self.ultimaPagina:
            self.paginaActual = self.paginaActual+1
            self.llenarTabla()
    
    def irAnteriorPagina(self):
        if (self.paginaActual - 1) >= 1:
            self.paginaActual = self.paginaActual-1
            self.llenarTabla()
    
    def buscarPersona(self):
        input_busqueda = self.InputBusqueda.text();
        if input_busqueda:
            self.busqueda = input_busqueda
            self.InputBusqueda.clear()
            self.llenarTabla()
            self.busqueda = None
        else:
            self.paginaActual = 1
            self.llenarTabla()      
            
    def eliminarRegistro(self,id):
        MessageBox = QMessageBox()
        MessageBox.setWindowTitle("Confirmar eliminacion")
        MessageBox.setText("¿Estas seguro que quieres eliminar esta persona?")
        btn_ok = MessageBox.addButton(QMessageBox.Ok)
        btn_cancel = MessageBox.addButton(QMessageBox.Cancel)
        MessageBox.setIcon(QMessageBox.Icon.Question)
        MessageBox.setStyleSheet(mesboxStyleSheet)
        btn_ok.setStyleSheet(btnStyleSheet)
        btn_cancel.setStyleSheet(btnEliminarStyleSheet)
        btn_ok.setText("Si")
        btn_cancel.setText("No")
        # Mostrar el QMessageBox y obtener la respuesta del usuario
        response = MessageBox.exec()
        if response == QMessageBox.Ok:
            Pservices = PersonaServices()
            result = Pservices.eliminarPersona(id)
            if result["success"]:
                MessageBox = QMessageBox()
                MessageBox.setWindowTitle("Confirmacion de eliminación")
                MessageBox.setText("Persona eliminada.")
                btn_ok = MessageBox.addButton(QMessageBox.Ok)
                MessageBox.setIcon(QMessageBox.Icon.Information)
                MessageBox.setStyleSheet(mesboxStyleSheet)
                btn_ok.setStyleSheet(btnStyleSheet)
                response = MessageBox.exec()
                if response == QMessageBox.Ok:
                    self.paginaActual = 1
                    self.llenarTabla()

    def crear_formulario_dialogo(self, lista = None,Titulo_ventana ="Registrar persona", label_titulo = "Registrar"):
        # Crear el diálogo
        dialogo = QDialog(self)
        dialogo.setWindowTitle(Titulo_ventana)
        dialogo.setFixedSize(500, 500)  # Tamaño fijo del modal
        dialogo.setStyleSheet(form_styleSheet)
    
        # Frame que contiene el formulario
        frame = QFrame(dialogo)
        form_layout = QFormLayout(frame)
        # Campos del formulario con placeholders
        inputNombre = QLineEdit()
        inputNombre.setPlaceholderText("Ingrese su nombre")
        inputApellido1 = QLineEdit()
        inputApellido1.setPlaceholderText("Ingrese su primer apellido")
        inputApellido2 = QLineEdit()
        inputApellido2.setPlaceholderText("Ingrese su segundo apellido")
        inputCedula = QLineEdit()
        inputCedula.setPlaceholderText("Ingrese su cédula")
        inputNacimiento = QDateEdit()
        inputNacimiento.setCalendarPopup(True)
        inputNacimiento.setDisplayFormat("yyyy-MM-dd")
        inputNacimiento.setMaximumDate(QDate.currentDate())  # Limita la fecha al día actual
        inputCorreo = QLineEdit()
        inputCorreo.setPlaceholderText("Ingrese su correo electrónico. Ejem: persona@example.com")
        inputEstCivil = QComboBox()
        inputEstCivil.addItems(["Soltero/a", "Casado/a", "Divorciado/a", "Viudo/a"])
        inputDireccion = QTextEdit()
        inputDireccion.setPlaceholderText("Ingrese su dirección completa")
        inputDireccion.setFixedHeight(50)
        
        if lista != None:
            inputNombre.setText(lista["nombre"])
            inputApellido1.setText(lista["apellido1"])
            inputApellido2.setText(lista["apellido2"])
            inputNacimiento.setDate(QDate.fromString(lista["fecha"], "yyyy-MM-dd"))
            inputCedula.setText(lista["cedula"])
            inputCorreo.setText(lista["correo"])
            inputDireccion.setPlainText(lista["direccion"])
            inputEstCivil.setCurrentText(lista["estadoCivil"])

        # Agregar campos al layout del formulario
        form_layout.addRow(QLabel("Nombre:"), inputNombre)
        form_layout.addRow(QLabel("Primer Apellido:"), inputApellido1)
        form_layout.addRow(QLabel("Segundo Apellido:"), inputApellido2)
        form_layout.addRow(QLabel("Cédula:"), inputCedula)
        form_layout.addRow(QLabel("Fecha de Nacimiento:"), inputNacimiento)
        form_layout.addRow(QLabel("Correo:"), inputCorreo)
        form_layout.addRow(QLabel("Estado Civil:"), inputEstCivil)
        form_layout.addRow(QLabel("Dirección:"), inputDireccion)

        # Botones del diálogo (Aceptar y Cancelar)
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.button(QDialogButtonBox.Ok).setStyleSheet(btnStyleSheet)
        button_box.button(QDialogButtonBox.Cancel).setStyleSheet(btnEliminarStyleSheet)
        button_box.button(QDialogButtonBox.Ok).setText("Guardar")
        
        button_box.accepted.connect(lambda: self.validar_campos(dialogo, inputNombre.text().strip(), 
                                    inputApellido1.text().strip(),inputApellido2.text().strip()
                                    , inputCedula.text().strip(),inputNacimiento.date().toString("yyyy-MM-dd"), inputCorreo.text().strip(),
                                    inputEstCivil.currentText(), inputDireccion.toPlainText().strip()))
        
        button_box.rejected.connect(dialogo.reject)
        
        # Layout principal del diálogo
        main_layout = QVBoxLayout()
        main_layout.addWidget(frame)
        main_layout.addWidget(button_box)
        dialogo.setLayout(main_layout)
        
        return dialogo, inputNombre, inputApellido1, inputApellido2, inputCedula, inputNacimiento, inputCorreo, inputEstCivil, inputDireccion

    def validar_campos(self,dialogo, inputNombre, inputApellido1, inputApellido2, inputCedula, inputNacimiento, inputCorreo, inputEstCivil, inputDireccion):
        # Verifica si los campos requeridos están vacíos
        if not inputNombre or not inputApellido1 or not inputApellido2 or not inputNacimiento or not inputCedula or not inputCorreo or not inputEstCivil or not inputDireccion or not inputCedula or not inputCorreo:
            MessageBox = QMessageBox()
            MessageBox.setWindowTitle("Campos vacios")
            MessageBox.setText("Porfavor, complete todos los campos.")
            btn_ok = MessageBox.addButton(QMessageBox.Ok)
            MessageBox.setIcon(QMessageBox.Icon.Warning)
            MessageBox.setStyleSheet(mesboxStyleSheet)
            btn_ok.setStyleSheet(btnStyleSheet)
            response = MessageBox.exec()
        else:
            result = self.Pservices.verificacionCorreo(inputCorreo) 
            if not result["success"]:
                MessageBox = QMessageBox()
                MessageBox.setWindowTitle("Correo no valido")
                MessageBox.setText(result["message"])
                btn_ok = MessageBox.addButton(QMessageBox.Ok)
                MessageBox.setIcon(QMessageBox.Icon.Warning)
                MessageBox.setStyleSheet(mesboxStyleSheet)
                btn_ok.setStyleSheet(btnStyleSheet)
                response = MessageBox.exec()
            else:
                dialogo.accept()

    def abrir_formulario_modal(self):
        dialogo, inputNombre, inputApellido1, inputApellido2, inputCedula, inputNacimiento, inputCorreo, inputEstCivil, inputDireccion = self.crear_formulario_dialogo()
        if dialogo.exec_() == QDialog.Accepted:
            nombre = inputNombre.text()
            apellido1 = inputApellido1.text()
            apellido2 = inputApellido2.text()
            cedula = inputCedula.text()
            fecha_nacimiento = inputNacimiento.date().toString("yyyy-MM-dd")
            correo = inputCorreo.text()
            estado_civil = inputEstCivil.currentText()
            direccion = inputDireccion.toPlainText()
            
            persona = Persona(nombre,apellido1,apellido2,fecha_nacimiento,cedula,estado_civil,correo,direccion)            
            result = self.Pservices.insertarPersona(persona)
            print(result)
            if result["success"]:
                MessageBox = QMessageBox()
                MessageBox.setWindowTitle("Exito")
                MessageBox.setText("La persona se guardo correctamente.")
                btn_ok = MessageBox.addButton(QMessageBox.Ok)
                MessageBox.setIcon(QMessageBox.Icon.Information)
                MessageBox.setStyleSheet(mesboxStyleSheet)
                btn_ok.setStyleSheet(btnStyleSheet)
                # Mostrar el QMessageBox y obtener la respuesta del usuario
                response = MessageBox.exec()
                self.llenarTabla()
            else:
                MessageBox = QMessageBox()
                MessageBox.setWindowTitle("Error")
                MessageBox.setText("Error al guardar al persona.")
                btn_ok = MessageBox.addButton(QMessageBox.Ok)
                MessageBox.setIcon(QMessageBox.Icon.Critical)
                MessageBox.setStyleSheet(mesboxStyleSheet)
                btn_ok.setStyleSheet(btnStyleSheet)
                # Mostrar el QMessageBox y obtener la respuesta del usuario
                response = MessageBox.exec()
            
    def editar_Persona(self, fila, id):
        lista = self.obtenerDatosDeTabla(fila)
        dialogo, inputNombre, inputApellido1, inputApellido2, inputCedula, inputNacimiento, inputCorreo, inputEstCivil, inputDireccion = self.crear_formulario_dialogo(lista,"Editar registro")
        if dialogo.exec_() == QDialog.Accepted:
            nombre = inputNombre.text()
            apellido1 = inputApellido1.text()
            apellido2 = inputApellido2.text()
            cedula = inputCedula.text()
            fecha_nacimiento = inputNacimiento.date().toString("yyyy-MM-dd")
            correo = inputCorreo.text()
            estado_civil = inputEstCivil.currentText()
            direccion = inputDireccion.toPlainText()
            
            persona = Persona(nombre,apellido1,apellido2,fecha_nacimiento,cedula,estado_civil,correo,direccion,id)            
            result = self.Pservices.modificarPersona(persona)
            if result["success"]:
                MessageBox = QMessageBox()
                MessageBox.setWindowTitle("Exito")
                MessageBox.setText("Se guardo la nueva\ninformacion correctamente.")
                btn_ok = MessageBox.addButton(QMessageBox.Ok)
                MessageBox.setIcon(QMessageBox.Icon.Information)
                MessageBox.setStyleSheet(mesboxStyleSheet)
                btn_ok.setStyleSheet(btnStyleSheet)
                # Mostrar el QMessageBox y obtener la respuesta del usuario
                response = MessageBox.exec()
                self.llenarTabla()
            else:
                MessageBox = QMessageBox()
                MessageBox.setWindowTitle("Error")
                MessageBox.setText("Error al guardar la nueva\ninformacion de la persona.")
                btn_ok = MessageBox.addButton(QMessageBox.Ok)
                MessageBox.setIcon(QMessageBox.Icon.Critical)
                MessageBox.setStyleSheet(mesboxStyleSheet)
                btn_ok.setStyleSheet(btnStyleSheet)
                # Mostrar el QMessageBox y obtener la respuesta del usuario
                response = MessageBox.exec()
        
    def obtenerDatosDeTabla(self,fila):
        lista = {}
        lista["nombre"] = self.tbPersona.item(fila, 0).text()
        lista["apellido1"] = self.tbPersona.item(fila, 1).text()
        lista["apellido2"] = self.tbPersona.item(fila, 2).text()
        lista["cedula"] = self.tbPersona.item(fila, 3).text()
        lista["correo"] = self.tbPersona.item(fila,4).text()
        lista["fecha"] = self.tbPersona.item(fila,5).text()
        lista["estadoCivil"] = self.tbPersona.item(fila,6).text()
        lista["direccion"] = self.tbPersona.item(fila,7).text()
        return lista

    def retranslateUi(self, personaInterfaz):
        personaInterfaz.setWindowTitle(QCoreApplication.translate("personaInterfaz", u"Form", None))
        self.btnConfigPag.setText(QCoreApplication.translate("personaInterfaz", u"PushButton", None))
        self.label_3.setText(QCoreApplication.translate("personaInterfaz", u"Avatar", None))
        self.lblNombrePagina.setText(QCoreApplication.translate("personaInterfaz", u"Administracion de personas", None))
        self.label.setText(QCoreApplication.translate("personaInterfaz", u"Acceso Biometrico de Empleados", None))
        self.btnRegresarMenu.setText(QCoreApplication.translate("personaInterfaz", u"Menu", None))
        self.InputBusqueda.setPlaceholderText(QCoreApplication.translate("personaInterfaz", u"Ingrese algun texto para buscar.", None))
        self.btnBuscar.setText(QCoreApplication.translate("personaInterfaz", u"Buscar", None))
        self.btnCrearPersona.setText(QCoreApplication.translate("personaInterfaz", u"Crear persona", None))
        self.btnPrimerPagina.setText(QCoreApplication.translate("personaInterfaz", u"Primer pagina", None))
        self.btnAnterior.setText(QCoreApplication.translate("personaInterfaz", u"Anterior", None))
        self.btnSiguiente.setText(QCoreApplication.translate("personaInterfaz", u"Siguiente", None))
        self.btnUltimaPagina.setText(QCoreApplication.translate("personaInterfaz", u"Ultima pagina", None))
    # retranslateUi
