from models.rol import Rol
from data.data import conection
from settings.config import *

class RolData:
    
    def create_rol(self, rol: Rol):
        conexion, resultado = conection()
        if not resultado["success"]:
            return resultado
        
        try:
            cursor = conexion.cursor()
            query = f"""INSERT INTO {TBROL}(
            {TBROL_NOMBRE},
            {TBROL_DESCRIPCION})
            VALUES (%s, %s)"""
            
            cursor.execute(query, (
                rol.nombre,
                rol.descripcion
            ))
            conexion.commit()
            resultado["success"] = True
            resultado["message"] = "Rol creado exitosamente."
        except Exception as e:
            resultado["success"] = False
            resultado["message"] = f"Error al crear rol: {e}"
        finally:
            if conexion:
                conexion.close()
        return resultado
    
    def update_rol(self, rol: Rol):
        conexion, resultado = conection()
        if not resultado["success"]:
            return resultado
        
        try:
            cursor = conexion.cursor()
            query = f"""UPDATE {TBROL} SET 
            {TBROL_NOMBRE} = %s,
            {TBROL_DESCRIPCION} = %s
            WHERE {TBROL_ID} = %s"""
            
            cursor.execute(query, (
                rol.nombre,
                rol.descripcion,
                rol.id
            ))
            conexion.commit()
            resultado["success"] = True
            resultado["message"] = "Rol actualizado exitosamente."
        except Exception as e:
            resultado["success"] = False
            resultado["message"] = f"Error al actualizar rol: {e}"
        finally:
            if conexion:
                conexion.close()
        return resultado
    
    def delete_rol(self, rol_id):
        conexion, resultado = conection()
        if not resultado["success"]:
            return resultado
        
        try:
            cursor = conexion.cursor()
            query = f"DELETE FROM {TBROL} WHERE {TBROL_ID} = %s"
            
            cursor.execute(query, (rol_id,))
            conexion.commit()
            
            resultado["success"] = True
            resultado["message"] = "Rol eliminado exitosamente."
        except Exception as e:
            resultado["success"] = False
            resultado["message"] = f"Error al eliminar rol: {e}"
        finally:
            if conexion:
                conexion.close()
        return resultado
    
    def list_roles(self, pagina=1, tam_pagina=10, ordenar_por=TBROL_ID, tipo_orden="ASC", busqueda=None):
        conexion, resultado = conection()
        if not resultado["success"]:
            return resultado
        
        listaRoles = []
        try:
            cursor = conexion.cursor(dictionary=True)
            columna_orden = {
                "nombre": TBROL_NOMBRE,
                "descripcion": TBROL_DESCRIPCION
            }
            ordenar_por = columna_orden.get(ordenar_por, TBROL_ID)
            tipo_orden = "DESC" if tipo_orden != "ASC" else "ASC"
            
            query = f"SELECT * FROM {TBROL}"
            valores = []
            if busqueda:
                query += f" WHERE {TBROL_NOMBRE} LIKE %s OR {TBROL_DESCRIPCION} LIKE %s"
                valores = [f"%{busqueda}%", f"%{busqueda}%"]
            
            query += f" ORDER BY {ordenar_por} {tipo_orden} LIMIT %s OFFSET %s"
            valores.extend([tam_pagina, (pagina - 1) * tam_pagina])
            
            cursor.execute(query, valores)
            registros = cursor.fetchall()
            for registro in registros:
                rol = Rol(
                    nombre=registro[TBROL_NOMBRE],
                    descripcion=registro[TBROL_DESCRIPCION],
                    id=registro[TBROL_ID]
                )
                listaRoles.append(rol)
            
            cursor.execute(f"SELECT COUNT(*) as total FROM {TBROL}")
            total_registros = cursor.fetchone()["total"]
            total_paginas = (total_registros + tam_pagina - 1) // tam_pagina
            
            resultado["data"] = {
                "listaRoles": listaRoles,
                "pagina_actual": pagina,
                "tam_pagina": tam_pagina,
                "total_paginas": total_paginas,
                "total_registros": total_registros
            }
            resultado["success"] = True
            resultado["message"] = "Roles listados exitosamente."
        except Exception as e:
            resultado["success"] = False
            resultado["message"] = f"Error al listar roles: {e}"
        finally:
            if cursor:
                cursor.close()
            if conexion:
                conexion.close()
        return resultado
    
    def get_rol_by_id(self, rol_id):
        conexion, resultado = conection()
        if not resultado["success"]:
            return resultado

        try:
            cursor = conexion.cursor()
            query = f"""SELECT
                            {TBROL_NOMBRE}, 
                            {TBROL_DESCRIPCION}, 
                            {TBROL_ID} 
                        FROM {TBROL} 
                        WHERE {TBROL_ID} = %s"""
            
            cursor.execute(query, (rol_id,))
            data = cursor.fetchone()
            
            if data:
                rol = Rol(
                    nombre=data[0],
                    descripcion=data[1],
                    id=data[2]
                )
                resultado["success"] = True
                resultado["data"] = rol
            else:
                resultado["success"] = False
                resultado["message"] = "No se encontró ningún rol con el ID proporcionado."
        except Exception as e:
            resultado["success"] = False
            resultado["message"] = f"Error al obtener rol: {e}"
        finally:
            if conexion:
                conexion.close()
        return resultado

    def obtener_todo_roles(self):
        conexion, resultado = conection()
        if not resultado["success"]:
            return resultado
        
        listaRoles = []
        try:
            with conexion.cursor(dictionary=True) as cursor:
                query = f"SELECT * FROM {TBROL}"
                cursor.execute(query)
                registros = cursor.fetchall()
                for registro in registros:
                    rol = Rol(
                        nombre=registro[TBROL_NOMBRE],
                        descripcion=registro[TBROL_DESCRIPCION],
                        id=registro[TBROL_ID]
                    )
                    listaRoles.append(rol)
                
                resultado["data"] = {
                    "listaRoles": listaRoles,
                }
                resultado["success"] = True
                resultado["message"] = "Roles listados exitosamente."
        except Exception as e:
            resultado["success"] = False
            resultado["message"] = f"Error al listar roles: {e}"
        finally:
            if cursor:
                cursor.close()
            if conexion:
                conexion.close()
        return resultado