from data.EmpleadoData import EmpleadoData
from settings.config import TBPERSONA_ID
from typing import Dict, Any
import bcrypt 
class EmpleadoServices:
    def __init__(self):
        self.empleServ = EmpleadoData()
        
    def __contrasenaHash(self,contrasena):
        contrasena = str(contrasena).encode("utf-8")
        contrasena_hash = bcrypt.hashpw(contrasena,bcrypt.gensalt())
        return contrasena_hash
    
    def crear_empleado(self,datos:Dict[str,Any]):
        usuario = datos.get('usuario')
        if usuario:
            usuario.contrasena = self.__contrasenaHash(usuario.contrasena)
            datos['usuario'] = usuario

        return self.empleServ.create_Empleado(datos)
    
    def eliminar_empleado(self, id_empleado:int):
        return self.empleServ.delete_Empleado(id_empleado)
    
    def actualizar_empleado(self,id_empleado:int, datos:Dict[str,Any]):
        usuario = datos.get('usuario')
        if usuario:
            if usuario.id and usuario.contrasena:
                usuario.contrasena = self.__contrasenaHash(usuario.contrasena)
                datos['usuario'] = usuario
            elif usuario.id is None:
                usuario.contrasena = self.__contrasenaHash(usuario.contrasena)
                datos['usuario'] = usuario

        return self.empleServ.update_Empleado(id_empleado,datos)
    
    def obtener_empleado_por_id(self, id_empleado):
        return self.empleServ.getEmpleadoById(id_empleado)

    def listar_empleados(self,pagina=1, tam_pagina=10, ordenar_por=TBPERSONA_ID, tipo_orden="ASC", busqueda=None):
        return self.empleServ.list_Empleados(pagina, tam_pagina, ordenar_por, tipo_orden, busqueda)
    
    def obtener_todo_empleados(self):
        return self.empleServ.obtener_todo_empleados()
