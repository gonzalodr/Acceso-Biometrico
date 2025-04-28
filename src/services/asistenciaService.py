import re
from models.asistencia          import Asistencia
from models.detalle_asistencia  import DetalleAsistencia
from data.asistenciaData        import AsistenciaData
from datetime                   import date,datetime
from typing                     import Optional, List, Union, Tuple
from .ZKService                 import ZKServices

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
    
    def obtenerAsistenciaPorEmpleado(self, id_empleado):
        return self.asistenciaData.listar_asistencia_por_empleado(id_empleado)

    def registrarAsistenciaEmpleado(self,id_empleado:int=None,fecha:date=None,rango_fechas: Optional[Union[Tuple[date, date], List[str]]] = None):
        result = ZKServices().obtener_asistencias(id_empleado,fecha,rango_fechas)
        if not result['success']:
            return result
        
        if len(result['asistencias']) == 0:
            return {'success':False, 'message':'No hay asistencias registradas.'}
        
        listAsistencia = []
        for asistEmpl in result['asistencias']:
            if asistEmpl[0] and int(asistEmpl[0].user_id) == 1:
                asist = Asistencia(id_empleado = asistEmpl[0].user_id, fecha = asistEmpl[1].timestamp.date(),estado_asistencia = 'presente')
                listAsistencia.append((asist, asistEmpl[1].timestamp.time() ))

        if len(listAsistencia) == 0:
            return {'success':False, 'message':'No hay asistencias registradas.'}
        return self.asistenciaData.registrar_asistencia(listAsistencia)
        
