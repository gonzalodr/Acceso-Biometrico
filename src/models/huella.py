
class Huella:
    def __init__(self, huella: bytes, id_huella: int = 0):
        self.id_huella  = id_huella  # PK
        self.huella     = huella  # Datos binarios de la huella

    def __str__(self):
        return f"ID Huella: {self.id_huella}, Huella: {self.huella.hex()}"  # Representación hexadecimal de la huella
