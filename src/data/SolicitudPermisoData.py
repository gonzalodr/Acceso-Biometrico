from models.solicitud_permisos import SolicitudPermiso
from data.data import conection
from mysql.connector import Error
from settings.config import *
from settings.logger import logger


class SolicitudPermisoData:

    def crear_solicitud(solicitud: SolicitudPermiso):
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
            if conexion and conexion.is_connected():
                # cierre de conexion
                conexion.close()
