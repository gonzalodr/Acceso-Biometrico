from data.huellaData import HuellaData
from models.huella import Huella

class HuellaService:

    def __init__(self):
        self.huellaData = HuellaData()

    def insertarHuella(self, huella: Huella):
        # Inserción en la capa de datos
        return self.huellaData.create_huella(huella)
