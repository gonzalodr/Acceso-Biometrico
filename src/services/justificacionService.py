import re
from models.justificacion import Justificacion
from data.justificacionData import JustificacionData


class JustificacionServices:
    def __init__(self):
        self.justificacionData = JustificacionData()
    
    ##
    # Métodos privados de validación
    ##

    def _validarMotivo(self, motivo):
        # Validar que el motivo no esté vacío y cumpla con un patrón (solo letras y espacios, hasta 100 caracteres)
        patron = r"^[A-Za-z\s]{1,100}$"
        result = re.match(patron, motivo)
        if result:
            return {"success": True, "message": "Motivo válido."}
        else:
            return {"success": False, "message": "El motivo de la justificación no es válido."}

    def _validarDescripcion(self, descripcion):
        # Validar que la descripción sea adecuada (hasta 255 caracteres)
        if isinstance(descripcion, str) and len(descripcion) <= 255:
            return {"success": True, "message": "Descripción válida."}
        else:
            return {"success": False, "message": "La descripción de la justificación no es válida."}

    ##
    # Funciones públicas
    ##

    def insertarJustificacion(self, justificacion: Justificacion):
        # Validar datos antes de pasar a la capa de datos
        result = self._validarMotivo(justificacion.motivo)
        if not result["success"]:
            return result

        result = self._validarDescripcion(justificacion.descripcion)
        if not result["success"]:
            return result

        # Inserción en la capa de datos
        return self.justificacionData.create_justificacion(justificacion)

    def modificarJustificacion(self, justificacion: Justificacion):
        # Validar datos antes de actualizar en la capa de datos
        result = self._validarMotivo(justificacion.motivo)
        if not result["success"]:
            return result

        result = self._validarDescripcion(justificacion.descripcion)
        if not result["success"]:
            return result

        # Actualización en la capa de datos
        return self.justificacionData.update_justificacion(justificacion)

    def eliminarJustificacion(self, id_justificacion):
        return self.justificacionData.delete_justificacion(id_justificacion)

    def obtenerListaJustificacion(self, pagina=1, tam_pagina=10, ordenar_por="id_justificacion", tipo_orden="ASC", busqueda=None):
        return self.justificacionData.list_justificaciones(pagina, tam_pagina, ordenar_por, tipo_orden, busqueda)

    def obtenerJustificacionPorId(self, id_justificacion):
        return self.justificacionData.get_justificacion_by_id(id_justificacion)
