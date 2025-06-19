class Huella:
    def __init__(
        self,
        id_huella: int = 0,
        id_empleado: int = 0,
    ):
        self.id_huella = id_huella  # PK o ID que da el dispositivo
        self.id_empleado = id_empleado  # ID del empleado en tu sistema

    def __str__(self):
        return f"ID Huella: {self.id_huella}, ID Empleado: {self.id_empleado}"
