
class Huella:
    def __init__(self, id_empleado: bytes, id_huella: int = 0):
        self.id_empleado  = id_empleado 
        self.id_huella     = id_huella  

    def __str__(self):
        return f"ID Empleado: {self.id_empleado}, ID Empleado: {self.id_huella}"  # Representación hexadecimal de la huella
