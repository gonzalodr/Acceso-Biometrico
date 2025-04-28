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
