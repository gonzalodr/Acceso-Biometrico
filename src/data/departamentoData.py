from mysql.connector import Error
from models.departamento import Departamento
from data.data import conection
from settings.config import *
from settings.logger import logger

class DepartamentoData:

    def create_departamento(self, departamento: Departamento):
        conexion, resultado = conection()
        if not resultado["success"]:
            return resultado

        try:
            with conexion.cursor() as cursor:
                # Primero verificamos si el departamento ya existe
                query = f"""
                    SELECT COUNT(*) 
                      FROM {TBDEPARTAMENTO}
                     WHERE {TBDEPARTAMENTO_NOMBRE} = %s
                """  # nosec B608
                cursor.execute(query, (departamento.nombre,))
                count = cursor.fetchone()[0]

                if count > 0:
                    return {
                        'success': False,
                        'message': 'El departamento ya existe y no puede ser creado nuevamente.'
                    }

                query = f"""
                    INSERT INTO {TBDEPARTAMENTO} (
                        {TBDEPARTAMENTO_NOMBRE},
                        {TBDEPARTAMENTO_DESCRIPCION}
                    ) VALUES (%s, %s)
                """  # nosec B608
                cursor.execute(query, (
                    departamento.nombre,
                    departamento.descripcion
                ))
                conexion.commit()
                return {
                    'success': True,
                    'message': 'El departamento se guardó correctamente.'
                }
        except Error as e:
            logger.error(f'Error al crear departamento: {e}')
            return {
                'success': False,
                'message': 'Ocurrió un error al guardar el departamento.'
            }
        finally:
            conexion.close()

    def update_departamento(self, departamento: Departamento):
        conexion, resultado = conection()
        if not resultado["success"]:
            return resultado

        try:
            with conexion.cursor() as cursor:
                # Verificamos duplicado excluyendo este ID
                query = f"""
                    SELECT COUNT(*) 
                      FROM {TBDEPARTAMENTO}
                     WHERE {TBDEPARTAMENTO_NOMBRE} = %s
                       AND {TBDEPARTAMENTO_ID} != %s
                """  # nosec B608
                cursor.execute(query, (departamento.nombre, departamento.id))
                count = cursor.fetchone()[0]

                if count > 0:
                    return {
                        'success': False,
                        'message': 'El departamento ya existe, intente actualizar con un nombre distinto.'
                    }

                query = f"""
                    UPDATE {TBDEPARTAMENTO}
                       SET {TBDEPARTAMENTO_NOMBRE} = %s,
                           {TBDEPARTAMENTO_DESCRIPCION} = %s
                     WHERE {TBDEPARTAMENTO_ID} = %s
                """  # nosec B608
                cursor.execute(query, (
                    departamento.nombre,
                    departamento.descripcion,
                    departamento.id
                ))
                conexion.commit()
                return {
                    'success': True,
                    'message': 'Departamento actualizado exitosamente.'
                }
        except Error as e:
            logger.error(f'Error al actualizar departamento: {e}')
            return {
                'success': False,
                'message': 'Ocurrió un error al actualizar el departamento.'
            }
        finally:
            conexion.close()

    def delete_departamento(self, departamento_id):
        conexion, resultado = conection()
        if not resultado["success"]:
            return resultado

        try:
            with conexion.cursor() as cursor:
                query = f"""
                    DELETE FROM {TBDEPARTAMENTO}
                     WHERE {TBDEPARTAMENTO_ID} = %s
                """  # nosec B608
                cursor.execute(query, (departamento_id,))
                conexion.commit()
                return {
                    'success': True,
                    'message': 'El departamento se eliminó correctamente.'
                }
        except Error as e:
            logger.error(f'Error al eliminar departamento: {e}')
            return {
                'success': False,
                'message': 'Ocurrió un error al eliminar el departamento.'
            }
        finally:
            conexion.close()

    def list_departamentos(self, pagina=1, tam_pagina=10,
                           ordenar_por=TBDEPARTAMENTO_ID, tipo_orden="ASC", busqueda=None):
        conexion, resultado = conection()
        if not resultado["success"]:
            return resultado

        try:
            with conexion.cursor(dictionary=True) as cursor:
                # Mapear alias de orden
                columna_orden = {
                    "nombre": TBDEPARTAMENTO_NOMBRE,
                    "descripcion": TBDEPARTAMENTO_DESCRIPCION,
                }
                col = columna_orden.get(ordenar_por, TBDEPARTAMENTO_ID)
                orden = "DESC" if tipo_orden.upper() != "ASC" else "ASC"

                query = f"SELECT * FROM {TBDEPARTAMENTO}"  # nosec B608
                params = []

                if busqueda:
                    query += f"""
                        WHERE {TBDEPARTAMENTO_NOMBRE} LIKE %s
                           OR {TBDEPARTAMENTO_DESCRIPCION} LIKE %s
                    """  # nosec B608
                    params += [f"%{busqueda}%", f"%{busqueda}%"]

                query += f" ORDER BY {col} {orden} LIMIT %s OFFSET %s"  # nosec B608
                params += [tam_pagina, (pagina - 1) * tam_pagina]

                cursor.execute(query, params)
                filas = cursor.fetchall()

                lista = [
                    Departamento(
                        fila[TBDEPARTAMENTO_NOMBRE],
                        fila[TBDEPARTAMENTO_DESCRIPCION],
                        fila[TBDEPARTAMENTO_ID]
                    ) for fila in filas
                ]

                # Total de registros
                count_query = f"SELECT COUNT(*) AS total FROM {TBDEPARTAMENTO}"  # nosec B608
                cursor.execute(count_query)
                total = cursor.fetchone()["total"]
                total_paginas = (total + tam_pagina - 1) // tam_pagina

                return {
                    'success': True,
                    'data': {
                        'listaDepartamentos': lista,
                        'pagina_actual': pagina,
                        'tam_pagina': tam_pagina,
                        'total_paginas': total_paginas,
                        'total_registros': total
                    },
                    'message': 'Departamentos listados exitosamente.'
                }
        except Error as e:
            logger.error(f'Error al listar departamentos: {e}')
            return {
                'success': False,
                'message': 'Ocurrió un error al cargar la lista de departamentos.'
            }
        finally:
            conexion.close()

    def get_departamento_by_id(self, departamento_id):
        conexion, resultado = conection()
        if not resultado["success"]:
            return resultado

        try:
            with conexion.cursor() as cursor:
                query = f"""
                    SELECT {TBDEPARTAMENTO_NOMBRE},
                           {TBDEPARTAMENTO_DESCRIPCION},
                           {TBDEPARTAMENTO_ID}
                      FROM {TBDEPARTAMENTO}
                     WHERE {TBDEPARTAMENTO_ID} = %s
                """  # nosec B608
                cursor.execute(query, (departamento_id,))
                fila = cursor.fetchone()

                if fila:
                    return {
                        'success': True,
                        'exists': True,
                        'departamento': Departamento(
                            nombre=fila[0],
                            descripcion=fila[1],
                            id=fila[2]
                        )
                    }
                else:
                    return {
                        'success': True,
                        'exists': False,
                        'message': 'No se encontró el departamento.'
                    }
        except Error as e:
            logger.error(f'Error al obtener departamento: {e}')
            return {
                'success': False,
                'message': 'Ocurrió un error al obtener el departamento.'
            }
        finally:
            conexion.close()

    def obtener_todo_departamentos(self):
        conexion, resultado = conection()
        if not resultado["success"]:
            return resultado

        try:
            with conexion.cursor(dictionary=True) as cursor:
                query = f"SELECT * FROM {TBDEPARTAMENTO}"  # nosec B608
                cursor.execute(query)
                filas = cursor.fetchall()

                lista = [
                    Departamento(
                        f[TBDEPARTAMENTO_NOMBRE],
                        f[TBDEPARTAMENTO_DESCRIPCION],
                        f[TBDEPARTAMENTO_ID]
                    ) for f in filas
                ]
                return {
                    'success': True,
                    'listaDepa': lista,
                    'message': 'Se obtuvieron todos los departamentos registrados.'
                }
        except Error as e:
            logger.error(f'Error al listar todos los departamentos: {e}')
            return {
                'success': False,
                'message': 'Ocurrió un error al listar todos los departamentos.'
            }
        finally:
            conexion.close()
