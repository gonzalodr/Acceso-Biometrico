class Huella:
    def __init__(
        self,
        id_huella: int = 0,
        id_empleado: int = 0,
        id_user: int = 0,
        privilegio: int = 0,
    ):
        self.id_huella = id_huella  # PK o ID que da el dispositivo
        self.id_empleado = id_empleado  # ID del empleado en tu sistema
        self.id_user = id_user  # user_id que maneja el dispositivo
        self.privilegio = privilegio  # Nivel de privilegio (0=normal, 1=admin.)

    def __str__(self):
        return f"ID Huella: {self.id_huella}, ID Empleado: {self.id_empleado}, ID User: {self.id_user}, Privilegio: {self.privilegio}"
