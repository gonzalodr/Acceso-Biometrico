from datetime import date

class Mantenimiento:
    def __init__(self, id_usuario: int, fecha: date, accion_realizada: str, descripcion: str = None, id_mantenimiento: int = 0):
        self.id_mantenimiento = id_mantenimiento  # PK
        self.id_usuario = id_usuario  # FK
        self.fecha      = fecha
        self.accion_realizada = accion_realizada
        self.descripcion = descripcion  # Puede ser None

    def __str__(self):
        return (f"id_mantenimiento: {self.id_mantenimiento}, id_mantenimiento Usuario: {self.id_usuario}, Fecha: {self.fecha}, "
                f"Acción Realizada: {self.accion_realizada}, Descripción: {self.descripcion}")

    def __repr__(self):
        return (f"Mantenimiento(id_mantenimiento={self.id_mantenimiento}, id_usuario={self.id_usuario}, fecha={self.fecha}, "
                f"accion_realizada='{self.accion_realizada}', descripcion='{self.descripcion}')")