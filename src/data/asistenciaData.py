from models.asistencia          import Asistencia
from models.detalle_asistencia  import DetalleAsistencia

from data.data import conection # importa la funcion de conection para crear la conexion enla base de datos
from settings.config import * 
from mysql.connector import Error
from settings.logger import logger
from datetime        import datetime, timedelta
from data.horarioData import HorarioData

class AsistenciaData:
    def __init__(self):
        self.horarioData = HorarioData()
    
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
                    WHERE Id_Empleado = %s AND Estado_Asistencia = 'Ausente'
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

    def registrar_asistencia(self, lista):
        conexion, resultado = conection()
        if not resultado['success']:
            return resultado

        try:
            with conexion.cursor(dictionary=True) as cursor:
                nuevas_asistencias      = []
                nuevos_detalles         = []
                asistencias_existentes  = []

                # listaHorario            = self.horarioData.get_horario_by_empleado()
                
                
                for asistencia, hora in lista:
                    # Verificar si ya existe la asistencia para ese empleado y fecha
                    cursor.execute(f'''
                        SELECT * FROM {TBASISTENCIA}
                        WHERE {TBASISTENCIA_FECHA} = %s
                        AND {TBASISTENCIA_ID_EMPLEADO} = %s;
                    ''', (asistencia.fecha, asistencia.id_empleado))

                    existe = cursor.fetchone()

                    if existe:
                        asistencia.id = existe[TBASISTENCIA_ID]
                        asistencias_existentes.append((asistencia, hora))  # Se procesan uno a uno
                    else:
                        nuevas_asistencias.append((asistencia.id_empleado, asistencia.fecha, asistencia.estado_asistencia))
                        nuevos_detalles.append((None, hora))  # ID se completará luego

                # Insertar nuevas asistencias
                if nuevas_asistencias:
                    cursor.executemany(f'''
                        INSERT INTO {TBASISTENCIA} (
                            {TBASISTENCIA_ID_EMPLEADO},
                            {TBASISTENCIA_FECHA},
                            {TBASISTENCIA_ESTADO_ASISTENCIA}
                        ) VALUES (%s, %s, %s);
                    ''', nuevas_asistencias)

                    # Recuperar los IDs insertados
                    primer_id = cursor.lastrowid
                    for i in range(len(nuevas_asistencias)):
                        nuevos_detalles[i] = (primer_id + i, nuevos_detalles[i][1]) 

                    # Insertar nuevos detalles
                    cursor.executemany(f'''
                        INSERT INTO {TBDETALLEASISTENCIA} (
                            {TBDETALLEASISTENCIA_ID_ASISTENCIA},
                            {TBDETALLEASISTENCIA_HORA_ENTRADA}
                        ) VALUES (%s, %s);
                    ''', nuevos_detalles)

                # Procesar actualizaciones de asistencias existentes
                for asistencia, hora in asistencias_existentes:
                    cursor.execute(f'''
                        SELECT * FROM {TBDETALLEASISTENCIA}
                        WHERE {TBDETALLEASISTENCIA_ID_ASISTENCIA} = %s;
                    ''', (asistencia.id,))

                    data = cursor.fetchone()
                    if data:
                        detalle = DetalleAsistencia(
                            id_detalle=data[TBDETALLEASISTENCIA_ID],
                            id_asistencia=data[TBDETALLEASISTENCIA_ID_ASISTENCIA],
                            hora_entrada=data[TBDETALLEASISTENCIA_HORA_ENTRADA],
                            hora_salida=data[TBDETALLEASISTENCIA_HORA_SALIDA],
                            horas_trabajadas=data[TBDETALLEASISTENCIA_HORAS_TRABAJADAS]
                        )

                        # Normalizar hora_entrada si viene como timedelta
                        if isinstance(detalle.hora_entrada, timedelta):
                            detalle.hora_entrada = (datetime.min + detalle.hora_entrada).time()

                        if detalle.hora_entrada is None:
                            detalle.hora_entrada = hora
                        elif detalle.hora_entrada == hora or hora < detalle.hora_entrada:
                            continue
                        else:
                            detalle.hora_salida = hora
                            fecha_actual        = datetime.now().date()
                            datetime_salida     = datetime.combine(fecha_actual, detalle.hora_salida)
                            datetime_entrada    = datetime.combine(fecha_actual, detalle.hora_entrada)
                            diferencia          = datetime_salida - datetime_entrada
                            detalle.horas_trabajadas = round(diferencia.total_seconds() / 3600, 2)

                        # Actualizar detalle
                        cursor.execute(f'''
                            UPDATE {TBDETALLEASISTENCIA}
                            SET
                                {TBDETALLEASISTENCIA_HORA_ENTRADA} = %s,
                                {TBDETALLEASISTENCIA_HORA_SALIDA} = %s,
                                {TBDETALLEASISTENCIA_HORAS_TRABAJADAS} = %s
                            WHERE {TBDETALLEASISTENCIA_ID} = %s;
                        ''', (
                            detalle.hora_entrada,
                            detalle.hora_salida,
                            detalle.horas_trabajadas,
                            detalle.id_detalle
                        ))

                conexion.commit()
                return {'success': True, 'message': 'Asistencia registrada correctamente.'}

        except Exception as e:
            conexion.rollback()
            logger.error(f'Error al registrar asistencia: {e}')
            return {'success': False, 'message': 'Ocurrió un error al registrar la asistencia.'}
        finally:
            if conexion: conexion.close()

    # def registrar_asistencia(self, lista):
    #     conexion, resultado = conection()
    #     if not resultado['success']:
    #         return resultado

    #     try:
    #         with conexion.cursor(dictionary=True) as cursor:
    #             for item in lista:
    #                 # item[0] = Asistencia, item[1] = Hora
    #                 asistencia  = item[0]
    #                 hora        = item[1]
    #                 # Verificar si ya existe un registro de asistencia para ese día y empleado
    #                 cursor.execute(f'''
    #                     SELECT * FROM {TBASISTENCIA}
    #                     WHERE {TBASISTENCIA_FECHA} = %s
    #                     AND {TBASISTENCIA_ID_EMPLEADO} = %s;
    #                 ''', (asistencia.fecha, asistencia.id_empleado))

    #                 existe = cursor.fetchone()

    #                 if existe:
    #                     asistencia.id = existe[TBASISTENCIA_ID]
    #                     # Buscar detalle de asistencia
    #                     cursor.execute(f'''
    #                         SELECT * FROM {TBDETALLEASISTENCIA}
    #                         WHERE {TBDETALLEASISTENCIA_ID_ASISTENCIA} = %s;
    #                     ''', (asistencia.id,))
                        
    #                     data = cursor.fetchone()
    #                     if data:
    #                         detalle = DetalleAsistencia(
    #                             id_detalle      =data[TBDETALLEASISTENCIA_ID],
    #                             id_asistencia   =data[TBDETALLEASISTENCIA_ID_ASISTENCIA],
    #                             hora_entrada    =data[TBDETALLEASISTENCIA_HORA_ENTRADA],
    #                             hora_salida     =data[TBDETALLEASISTENCIA_HORA_SALIDA],
    #                             horas_trabajadas=data[TBDETALLEASISTENCIA_HORAS_TRABAJADAS]
    #                         )
    #                         detalle.hora_entrada = (datetime.min + detalle.hora_entrada).time()
                            
                            
    #                         # Actualiza hora entrada o salida
    #                         if detalle.hora_entrada is None:
    #                             detalle.hora_entrada = hora  
    #                         elif detalle.hora_entrada == hora or hora < detalle.hora_entrada: 
    #                             continue 
    #                         else:
    #                             detalle.hora_salida = hora  
    #                             fecha_actual        = datetime.now().date()
    #                             datetime_salida     = datetime.combine(fecha_actual, detalle.hora_salida)
    #                             datetime_entrada    = datetime.combine(fecha_actual, detalle.hora_entrada)
                                
    #                             diferencia = datetime_salida - datetime_entrada

    #                             # Calcular las horas trabajadas en decimal
    #                             detalle.horas_trabajadas = round(diferencia.total_seconds() / 3600, 2)
                                
    #                         # Actualizar detalle
    #                         cursor.execute(f'''
    #                             UPDATE {TBDETALLEASISTENCIA}
    #                             SET
    #                                 {TBDETALLEASISTENCIA_HORA_ENTRADA} = %s,
    #                                 {TBDETALLEASISTENCIA_HORA_SALIDA} = %s,
    #                                 {TBDETALLEASISTENCIA_HORAS_TRABAJADAS} = %s
    #                             WHERE {TBDETALLEASISTENCIA_ID} = %s;
    #                         ''', (
    #                             detalle.hora_entrada,
    #                             detalle.hora_salida,
    #                             detalle.horas_trabajadas,
    #                             detalle.id_detalle
    #                         ))

    #                 else:
    #                     # Insertar nuevo registro en asistencia
    #                     cursor.execute(f'''
    #                         INSERT INTO {TBASISTENCIA} (
    #                             {TBASISTENCIA_ID_EMPLEADO},
    #                             {TBASISTENCIA_FECHA},
    #                             {TBASISTENCIA_ESTADO_ASISTENCIA}
    #                         ) VALUES (%s, %s, %s);
    #                     ''', (
    #                         asistencia.id_empleado,
    #                         asistencia.fecha,
    #                         asistencia.estado_asistencia
    #                     ))

    #                     id_asistencia = cursor.lastrowid
    #                     # Insertar nuevo detalle de asistencia con hora de entrada
    #                     cursor.execute(f'''
    #                         INSERT INTO {TBDETALLEASISTENCIA} (
    #                             {TBDETALLEASISTENCIA_ID_ASISTENCIA},
    #                             {TBDETALLEASISTENCIA_HORA_ENTRADA}
    #                         ) VALUES (%s, %s);
    #                     ''', (id_asistencia, hora))
    #             conexion.commit()
    #             return {'success': True, 'message': 'Asistencia registrada correctamente.'}
    #     except Exception as e:
    #         conexion.rollback()
    #         logger.error(f'Error al registrar asistencia: {e}')
    #         return {'success': False, 'message': 'Ocurrió un error al registrar la asistencia.'}
    #     finally:
    #         if conexion: conexion.close()
