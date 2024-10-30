from PySide6.QtWidgets import *
from PySide6.QtCore import *
from Utils.Utils import *
from UI.DialogoEmergente import *
from services.departamentoService import *

class formDepartamento(QDialog):
    update:bool = False
    Pservices = DepartamentoServices()
    idP = None