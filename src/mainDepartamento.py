# -*- coding: utf-8 -*-
from UI.ui_departamentoInterfaz import Ui_departamentoInterfaz
from PySide6.QtWidgets import QMainWindow, QApplication, QStackedWidget
import sys

class MainWindow(QMainWindow, Ui_departamentoInterfaz):
    def __init__(self):
        super().__init__()
        # self.StackVentanas = QStackedWidget()  # Lista de vistas, si se requiere para navegación
        self.setupUi(self)
        
    # ## busca una vista por nombre    
    # def SeleccionarVistaPorNombre(self, nombreVista):
    #     for i in range(self.StackVentanas.count()):
    #         widget = self.StackVentanas.widget(i)
    #         if widget.objectName() == nombreVista:
    #             self.StackVentanas.setCurrentIndex(i)
    #             return  # Salida del bucle
    
    # def SeleccionarVistaPorIndex(self, index=0):
    #     self.StackVentanas.setCurrentIndex(index) 

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
