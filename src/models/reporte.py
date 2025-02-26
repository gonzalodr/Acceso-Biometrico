from datetime import datetime

class Reporte:
    def __init__(self, id_empleado: int, fecha_generacion: datetime, tipo_reporte: str, contenido: str, id: int = 0):
        self.id = id  # PK
        self.id_empleado = id_empleado  # FK
        self.fecha_generacion = fecha_generacion
        self.tipo_reporte = tipo_reporte
        self.contenido = contenido

    def __str__(self):
        return (f"ID: {self.id}, ID Empleado: {self.id_empleado}, Fecha Generación: {self.fecha_generacion}, "
                f"Tipo Reporte: {self.tipo_reporte}, Contenido: {self.contenido}")

    def __repr__(self):
        return (f"Reporte(id={self.id}, id_empleado={self.id_empleado}, fecha_generacion={self.fecha_generacion}, "
                f"tipo_reporte='{self.tipo_reporte}', contenido='{self.contenido}')")