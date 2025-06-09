import re
from mysql.connector import Error
from models.justificacion import Justificacion
from data.data import conection
from settings.config import *
from settings.logger import logger

class JustificacionData:
    ALLOWED_TYPES = ["Permiso", "Falta justificada", "Vacaciones"]

    def validate_string(self, value, max_length, pattern=r"^[A-Za-z\s]+$"):
        if not isinstance(value, str) or len(value) > max_length or not re.match(pattern, value):
            return False
        return True

    def create_justificacion(self, justificacion: Justificacion):
        # Validaciones adicionales
        if not isinstance(justificacion.id_empleado, int) or not isinstance(justificacion.id_asistencia, int):
            return {'success': False, 'message': 'IDs deben ser enteros.'}
        if not self.validate_string(justificacion.motivo, 100):
            return {'success': False, 'message': 'Motivo inválido.'}
        if not self.validate_string(justificacion.descripcion, 255):
            return {'success': False, 'message': 'Descripción inválida.'}
        if justificacion.tipo not in self.ALLOWED_TYPES:
            return {'success': False, 'message': 'Tipo de justificación no permitido.'}

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
                    VALUES (%s, %s, %s, %s, %s)"""  # nosec B608
                cursor.execute(query, (
                    justificacion.id_empleado,
                    justificacion.id_asistencia,
                    justificacion.motivo,
                    justificacion.descripcion,
                    justificacion.tipo
                ))

                query_update = f"""
                    UPDATE {TBASISTENCIA}
                    SET {TBASISTENCIA_ESTADO_ASISTENCIA} = %s
                    WHERE {TBASISTENCIA_ID} = %s
                """  # nosec B608
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
        # Validaciones adicionales
        if not isinstance(justificacion.id_empleado, int) or not isinstance(justificacion.id_asistencia, int):
            return {'success': False, 'message': 'IDs deben ser enteros.'}
        if not self.validate_string(justificacion.motivo, 100):
            return {'success': False, 'message': 'Motivo inválido.'}
        if not self.validate_string(justificacion.descripcion, 255):
            return {'success': False, 'message': 'Descripción inválida.'}
        if justificacion.tipo not in self.ALLOWED_TYPES:
            return {'success': False, 'message': 'Tipo de justificación no permitido.'}

        conexion, resultado = conection()
        if not resultado["success"]:
            return resultado

        try:
            cursor = conexion.cursor()
            if old_id_asistencia:
                query_old_asistencia = f"""
                    UPDATE {TBASISTENCIA}
                    SET {TBASISTENCIA_ESTADO_ASISTENCIA} = 'Ausente'
                    WHERE {TBASISTENCIA_ID} = %s
                """  # nosec B608
                cursor.execute(query_old_asistencia, (old_id_asistencia,))

            if justificacion.id_asistencia:
                query_new_asistencia = f"""
                    UPDATE {TBASISTENCIA}
                    SET {TBASISTENCIA_ESTADO_ASISTENCIA} = 'Justificado'
                    WHERE {TBASISTENCIA_ID} = %s
                """  # nosec B608
                cursor.execute(query_new_asistencia, (justificacion.id_asistencia,))

            query = f"""UPDATE {TBJUSTIFICACION} SET
                {TBJUSTIFICACION_ID_EMPLEADO} = %s,
                {TBJUSTIFICACION_ID_ASISTENCIA} = %s,
                {TBJUSTIFICACION_MOTIVO} = %s,
                {TBJUSTIFICACION_DESCRIPCION} = %s,
                {TBJUSTIFICACION_TIPO} = %s
                WHERE {TBJUSTIFICACION_ID} = %s"""  # nosec B608
            cursor.execute(query, (
                justificacion.id_empleado,
                justificacion.id_asistencia,
                justificacion.motivo,
                justificacion.descripcion,
                justificacion.tipo,
                justificacion.id_justificacion
            ))

            conexion.commit()
            return {'success': True, 'message': 'Justificación actualizada exitosamente.'}
        except Error as e:
            logger.error(f'Error: {e}')
            return {'success': False, 'message': 'Ocurrió un error al actualizar la justificación.'}
        finally:
            if conexion:
                conexion.close()

    def delete_justificacion(self, justificacion_id):
        if not isinstance(justificacion_id, int):
            return {'success': False, 'message': 'ID de justificación debe ser un entero.'}

        conexion, resultado = conection()
        if not resultado["success"]:
            return resultado
        
        try:
            with conexion.cursor() as cursor:
                query = f"DELETE FROM {TBJUSTIFICACION} WHERE {TBJUSTIFICACION_ID} = %s"  # nosec B608
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
        # Validar parámetros
        if not isinstance(pagina, int) or not isinstance(tam_pagina, int):
            return {'success': False, 'message': 'Parámetros de paginación deben ser enteros.'}
        if busqueda and (not isinstance(busqueda, str) or len(busqueda) > 100):
            return {'success': False, 'message': 'Término de búsqueda inválido o demasiado largo.'}
        tam_pagina = min(tam_pagina, 100)  # Limitar tamaño de página

        conexion, resultado = conection()
        if not resultado["success"]:
            return resultado

        listaJustificaciones = []
        try:
            with conexion.cursor(dictionary=True) as cursor:
                columna_orden = {
                    "motivo": TBJUSTIFICACION_MOTIVO,
                    "descripcion": TBJUSTIFICACION_DESCRIPCION,
                    "id_empleado": TBJUSTIFICACION_ID_EMPLEADO,
                    "id_asistencia": TBJUSTIFICACION_ID_ASISTENCIA,
                    "nombre_empleado": TBPERSONA_NOMBRE,
                    "apellido_empleado": TBPERSONA_APELLIDOS,
                    "fecha": TBJUSTIFICACION_FECHA,
                    "tipo": TBJUSTIFICACION_TIPO
                }
                ordenar_por = columna_orden.get(ordenar_por, TBJUSTIFICACION_FECHA)
                tipo_orden = "DESC" if tipo_orden != "ASC" else "ASC"

                query = f"""
                    SELECT J.*, P.{TBPERSONA_NOMBRE} AS nombre_empleado, P.{TBPERSONA_APELLIDOS} AS apellido_empleado,
                        A.{TBASISTENCIA_FECHA} AS fecha_asistencia
                    FROM {TBJUSTIFICACION} J
                    INNER JOIN EMPLEADO E ON J.{TBJUSTIFICACION_ID_EMPLEADO} = E.ID
                    INNER JOIN {TBPERSONA} P ON E.ID_PERSONA = P.{TBPERSONA_ID}
                    LEFT JOIN {TBASISTENCIA} A ON J.{TBJUSTIFICACION_ID_ASISTENCIA} = A.{TBASISTENCIA_ID}
                """  # nosec B608

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

                query += f" ORDER BY {ordenar_por} {tipo_orden} LIMIT %s OFFSET %s"
                valores.extend([tam_pagina, (pagina - 1) * tam_pagina])

                cursor.execute(query, valores)
                registros = cursor.fetchall()
                for registro in registros:
                    justificacion = {
                        "id_justificacion": registro[TBJUSTIFICACION_ID],
                        "motivo": registro[TBJUSTIFICACION_MOTIVO],
                        "descripcion": registro[TBJUSTIFICACION_DESCRIPCION],
                        "tipo": registro[TBJUSTIFICACION_TIPO],
                        "id_empleado": registro[TBJUSTIFICACION_ID_EMPLEADO],
                        "id_asistencia": registro[TBJUSTIFICACION_ID_ASISTENCIA],
                        "nombre_completo_empleado": f"{registro['nombre_empleado']} {registro['apellido_empleado']}",
                        "fecha_realizado": registro[TBJUSTIFICACION_FECHA],
                        "fecha_asistencia": registro["fecha_asistencia"]
                    }
                    listaJustificaciones.append(justificacion)

                cursor.execute(f"SELECT COUNT(*) as total FROM {TBJUSTIFICACION}")  # nosec B608
                total_registros = cursor.fetchone()["total"]
                total_paginas = (total_registros + tam_pagina - 1) // tam_pagina

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
            logger.error(f'Error al cargar la lista de justificaciones: {e}')
            return {'success': False, 'message': f'Ocurrió un error al cargar la lista de justificaciones: {str(e)}'}
        except Exception as e:
            logger.error(f'Error inesperado: {e}')
            return {'success': False, 'message': f'Ocurrió un error inesperado: {str(e)}'}
        finally:
            if conexion:
                conexion.close()

    def get_justificacion_by_id(self, justificacion_id):
        if not isinstance(justificacion_id, int):
            return {'success': False, 'message': 'ID de justificación debe ser un entero.'}

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
                    P.{TBPERSONA_APELLIDOS} AS apellido_empleado,
                    A.{TBASISTENCIA_FECHA} AS fecha_asistencia
                    FROM {TBJUSTIFICACION} J
                    LEFT JOIN EMPLEADO E ON J.{TBJUSTIFICACION_ID_EMPLEADO} = E.ID
                    LEFT JOIN {TBPERSONA} P ON E.ID_PERSONA = P.{TBPERSONA_ID}
                    LEFT JOIN {TBASISTENCIA} A ON J.{TBJUSTIFICACION_ID_ASISTENCIA} = A.{TBASISTENCIA_ID}
                    WHERE J.{TBJUSTIFICACION_ID} = %s"""  # nosec B608
                
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
                    nombre_completo_empleado = f"{data[7]} {data[8]}"  # Corregir índices
                    return {
                        'success': True,
                        'exists': True,
                        'justificacion': justificacion,
                        'nombre_completo_empleado': nombre_completo_empleado,
                        'fecha_asistencia': data[9],
                        'fecha_realizado': data[2]
                    }
                else:
                    return {'success': True, 'exists': False, 'message': 'No se encontró la justificación.'}
        except Error as e:
            logger.error(f'Error: {e}')
            return {'success': False, 'message': 'Ocurrió un error al obtener la justificación.'}
        finally:
            if conexion:
                conexion.close()