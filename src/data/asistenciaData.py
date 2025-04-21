from models.asistencia import Asistencia #importa la clase de reportes 
from data.data import conection # importa la funcion de conection para crear la conexion enla base de datos
from settings.config import * 
from mysql.connector import Error
from settings.logger import logger

class AsistenciaData:
    
    def create_asistencia(self, asistencia: Asistencia):
        conexion, resultado = conection() 
        # verifica si la conexion falló
        if not resultado["success"]:
            return resultado
        
        try:
            #se crea el cursor para ejecutar las consultas SQL
            cursor = conexion.cursor()
            query = f"""INSERT INTO {TBASISTENCIA}(
            {TBASISTENCIA_ID_EMPLEADO},
            {TBASISTENCIA_FECHA},
            {TBASISTENCIA_ESTADO_ASISTENCIA})
            VALUES (%s, %s, %s)"""
            
            #define la consulta SQL pasando los objetos del reporte
            cursor.execute(query,(
                asistencia.id_empleado,
                asistencia.fecha,
                asistencia.estado_asistencia,
            ))
            #confirma los cambios en la base de datos
            conexion.commit()
            #actualiza el resultado indicando que la operacion fue exitosa
            resultado["success"] = True
            resultado["message"] = "Reporte creado exitosamente"
            #captura cualquier excepcion que ocurra duante la consulta
        except Exception as e :
            resultado["success"] = False
            #guarda el mensaje de error
            resultado["message"] = f"Erorr al crear reporte:  {e}"
            #cierra la conexion si esta abierta
        finally:
            if conexion:
                conexion.close()
        return resultado 
    
    
    #metodo para actualizar el reporte
    def update_asistencia(self, asistencia: Asistencia):
        #llama a la funcion conection para tener conexion a la base datos
        conexion, resultado = conection()
        # verifica si la conexion falló
        if not resultado["success"]:
            return resultado
        
        try:
            #se crea el cursor para ejecutar las consultas SQL
            cursor = conexion.cursor()
            
            #consulta SQL para actualizar un reporte en la tabla TBREPORTE
            query = f"""UPDATE {TBASISTENCIA} SET
            {TBASISTENCIA_ID_EMPLEADO} = %s,
            {TBASISTENCIA_FECHA} = %s,
            {TBASISTENCIA_ESTADO_ASISTENCIA} = %s
            WHERE {TBASISTENCIA_ID} = %s"""
            
            #define la consulta SQL pasando los valores actualizados del  objetos reporte
            cursor.execute(query, (
                asistencia.id_empleado,
                asistencia.fecha,
                asistencia.estado_asistencia,
                asistencia.id
            ))
            #confirma los cambios en la base de datos
            conexion.commit()
            #indica que la operacion fue exitosa
            resultado["success"] = True
            resultado["message"] = "Reporte actualizado exitosamente."
            #captura cualquier excepcion que ocurra duante la consulta
        except Exception as e:
            resultado["success"] = False
            #guarda el mensaje de error
            resultado["message"] = f"Error al actualizar reporte: {e}"
        #cierra la conexion si esta abierta    
        finally:
            if conexion:
                conexion.close()
        return resultado
    
    #metodo de eliminar un reporte
    def delete_asistencia(self, id):
        #llama a la funcion conection para tener conexion a la base datos
        conexion, resultado = conection()
        # verifica si la conexion falló
        if not resultado["success"]:
            return resultado
        
        try:
            #se crea el cursor para ejecutar las consultas SQL
            cursor = conexion.cursor()
            #define la consulta SQL, pasando el ID del reporte a eliminar
            query = f"DELETE FROM {TBASISTENCIA} WHERE {TBASISTENCIA_ID} = %s"
            # Ejecuta la consulta SQL pasando el ID del reporte a eliminar
            cursor.execute(query, (id,))
            # Confirma los cambios en la base de datos
            conexion.commit()
            # Indica que la eliminacion fue exitosa
            resultado["success"] = True
            resultado["message"] = "Reporte eliminado exitosamente."
        # Captura cualquier excepcion que ocurra durante la eliminacion
        except Exception as e:
            resultado["success"] = False
            #gaurda el mensaje de error
            resultado["message"] = f"Error al eliminar reporte: {e}"
        #cierra la conexion si esta abierta
        finally:
            if conexion:
                conexion.close()
        return resultado
    
    def list_asistencias(self, pagina=1, tam_pagina=10, ordenar_por=TBASISTENCIA_ID, tipo_orden="ASC", busqueda=None):
        conexion, resultado = conection()
        if not resultado["success"]:
            return resultado
        
        listaAsistencias = [] #lista donde se almacenan los perfiles
        try:
            cursor = conexion.cursor(dictionary=True) #cursor para ejecutar las consultas
            #diccionario para  mapear los nombres de las columnas
            columna_orden = {
                "id_empleado": TBASISTENCIA_ID_EMPLEADO,
                "fecha": TBASISTENCIA_FECHA,
                "estado_asistencia": TBASISTENCIA_ESTADO_ASISTENCIA
            }
            # si la columna esta desordenada se ordena por id
            ordenar_por = columna_orden.get(ordenar_por, TBASISTENCIA_ID)
            #se ajusta
            tipo_orden = "DESC" if tipo_orden != "ASC" else "ASC"
            
            query = f"""SELECT 
                    a.*,
                    p.{TBPERSONA_NOMBRE} AS nombre_persona
                FROM {TBASISTENCIA} a
                INNER JOIN {TBEMPLEADO} e ON a.{TBASISTENCIA_ID_EMPLEADO} = e.{TBEMPLEADO_ID}
                INNER JOIN {TBPERSONA} p ON e.{TBEMPLEADO_PERSONA} = p.{TBPERSONA_ID}"""
            valores = []
            
            if busqueda:
                query += f""" WHERE {TBASISTENCIA_ID_EMPLEADO} LIKE %s 
                              OR {TBASISTENCIA_FECHA} LIKE %s
                              OR {TBASISTENCIA_ESTADO_ASISTENCIA} LIKE %s """
                valores = [f"%{busqueda}%", f"%{busqueda}%", f"%{busqueda}%"]
            
            query += f" ORDER BY {ordenar_por} {tipo_orden} LIMIT %s OFFSET %s"
            valores.extend([tam_pagina, (pagina - 1) * tam_pagina])
            
            cursor.execute(query, valores) # Ejecuta la consulta SQL
            registros = cursor.fetchall()# Obtiene todos los registros
            for registro in registros:        # Se iteran los registros obtenidos y se convierten en objetos de tipo Perfil
                asistencia = Asistencia(
                    id_empleado=registro[TBASISTENCIA_ID_EMPLEADO],
                    fecha=registro[TBASISTENCIA_FECHA],
                    estado_asistencia=registro[TBASISTENCIA_ESTADO_ASISTENCIA],
                    id=registro[TBASISTENCIA_ID]
                )
                listaAsistencias.append({'asistencia': asistencia, 'nombre_empleado': registro['nombre_persona']})# Se añade el perfil a la lista
            
            cursor.execute(f"SELECT COUNT(*) as total FROM {TBASISTENCIA}") #TBROL
            total_registros = cursor.fetchone()["total"]  # Se obtiene el número total de registros
            total_paginas = (total_registros + tam_pagina - 1) // tam_pagina
            
            resultado["data"] = {
                "listaAsistencias": listaAsistencias,
                "pagina_actual": pagina,
                "tam_pagina": tam_pagina,
                "total_paginas": total_paginas,
                "total_registros": total_registros
            }
            resultado["success"] = True
            resultado["message"] = "Asistencias listados exitosamente."
        except Exception as e:
            resultado["success"] = False
            resultado["message"] = f"Error al listar asistencias: {e}"
        finally:
            if cursor:
                cursor.close()
            if conexion:
                conexion.close()
        return resultado
    
    def get_asistencia_by_id(self, asistencia_id):
        conexion, resultado = conection()
        if not resultado["success"]:
            return resultado

        try:
            cursor = conexion.cursor()
              # Consulta SQL para obtener el perfil por su ID
            query = f"""SELECT
                            {TBASISTENCIA_ID_EMPLEADO}, 
                            {TBASISTENCIA_FECHA}, 
                            {TBASISTENCIA_ESTADO_ASISTENCIA}, 
                            {TBASISTENCIA_ID} 
                        FROM {TBASISTENCIA} 
                        WHERE {TBASISTENCIA_ID} = %s"""
            
            cursor.execute(query, (asistencia_id,)) #busca segun el id
            data = cursor.fetchone() # se obtiene el resultado
            
            if data: #si se encuentra el perfil
                asistencia = Asistencia(
                    id_empleado=data[0],
                    fecha=data[1],
                    estado_asistencia=data[2],
                    id=data[3]
                )
                resultado["success"] = True
                resultado["data"] = asistencia
            else:
                resultado["success"] = False
                resultado["message"] = "No se encontró ninguna asistencia con el ID proporcionado."
        except Exception as e:
            resultado["success"] = False
            resultado["message"] = f"Error al obtener asistencia: {e}"
        finally:
            if conexion:
                conexion.close()
        return resultado
    
    def obtener_todo_asistencias(self):
        conexion, resultado = conection()
        if not resultado["success"]:
            return resultado
        
        listaAsistencias = []  # Lista donde se almacenarán los perfiles ob
        try:
            with conexion.cursor(dictionary=True) as cursor:
                query = f"SELECT * FROM {TBASISTENCIA}"
                cursor.execute(query)
                registros = cursor.fetchall()
                
                 # Se convierten los registros en objetos de tipo Perfil y se almacenan en la lista
                for registro in registros:
                    asistencia = Asistencia(
                        id_empleado=registro[TBASISTENCIA_ID_EMPLEADO],
                        fecha=registro[TBASISTENCIA_FECHA],
                        estado_asistencia=registro[TBASISTENCIA_ESTADO_ASISTENCIA],
                        id=registro[TBASISTENCIA_ID]
                    )
                    listaAsistencias.append(asistencia)
                
                resultado["data"] = {
                    "listaAsistencias": listaAsistencias,
                }
                resultado["success"] = True
                resultado["message"] = "Asistencias listadas exitosamente."
        except Exception as e:
            resultado["success"] = False
            resultado["message"] = f"Error al listar asistencias: {e}"
        finally:
            if cursor:
                cursor.close()# Se cierra el cursor
            if conexion:
                conexion.close()# Se cierra la conexión a la base de datos

        return resultado


    def listar_asistencia_por_empleado(self, id_empleado: int):
        conexion, resultado = conection()
        if not resultado["success"]:
            return resultado
        
        listaAsistencias = []
        try:
            with conexion.cursor(dictionary=True) as cursor:
                query = f'''
                    SELECT Id, Id_Empleado, Fecha, Estado_Asistencia 
                    FROM Asistencia 
                    WHERE Id_Empleado = %s AND Estado_Asistencia = 'No_Justificada'
                    ORDER BY Fecha DESC
                '''
                cursor.execute(query, (id_empleado,))
                registros = cursor.fetchall()
                
                for data in registros:
                    asistencia = Asistencia(
                        id=data["Id"],
                        id_empleado=data["Id_Empleado"],
                        fecha=data["Fecha"],
                        estado_asistencia=data["Estado_Asistencia"]
                    )
                    listaAsistencias.append(asistencia)
                
                return {
                    "data": listaAsistencias,
                    "success": True,
                    "message": "Asistencias listadas exitosamente."
                }
        except Error as e:
            logger.error(f"Error al listar asistencias: {e}")
            return {"success": False, "message": "Ocurrió un error al listar las asistencias."}
        finally:
            if conexion:
                conexion.close()
