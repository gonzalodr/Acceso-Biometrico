from datetime import date  # Importa el tipo de dato 'date' para las fechas

class Asistencia:
    def __init__(self, id_empleado: int, fecha: date, estado_asistencia: str, id: int = 0):
        self.id  = id  # PK
        self.id_empleado    = id_empleado  # FK
        self.fecha          = fecha
        self.estado_asistencia = estado_asistencia

    def mostrar(self):
        return f"{self.id}\n{self.id_empleado}\n{self.fecha}\n{self.estado_asistencia}"