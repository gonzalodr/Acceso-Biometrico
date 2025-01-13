from data.permisosPerfilData import *

class PermisosRolServices:
    def __init__(self):
        self.permisorperfildata = PermisosPerfilData()

    def insertar_permiso_perfil(self,permiso:Permiso_Perfil):
        return self.permisorperfildata.create_permiso_perfil(permiso)
    
    def actualizar_permiso_perfil(self,permiso:Permiso_Perfil):
        return self.permisorperfildata.update_permiso_perfil(permiso=permiso)
    
    def eliminar_permiso_perfil(self, id_permiso):
        return self.permisorperfildata.delete_permiso_perfil(permiso_rol_id=id_permiso)
    
    def listar_permisos_perfil(self,pagina=1, tam_pagina=10, ordenar_por = TBPERMISOPERFIL_ID, tipo_orden="ASC", busqueda = None):
        return self.permisorperfildata.lista_permisos_perfil(pagina, tam_pagina, ordenar_por, tipo_orden, busqueda)
    
    def obtener_permiso_perfil_por_id(self,id):
        return self.permisorperfildata.get_permiso_perfil_ById(id)
    
    def verificar_permiso_perfil_tabla(self, perfil_id:int, tabla:str, id:int =0):
        return self.permisorperfildata.verificar_perfil_permiso(perfil_id=perfil_id,tabla=tabla,id=id)
    
    def verificar_permisos_accesos_tabla(self,permisos:Permiso_Perfil):
        if permisos.editar:
            permisos.ver = True
            
        if permisos.crear:
            permisos.ver = True
            
        if permisos.eliminar:
            permisos.ver = True
        return permisos