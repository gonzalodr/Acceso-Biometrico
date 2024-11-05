from data.permisosRolData import *

class PermisosRolServices:
    def __init__(self):
        self.permisoroldata = PermisosRolData()

    def insertar_permiso_rol(self,permiso:Permiso_Rol):
        return self.permisoroldata.create_permiso_rol(permiso)
    
    def actualizar_permiso_rol(self,permiso:Permiso_Rol):
        return self.permisoroldata.update_permiso_rol(permiso=permiso)
    
    def eliminar_permiso_rol(self, id_permiso):
        return self.permisoroldata.delete_permiso_rol(permiso_rol_id=id_permiso)
    
    def listar_permisos_rol(self,pagina=1, tam_pagina=10, ordenar_por = TBPERMISOROL_ID, tipo_orden="ASC", busqueda = None):
        return self.permisoroldata.lista_permisos_rol(pagina, tam_pagina, ordenar_por, tipo_orden, busqueda)
    
    def obtener_permiso_rol_por_id(self,id):
        return self.permisoroldata.get_permiso_rol_ById(id)
    
    def verificar_permiso_rol_tabla(self, rol_id:int, tabla:str, id:int =0):
        return self.permisoroldata.verificar_rol_permiso(rol_id=rol_id,tabla=tabla,id=id)
    
    def verificar_permisos_accesos_tabla(self,permisos:Permiso_Rol):
        if permisos.editar:
            permisos.ver = True
            
        if permisos.crear:
            permisos.ver = True
            
        if permisos.eliminar:
            permisos.ver = True
        return permisos