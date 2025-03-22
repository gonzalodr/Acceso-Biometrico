import re
from models.asistencia import Asistencia
from data.asistenciaData import AsistenciaData

class AsistenciaServices:
    def __init__(self):
        self.asistenciaData = AsistenciaData()
        
    def insertarAsistencia(self, asistencia: Asistencia):
        return self.asistenciaData.create_asistencia(asistencia)
    
    def modificarAsistencia(self, asistencia: Asistencia):
        return self.asistenciaData.update_asistencia(asistencia)
    
    def eliminarAsistencia(self, id):
        return self.asistenciaData.delete_asistencia(id)
    
    def obtenerListaAsistencia(self, pagina=1, tam_pagina=10, ordenar_por="id", tipo_orden="ASC", busqueda=None):
        return self.asistenciaData.list_asistencias(pagina, tam_pagina, ordenar_por, tipo_orden, busqueda)
    
    def obtenerAsistenciaPorId(self, id):
        return self.asistenciaData.get_asistencia_by_id(id)
    
    def obtenerTodoAsistencia(self):
        return self.asistenciaData.obtener_todo_asistencias()