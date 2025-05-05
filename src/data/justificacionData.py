from mysql.connector import Error
from models.justificacion import Justificacion
from data.data import conection
from settings.config import *
from settings.logger import logger

class JustificacionData:
    
    def create_justificacion(self, justificacion: Justificacion):
        conexion, resultado = conection()
        if not resultado["success"]:
            return resultado
        
        try:
            with conexion.cursor() as cursor:
                query = f"""INSERT INTO {TBJUSTIFICACION}(
                {TBJUSTIFICACION_ID_EMPLEADO},
                {TBJUSTIFICACION_ID_ASISTENCIA},
                {TBJUSTIFICACION_MOTIVO},
                {TBJUSTIFICACION_DESCRIPCION},
                {TBJUSTIFICACION_TIPO})
                VALUES (%s, %s, %s, %s, %s)"""
                
                cursor.execute(query, (
                    justificacion.id_empleado,
                    justificacion.id_asistencia,
                    justificacion.motivo,
                    justificacion.descripcion,
                    justificacion.tipo
                ))

                # Actualiza el estado de la asistencia correspondiente a "Justificado"
                query_update = f"""
                UPDATE {TBASISTENCIA}
                SET {TBASISTENCIA_ESTADO_ASISTENCIA} = %s
                WHERE {TBASISTENCIA_ID} = %s
                """
                cursor.execute(query_update, (
                    "Justificado",
                    justificacion.id_asistencia
                ))
                conexion.commit()
                return {'success': True, 'message': 'La justificación se guardó correctamente.'}
        except Error as e:
            logger.error(f'Error: {e}')
            return {'success': False, 'message': 'Ocurrió un error al guardar la justificación.'}
        finally:
            if conexion:
                conexion.close()
    
    def update_justificacion(self, justificacion: Justificacion, old_id_asistencia: int):
        print("id asistencia old: " + str(old_id_asistencia))
        print("id asistencia new: " + str(justificacion.id_asistencia))
        conexion, resultado = conection()
        if not resultado["success"]:
            return resultado

        try:
            # Mantener la conexión abierta
            cursor = conexion.cursor()

            # Cambiar el estado de la asistencia anterior a "Ausente"
            if old_id_asistencia:
                query_old_asistencia = f"""
                UPDATE {TBASISTENCIA} 
                SET {TBASISTENCIA_ESTADO_ASISTENCIA} = 'Ausente' 
                WHERE {TBASISTENCIA_ID} = %s
                """
                cursor.execute(query_old_asistencia, (old_id_asistencia,))

            # Cambiar el estado de la nueva asistencia a "Justificado"
            if justificacion.id_asistencia:
                query_new_asistencia = f"""
                UPDATE {TBASISTENCIA} 
                SET {TBASISTENCIA_ESTADO_ASISTENCIA} = 'Justificado' 
                WHERE {TBASISTENCIA_ID} = %s
                """
                cursor.execute(query_new_asistencia, (justificacion.id_asistencia,))

            # Actualizar la justificación
            query = f"""UPDATE {TBJUSTIFICACION} SET 
            {TBJUSTIFICACION_ID_EMPLEADO} = %s,
            {TBJUSTIFICACION_ID_ASISTENCIA} = %s,
            {TBJUSTIFICACION_MOTIVO} = %s,
            {TBJUSTIFICACION_DESCRIPCION} = %s,
            {TBJUSTIFICACION_TIPO} = %s
            WHERE {TBJUSTIFICACION_ID} = %s"""

            cursor.execute(query, (
                justificacion.id_empleado,
                justificacion.id_asistencia,
                justificacion.motivo,
                justificacion.descripcion,
                justificacion.tipo,
                justificacion.id_justificacion
            ))

            # Confirmar los cambios en la base de datos
            conexion.commit()

            return {'success': True, 'message': 'Justificación actualizada exitosamente.'}
        except Error as e:
            logger.error(f'Error: {e}')
            return {'success': False, 'message': 'Ocurrió un error al actualizar la justificación.'}
        finally:
            if conexion:
                conexion.close()

    
    def delete_justificacion(self, justificacion_id):
        conexion, resultado = conection()
        if not resultado["success"]:
            return resultado
        
        try:
            with conexion.cursor() as cursor:
                query = f"DELETE FROM {TBJUSTIFICACION} WHERE {TBJUSTIFICACION_ID} = %s"
                cursor.execute(query, (justificacion_id,))
                conexion.commit()
                return {'success': True, 'message': 'La justificación se eliminó correctamente.'}
        except Error as e:
            logger.error(f'Error: {e}')
            return {'success': False, 'message': 'Ocurrió un error al eliminar la justificación.'}
        finally:
            if conexion:
                conexion.close()

    def list_justificaciones(self, pagina=1, tam_pagina=10, ordenar_por="fecha", tipo_orden="DESC", busqueda=None):
        conexion, resultado = conection()
        cursor = None
        if not resultado["success"]:
            return resultado

        listaJustificaciones = []
        try:
            with conexion.cursor(dictionary=True) as cursor:
                # Validación de la columna de ordenamiento
                columna_orden = {
                    "motivo": TBJUSTIFICACION_MOTIVO,
                    "descripcion": TBJUSTIFICACION_DESCRIPCION,
                    "id_empleado": TBJUSTIFICACION_ID_EMPLEADO,
                    "id_asistencia": TBJUSTIFICACION_ID_ASISTENCIA,
                    "nombre_empleado": TBPERSONA_NOMBRE,  # Para ordenar por nombre del empleado
                    "apellido_empleado": TBPERSONA_APELLIDOS,  # Para ordenar por apellido del empleado
                    "fecha": TBJUSTIFICACION_FECHA,  # Para ordenar por fecha
                    "tipo": TBJUSTIFICACION_TIPO
                }
                ordenar_por = columna_orden.get(ordenar_por, TBJUSTIFICACION_FECHA)

                # Asigna el tipo de orden ascendente o descendente
                tipo_orden = "DESC" if tipo_orden != "ASC" else "ASC"

                # Construcción de la consulta base
                query = f"""
                    SELECT J.*, P.{TBPERSONA_NOMBRE} AS nombre_empleado, P.{TBPERSONA_APELLIDOS} AS apellido_empleado, 
                        A.{TBASISTENCIA_FECHA} AS fecha_asistencia
                    FROM {TBJUSTIFICACION} J
                    INNER JOIN EMPLEADO E ON J.{TBJUSTIFICACION_ID_EMPLEADO} = E.ID
                    INNER JOIN {TBPERSONA} P ON E.ID_PERSONA = P.{TBPERSONA_ID}
                    LEFT JOIN {TBASISTENCIA} A ON J.{TBJUSTIFICACION_ID_ASISTENCIA} = A.{TBASISTENCIA_ID}
                """

                # Añadir cláusula de búsqueda si se proporciona
                valores = []
                if busqueda:
                    query += f"""
                        WHERE J.{TBJUSTIFICACION_MOTIVO} LIKE %s 
                        OR J.{TBJUSTIFICACION_DESCRIPCION} LIKE %s
                        OR J.{TBJUSTIFICACION_ID_EMPLEADO} LIKE %s
                        OR J.{TBJUSTIFICACION_ID_ASISTENCIA} LIKE %s
                        OR P.{TBPERSONA_NOMBRE} LIKE %s
                        OR P.{TBPERSONA_APELLIDOS} LIKE %s
                    """
                    valores = [f"%{busqueda}%"] * 6

                # Añadir la cláusula ORDER BY y LIMIT/OFFSET
                pagina = max(1, pagina)
                query += f" ORDER BY {ordenar_por} {tipo_orden} LIMIT %s OFFSET %s"
                valores.extend([tam_pagina, (pagina - 1) * tam_pagina])

                # Ejecutar la consulta con los parámetros de forma segura
                cursor.execute(query, valores)

                # Leer los registros
                registros = cursor.fetchall()
                for registro in registros:
                    justificacion = {
                        "id_justificacion": registro[TBJUSTIFICACION_ID],  # ID de la justificación
                        "motivo": registro[TBJUSTIFICACION_MOTIVO],
                        "descripcion": registro[TBJUSTIFICACION_DESCRIPCION],
                        "tipo": registro[TBJUSTIFICACION_TIPO],
                        "id_empleado": registro[TBJUSTIFICACION_ID_EMPLEADO],
                        "id_asistencia": registro[TBJUSTIFICACION_ID_ASISTENCIA],
                        "nombre_completo_empleado": f"{registro['nombre_empleado']} {registro['apellido_empleado']}",  # Unir nombre y apellido
                        "fecha_realizado": registro[TBJUSTIFICACION_FECHA],  # Fecha de registro de la justificación
                        "fecha_asistencia": registro["fecha_asistencia"]  # Fecha de asistencia
                    }
                    listaJustificaciones.append(justificacion)

                # Obtener el total de registros para calcular el número total de páginas
                cursor.execute(f"SELECT COUNT(*) as total FROM {TBJUSTIFICACION}")
                total_registros = cursor.fetchone()["total"]
                total_paginas = (total_registros + tam_pagina - 1) // tam_pagina  # Redondear hacia arriba

                resultado["data"] = {
                    "listaJustificaciones": listaJustificaciones,
                    "pagina_actual": pagina,
                    "tam_pagina": tam_pagina,
                    "total_paginas": total_paginas,
                    "total_registros": total_registros
                }
                resultado["success"] = True
                resultado["message"] = "Justificaciones listadas exitosamente."
                return resultado
        except Error as e:
            logger.error(f'Error al cargar la lista de justificaciones: {e}')  # Mensaje de error específico
            return {'success': False, 'message': f'Ocurrió un error al cargar la lista de justificaciones: {str(e)}'}
        except Exception as e:
            logger.error(f'Error inesperado: {e}')  # Captura de errores inesperados
            return {'success': False, 'message': f'Ocurrió un error inesperado: {str(e)}'}
        finally:
            if conexion:
                conexion.close()



    
    def get_justificacion_by_id(self, justificacion_id):
        conexion, resultado = conection()
        if not resultado["success"]:
            return resultado
        
        try:
            with conexion.cursor() as cursor:
                query = f"""SELECT
                                J.{TBJUSTIFICACION_ID_EMPLEADO},
                                J.{TBJUSTIFICACION_ID_ASISTENCIA},
                                J.{TBJUSTIFICACION_FECHA} AS fecha_realizado,
                                J.{TBJUSTIFICACION_MOTIVO},
                                J.{TBJUSTIFICACION_DESCRIPCION},
                                J.{TBJUSTIFICACION_TIPO},
                                J.{TBJUSTIFICACION_ID},
                                P.{TBPERSONA_NOMBRE} AS nombre_empleado,
                                P.{TBPERSONA_APELLIDOS} AS apellido_empleado,  -- Agregar apellido
                                A.{TBASISTENCIA_FECHA} AS fecha_asistencia
                            FROM {TBJUSTIFICACION} J
                            LEFT JOIN EMPLEADO E ON J.{TBJUSTIFICACION_ID_EMPLEADO} = E.ID
                            LEFT JOIN {TBPERSONA} P ON E.ID_PERSONA = P.{TBPERSONA_ID}
                            LEFT JOIN {TBASISTENCIA} A ON J.{TBJUSTIFICACION_ID_ASISTENCIA} = A.{TBASISTENCIA_ID}
                            WHERE J.{TBJUSTIFICACION_ID} = %s"""
                
                cursor.execute(query, (justificacion_id,))
                data = cursor.fetchone()
                
                if data:
                    justificacion = Justificacion(
                        id_empleado=data[0],
                        id_asistencia=data[1],
                        fecha=data[2],  
                        motivo=data[3],
                        descripcion=data[4],
                        tipo=data[5],
                        id_justificacion=data[6]
                    )
                    # Agregar el nombre completo del empleado y la fecha de asistencia al resultado
                    nombre_completo_empleado = f"{data[6]} {data[7]}"  # Unir nombre y apellido
                    return {
                        'success': True,
                        'exists': True,
                        'justificacion': justificacion,
                        'nombre_completo_empleado': nombre_completo_empleado,  # Usar el nombre completo
                        'fecha_asistencia': data[8],  # Esta es la fecha de asistencia
                        'fecha_realizado': data[2]  # Esta es la fecha de realización
                    }
                else:
                    return {'success': True, 'exists': False, 'message': 'No se encontró la justificación.'}
        except Error as e:
            logger.error(f'Error: {e}')
            return {'success': False, 'message': 'Ocurrió un error al obtener la justificación.'}
        finally:
            if conexion:
                conexion.close()