from PySide6.QtWidgets import QApplication
from PySide6.QtCore import *
import sys
from UI.Ventana import Ventana


from models.persona import *
from services.personaService import *
from models.usuario import *
from services.usuarioService import *
## Main principal no tocar
if __name__ == "__main__":

    app = QApplication(sys.argv)
    ventana = Ventana()
    ventana.show()
    ventana.showMaximized()
    sys.exit(app.exec())
