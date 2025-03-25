from models.perfil import Perfil
from data.data import conection
from settings.config import *
from settings.logger import logger
from data.permisosPerfilData import PermisosPerfilData
import traceback

class PerfilData:
    def __init__(self):
        self.permisoPerfilData = PermisosPerfilData()
    def create_perfil(self, perfil: Perfil): #metodo para crear el perfil en la base de datos
        conexion, resultado = conection() 
        if not resultado["success"]: # si falla la conexion retorna error
            return resultado
        
        try:
            cursor = conexion.cursor() #se utiliza el cursor para las consultas a la base de datos
            query = f"""INSERT INTO {TBPERFIL}(
            {TBPERFIL_NOMBRE},
            {TBPERFIL_DESCRIPCION})
            VALUES (%s, %s)""" #campos o posciones 
            
            cursor.execute(query,(
                perfil.nombre,
                perfil.descripcion
            ))
            conexion.commit() #uarda los cambios
            resultado["success"] = True
            resultado["message"] = "Perfil creado exitosamente"
        except Exception as e: #captura errores
            resultado["success"] = False
            resultado["message"] = f"Error al crear perfil: {e}"
        finally:
            if conexion:
                conexion.close()
        return resultado
    
    def update_perfil(self, perfil: Perfil): #metodo para actualizar perfil
        conexion, resultado = conection() # obtiene el estado de la conexion
        if not resultado["success"]: # error
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
        
        listaPerfiles = [] #lista donde se almacenan los perfiles
        try:
            with conexion.cursor(dictionary=True)  as cursor:

                columna_orden = {
                    "nombre"        : TBPERFIL_NOMBRE,
                    "descripcion"   : TBPERFIL_DESCRIPCION
                }

                ordenar_por = columna_orden.get(ordenar_por, TBPERFIL_ID)
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
                        nombre      =registro[TBPERFIL_NOMBRE],
                        descripcion =registro[TBPERFIL_DESCRIPCION],
                        id          =registro[TBPERFIL_ID]
                    )
                    result        = self.permisoPerfilData.get_permisos_perfil_ByPerfilId(perfil.id)
                    if not result['success']:
                        return result
                    listaPerfiles.append({'perfil':perfil,'listaPermisos':result['listaPermiso']})
                    
                cursor.execute(f"SELECT COUNT(*) as total FROM {TBPERFIL}") 
                total_registros = cursor.fetchone()["total"] 
                total_paginas = (total_registros + tam_pagina - 1) // tam_pagina
                
                 
                return {'success':True,'message':'Perfiles listados correctamente.','data':{
                    "listaPerfiles": listaPerfiles,
                    "pagina_actual": pagina,
                    "tam_pagina": tam_pagina,
                    "total_paginas": total_paginas,
                    "total_registros": total_registros
                }}
    
        except Exception as e:
            logger.error(f'{e}-Traceback: {traceback.format_exc()}')
            return {'success':False,'message':'Ocurrio un error al listar los perfiles.'}
        finally:
            if conexion:
                conexion.close()
    
    def get_perfil_by_id(self, perfil_id):
        conexion, resultado = conection()
        if not resultado["success"]:
            return resultado

        try:
            cursor = conexion.cursor()
              # Consulta SQL para obtener el perfil por su ID
            query = f"""SELECT
                            {TBPERFIL_NOMBRE}, 
                            {TBPERFIL_DESCRIPCION}, 
                            {TBPERFIL_ID} 
                        FROM {TBPERFIL} 
                        WHERE {TBPERFIL_ID} = %s"""
            
            cursor.execute(query, (perfil_id,)) #busca segun el id
            data = cursor.fetchone() # se obtiene el resultado
            
            if data: #si se encuentra el perfil
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
        
        listaPerfiles = []  # Lista donde se almacenarán los perfiles ob
        try:
            with conexion.cursor(dictionary=True) as cursor:
                query = f"SELECT * FROM {TBPERFIL}"
                cursor.execute(query)
                registros = cursor.fetchall()
                
                 # Se convierten los registros en objetos de tipo Perfil y se almacenan en la lista
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
                cursor.close()# Se cierra el cursor
            if conexion:
                conexion.close()# Se cierra la conexión a la base de datos

        return resultado