from models.perfil import Perfil
from data.data import conection
from settings.config import *

class PerfilData:
    
    def create_perfil(self, perfil: Perfil):
        conexion, resultado = conection()
        if not resultado["success"]:
            return resultado
        
        try:
            cursor = conexion.cursor()
            query = f"""INSERT INTO {TBPERFIL}(
            {TBPERFIL_NOMBRE},
            {TBPERFIL_DESCRIPCION})
            VALUES (%s, %s)"""
            
            cursor.execute(query,(
                perfil.nombre,
                perfil.descripcion
            ))
            conexion.commit()
            resultado["success"] = True
            resultado["message"] = "Perfil creado exitosamente"
        except Exception as e:
            resultado["success"] = False
            resultado["message"] = f"Error al crear perfil: {e}"
        finally:
            if conexion:
                conexion.close()
        return resultado
    
    def update_perfil(self, perfil: Perfil):
        conexion, resultado = conection()
        if not resultado["success"]:
            return resultado
        
        try:
            cursor = conexion.cursor()
            query = f"""UPDATE {TBPERFIL} SET 
            {TBPERFIL_NOMBRE} = %s,
            {TBPERFIL_DESCRIPCION} = %s
            WHERE {TBPERFIL_ID} = %s"""
            
            cursor.execute(query, (
                perfil.nombre,
                perfil.descripcion,
                perfil.id
            ))
            conexion.commit()
            resultado["success"] = True
            resultado["message"] = "Perfil actualizado exitosamente."
        except Exception as e:
            resultado["success"] = False
            resultado["message"] = f"Error al actualizar perfil: {e}"
        finally:
            if conexion:
                conexion.close()
        return resultado
    
    def delete_perfil(self, perfil_id):
        conexion, resultado = conection()
        if not resultado["success"]:
            return resultado
        
        try:
            cursor = conexion.cursor()
            query = f"DELETE FROM {TBPERFIL} WHERE {TBPERFIL_ID} = %s"
            
            cursor.execute(query, (perfil_id,))
            conexion.commit()
            
            resultado["success"] = True
            resultado["message"] = "Perfil eliminado exitosamente."
        except Exception as e:
            resultado["success"] = False
            resultado["message"] = f"Error al eliminar perfil: {e}"
        finally:
            if conexion:
                conexion.close()
        return resultado
    
    def list_perfiles(self, pagina=1, tam_pagina=10, ordenar_por=TBPERFIL_ID, tipo_orden="ASC", busqueda=None):
        conexion, resultado = conection()
        if not resultado["success"]:
            return resultado
        
        listaPerfiles = []
        try:
            cursor = conexion.cursor(dictionary=True)
            columna_orden = {
                "nombre": TBPERFIL_NOMBRE,
                "descripcion": TBPERFIL_DESCRIPCION
            }
            ordenar_por = columna_orden.get(ordenar_por, TBROL_ID)
            tipo_orden = "DESC" if tipo_orden != "ASC" else "ASC"
            
            query = f"SELECT * FROM {TBPERFIL}"
            valores = []
            if busqueda:
                query += f" WHERE {TBPERFIL_NOMBRE} LIKE %s OR {TBPERFIL_DESCRIPCION} LIKE %s"
                valores = [f"%{busqueda}%", f"%{busqueda}%"]
            
            query += f" ORDER BY {ordenar_por} {tipo_orden} LIMIT %s OFFSET %s"
            valores.extend([tam_pagina, (pagina - 1) * tam_pagina])
            
            cursor.execute(query, valores)
            registros = cursor.fetchall()
            for registro in registros:
                perfil = Perfil(
                    nombre=registro[TBPERFIL_NOMBRE],
                    descripcion=registro[TBPERFIL_DESCRIPCION],
                    id=registro[TBPERFIL_ID]
                )
                listaPerfiles.append(perfil)
            
            cursor.execute(f"SELECT COUNT(*) as total FROM {TBROL}")
            total_registros = cursor.fetchone()["total"]
            total_paginas = (total_registros + tam_pagina - 1) // tam_pagina
            
            resultado["data"] = {
                "listaPerfiles": listaPerfiles,
                "pagina_actual": pagina,
                "tam_pagina": tam_pagina,
                "total_paginas": total_paginas,
                "total_registros": total_registros
            }
            resultado["success"] = True
            resultado["message"] = "Perfiles listados exitosamente."
        except Exception as e:
            resultado["success"] = False
            resultado["message"] = f"Error al listar perfiles: {e}"
        finally:
            if cursor:
                cursor.close()
            if conexion:
                conexion.close()
        return resultado
    
    def get_perfil_by_id(self, perfil_id):
        conexion, resultado = conection()
        if not resultado["success"]:
            return resultado

        try:
            cursor = conexion.cursor()
            query = f"""SELECT
                            {TBPERFIL_NOMBRE}, 
                            {TBPERFIL_DESCRIPCION}, 
                            {TBPERFIL_ID} 
                        FROM {TBPERFIL} 
                        WHERE {TBPERFIL_ID} = %s"""
            
            cursor.execute(query, (perfil_id,))
            data = cursor.fetchone()
            
            if data:
                perfil = Perfil(
                    nombre=data[0],
                    descripcion=data[1],
                    id=data[2]
                )
                resultado["success"] = True
                resultado["data"] = perfil
            else:
                resultado["success"] = False
                resultado["message"] = "No se encontró ningún perfil con el ID proporcionado."
        except Exception as e:
            resultado["success"] = False
            resultado["message"] = f"Error al obtener perfil: {e}"
        finally:
            if conexion:
                conexion.close()
        return resultado
    
    def obtener_todo_perfiles(self):
        conexion, resultado = conection()
        if not resultado["success"]:
            return resultado
        
        listaPerfiles = []
        try:
            with conexion.cursor(dictionary=True) as cursor:
                query = f"SELECT * FROM {TBPERFIL}"
                cursor.execute(query)
                registros = cursor.fetchall()
                for registro in registros:
                    perfil = Perfil(
                        nombre=registro[TBPERFIL_NOMBRE],
                        descripcion=registro[TBPERFIL_DESCRIPCION],
                        id=registro[TBPERFIL_ID]
                    )
                    listaPerfiles.append(perfil)
                
                resultado["data"] = {
                    "listaPerfiles": listaPerfiles,
                }
                resultado["success"] = True
                resultado["message"] = "Perfiles listados exitosamente."
        except Exception as e:
            resultado["success"] = False
            resultado["message"] = f"Error al listar perfiles: {e}"
        finally:
            if cursor:
                cursor.close()
            if conexion:
                conexion.close()
        return resultado