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
                {TBJUSTIFICACION_FECHA},
                {TBJUSTIFICACION_MOTIVO},
                {TBJUSTIFICACION_DESCRIPCION})
                VALUES (%s, %s, %s, %s, %s)"""
                
                cursor.execute(query, (
                    justificacion.id_empleado,
                    justificacion.id_asistencia,
                    justificacion.fecha,
                    justificacion.motivo,
                    justificacion.descripcion
                ))
                conexion.commit()
                return {'success': True, 'message': 'La justificación se guardó correctamente.'}
        except Error as e:
            logger.error(f'Error: {e}')
            return {'success': False, 'message': 'Ocurrió un error al guardar la justificación.'}
        finally:
            if conexion:
                conexion.close()
    
    def update_justificacion(self, justificacion: Justificacion):
        conexion, resultado = conection()
        if not resultado["success"]:
            return resultado
        try:
            with conexion.cursor() as cursor:
                query = f"""UPDATE {TBJUSTIFICACION} SET 
                {TBJUSTIFICACION_ID_EMPLEADO} = %s,
                {TBJUSTIFICACION_ID_ASISTENCIA} = %s,
                {TBJUSTIFICACION_FECHA} = %s,
                {TBJUSTIFICACION_MOTIVO} = %s,
                {TBJUSTIFICACION_DESCRIPCION} = %s
                WHERE {TBJUSTIFICACION_ID} = %s"""
            
                cursor.execute(query, (
                    justificacion.id_empleado,
                    justificacion.id_asistencia,
                    justificacion.fecha,
                    justificacion.motivo,
                    justificacion.descripcion,
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

    def list_justificaciones(self, pagina=1, tam_pagina=10, ordenar_por="ID_JUSTIFICACION", tipo_orden="ASC", busqueda=None):
        conexion, resultado = conection()
        cursor = None
        if not resultado["success"]:
            return resultado

        listaJustificaciones = []
        try:
            with conexion.cursor(dictionary=True) as cursor:
                # Validación de la columna de ordenamiento
                columna_orden = {
                    "motivo": "MOTIVO",
                    "descripcion": "DESCRIPCION",
                    "id_empleado": "ID_EMPLEADO",
                    "id_asistencia": "ID_ASISTENCIA"
                }
                ordenar_por = columna_orden.get(ordenar_por, "ID_JUSTIFICACION")

                # Asigna el tipo de orden ascendente o descendente
                tipo_orden = "DESC" if tipo_orden != "ASC" else "ASC"

                # Construcción de la consulta base
                query = "SELECT * FROM TBJUSTIFICACION"

                # Añadir cláusula de búsqueda si se proporciona
                valores = []
                if busqueda:
                    query += """
                        WHERE MOTIVO LIKE %s 
                        OR DESCRIPCION LIKE %s
                        OR ID_EMPLEADO LIKE %s
                        OR ID_ASISTENCIA LIKE %s
                    """
                    valores = [f"%{busqueda}%", f"%{busqueda}%", f"%{busqueda}%", f"%{busqueda}%"]

            # Añadir la cláusula ORDER BY y LIMIT/OFFSET
            query += f" ORDER BY {ordenar_por} {tipo_orden} LIMIT %s OFFSET %s"
            valores.extend([tam_pagina, (pagina - 1) * tam_pagina])

            # Ejecutar la consulta con los parámetros de forma segura
            cursor.execute(query, valores)

            # Leer los registros
            registros = cursor.fetchall()
            for registro in registros:
                justificacion = {
                    "id_justificacion": registro["ID_JUSTIFICACION"],
                    "motivo": registro["MOTIVO"],
                    "descripcion": registro["DESCRIPCION"],
                    "id_empleado": registro["ID_EMPLEADO"],
                    "id_asistencia": registro["ID_ASISTENCIA"]
                }
                listaJustificaciones.append(justificacion)

            # Obtener el total de registros para calcular el número total de páginas
            cursor.execute("SELECT COUNT(*) as total FROM TBJUSTIFICACION")
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
            logger.error(f'Error: {e}')
            return {'success': False, 'message': 'Ocurrió un error al cargar la lista de justificaciones.'}
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
                                {TBJUSTIFICACION_ID_EMPLEADO},
                                {TBJUSTIFICACION_ID_ASISTENCIA},
                                {TBJUSTIFICACION_FECHA},
                                {TBJUSTIFICACION_MOTIVO},
                                {TBJUSTIFICACION_DESCRIPCION},
                                {TBJUSTIFICACION_ID}
                            FROM {TBJUSTIFICACION} 
                            WHERE {TBJUSTIFICACION_ID} = %s"""
                
                cursor.execute(query, (justificacion_id,))
                data = cursor.fetchone()
                
                if data:
                    justificacion = Justificacion(
                        id_empleado=data[0],
                        id_asistencia=data[1],
                        fecha=data[2],
                        motivo=data[3],
                        descripcion=data[4],
                        id_justificacion=data[5]
                    )
                    return {'success': True, 'exists': True, 'justificacion': justificacion}
                else:
                    return {'success': True, 'exists': False, 'message': 'No se encontró la justificación.'}
        except Error as e:
            logger.error(f'Error: {e}')
            return {'success': False, 'message': 'Ocurrió un error al obtener la justificación.'}
        finally:
            if conexion:
                conexion.close()
