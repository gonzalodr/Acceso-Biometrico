from UI.ui_personaInterfaz import Ui_personaInterfaz
from UI.ui_departamentoInterfaz import Ui_departamentoInterfaz
from PySide6.QtWidgets import QMainWindow, QApplication,QStackedWidget, QWidget
import sys

class MainWindow(QMainWindow,Ui_personaInterfaz):
    def __init__(self):
        super().__init__()
        # self.StackVentanas = QStackedWidget()#Lista de vistas
        self.setupUi(self)
        
    # ## busca una vista por nombre    
    # def SeleccionarVistaPorNombre(self,nombreVista):
    #     for i in range(self.StackVentanas.count()):
    #         widget = self.stacked_widget.widget(i)
    #         if widget.objectName() == nombreVista:
    #             self.StackVentanas.setCurrentIndex(i)
    #             return ##salidad del bucle
    
    # def SeleccionarVistaPorIndex(self, index = 0):
    #     self.StackVentanas.setCurrentIndex(0) 

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()





