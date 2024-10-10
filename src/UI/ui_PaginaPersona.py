# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'PaginaPersonatpoIei.ui'
##
## Created by: Qt User Interface Compiler version 6.7.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QFrame, QGridLayout,
    QHBoxLayout, QHeaderView, QLabel, QLineEdit,
    QPushButton, QSizePolicy, QSpacerItem, QTableWidget,
    QTableWidgetItem, QVBoxLayout, QWidget)

class Ui_PaginaPersona(object):
    def setupUi(self, PaginaPersona):
        if not PaginaPersona.objectName():
            PaginaPersona.setObjectName(u"PaginaPersona")
        PaginaPersona.resize(1200, 800)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(PaginaPersona.sizePolicy().hasHeightForWidth())
        PaginaPersona.setSizePolicy(sizePolicy)
        PaginaPersona.setMinimumSize(QSize(600, 400))
        PaginaPersona.setMaximumSize(QSize(1200, 800))
        font = QFont()
        font.setBold(True)
        font.setStyleStrategy(QFont.PreferAntialias)
        PaginaPersona.setFont(font)
        PaginaPersona.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        PaginaPersona.setStyleSheet(u"background-color:rgb(255, 255, 255);\n"
"")
        self.frame = QFrame(PaginaPersona)
        self.frame.setObjectName(u"frame")
        self.frame.setGeometry(QRect(0, 0, 1201, 101))
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setStyleSheet(u" background-color: rgb(0, 0, 127); /* Color azul */\n"
" border-radius: 0px 0px 5px 5px; /* Bordes redondeados */\n"
" box-shadow: 10px 10px rgba(0, 0,0, 0.5); /* Sombra exterior */\n"
"")
        self.frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QFrame.Shadow.Sunken)
        self.frame.setLineWidth(5)
        self.gridLayoutWidget = QWidget(self.frame)
        self.gridLayoutWidget.setObjectName(u"gridLayoutWidget")
        self.gridLayoutWidget.setGeometry(QRect(0, 0, 1201, 104))
        self.gridLayout = QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(self.gridLayoutWidget)
        self.label.setObjectName(u"label")
        self.label.setEnabled(True)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        font1 = QFont()
        font1.setFamilies([u"Segoe UI"])
        font1.setPointSize(20)
        font1.setBold(True)
        font1.setItalic(False)
        font1.setKerning(True)
        font1.setStyleStrategy(QFont.PreferDefault)
        self.label.setFont(font1)
        self.label.setStyleSheet(u"background-color:transparent;/*rgb(0, 3, 206);*/\n"
"color:white;\n"
"font: 700 20pt \"Segoe UI\";")
        self.label.setTextFormat(Qt.TextFormat.AutoText)
        self.label.setScaledContents(True)
        self.label.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)
        self.label.setMargin(10)

        self.verticalLayout.addWidget(self.label)

        self.lblnombreVista = QLabel(self.gridLayoutWidget)
        self.lblnombreVista.setObjectName(u"lblnombreVista")
        self.lblnombreVista.setStyleSheet(u"background-color:transparent;\n"
"font: 700 12pt \"Segoe UI\";\n"
"color: white;")
        self.lblnombreVista.setFrameShadow(QFrame.Shadow.Plain)
        self.lblnombreVista.setLineWidth(0)
        self.lblnombreVista.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)
        self.lblnombreVista.setMargin(10)

        self.verticalLayout.addWidget(self.lblnombreVista)


        self.gridLayout.addLayout(self.verticalLayout, 1, 0, 1, 1)

        self.gridLayout_4 = QGridLayout()
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.horizontalSpacer_12 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_4.addItem(self.horizontalSpacer_12, 1, 2, 1, 1)

        self.horizontalSpacer_13 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_4.addItem(self.horizontalSpacer_13, 1, 0, 1, 1)

        self.horizontalSpacer_14 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_4.addItem(self.horizontalSpacer_14, 1, 4, 1, 1)

        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_4.addItem(self.verticalSpacer_3, 0, 1, 1, 1)

        self.lblAvatar = QLabel(self.gridLayoutWidget)
        self.lblAvatar.setObjectName(u"lblAvatar")
        sizePolicy.setHeightForWidth(self.lblAvatar.sizePolicy().hasHeightForWidth())
        self.lblAvatar.setSizePolicy(sizePolicy)

        self.gridLayout_4.addWidget(self.lblAvatar, 1, 1, 1, 1)

        self.btnConfigBar = QPushButton(self.gridLayoutWidget)
        self.btnConfigBar.setObjectName(u"btnConfigBar")
        sizePolicy.setHeightForWidth(self.btnConfigBar.sizePolicy().hasHeightForWidth())
        self.btnConfigBar.setSizePolicy(sizePolicy)

        self.gridLayout_4.addWidget(self.btnConfigBar, 1, 3, 1, 1)

        self.verticalSpacer_4 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_4.addItem(self.verticalSpacer_4, 2, 1, 1, 1)

        self.verticalSpacer_5 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_4.addItem(self.verticalSpacer_5, 2, 3, 1, 1)

        self.verticalSpacer_6 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_4.addItem(self.verticalSpacer_6, 0, 3, 1, 1)

        self.gridLayout_4.setColumnStretch(0, 1)
        self.gridLayout_4.setColumnStretch(1, 2)
        self.gridLayout_4.setColumnStretch(2, 1)
        self.gridLayout_4.setColumnStretch(3, 2)
        self.gridLayout_4.setColumnStretch(4, 1)

        self.gridLayout.addLayout(self.gridLayout_4, 1, 1, 1, 1)

        self.gridLayout.setColumnStretch(0, 5)
        self.gridLayout.setColumnStretch(1, 1)
        self.verticalLayoutWidget_2 = QWidget(PaginaPersona)
        self.verticalLayoutWidget_2.setObjectName(u"verticalLayoutWidget_2")
        self.verticalLayoutWidget_2.setGeometry(QRect(0, 100, 1201, 701))
        self.verticalLayout_2 = QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.frame_2 = QFrame(self.verticalLayoutWidget_2)
        self.frame_2.setObjectName(u"frame_2")
        sizePolicy.setHeightForWidth(self.frame_2.sizePolicy().hasHeightForWidth())
        self.frame_2.setSizePolicy(sizePolicy)
        self.frame_2.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_2.setFrameShadow(QFrame.Shadow.Sunken)
        self.frame_2.setLineWidth(12)
        self.frame_2.setMidLineWidth(5)
        self.horizontalLayoutWidget_2 = QWidget(self.frame_2)
        self.horizontalLayoutWidget_2.setObjectName(u"horizontalLayoutWidget_2")
        self.horizontalLayoutWidget_2.setGeometry(QRect(0, 550, 1201, 41))
        self.horizontalLayout_2 = QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)

        self.btnprimerpagina = QPushButton(self.horizontalLayoutWidget_2)
        self.btnprimerpagina.setObjectName(u"btnprimerpagina")
        self.btnprimerpagina.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btnprimerpagina.setStyleSheet(u"QPushButton {\n"
"    background-color: rgb(99, 118, 244); /* Color de fondo azul claro */\n"
"    color: white; /* Color del texto blanco */\n"
"    border: none; /* Sin borde */\n"
"    padding: 10px; /* Espaciado interno */\n"
"    border-radius: 5px; /* Bordes redondeados */\n"
"	font: 700 10pt \"Segoe UI\";\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: rgb(76, 64, 207); /* Color m\u00e1s oscuro al pasar el cursor */\n"
"}\n"
"\n"
"")

        self.horizontalLayout_2.addWidget(self.btnprimerpagina)

        self.btnanterior = QPushButton(self.horizontalLayoutWidget_2)
        self.btnanterior.setObjectName(u"btnanterior")
        self.btnanterior.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btnanterior.setStyleSheet(u"QPushButton {\n"
"    background-color: rgb(99, 118, 244); /* Color de fondo azul claro */\n"
"    color: white; /* Color del texto blanco */\n"
"    border: none; /* Sin borde */\n"
"    padding: 10px; /* Espaciado interno */\n"
"    border-radius: 5px; /* Bordes redondeados */\n"
"	font: 700 10pt \"Segoe UI\";\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: rgb(76, 64, 207); /* Color m\u00e1s oscuro al pasar el cursor */\n"
"}\n"
"\n"
"")

        self.horizontalLayout_2.addWidget(self.btnanterior)

        self.horizontalSpacer_10 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_10)

        self.lblnumeropagina = QLabel(self.horizontalLayoutWidget_2)
        self.lblnumeropagina.setObjectName(u"lblnumeropagina")
        font2 = QFont()
        font2.setPointSize(10)
        font2.setBold(True)
        self.lblnumeropagina.setFont(font2)

        self.horizontalLayout_2.addWidget(self.lblnumeropagina)

        self.horizontalSpacer_11 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_11)

        self.btnsiguiente = QPushButton(self.horizontalLayoutWidget_2)
        self.btnsiguiente.setObjectName(u"btnsiguiente")
        self.btnsiguiente.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btnsiguiente.setStyleSheet(u"QPushButton {\n"
"    background-color: rgb(99, 118, 244); /* Color de fondo azul claro */\n"
"    color: white; /* Color del texto blanco */\n"
"    border: none; /* Sin borde */\n"
"    padding: 10px; /* Espaciado interno */\n"
"    border-radius: 5px; /* Bordes redondeados */\n"
"	font: 700 10pt \"Segoe UI\";\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: rgb(76, 64, 207); /* Color m\u00e1s oscuro al pasar el cursor */\n"
"}\n"
"\n"
"")

        self.horizontalLayout_2.addWidget(self.btnsiguiente)

        self.btnultimapagina = QPushButton(self.horizontalLayoutWidget_2)
        self.btnultimapagina.setObjectName(u"btnultimapagina")
        self.btnultimapagina.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btnultimapagina.setStyleSheet(u"QPushButton {\n"
"    background-color: rgb(99, 118, 244); /* Color de fondo azul claro */\n"
"    color: white; /* Color del texto blanco */\n"
"    border: none; /* Sin borde */\n"
"    padding: 10px; /* Espaciado interno */\n"
"    border-radius: 5px; /* Bordes redondeados */\n"
"	font: 700 10pt \"Segoe UI\";\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: rgb(76, 64, 207); /* Color m\u00e1s oscuro al pasar el cursor */\n"
"}\n"
"\n"
"")

        self.horizontalLayout_2.addWidget(self.btnultimapagina)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)

        self.horizontalLayout_2.setStretch(0, 1)
        self.horizontalLayout_2.setStretch(8, 1)
        self.gridLayoutWidget_2 = QWidget(self.frame_2)
        self.gridLayoutWidget_2.setObjectName(u"gridLayoutWidget_2")
        self.gridLayoutWidget_2.setGeometry(QRect(0, 70, 1201, 481))
        self.gridLayout_2 = QGridLayout(self.gridLayoutWidget_2)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.tablaPersonas = QTableWidget(self.gridLayoutWidget_2)
        if (self.tablaPersonas.columnCount() < 8):
            self.tablaPersonas.setColumnCount(8)
        __qtablewidgetitem = QTableWidgetItem()
        self.tablaPersonas.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.tablaPersonas.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.tablaPersonas.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.tablaPersonas.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.tablaPersonas.setHorizontalHeaderItem(4, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.tablaPersonas.setHorizontalHeaderItem(5, __qtablewidgetitem5)
        __qtablewidgetitem6 = QTableWidgetItem()
        self.tablaPersonas.setHorizontalHeaderItem(6, __qtablewidgetitem6)
        __qtablewidgetitem7 = QTableWidgetItem()
        self.tablaPersonas.setHorizontalHeaderItem(7, __qtablewidgetitem7)
        if (self.tablaPersonas.rowCount() < 5):
            self.tablaPersonas.setRowCount(5)
        __qtablewidgetitem8 = QTableWidgetItem()
        self.tablaPersonas.setVerticalHeaderItem(0, __qtablewidgetitem8)
        __qtablewidgetitem9 = QTableWidgetItem()
        self.tablaPersonas.setVerticalHeaderItem(1, __qtablewidgetitem9)
        __qtablewidgetitem10 = QTableWidgetItem()
        self.tablaPersonas.setVerticalHeaderItem(2, __qtablewidgetitem10)
        __qtablewidgetitem11 = QTableWidgetItem()
        self.tablaPersonas.setVerticalHeaderItem(3, __qtablewidgetitem11)
        __qtablewidgetitem12 = QTableWidgetItem()
        self.tablaPersonas.setItem(4, 0, __qtablewidgetitem12)
        __qtablewidgetitem13 = QTableWidgetItem()
        self.tablaPersonas.setItem(4, 1, __qtablewidgetitem13)
        __qtablewidgetitem14 = QTableWidgetItem()
        self.tablaPersonas.setItem(4, 2, __qtablewidgetitem14)
        __qtablewidgetitem15 = QTableWidgetItem()
        self.tablaPersonas.setItem(4, 3, __qtablewidgetitem15)
        self.tablaPersonas.setObjectName(u"tablaPersonas")
        self.tablaPersonas.setEnabled(True)
        self.tablaPersonas.viewport().setProperty(u"cursor", QCursor(Qt.CursorShape.ArrowCursor))
        self.tablaPersonas.setMouseTracking(True)
        self.tablaPersonas.setStyleSheet(u"QTableWidget {\n"
"    background-color: white; /* Celeste */\n"
"    border: 2px solid #007acc; /* Borde del contenedor de la tabla */\n"
"    border-radius: 20px; /* Esquinas redondeadas */\n"
"    box-shadow: 5px 5px 10px rgba(0, 0, 0, 0.3); /* Sombra exterior */\n"
"}\n"
"\n"
"QHeaderView::section {\n"
"    background-color: rgb(38, 76, 182); /* Color del encabezado */\n"
"    color: white; /* Color del texto del encabezado */\n"
"    padding: 10px; /* Espaciado interno del encabezado */\n"
"	font: 700 10pt \"Segoe UI\";\n"
"}\n"
"")
        self.tablaPersonas.setFrameShape(QFrame.Shape.NoFrame)
        self.tablaPersonas.setFrameShadow(QFrame.Shadow.Sunken)
        self.tablaPersonas.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.tablaPersonas.setProperty(u"showDropIndicator", True)
        self.tablaPersonas.setDragDropOverwriteMode(False)
        self.tablaPersonas.setAlternatingRowColors(True)
        self.tablaPersonas.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        self.tablaPersonas.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.tablaPersonas.setVerticalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)
        self.tablaPersonas.setHorizontalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)
        self.tablaPersonas.horizontalHeader().setCascadingSectionResizes(False)
        self.tablaPersonas.horizontalHeader().setDefaultSectionSize(117)
        self.tablaPersonas.horizontalHeader().setHighlightSections(False)
        self.tablaPersonas.horizontalHeader().setProperty(u"showSortIndicator", False)
        self.tablaPersonas.horizontalHeader().setStretchLastSection(True)
        self.tablaPersonas.verticalHeader().setVisible(False)
        self.tablaPersonas.verticalHeader().setCascadingSectionResizes(False)
        self.tablaPersonas.verticalHeader().setStretchLastSection(False)

        self.gridLayout_2.addWidget(self.tablaPersonas, 2, 1, 1, 1)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_2.addItem(self.verticalSpacer_2, 3, 1, 1, 1)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer_3, 2, 2, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_2.addItem(self.verticalSpacer, 1, 1, 1, 1)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer_4, 2, 0, 1, 1)

        self.gridLayout_2.setRowStretch(1, 1)
        self.gridLayout_2.setRowStretch(2, 10)
        self.gridLayout_2.setRowStretch(3, 1)
        self.gridLayout_2.setColumnStretch(0, 1)
        self.gridLayout_2.setColumnStretch(1, 10)
        self.gridLayout_2.setColumnStretch(2, 1)
        self.horizontalLayoutWidget_3 = QWidget(self.frame_2)
        self.horizontalLayoutWidget_3.setObjectName(u"horizontalLayoutWidget_3")
        self.horizontalLayoutWidget_3.setGeometry(QRect(0, 0, 1201, 71))
        self.horizontalLayout_3 = QHBoxLayout(self.horizontalLayoutWidget_3)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_5)

        self.ir_menu = QPushButton(self.horizontalLayoutWidget_3)
        self.ir_menu.setObjectName(u"ir_menu")
        self.ir_menu.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.ir_menu.setStyleSheet(u"QPushButton {\n"
"    background-color: rgb(99, 118, 244); /* Color de fondo azul claro */\n"
"    color: white; /* Color del texto blanco */\n"
"    border: none; /* Sin borde */\n"
"    padding: 10px; /* Espaciado interno */\n"
"    border-radius: 5px; /* Bordes redondeados */\n"
"	font: 700 10pt \"Segoe UI\";\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: rgb(76, 64, 207); /* Color m\u00e1s oscuro al pasar el cursor */\n"
"}")

        self.horizontalLayout_3.addWidget(self.ir_menu)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_6)

        self.inputbuscar = QLineEdit(self.horizontalLayoutWidget_3)
        self.inputbuscar.setObjectName(u"inputbuscar")
        font3 = QFont()
        font3.setPointSize(10)
        self.inputbuscar.setFont(font3)
        self.inputbuscar.setStyleSheet(u" QLineEdit {\n"
"        background-color: rgb(247, 248, 255);\n"
"        color: rgb(0, 0, 0);\n"
"        border: 2px solid rgb(60, 0, 188);\n"
"        padding: 5px;\n"
"        border-radius: 10px;\n"
"		\n"
"    }\n"
"\n"
"    QLineEdit:focus {\n"
"        border: 2px solid darkblue;\n"
"    }\n"
"")

        self.horizontalLayout_3.addWidget(self.inputbuscar)

        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_7)

        self.btnbuscar = QPushButton(self.horizontalLayoutWidget_3)
        self.btnbuscar.setObjectName(u"btnbuscar")
        self.btnbuscar.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btnbuscar.setStyleSheet(u"QPushButton {\n"
"    background-color: rgb(99, 118, 244); /* Color de fondo azul claro */\n"
"    color: white; /* Color del texto blanco */\n"
"    border: none; /* Sin borde */\n"
"    padding: 10px; /* Espaciado interno */\n"
"    border-radius: 15px; /* Bordes redondeados */\n"
"	font: 700 10pt \"Segoe UI\";\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: rgb(76, 64, 207); /* Color m\u00e1s oscuro al pasar el cursor */\n"
"}")

        self.horizontalLayout_3.addWidget(self.btnbuscar)

        self.horizontalSpacer_8 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_8)

        self.btncrear = QPushButton(self.horizontalLayoutWidget_3)
        self.btncrear.setObjectName(u"btncrear")
        self.btncrear.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btncrear.setStyleSheet(u"QPushButton {\n"
"    background-color: rgb(0, 185, 77); /* Color de fondo azul claro */\n"
"    color: white; /* Color del texto blanco */\n"
"    border: none; /* Sin borde */\n"
"    padding: 10px; /* Espaciado interno */\n"
"    border-radius: 15px; /* Bordes redondeados */\n"
"	font: 700 10pt \"Segoe UI\";\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: rgb(0, 214, 50); /* Color m\u00e1s oscuro al pasar el cursor */\n"
"}")

        self.horizontalLayout_3.addWidget(self.btncrear)

        self.horizontalSpacer_9 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_9)

        self.horizontalLayout_3.setStretch(0, 1)
        self.horizontalLayout_3.setStretch(2, 4)
        self.horizontalLayout_3.setStretch(3, 6)
        self.horizontalLayout_3.setStretch(5, 2)
        self.horizontalLayout_3.setStretch(6, 2)
        self.horizontalLayout_3.setStretch(7, 2)
        self.horizontalLayout_3.setStretch(8, 2)

        self.verticalLayout_2.addWidget(self.frame_2)


        self.retranslateUi(PaginaPersona)

        QMetaObject.connectSlotsByName(PaginaPersona)
    # setupUi

    def retranslateUi(self, PaginaPersona):
        PaginaPersona.setWindowTitle(QCoreApplication.translate("PaginaPersona", u"Acceso Biometrico de Empleados", None))
        self.label.setText(QCoreApplication.translate("PaginaPersona", u"Acceso Biometrico de Empleados", None))
        self.lblnombreVista.setText(QCoreApplication.translate("PaginaPersona", u"Registros de Personas", None))
        self.lblAvatar.setText(QCoreApplication.translate("PaginaPersona", u"Avatar", None))
        self.btnConfigBar.setText(QCoreApplication.translate("PaginaPersona", u"Boto", None))
        self.btnprimerpagina.setText(QCoreApplication.translate("PaginaPersona", u"Primera pagina", None))
        self.btnanterior.setText(QCoreApplication.translate("PaginaPersona", u"Anterior", None))
        self.lblnumeropagina.setText(QCoreApplication.translate("PaginaPersona", u"Pagina 1", None))
        self.btnsiguiente.setText(QCoreApplication.translate("PaginaPersona", u"Siguiente", None))
        self.btnultimapagina.setText(QCoreApplication.translate("PaginaPersona", u"Ultima pagina", None))
        ___qtablewidgetitem = self.tablaPersonas.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("PaginaPersona", u"Nombre", None));
        ___qtablewidgetitem1 = self.tablaPersonas.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("PaginaPersona", u"1\u00b0 Apellido", None));
        ___qtablewidgetitem2 = self.tablaPersonas.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("PaginaPersona", u"2\u00b0 Apellido", None));
        ___qtablewidgetitem3 = self.tablaPersonas.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("PaginaPersona", u"Cedula", None));
        ___qtablewidgetitem4 = self.tablaPersonas.horizontalHeaderItem(4)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("PaginaPersona", u"Nacimiento", None));
        ___qtablewidgetitem5 = self.tablaPersonas.horizontalHeaderItem(5)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("PaginaPersona", u"Correo", None));
        ___qtablewidgetitem6 = self.tablaPersonas.horizontalHeaderItem(6)
        ___qtablewidgetitem6.setText(QCoreApplication.translate("PaginaPersona", u"Estado Civil", None));
        ___qtablewidgetitem7 = self.tablaPersonas.horizontalHeaderItem(7)
        ___qtablewidgetitem7.setText(QCoreApplication.translate("PaginaPersona", u"Direccion", None));
        ___qtablewidgetitem8 = self.tablaPersonas.verticalHeaderItem(0)
        ___qtablewidgetitem8.setText(QCoreApplication.translate("PaginaPersona", u"Nueva fila", None));
        ___qtablewidgetitem9 = self.tablaPersonas.verticalHeaderItem(1)
        ___qtablewidgetitem9.setText(QCoreApplication.translate("PaginaPersona", u"Nueva fila", None));
        ___qtablewidgetitem10 = self.tablaPersonas.verticalHeaderItem(2)
        ___qtablewidgetitem10.setText(QCoreApplication.translate("PaginaPersona", u"Nueva fila", None));
        ___qtablewidgetitem11 = self.tablaPersonas.verticalHeaderItem(3)
        ___qtablewidgetitem11.setText(QCoreApplication.translate("PaginaPersona", u"Nueva fila", None));

        __sortingEnabled = self.tablaPersonas.isSortingEnabled()
        self.tablaPersonas.setSortingEnabled(False)
        self.tablaPersonas.setSortingEnabled(__sortingEnabled)

        self.ir_menu.setText(QCoreApplication.translate("PaginaPersona", u"Ir al menu", None))
        self.inputbuscar.setPlaceholderText(QCoreApplication.translate("PaginaPersona", u"Ingrese algun texto para buscar", None))
        self.btnbuscar.setText(QCoreApplication.translate("PaginaPersona", u"Buscar", None))
        self.btncrear.setText(QCoreApplication.translate("PaginaPersona", u"Crear", None))
    # retranslateUi

