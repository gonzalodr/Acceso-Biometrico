from datetime import date

class Justificacion:
    def __init__(self, id_empleado: int, id_asistencia, fecha:date, motivo: str, descripcion: str,tipo: str, id_justificacion: int = 0):
        self.id_justificacion   = id_justificacion  # PK
        self.id_empleado      = id_empleado  # FK
        self.id_asistencia      = id_asistencia  # FK
        self.fecha              = fecha
        self.motivo             = motivo
        self.descripcion        = descripcion
        self.tipo               = tipo                 

    def __str__(self):
        return (f"ID Justificación: {self.id_justificacion}, ID Asistencia: {self.id_asistencia},Tipo: {self.tipo}, ID Empleado: {self.id_empleado}"
                f"Fecha: {self.fecha}, Motivo: {self.motivo}, Descripción: {self.descripcion}")