from datetime import time

class DetalleAsistencia:
    def __init__(self, id_asistencia:int, hora_entrada:time, hora_salida:time, horas_trabajadas:float, id_detalle:int=0):
        self.id_detalle     = id_detalle
        self.id_asistencia  = id_asistencia
        self.hora_entrada   = hora_entrada
        self.hora_salida    = hora_salida
        self.horas_trabajadas = horas_trabajadas

    def __str__(self):
        return (f"ID Detalle: {self.id_detalle}, ID Asistencia: {self.id_asistencia}, "
                f"Hora Entrada: {self.hora_entrada}, Hora Salida: {self.hora_salida}, "
                f"Horas Trabajadas: {self.horas_trabajadas}")