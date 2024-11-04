from data.data import conection  # Importa la función para obtener la conexión
from settings.config import * 
from models.permiso_rol import * 

class PermisosRolData:
    
    def verificar_rol_permiso(self,rol_id:int, tabla:str, id:int =0):
        conexion, resultado = conection()
        if not resultado["success"]:
            return False
        try:
            with conexion.cursor() as cursor:
                query = f"SELECT COUNT(*) FROM {TBPERMISOROL} WHERE {TBPERMISOROL_ROL_ID} = %s AND {TBPERMISOROL_TABLA} = %s "
                if id is not None and id > 0:
                    query += f" AND id != %s"
                    cursor.execute(query, (rol_id, tabla, id))
                else:
                    cursor.execute(query, (rol_id, tabla))
                count = cursor.fetchone()[0]
                return count > 0 
        except Exception as e:
            return False
        finally:
            if conexion:
                conexion.close()
    
    
    def create_permiso_rol(self, permiso:Permiso_Rol,conexion_externa = None):
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
                if conexion_externa is None:
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
        conexion, resultado = conection()
        cursor = None
        if not resultado["success"]:
            return resultado
        try:
            with conexion.cursor() as cursor:
                query = f"""UPDATE {TBPERMISOROL} SET 
                {TBPERMISOROL_ROL_ID} = %s,
                {TBPERMISOROL_TABLA} = %s,
                {TBPERMISOROL_VER} = %s,
                {TBPERMISOROL_INSERTAR} = %s,
                {TBPERMISOROL_EDITAR} = %s,
                {TBPERMISOROL_ELIMINAR} = %s 
                WHERE {TBPERMISOROL_ID} = %s"""
                
                cursor.execute(query, (
                    permiso.rol_id,
                    permiso.tabla,
                    permiso.ver,
                    permiso.crear,
                    permiso.editar,
                    permiso.eliminar,
                    permiso.id
                )) 
                conexion.commit()
                resultado["success"] = True
                resultado["message"] = "Permiso del rol actualizada exitosamente."
        except Exception as e:
            resultado["success"] = False
            resultado["message"] = f"Error al actualizar permisos del rol: {e}"
        finally:
            if conexion:
                conexion.close()
        return resultado
     
    def delete_permiso_rol(self,permiso_rol_id:int):
        conexion, resultado = conection()
        cursor = None
        if not resultado["success"]:
            return resultado
        try:
            cursor = conexion.cursor()
            query = f"DELETE FROM {TBPERMISOROL} WHERE {TBPERMISOROL_ID} = %s "
            
            cursor.execute(query, (permiso_rol_id,))
            conexion.commit()
            
            resultado["success"] = True
            resultado["message"] = "Persona eliminada exitosamente."
        except Exception as e:
            resultado["success"] = False
            resultado["message"] = f"Error al eliminar persona: {e}"
        finally:
            if conexion:
                conexion.close()

        return resultado
    
    def lista_permisos_rol(self,pagina=1, tam_pagina=10, ordenar_por = TBPERMISOROL_ID, tipo_orden="ASC", busqueda = None):
        conexion, resultado = conection()
        cursor = None
        if not resultado["success"]:
            return resultado
        
        listaPermisosRol = []
        try:
            with conexion.cursor(dictionary=True) as cursor: 
                #validacion de por que columna ordenar
                columna_orden = { 
                    "tabla":TBPERMISOROL_TABLA,
                    "ver":TBPERMISOROL_VER,
                    "crear":TBPERMISOROL_INSERTAR,
                    "editar":TBPERMISOROL_EDITAR,
                    "eliminar":TBPERMISOROL_ELIMINAR,
                    "id":TBPERMISOROL_ID
                }
                ## asigna sobre que tabla realizar el orden
                ordenar_por = columna_orden.get(ordenar_por, TBPERMISOROL_ID)
                    
                ## asigna el tipo de orden ascendente o descendente
                tipo_orden = "ASC" if tipo_orden.upper() == "ASC" else "DESC"
                # Construcción de la consulta base
                query = f"SELECT * FROM {TBPERMISOROL} "
                
                # Añadir cláusula de búsqueda si se proporciona
                valores = []
                if busqueda:
                    query += f"""
                        WHERE {TBPERMISOROL_TABLA} LIKE %s 
                    """
                    valores = [f"%{busqueda}%"]
                
                # Añadir la cláusula ORDER BY y LIMIT/OFFSET
                query += f" ORDER BY {ordenar_por} {tipo_orden} LIMIT %s OFFSET %s"
                valores.extend([tam_pagina, (pagina - 1) * tam_pagina])

                cursor.execute(query, valores)
                
                #Leyendo los registros de 
                registros = cursor.fetchall()
                for registro in registros:
                    permiso:Permiso_Rol = Permiso_Rol(
                        registro[TBPERMISOROL_ROL_ID],
                        registro[TBPERMISOROL_TABLA],
                        registro[TBPERMISOROL_VER],
                        registro[TBPERMISOROL_INSERTAR],
                        registro[TBPERMISOROL_EDITAR],
                        registro[TBPERMISOROL_ELIMINAR],
                        registro[TBPERMISOROL_ID]
                    )
                    listaPermisosRol.append(permiso)
                    
                # Obtener el total de registros para calcular el número total de páginas
                cursor.execute(f"SELECT COUNT(*) as total FROM {TBPERMISOROL}")
                total_registros = cursor.fetchone()["total"]
                total_paginas = (total_registros + tam_pagina - 1) // tam_pagina  # Redondear hacia arriba

                resultado["data"] = {
                    "listaPermisosRol": listaPermisosRol,
                    "pagina_actual": pagina,
                    "tam_pagina": tam_pagina,
                    "total_paginas": total_paginas,
                    "total_registros": total_registros
                }
                resultado["success"] = True
                resultado["message"] = "Permisos listadas exitosamente."
        except Exception as e:
            resultado["success"] = False
            resultado["message"] = f"Error al listar permisos: {e}"
        finally:
            if conexion:
                conexion.close()
        return resultado

    def get_permiso_rol_ById(self,permiso_rol_id:int):
        conexion, resultado = conection()
        if not resultado["success"]:
            return resultado

        try:
            with conexion.cursor() as cursor:
                query = f"""SELECT
                                {TBPERMISOROL_ROL_ID}, 
                                {TBPERMISOROL_TABLA}, 
                                {TBPERMISOROL_VER},
                                {TBPERMISOROL_INSERTAR}, 
                                {TBPERMISOROL_EDITAR}, 
                                {TBPERMISOROL_ELIMINAR}, 
                                {TBPERMISOROL_ID} 
                            FROM {TBPERMISOROL} 
                            WHERE id = %s"""
                
                cursor.execute(query, (permiso_rol_id,))
                data = cursor.fetchone()
                
                if data:
                    permiso = Permiso_Rol(
                        rol_id  = data[0],
                        tabla   = data[1],
                        ver     = data[2],
                        crear   = data[3],
                        editar  = data[4],
                        eliminar= data[5],
                        id      = data[6]                    
                    )
                    resultado["success"] = True
                    resultado["data"] = permiso
                else:
                    raise ValueError("No se encontró ningun permiso con el ID proporcionado.")
        except Exception as e:
            resultado["success"] = False
            resultado["message"] = f"Error al obtener permiso: {e}"
        finally:
            if conexion:
                conexion.close()
        return resultado