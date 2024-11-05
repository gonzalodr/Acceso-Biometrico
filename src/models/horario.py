class Horario:
    def __init__(self, dias_semanales, tipo_jornada, hora_inicio, hora_fin, descripcion=None, id=0):
        self.id = id
        self.dias_semanales  = dias_semanales
        self.tipo_jornada = tipo_jornada
        self.hora_inicio = hora_inicio
        self.hora_fin = hora_fin
        self.descripcion = descripcion

    def __repr__(self):
        return (
            f"Id: {self.id}\n"
            f"Días Semanales: {self.dias_semanales}\n"
            f"Tipo de Jornada: {self.tipo_jornada}\n"
            f"Hora de Inicio: {self.hora_inicio}\n"
            f"Hora de Fin: {self.hora_fin}\n"
            f"Descripción: {self.descripcion}"
        )
