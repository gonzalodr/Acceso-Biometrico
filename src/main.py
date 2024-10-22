from PySide6.QtWidgets import QApplication
from PySide6.QtCore import *
import sys
from UI.Ventana import Ventana


## Main principal no tocar
if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = Ventana()
    ventana.show()
    ventana.showMaximized()
    sys.exit(app.exec())
