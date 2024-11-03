from data.data import conection  # Importa la función para obtener la conexión
from settings.config import * 
from models.permiso_rol import * 

class PermisosRolData:
    def create_permiso_rol(self, permiso:Permiso_Rol,conexion_externa):
        resultado = {"success": False,"message":""}
        
        if conexion_externa is None:
            conexion, resultado = conection()
            if not resultado["success"]:
                return resultado
        else:
            conexion = conexion_externa

        try:
            with conexion.cursor() as cursor:
                query = f"""INSERT INTO {TBPERMISOROL} (
                    {TBPERMISOROL_ROL_ID}, 
                    {TBPERMISOROL_TABLA},  
                    {TBPERMISOROL_VER},
                    {TBPERMISOROL_INSERTAR},
                    {TBPERMISOROL_EDITAR},
                    {TBPERMISOROL_ELIMINAR}
                ) VALUES (%s, %s, %s, %s, %s, %s)"""
                cursor.execute(query, (
                   permiso.rol_id,
                   permiso.tabla,
                   permiso.ver,
                   permiso.crear,
                   permiso.editar,
                   permiso.eliminar
                ))
                conexion.commit()    
                id_permiso_rol = cursor.lastrowid
                
                resultado["success"] = True
                resultado["message"] = "Permiso rol creado exitosamente."
                resultado["id_permiso_rol"] = id_permiso_rol
        except Exception as e:
            resultado["success"] = False
            resultado["message"] = f"Error al crear el permiso rol: {e}"
        finally:
            if conexion_externa is None and conexion:
                conexion.close()
        return resultado
    
    def save_permisos_rol(self,listparmisos):
        ##realiza la conexion
        conexion, resultado = conection()
        if not resultado["success"]:
            return resultado
        
        ##comienza las consultas de inserccion
        try:
            ##comienza la transaccion para asegurar los datos
            conexion.start_transaction()
            ##guarda la lista de permismo
            for permisos in listparmisos:
                resultado = self.create_permiso_rol(permisos,conexion_externa = conexion)
                if not resultado["success"]:
                    conexion.rollback() ##revierte la transaccion
                    return resultado
            ## hace comit de la transaccion
            conexion.commit()
            
            resultado["success"] = True
            resultado["message"] = f"Permisos guardados correctamente"
        except Exception as e:
            conexion.rollback() ##revierte la transaccion
            resultado["success"] = False
            resultado["message"] = f"Error al crear los permiso rol: {e}"
        finally:
            if conexion:
                conexion.close()
        return resultado
    
    def update_permiso_rol(self,permiso:Permiso_Rol):
        pass
    
    def delete_permiso_rol(self,permiso_rol_id:int):
        pass
    
    def list_permisos_rol(self,pagina=1, tam_pagina=10, ordenar_por = TBPERSONA_ID, tipo_orden="ASC", busqueda = None):
        pass
    
    def get_permiso_rol_ById(self,permiso_rol_id:int):
        pass