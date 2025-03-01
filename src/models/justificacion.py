from datetime import date

class Justificacion:
    def __init__(self, id_asistencia: int, fecha:date, motivo: str, descripcion: str, id_justificacion: int = 0):
        self.id_justificacion   = id_justificacion  # PK
        self.id_asistencia      = id_asistencia  # FK
        self.fecha              = fecha
        self.motivo             = motivo
        self.descripcion        = descripcion

    def __str__(self):
        return (f"ID Justificación: {self.id_justificacion}, ID Asistencia: {self.id_asistencia}, "
                f"Fecha: {self.fecha}, Motivo: {self.motivo}, Descripción: {self.descripcion}")