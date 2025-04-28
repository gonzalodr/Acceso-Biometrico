from models.solicitud_permisos import SolicitudPermiso
from data.SolicitudPermisoData import SolicitudPermisoData
from settings.logger import logger
from datetime import date


class SolicitudPermisoService:
    def __init__(self):
        self.solicitudPermisoData = SolicitudPermisoData()

    def crear_permiso(self, solicitud: SolicitudPermiso):
        """
        Crea una nueva solicitud de permiso con validaciones previas

        Args:
            solicitud (SolicitudPermiso): Objeto con los datos de la solicitud
        """
        # Validaciones
        if not solicitud.id_empleado or solicitud.id_empleado <= 0:
            return {"success": False, "message": "ID de empleado inválido"}

        if not solicitud.tipo or len(solicitud.tipo.strip()) == 0:
            return {"success": False, "message": "El tipo de permiso es requerido"}

        if not isinstance(solicitud.fecha_inicio, date) or not isinstance(
            solicitud.fecha_fin, date
        ):
            return {"success": False, "message": "Fechas inválidas"}

        if solicitud.fecha_inicio > solicitud.fecha_fin:
            return {
                "success": False,
                "message": "La fecha de inicio no puede ser posterior a la fecha fin",
            }

        if not solicitud.descripcion or len(solicitud.descripcion.strip()) < 10:
            return {
                "success": False,
                "message": "La descripción debe tener al menos 10 caracteres",
            }

        # Validar estado (podría ser un enum en realidad)
        estados_validos = ["Pendiente", "Aprobado", "Rechazado"]
        if solicitud.estado not in estados_validos:
            return {
                "success": False,
                "message": f'Estado inválido. Debe ser uno de: {", ".join(estados_validos)}',
            }

        try:
            # procedemos a crear
            resultado = self.solicitudPermisoData.crear_solicitud(solicitud)

            return resultado

        except Exception as e:
            logger.error(f"Error en SolicitudPermisoService: {str(e)}")
            return {
                "success": False,
                "message": "Error interno al procesar la solicitud",
                "error_details": str(e),
            }

    def eliminar_permiso(self, id_solicitud: int) -> dict:
        """
        Elimina una solicitud de permiso con validaciones previas

        Args:
            id_solicitud (int): ID de la solicitud a eliminar

        Returns:
            dict: Resultado de la operación en un diccionario
        """
        # Validación de ID valido
        if not id_solicitud or id_solicitud <= 0:
            return {"success": False, "message": "ID de solicitud inválido"}

        try:
            return self.solicitudPermisoData.eliminar_solicitud(id_solicitud)

        except Exception as e:
            logger.error(f"Error en servicio al eliminar permiso: {str(e)}")
            return {
                "success": False,
                "message": "Error interno al procesar la eliminación",
                "error_details": str(e),
            }
