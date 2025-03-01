from datetime import date

class SolicitudPermiso:
    
    def __init__(self, id_empleado: int, tipo: str, fecha_inicio: date, fecha_fin: date, descripcion: str, estado: str, id_solicitud_permiso: int = 0):
        self.id_solicitud_permiso = id_solicitud_permiso  # PK
        self.id_empleado = id_empleado  # FK
        self.tipo = tipo
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin
        self.descripcion = descripcion
        self.estado = estado

    def __str__(self):
        return (f"ID Solicitud: {self.id_solicitud_permiso}, ID Empleado: {self.id_empleado}, Tipo: {self.tipo}, "
                f"Fecha Inicio: {self.fecha_inicio}, Fecha Fin: {self.fecha_fin}, Descripción: {self.descripcion}, "
                f"Estado: {self.estado}")

    def __repr__(self):
        return (f"SolicitudPermiso(id_solicitud_permiso={self.id_solicitud_permiso}, id_empleado={self.id_empleado}, "
                f"tipo='{self.tipo}', fecha_inicio={self.fecha_inicio}, fecha_fin={self.fecha_fin}, "
                f"descripcion='{self.descripcion}', estado='{self.estado}')")