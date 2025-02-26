from datetime import date  # Importa el tipo de dato 'date' para las fechas

class Asistencia:
    def __init__(self, id_empleado: int, fecha: date, estado_asistencia: str, id_asistencia: int = 0):
        self.id_asistencia  = id_asistencia  # PK
        self.id_empleado    = id_empleado  # FK
        self.fecha          = fecha
        self.estado_asistencia = estado_asistencia

    def __str__(self):
        return (f"ID Asistencia: {self.id_asistencia}, ID Empleado: {self.id_empleado}, "
                f"Fecha: {self.fecha}, Estado Asistencia: {self.estado_asistencia}")

    def __repr__(self):
        return (f"Asistencia(id_asistencia={self.id_asistencia}, id_empleado={self.id_empleado}, "
                f"fecha={self.fecha}, estado_asistencia='{self.estado_asistencia}')")