from data.data import conection  # Importa la función para obtener la conexión
from settings.config import * 
from models.permiso_perfil import * 

class PermisosPerfilData:
    
    def verificar_perfil_permiso(self,perfil_id:int, tabla:str, id:int =0):
        conexion, resultado = conection()
        if not resultado["success"]:
            return False
        try:
            with conexion.cursor() as cursor:
                query = f"SELECT COUNT(*) FROM {TBPERMISOPERFIL} WHERE {TBPERMISOPERFIL_ID} = %s AND {TBPERMISOPERFIL_TABLA} = %s "
                if id is not None and id > 0:
                    query += f" AND id != %s"
                    cursor.execute(query, (perfil_id, tabla, id))
                else:
                    cursor.execute(query, (perfil_id, tabla))
                count = cursor.fetchone()[0]
                return count > 0 
        except Exception as e:
            return False
        finally:
            if conexion:
                conexion.close()
                
    def create_permiso_perfil(self, permiso:Permiso_Perfil,conexion_externa = None):
        resultado = {"success": False,"message":""}
        
        if conexion_externa is None:
            conexion, resultado = conection()
            if not resultado["success"]:
                return resultado
        else:
            conexion = conexion_externa

        try:
            with conexion.cursor() as cursor:
                query = f"""INSERT INTO {TBPERMISOPERFIL} (
                    {TBPERMISOPERFIL_PERFIL_ID}, 
                    {TBPERMISOPERFIL_TABLA},  
                    {TBPERMISOPERFIL_VER},
                    {TBPERMISOPERFIL_INSERTAR},
                    {TBPERMISOPERFIL_EDITAR},
                    {TBPERMISOPERFIL_ELIMINAR}
                ) VALUES (%s, %s, %s, %s, %s, %s)"""
                cursor.execute(query, (
                   permiso.perfil_id,
                   permiso.tabla,
                   permiso.ver,
                   permiso.crear,
                   permiso.editar,
                   permiso.eliminar
                ))
                if conexion_externa is None:
                    conexion.commit()    
                
                id_permiso_perfil = cursor.lastrowid
                
                resultado["success"] = True
                resultado["message"] = "Permiso perfil creado exitosamente."
                resultado["id_permiso_perfil"] = id_permiso_perfil
        except Exception as e:
            resultado["success"] = False
            resultado["message"] = f"Error al crear el permiso perfil: {e}"
        finally:
            if conexion_externa is None and conexion:
                conexion.close()
        return resultado
    
    def save_permisos_perfil(self,listparmisos):
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
                resultado = self.create_permiso_perfil(permisos,conexion_externa = conexion)
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
            resultado["message"] = f"Error al crear los permiso perfil: {e}"
        finally:
            if conexion:
                conexion.close()
        return resultado
    
    def update_permiso_perfil(self,permiso:Permiso_Perfil):
        conexion, resultado = conection()
        cursor = None
        if not resultado["success"]:
            return resultado
        try:
            with conexion.cursor() as cursor:
                query = f"""UPDATE {TBPERMISOPERFIL} SET 
                {TBPERMISOPERFIL_PERFIL_ID} = %s,
                {TBPERMISOPERFIL_TABLA} = %s,
                {TBPERMISOPERFIL_VER} = %s,
                {TBPERMISOPERFIL_INSERTAR} = %s,
                {TBPERMISOPERFIL_EDITAR} = %s,
                {TBPERMISOPERFIL_ELIMINAR} = %s 
                WHERE {TBPERMISOPERFIL_ID} = %s"""
                
                cursor.execute(query, (
                    permiso.perfil_id,
                    permiso.tabla,
                    permiso.ver,
                    permiso.crear,
                    permiso.editar,
                    permiso.eliminar,
                    permiso.id
                )) 
                conexion.commit()
                resultado["success"] = True
                resultado["message"] = "Permiso del perfil actualizada exitosamente."
        except Exception as e:
            resultado["success"] = False
            resultado["message"] = f"Error al actualizar permisos del perfil: {e}"
        finally:
            if conexion:
                conexion.close()
        return resultado
    
    def delete_permiso_perfil(self,permiso_perfil_id:int):
        conexion, resultado = conection()
        cursor = None
        if not resultado["success"]:
            return resultado
        try:
            cursor = conexion.cursor()
            query = f"DELETE FROM {TBPERMISOPERFIL} WHERE {TBPERMISOPERFIL_ID} = %s "
            
            cursor.execute(query, (permiso_perfil_id,))
            conexion.commit()
            
            resultado["success"] = True
            resultado["message"] = "Eliminada exitosamente."
        except Exception as e:
            resultado["success"] = False
            resultado["message"] = f"Error al eliminar: {e}"
        finally:
            if conexion:
                conexion.close()

        return resultado
    
    
    def lista_permisos_perfil(self,pagina=1, tam_pagina=10, ordenar_por = TBPERMISOPERFIL_ID, tipo_orden="ASC", busqueda = None):
        conexion, resultado = conection()
        cursor = None
        if not resultado["success"]:
            return resultado
        
        listaPermisosPerfil = []
        try:
            with conexion.cursor(dictionary=True) as cursor: 
                #validacion de por que columna ordenar
                columna_orden = { 
                    "tabla":TBPERMISOPERFIL_TABLA,
                    "ver":TBPERMISOPERFIL_VER,
                    "crear":TBPERMISOPERFIL_INSERTAR,
                    "editar":TBPERMISOPERFIL_EDITAR,
                    "eliminar":TBPERMISOPERFIL_ELIMINAR,
                    "id":TBPERMISOPERFIL_ID
                }
                ## asigna sobre que tabla realizar el orden
                ordenar_por = columna_orden.get(ordenar_por, TBPERMISOPERFIL_ID)
                    
                ## asigna el tipo de orden ascendente o descendente
                tipo_orden = "ASC" if tipo_orden.upper() == "ASC" else "DESC"
                # Construcción de la consulta base
                query = f"SELECT * FROM {TBPERMISOPERFIL} "
                
                # Añadir cláusula de búsqueda si se proporciona
                valores = []
                if busqueda:
                    query += f"""
                        WHERE {TBPERMISOPERFIL_TABLA} LIKE %s 
                    """
                    valores = [f"%{busqueda}%"]
                
                # Añadir la cláusula ORDER BY y LIMIT/OFFSET
                query += f" ORDER BY {ordenar_por} {tipo_orden} LIMIT %s OFFSET %s"
                valores.extend([tam_pagina, (pagina - 1) * tam_pagina])

                cursor.execute(query, valores)
                
                #Leyendo los registros de 
                registros = cursor.fetchall()
                for registro in registros:
                    permiso:Permiso_Perfil = Permiso_Perfil(
                        registro[TBPERMISOPERFIL_PERFIL_ID],
                        registro[TBPERMISOPERFIL_TABLA],
                        registro[TBPERMISOPERFIL_VER],
                        registro[TBPERMISOPERFIL_INSERTAR],
                        registro[TBPERMISOPERFIL_EDITAR],
                        registro[TBPERMISOPERFIL_ELIMINAR],
                        registro[TBPERMISOPERFIL_ID]
                    )
                    listaPermisosPerfil.append(permiso)
                    
                # Obtener el total de registros para calcular el número total de páginas
                cursor.execute(f"SELECT COUNT(*) as total FROM {TBPERMISOPERFIL}")
                total_registros = cursor.fetchone()["total"]
                total_paginas = (total_registros + tam_pagina - 1) // tam_pagina  # Redondear hacia arriba

                resultado["data"] = {
                    "listaPermisosPerfil": listaPermisosPerfil,
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
    
    def get_permiso_perfil_ById(self,permiso_perfil_id:int):
        conexion, resultado = conection()
        if not resultado["success"]:
            return resultado

        try:
            with conexion.cursor() as cursor:
                query = f"""SELECT
                                {TBPERMISOPERFIL_PERFIL_ID}, 
                                {TBPERMISOPERFIL_TABLA}, 
                                {TBPERMISOPERFIL_VER},
                                {TBPERMISOPERFIL_INSERTAR}, 
                                {TBPERMISOPERFIL_EDITAR}, 
                                {TBPERMISOPERFIL_ELIMINAR}, 
                                {TBPERMISOPERFIL_ID} 
                            FROM {TBPERMISOPERFIL} 
                            WHERE id = %s"""
                
                cursor.execute(query, (permiso_perfil_id,))
                data = cursor.fetchone()
                
                if data:
                    permiso = Permiso_Perfil(
                        perfil_id  = data[0],
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