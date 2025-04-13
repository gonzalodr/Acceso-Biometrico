from data.EmpleadoData  import Empleado
from settings.config    import *       #obtener los nombres de tablas
from models.reporte     import Reporte #importa la clase de reportes 
from data.data          import conection # importa la funcion de conection para crear la conexion enla base de datos
from mysql.connector    import Error 
from settings.config    import *
from settings.logger    import logger
from datetime           import date



class ReporteData:
    
    #metodo para crear reporte en la base de datos
    def create_reporte(self, reporte: Reporte):
        #llama a la funcion conection para tener conexion a la base datos
        conexion, resultado = conection() 
        # verifica si la conexion falló
        if not resultado["success"]:
            return resultado
        
        try:
            #se crea el cursor para ejecutar las consultas SQL
            cursor = conexion.cursor()
            query = f"""INSERT INTO {TBREPORTE}(
            {TBREPORTE_ID_EMPLEADO},
            {TBREPORTE_FECHA_GENERACION},
            {TBREPORTE_TIPO_REPORTE},
            {TBREPORTE_CONTENIDO})
            VALUES (%s, %s, %s, %s)"""
            
            #define la consulta SQL pasando los objetos del reporte
            cursor.execute(query,(
                reporte.id_empleado,
                reporte.fecha_generacion,
                reporte.tipo_reporte,
                reporte.contenido
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
    def update_reporte(self, reporte: Reporte):
        #llama a la funcion conection para tener conexion a la base datos
        conexion, resultado = conection()
        # verifica si la conexion falló
        if not resultado["success"]:
            return resultado
        
        try:
            #se crea el cursor para ejecutar las consultas SQL
            cursor = conexion.cursor()
            
            #consulta SQL para actualizar un reporte en la tabla TBREPORTE
            query = f"""UPDATE {TBREPORTE} SET
            {TBREPORTE_ID_EMPLEADO} = %s,
            {TBREPORTE_FECHA_GENERACION} = %s,
            {TBREPORTE_TIPO_REPORTE} = %s,
            {TBREPORTE_CONTENIDO} = %s
            WHERE {TBREPORTE_ID} = %s"""
            
            #define la consulta SQL pasando los valores actualizados del  objetos reporte
            cursor.execute(query, (
                reporte.id_empleado,
                reporte.fecha_generacion,
                reporte.tipo_reporte,
                reporte.contenido,
                reporte.id
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
    def delete_reporte(self, id):
        #llama a la funcion conection para tener conexion a la base datos
        conexion, resultado = conection()
        # verifica si la conexion falló
        if not resultado["success"]:
            return resultado
        
        try:
            #se crea el cursor para ejecutar las consultas SQL
            cursor = conexion.cursor()
            #define la consulta SQL, pasando el ID del reporte a eliminar
            query = f"DELETE FROM {TBREPORTE} WHERE {TBREPORTE_ID} = %s"
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
    
    def list_reportes(self, pagina=1, tam_pagina=10, ordenar_por=TBREPORTE_ID, tipo_orden="ASC", busqueda=None):
        conexion, resultado = conection()
        if not resultado["success"]:
            return resultado
        
        listaReportes = [] #lista donde se almacenan los perfiles
        try:
            cursor = conexion.cursor(dictionary=True) #cursor para ejecutar las consultas
            #diccionario para  mapear los nombres de las columnas
            columna_orden = {
                "id_empleado": TBREPORTE_ID_EMPLEADO,
                "fecha_generacion": TBREPORTE_FECHA_GENERACION,
                "tipo_reporte": TBREPORTE_TIPO_REPORTE,
                "contenido": TBREPORTE_CONTENIDO
            }
            # si la columna esta desordenada se ordena por id
            ordenar_por = columna_orden.get(ordenar_por, TBREPORTE_ID)
            #se ajusta
            tipo_orden = "DESC" if tipo_orden != "ASC" else "ASC"
            
            query = f"""SELECT 
                    r.*,
                    p.{TBPERSONA_NOMBRE} AS nombre_persona
                FROM {TBREPORTE} r
                INNER JOIN {TBEMPLEADO} e ON r.{TBREPORTE_ID_EMPLEADO} = e.{TBEMPLEADO_ID}
                INNER JOIN {TBPERSONA} p ON e.{TBEMPLEADO_PERSONA} = p.{TBPERSONA_ID}"""
            valores = []
            
            if busqueda:
                query += f""" WHERE p.{TBPERSONA_NOMBRE} LIKE %s 
                              OR r.{TBREPORTE_ID_EMPLEADO} LIKE %s 
                              OR r.{TBREPORTE_FECHA_GENERACION} LIKE %s 
                              OR r.{TBREPORTE_TIPO_REPORTE} LIKE %s 
                              OR r.{TBREPORTE_CONTENIDO} LIKE %s """
                valores = [f"%{busqueda}%", f"%{busqueda}%", f"%{busqueda}%", f"%{busqueda}%", f"%{busqueda}%"]
            
            query += f" ORDER BY {ordenar_por} {tipo_orden} LIMIT %s OFFSET %s"
            valores.extend([tam_pagina, (pagina - 1) * tam_pagina])
            
            cursor.execute(query, valores) # Ejecuta la consulta SQL
            registros = cursor.fetchall()# Obtiene todos los registros
            for registro in registros:        # Se iteran los registros obtenidos y se convierten en objetos de tipo Perfil
                reporte = Reporte(
                    id_empleado=registro[TBREPORTE_ID_EMPLEADO],
                    fecha_generacion=registro[TBREPORTE_FECHA_GENERACION],
                    tipo_reporte=registro[TBREPORTE_TIPO_REPORTE],
                    contenido=registro[TBREPORTE_CONTENIDO],
                    id=registro[TBREPORTE_ID]
                )
                listaReportes.append({'reporte': reporte,'nombre_empleado': registro['nombre_persona'] })# Se añade el perfil a la lista
            
            cursor.execute(f"SELECT COUNT(*) as total FROM {TBREPORTE}") #TBROL
            total_registros = cursor.fetchone()["total"]  # Se obtiene el número total de registros
            total_paginas = (total_registros + tam_pagina - 1) // tam_pagina
            
            resultado["data"] = {
                "listaReportes": listaReportes,
                "pagina_actual": pagina,
                "tam_pagina": tam_pagina,
                "total_paginas": total_paginas,
                "total_registros": total_registros
            }
            resultado["success"] = True
            resultado["message"] = "Reportes listados exitosamente."
        except Exception as e:
            resultado["success"] = False
            resultado["message"] = f"Error al listar reportes: {e}"
        finally:
            if cursor:
                cursor.close()
            if conexion:
                conexion.close()
        return resultado
    
    def get_reporte_by_id(self, reporte_id):
        conexion, resultado = conection()
        if not resultado["success"]:
            return resultado

        try:
            cursor = conexion.cursor()
              # Consulta SQL para obtener el perfil por su ID
            query = f"""SELECT
                            {TBREPORTE_ID_EMPLEADO}, 
                            {TBREPORTE_FECHA_GENERACION}, 
                            {TBREPORTE_TIPO_REPORTE}, 
                            {TBREPORTE_CONTENIDO},
                            {TBREPORTE_ID} 
                        FROM {TBREPORTE} 
                        WHERE {TBREPORTE_ID} = %s"""
            
            cursor.execute(query, (reporte_id,)) #busca segun el id
            data = cursor.fetchone() # se obtiene el resultado
            
            if data: #si se encuentra el perfil
                reporte = Reporte(
                    id_empleado=data[0],
                    fecha_generacion=data[1],
                    tipo_reporte=data[2],
                    contenido=data[3],
                    id=data[4]
                )
                resultado["success"] = True
                resultado["data"] = reporte
            else:
                resultado["success"] = False
                resultado["message"] = "No se encontró ningún reporte con el ID proporcionado."
        except Exception as e:
            resultado["success"] = False
            resultado["message"] = f"Error al obtener reporte: {e}"
        finally:
            if conexion:
                conexion.close()
        return resultado
    
    def obtener_todo_reportes(self):
        conexion, resultado = conection()
        if not resultado["success"]:
            return resultado
        
        listaReportes = []  # Lista donde se almacenarán los perfiles ob
        try:
            with conexion.cursor(dictionary=True) as cursor:
                query = f"SELECT * FROM {TBREPORTE}"
                cursor.execute(query)
                registros = cursor.fetchall()
                
           # Se convierten los registros en objetos de tipo Reporte y se almacenan en la lista
                for registro in registros:
                    reporte = Reporte(
                        id_empleado=registro[TBREPORTE_ID_EMPLEADO],
                        fecha_generacion=registro[TBREPORTE_FECHA_GENERACION],
                        tipo_reporte=registro[TBREPORTE_TIPO_REPORTE],
                        contenido=registro[TBREPORTE_CONTENIDO],
                        id=registro[TBREPORTE_ID],
                    )
                    listaReportes.append(reporte)
                
                resultado["data"] = {
                    "listaReportes": listaReportes,
                }
                resultado["success"] = True
                resultado["message"] = "Reportes listados exitosamente."
        except Exception as e:
            resultado["success"] = False
            resultado["message"] = f"Error al listar reportes: {e}"
        finally:
            if cursor:
                cursor.close()# Se cierra el cursor
            if conexion:
                conexion.close()# Se cierra la conexión a la base de datos
        
        return resultado
        
    def obtener_datos_para_reporte(self,limit:int,offset:int, tipoReporte:str='todo', departamento:int = None,rol:int = None, id_empleado:int = None, rangoFechas:dict[str,date]= None):
        # conexion, resultado = conection()
        # if not resultado['success']:
        #     return resultado
        try:
            # with conexion.cursor(dictionary=True) as cursor:
                datosSelect = []
                leftJoin    = []
                condicion   = []
                valores     = ()

                if rangoFechas:
                    if len(rangoFechas) < 2:
                        return {'success':False, 'message':'Error de fechas no proporcionadas correctamente.'}


                if id_empleado:
                    condicion.append(f'E.{TBEMPLEADO_ID} == %s')
                    valores += (id_empleado,)
                    pass

                if tipoReporte:
                    if tipoReporte  == 'justificacion'  or tipoReporte == 'todo':
                        leftJoin.append(F'LEFT JOIN {TBJUSTIFICACION} J ON J.{TBJUSTIFICACION_ID_EMPLEADO} == E.{TBEMPLEADO_ID}')
                        datosSelect.append(f'J.{TBJUSTIFICACION_ID}')
                        datosSelect.append(f'J.{TBJUSTIFICACION_ID_EMPLEADO}')
                        datosSelect.append(f'J.{TBJUSTIFICACION_ID_ASISTENCIA}')
                        datosSelect.append(f'J.{TBJUSTIFICACION_FECHA}')
                        datosSelect.append(f'J.{TBJUSTIFICACION_MOTIVO}')
                        datosSelect.append(f'J.{TBJUSTIFICACION_DESCRIPCION}')
                        if rangoFechas:
                            condicion.append(f'J.{TBJUSTIFICACION_FECHA} >= %s')
                            valores += (rangoFechas[0],)
                            condicion.append(f'J.{TBJUSTIFICACION_FECHA} <= %s')
                            valores += (rangoFechas[1],)

                    if tipoReporte  == 'asistencias'    or tipoReporte == 'todo':
                        leftJoin.append(f'LEFT JOIN {TBASISTENCIA} A ON A.{TBASISTENCIA_ID_EMPLEADO} == E.{TBEMPLEADO_ID}')
                        datosSelect.append(f'A.{TBASISTENCIA_ID}')
                        datosSelect.append(f'A.{TBASISTENCIA_ID_EMPLEADO}')
                        datosSelect.append(f'A.{TBASISTENCIA_FECHA}')
                        datosSelect.append(f'A.{TBASISTENCIA_ESTADO_ASISTENCIA}')
                        if rangoFechas:
                            condicion.append(f'A.{TBASISTENCIA_FECHA} >= %s')
                            valores += (rangoFechas[0],)
                            condicion.append(f'A.{TBASISTENCIA_FECHA} <= %s')
                            valores += (rangoFechas[1],)
                        
                    if tipoReporte  == 'permisos'       or tipoReporte == 'todo':
                        leftJoin.append(f'LEFT JOIN {TBSOLICITUDPERMISOS} SP ON SP.{TBSOLICITUDPERMISOS_ID_EMPLEADO} == E.{TBEMPLEADO_ID}')
                        datosSelect.append(f'SP.{TBSOLICITUDPERMISOS_ID}')
                        datosSelect.append(f'SP.{TBSOLICITUDPERMISOS_ID_EMPLEADO}')
                        datosSelect.append(f'SP.{TBSOLICITUDPERMISOS_TIPO}')
                        datosSelect.append(f'SP.{TBSOLICITUDPERMISOS_FECHA_INICIO}')
                        datosSelect.append(f'SP.{TBSOLICITUDPERMISOS_FECHA_FIN}')
                        datosSelect.append(f'SP.{TBSOLICITUDPERMISOS_DESCRIPCION}')
                        datosSelect.append(f'SP.{TBSOLICITUDPERMISOS_ESTADO}')
                        if rangoFechas:
                            condicion.append(f'SP.{TBSOLICITUDPERMISOS_FECHA_INICIO} >= %s')
                            valores += (rangoFechas[0],)
                            condicion.append(f'SP.{TBSOLICITUDPERMISOS_FECHA_FIN} <= %s')
                            valores += (rangoFechas[1],)
                

                    
                query =f'''SELECT \n {',\n'.join(datosSelect)} \n FROM {TBEMPLEADO} E \n{'\n'.join(leftJoin)} \nWHERE {'\n AND '.join(condicion)}'''
    

                print(query)
                print(valores)


        except Exception as e:
            logger.error(f'{e}')
            return {'succces':False, 'message':'Ocurrio un error al obtener los datos para el reporte.'}
        pass