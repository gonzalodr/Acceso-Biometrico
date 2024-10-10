# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Prueba.ui'
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
from PySide6.QtWidgets import (QApplication, QHeaderView, QLabel, QLineEdit,
    QMainWindow, QMenuBar, QPushButton, QSizePolicy,
    QStatusBar, QTableWidget, QTableWidgetItem, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(138, 130, 81, 20))
        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(138, 170, 81, 20))
        self.campoNombre = QLineEdit(self.centralwidget)
        self.campoNombre.setObjectName(u"campoNombre")
        self.campoNombre.setGeometry(QRect(240, 130, 113, 21))
        self.campoNombre.setMaxLength(100)
        self.campoDescripcion = QLineEdit(self.centralwidget)
        self.campoDescripcion.setObjectName(u"campoDescripcion")
        self.campoDescripcion.setGeometry(QRect(240, 170, 113, 21))
        self.campoDescripcion.setMaxLength(100)
        self.btnCrear = QPushButton(self.centralwidget)
        self.btnCrear.setObjectName(u"btnCrear")
        self.btnCrear.setGeometry(QRect(80, 260, 75, 24))
        self.btnEliminar = QPushButton(self.centralwidget)
        self.btnEliminar.setObjectName(u"btnEliminar")
        self.btnEliminar.setGeometry(QRect(180, 260, 75, 24))
        self.btnEditar = QPushButton(self.centralwidget)
        self.btnEditar.setObjectName(u"btnEditar")
        self.btnEditar.setGeometry(QRect(280, 260, 75, 24))
        self.tableWidget = QTableWidget(self.centralwidget)
        self.tableWidget.setObjectName(u"tableWidget")
        self.tableWidget.setGeometry(QRect(390, 10, 321, 231))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 33))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Nombre:", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Descripci\u00f3n:", None))
        self.btnCrear.setText(QCoreApplication.translate("MainWindow", u"Crear", None))
        self.btnEliminar.setText(QCoreApplication.translate("MainWindow", u"Eliminar", None))
        self.btnEditar.setText(QCoreApplication.translate("MainWindow", u"Editar", None))
    # retranslateUi

import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox
from departamento import Ui_MainWindow  # Importa la interfaz generada

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Conectar los botones a sus respectivos métodos
        self.ui.btnCrear.clicked.connect(self.crear_departamento)
        self.ui.btnEliminar.clicked.connect(self.eliminar_departamento)
        self.ui.btnEditar.clicked.connect(self.editar_departamento)

        # Configurar la tabla
        self.ui.tableWidget.setColumnCount(2)  # Número de columnas (Nombre y Descripción)
        self.ui.tableWidget.setHorizontalHeaderLabels(["Nombre", "Descripción"])

    def crear_departamento(self):
        nombre = self.ui.campoNombre.text()
        descripcion = self.ui.campoDescripcion.text()
        
        # Añadir el nuevo departamento a la tabla (en una aplicación real, aquí iría la inserción en la base de datos)
        row_position = self.ui.tableWidget.rowCount()
        self.ui.tableWidget.insertRow(row_position)
        self.ui.tableWidget.setItem(row_position, 0, QTableWidgetItem(nombre))
        self.ui.tableWidget.setItem(row_position, 1, QTableWidgetItem(descripcion))

        QMessageBox.information(self, "Éxito", "Departamento creado exitosamente.")

    def eliminar_departamento(self):
        selected_row = self.ui.tableWidget.currentRow()
        if selected_row >= 0:
            self.ui.tableWidget.removeRow(selected_row)
            QMessageBox.information(self, "Éxito", "Departamento eliminado exitosamente.")
        else:
            QMessageBox.warning(self, "Error", "Selecciona un departamento para eliminar.")

    def editar_departamento(self):
        selected_row = self.ui.tableWidget.currentRow()
        if selected_row >= 0:
            nombre = self.ui.campoNombre.text()
            descripcion = self.ui.campoDescripcion.text()

            self.ui.tableWidget.setItem(selected_row, 0, QTableWidgetItem(nombre))
            self.ui.tableWidget.setItem(selected_row, 1, QTableWidgetItem(descripcion))

            QMessageBox.information(self, "Éxito", "Departamento actualizado exitosamente.")
        else:
            QMessageBox.warning(self, "Error", "Selecciona un departamento para editar.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
