from data.data import conection  # Asegúrate de que este sea el path correcto
from settings.logger import logger
from models.huella import Huella
from mysql.connector import Error
from settings.config import *

class HuellaData:
    @staticmethod
    def registrar_huella(
        id_empleado: int,
        uid_dispositivo: int,
        user_id_dispositivo: str,
        nombre_guardado: str,
        privilegio: int = 0,
        tiene_huella: bool = True,
    ):
        conexion, resultado = conection()
        if not resultado["success"]:
            return resultado

        try:
            with conexion.cursor() as cursor:
                query = """
                INSERT INTO huella 
                (id_empleado, uid_dispositivo, user_id_dispositivo, nombre_guardado, privilegio, tiene_huella)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            valores = (
                id_empleado,
                uid_dispositivo,
                user_id_dispositivo,
                nombre_guardado,
                privilegio,
                tiene_huella,
            )
            cursor.execute(query, valores)
            conexion.commit()
            return {"success": True, "message": "Huella registrada correctamente."}
        except Exception as e:
            logger.error(f"Error al registrar huella: {e}")
            return {"success": False, "message": "Error al registrar la huella."}
        finally:
            if conexion:
                cursor.close()
                conexion.close()


    def create_huella(self, huella: Huella):
        conexion, resultado = conection()
        if not resultado["success"]:
            return resultado
        
        try:
            with conexion.cursor() as cursor:
                query = f"""INSERT INTO {TBHUELLA}(
                {TBHUELLA_ID_EMPLEADO},
                {TBHUELLA_HUELLA})
                VALUES (%s, %s)"""
                
                cursor.execute(query, (
                    huella.id_empleado,
                    huella.id_huella  # Asegúrate de que este campo contenga la huella en el formato correcto
                ))
                conexion.commit()
                return {'success': True, 'message': 'La huella se guardó correctamente.'}
        except Error as e:
            logger.error(f'Error: {e}')
            return {'success': False, 'message': 'Ocurrió un error al guardar la huella.'}
        finally:
            if conexion:
                conexion.close()

    def listar_huellas(self, pagina=1, tam_pagina=10, ordenar_por="Id", tipo_orden="DESC", busqueda=None):
        """
        Lista las huellas con paginación y opción de búsqueda.
        """
        conexion, resultado = conection()
        if not resultado["success"]:
            return resultado

        lista_huellas = []
        try:
            with conexion.cursor(dictionary=True) as cursor:
                # Validación de la columna de ordenamiento
                columna_orden = {
                    "id": TBHUELLA_ID,
                    "id_empleado": TBHUELLA_ID_EMPLEADO,
                    "huella": TBHUELLA_HUELLA,
                }
                ordenar_por = columna_orden.get(ordenar_por, TBHUELLA_ID)

                # Asigna el tipo de orden ascendente o descendente
                tipo_orden = "DESC" if tipo_orden != "ASC" else "ASC"

                # Construcción de la consulta base
                query = f"""
                    SELECT {TBHUELLA_ID}, {TBHUELLA_ID_EMPLEADO}, {TBHUELLA_HUELLA}
                    FROM {TBHUELLA}
                """

                # Añadir cláusula de búsqueda si se proporciona
                valores = []
                if busqueda:
                    query += f"""
                        WHERE {TBHUELLA_ID_EMPLEADO} LIKE %s
                        OR {TBHUELLA_HUELLA} LIKE %s
                    """
                    valores = [f"%{busqueda}%"] * 2

                # Añadir la cláusula ORDER BY y LIMIT/OFFSET
                pagina = max(1, pagina)
                query += f" ORDER BY {ordenar_por} {tipo_orden} LIMIT %s OFFSET %s"
                valores.extend([tam_pagina, (pagina - 1) * tam_pagina])

                # Ejecutar la consulta con los parámetros
                cursor.execute(query, valores)

                # Leer los registros
                registros = cursor.fetchall()
                for registro in registros:
                    huella = {
                        "id": registro[TBHUELLA_ID],
                        "id_empleado": registro[TBHUELLA_ID_EMPLEADO],
                        "huella": registro[TBHUELLA_HUELLA],
                    }
                    lista_huellas.append(huella)

                # Obtener el total de registros para calcular el número total de páginas
                cursor.execute(f"SELECT COUNT(*) as total FROM {TBHUELLA}")
                total_registros = cursor.fetchone()["total"]
                total_paginas = (total_registros + tam_pagina - 1) // tam_pagina  # Redondear hacia arriba

                resultado["data"] = {
                    "lista_huellas": lista_huellas,
                    "pagina_actual": pagina,
                    "tam_pagina": tam_pagina,
                    "total_paginas": total_paginas,
                    "total_registros": total_registros,
                }
                resultado["success"] = True
                resultado["message"] = "Huellas listadas exitosamente."
                return resultado
        except Error as e:
            logger.error(f'Error al listar huellas: {e}')
            return {'success': False, 'message': f'Ocurrió un error al listar huellas: {str(e)}'}
        finally:
            if conexion:
                conexion.close()

    def get_huella_by_id(self, id_huella):
        """
        Obtiene una huella por su identificador único.
        """
        conexion, resultado = conection()
        if not resultado["success"]:
            return resultado

        try:
            with conexion.cursor(dictionary=True) as cursor:
                query = f"""
                    SELECT {TBHUELLA_ID}, {TBHUELLA_ID_EMPLEADO}, {TBHUELLA_HUELLA}
                    FROM {TBHUELLA}
                    WHERE {TBHUELLA_ID} = %s
                """
                cursor.execute(query, (id_huella,))
                data = cursor.fetchone()

                if data:
                    huella = {
                        "id": data[TBHUELLA_ID],
                        "id_empleado": data[TBHUELLA_ID_EMPLEADO],
                        "huella": data[TBHUELLA_HUELLA],
                    }
                    return {
                        'success': True,
                        'exists': True,
                        'huella': huella,
                    }
                else:
                    return {'success': True, 'exists': False, 'message': 'No se encontró la huella.'}
        except Error as e:
            logger.error(f'Error al obtener la huella: {e}')
            return {'success': False, 'message': f'Ocurrió un error al obtener la huella: {str(e)}'}
        finally:
            if conexion:
                conexion.close()

    def buscar_huella_por_empleado(self, id_empleado: int):

        conexion, resultado = conection()
        if not resultado["success"]:
            return resultado

        try:
            with conexion.cursor(dictionary=True) as cursor:
                query = f"""
                    SELECT {TBHUELLA_ID}, {TBHUELLA_ID_EMPLEADO}, {TBHUELLA_HUELLA}
                    FROM {TBHUELLA}
                    WHERE {TBHUELLA_ID_EMPLEADO} = %s
                    LIMIT 1
                """
                cursor.execute(query, (id_empleado,))
                huella = cursor.fetchone()

                if huella:
                    return {
                        'success': True,
                        'exists': True,
                        'id_huella': huella.get(TBHUELLA_ID),  # ID de la tabla huella
                        'huella': huella.get(TBHUELLA_HUELLA),  # Valor de la huella
                    }
                else:
                    return {
                        'success': True,
                        'exists': False,
                        'message': 'No se encontró una huella para el empleado especificado.'
                    }
        except Error as e:
            logger.error(f'Error al buscar huella por empleado: {e}')
            return {
                'success': False,
                'message': f'Ocurrió un error al buscar huella por empleado: {str(e)}'
            }
        finally:
            if conexion:
                conexion.close()

    def eliminar_huella(id_huella: int):

        conexion, resultado = conection()
        if not resultado["success"]:
            return resultado

        try:
            with conexion.cursor() as cursor:
                query = f"DELETE FROM {TBHUELLA} WHERE {TBHUELLA_ID} = %s"
                cursor.execute(query, (id_huella,))
                conexion.commit()

                if cursor.rowcount > 0:
                    return {"success": True, "message": "Huella eliminada correctamente."}
                else:
                    return {"success": False, "message": "No se encontró una huella con el ID especificado."}
        except Error as e:
            logger.error(f"Error al eliminar huella: {e}")
            return {"success": False, "message": "Error al intentar eliminar la huella."}
        finally:
            if conexion:
                conexion.close()

