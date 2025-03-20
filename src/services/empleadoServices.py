from data.EmpleadoData import EmpleadoData
from settings.tablas import TBPERSONA_ID
from typing import Dict, Any

class EmpleadoServices:
    def __init__(self):
        self.empleServ = EmpleadoData()
    
    def crear_empleado(self,datos:Dict[str,Any]):
        return self.empleServ.create_Empleado(datos)
    
    def eliminar_empleado(self, id_empleado:int):
        return self.empleServ.delete_Empleado(id_empleado)
    
    def actualizar_empleado(self, datos:Dict[str,Any]):
        return self.empleServ.update_Empleado(datos)
    
    def listar_empleados(self,pagina=1, tam_pagina=10, ordenar_por=TBPERSONA_ID, tipo_orden="ASC", busqueda=None):
        return self.empleServ.list_Empleados(pagina, tam_pagina, ordenar_por, tipo_orden, busqueda)
    
    def obtener_todo_empleados(self):
        return self.empleServ.obtener_todo_empleados()