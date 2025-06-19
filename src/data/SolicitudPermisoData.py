from models.solicitud_permisos import SolicitudPermiso
from data.data import conection
from mysql.connector import Error
from settings.config import *
from settings.logger import logger


class SolicitudPermisoData:

    def crear_solicitud(self, solicitud: SolicitudPermiso):
        """
        Crea una nueva solicitud de permiso en la base de datos

        Args:
            solicitud (SolicitudPermiso): Objeto con los datos de la solicitud

        Returns:
            dict: Diccionario con el resultado de la operación
        """
        conexion, resultado = conection()
        if not resultado["success"]:
            return resultado

        try:
            with conexion.cursor() as cursor:

                conexion.start_transaction()

                query = f"""
                    INSERT INTO {TBSOLICITUD_PERMISO} 
                    ({TBSOLICITUD_PERMISO_ID_EMPLEADO}, {TBSOLICITUD_PERMISO_TIPO}, 
                     {TBSOLICITUD_PERMISO_FECHA_INICIO}, {TBSOLICITUD_PERMISO_FECHA_FIN}, 
                     {TBSOLICITUD_PERMISO_DESCRIPCION}, {TBSOLICITUD_PERMISO_ESTADO}) 
                    VALUES (%s, %s, %s, %s, %s, %s)
                """
                valores = (
                    solicitud.id_empleado,
                    solicitud.tipo,
                    solicitud.fecha_inicio,
                    solicitud.fecha_fin,
                    solicitud.descripcion,
                    solicitud.estado,
                )

                cursor.execute(query, valores)

                # ID generado
                solicitud.id_solicitud_permiso = cursor.lastrowid

                # Commit
                conexion.commit()

                return {
                    "success": True,
                    "message": "Solicitud creada exitosamente",
                    "id_solicitud": cursor.lastrowid,
                }

        except Error as e:
            # Rollback
            if conexion.in_transaction:
                conexion.rollback()

            logger.error(f"Error al crear solicitud: {e}")
            return {
                "success": False,
                "message": "Error al crear la solicitud en la base de datos",
                "error_details": str(e),
            }
        finally:

            # cierre de conexion
            conexion.close()

    def eliminar_solicitud(self, id_solicitud: int) -> dict:
        """
        Elimina una solicitud de permiso de la base de datos

        Args:
            id_solicitud (int): ID de la solicitud a eliminar

        Returns:
            dict: Resultado de la operación con la estructura:
                {
                    'success': bool,
                    'message': str,
                    'error_details': str (opcional)
                }
        """
        conexion, resultado = conection()
        if not resultado["success"]:
            return resultado

        try:
            with conexion.cursor() as cursor:
                # Iniciamos transacción
                conexion.start_transaction()

                query = f"""
                    DELETE FROM {TBSOLICITUD_PERMISO} 
                    WHERE {TBSOLICITUD_PERMISO_ID} = %s
                """
                cursor.execute(query, (id_solicitud,))

                # Verificamos si se afectó alguna fila
                if cursor.rowcount == 0:
                    conexion.rollback()
                    return {
                        "success": False,
                        "message": "No se encontró la solicitud con el ID proporcionado",
                    }

                conexion.commit()

                return {"success": True, "message": "Solicitud eliminada correctamente"}

        except Error as e:
            if conexion.in_transaction:
                conexion.rollback()

            logger.error(f"Error al eliminar solicitud {id_solicitud}: {str(e)}")
            return {
                "success": False,
                "message": "Error al eliminar la solicitud",
                "error_details": str(e),
            }

        finally:
            if conexion and conexion.is_connected():
                conexion.close()

    def list_solicitudes_permisos(
        self,
        pagina=1,
        tam_pagina=10,
        ordenar_por=TBSOLICITUD_PERMISO_ID,
        tipo_orden="DESC",
        busqueda=None,
    ):
        conexion, resultado = conection()
        if not resultado["success"]:
            return resultado

        try:
            with conexion.cursor(dictionary=True) as cursor:

                # Validación de columnas por las que se puede ordenar
                columnas_validas = {
                    "id": TBSOLICITUD_PERMISO_ID,
                    "empleado": TBPERSONA_NOMBRE,  # Nombre de la persona
                    "tipo": TBSOLICITUD_PERMISO_TIPO,
                    "fecha_inicio": TBSOLICITUD_PERMISO_FECHA_INICIO,
                    "fecha_fin": TBSOLICITUD_PERMISO_FECHA_FIN,
                    "estado": TBSOLICITUD_PERMISO_ESTADO,
                }
                ordenar_por = columnas_validas.get(ordenar_por, TBSOLICITUD_PERMISO_ID)

                if tipo_orden not in ["ASC", "DESC"]:
                    tipo_orden = "DESC"

                # Consulta base con JOIN para traer nombre del empleado
                query = f"""
                SELECT 
                    sp.{TBSOLICITUD_PERMISO_ID},
                    sp.{TBSOLICITUD_PERMISO_TIPO},
                    sp.{TBSOLICITUD_PERMISO_FECHA_INICIO},
                    sp.{TBSOLICITUD_PERMISO_FECHA_FIN},
                    sp.{TBSOLICITUD_PERMISO_DESCRIPCION},
                    sp.{TBSOLICITUD_PERMISO_ESTADO},
                    p.{TBPERSONA_NOMBRE} AS nombre_empleado,
                    p.{TBPERSONA_APELLIDOS} AS apellidos_empleado
                FROM {TBSOLICITUD_PERMISO} sp
                LEFT JOIN {TBEMPLEADO} e ON sp.{TBSOLICITUD_PERMISO_ID_EMPLEADO} = e.{TBEMPLEADO_ID}
                LEFT JOIN {TBPERSONA} p ON e.{TBEMPLEADO_PERSONA} = p.{TBPERSONA_ID}
                """

                valores = []
                if busqueda:
                    query += f"""
                    WHERE p.{TBPERSONA_NOMBRE} LIKE %s
                    OR p.{TBPERSONA_APELLIDOS} LIKE %s
                    OR sp.{TBSOLICITUD_PERMISO_TIPO} LIKE %s
                    OR sp.{TBSOLICITUD_PERMISO_ESTADO} LIKE %s
                    """
                    valores = [f"%{busqueda}%"] * 4

                query += f" ORDER BY {ordenar_por} {tipo_orden} LIMIT %s OFFSET %s"
                valores.extend([tam_pagina, (pagina - 1) * tam_pagina])

                cursor.execute(query, valores)

                registros = cursor.fetchall()
                lista_solicitudes = []
                for registro in registros:
                    solicitud = {
                        "id": registro[TBSOLICITUD_PERMISO_ID],
                        "tipo": registro[TBSOLICITUD_PERMISO_TIPO],
                        "fecha_inicio": registro[TBSOLICITUD_PERMISO_FECHA_INICIO],
                        "fecha_fin": registro[TBSOLICITUD_PERMISO_FECHA_FIN],
                        "descripcion": registro[TBSOLICITUD_PERMISO_DESCRIPCION],
                        "estado": registro[TBSOLICITUD_PERMISO_ESTADO],
                        "nombre_empleado": f"{registro['nombre_empleado']} {registro['apellidos_empleado']}",
                    }
                    lista_solicitudes.append(solicitud)

                # Obtener el total de registros
                cursor.execute(f"SELECT COUNT(*) as total FROM {TBSOLICITUD_PERMISO}")
                total_registros = cursor.fetchone()["total"]
                total_paginas = (total_registros + tam_pagina - 1) // tam_pagina

                return {
                    "success": True,
                    "data": {
                        "listaSolicitudes": lista_solicitudes,
                        "pagina_actual": pagina,
                        "tam_pagina": tam_pagina,
                        "total_paginas": total_paginas,
                        "total_registros": total_registros,
                    },
                    "message": "Solicitudes de permisos listadas exitosamente.",
                }

        except Exception as e:
            return {"success": False, "message": f"Error al listar solicitudes: {e}"}
        finally:
            conexion.close()
