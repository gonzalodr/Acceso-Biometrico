import re
from models.asistencia import Asistencia
from data.asistenciaData import AsistenciaData

class AsistenciaServices:
    def __init__(self):
        self.asistenciaData = AsistenciaData()

    def obtenerAsistenciaPorEmpleado(self, id_empleado):
        return self.asistenciaData.listar_asistencia_por_empleado(id_empleado)