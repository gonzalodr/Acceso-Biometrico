import re
from models.reporte import Reporte
from data.reporteData import ReporteData

class ReporteServices:
    def __init__(self):
        self.reporteData = ReporteData()
        
    def insertarReporte(self, reporte: Reporte):
        return self.reporteData.create_reporte(reporte)
    
    def modificarReporte(self, reporte: Reporte):
        return self.reporteData.update_reporte(reporte)
        
    def eliminarReporte(self, id):
        return self.reporteData.delete_reporte(id)

    def obtenerListaReporte(self, pagina=1, tam_pagina=10, ordenar_por="id", tipo_orden="ASC", busqueda=None):
        return self.reporteData.list_reportes(pagina, tam_pagina, ordenar_por, tipo_orden, busqueda)

    def obtenerReportePorId(self, id):
        return self.reporteData.get_reporte_by_id(id)
    
    def obtenerTodoReporte(self):
        return self.reporteData.obtener_todo_reportes()