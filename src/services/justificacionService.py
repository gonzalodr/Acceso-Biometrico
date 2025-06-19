import re
from datetime import date
from models.justificacion import Justificacion
from data.justificacionData import JustificacionData


class JustificacionServices:
    def __init__(self):
        self.justificacionData = JustificacionData()
    
    ##
    # Métodos privados de validación
    ##

    def validate_string(self, value, max_length, pattern=r"^[A-Za-z\s]+$"):
        if not isinstance(value, str) or len(value) > max_length or not re.match(pattern, value):
            return False
        return True

    def _validarMotivo(self, motivo):
        if not motivo or not isinstance(motivo, str):
            return {"success": False, "message": "El motivo no puede estar vacío."}
        
        motivo = motivo.strip()  # Elimina espacios al inicio y al final

        if not motivo:  # Si después de strip queda vacío
            return {"success": False, "message": "El motivo no puede estar vacío."}

        patron = r"^[A-Za-z\s]{1,100}$"
        if re.match(patron, motivo):
            return {"success": True, "message": "Motivo válido."}
        if len(motivo) > 100:
            return {"success": False, "message": "El motivo no puede exceder los 100 caracteres."}
        return {"success": False, "message": "El motivo contiene caracteres inválidos."}

    def _validarDescripcion(self, descripcion):
        if not descripcion or not isinstance(descripcion, str):
            return {"success": False, "message": "La descripción no puede estar vacía."}
        
        if len(descripcion) > 255:
            return {"success": False, "message": "La descripción no puede exceder los 255 caracteres."}
        return {"success": True, "message": "Descripción válida."}

        
    from datetime import date

    def _validarFecha(self, fecha):
        if not isinstance(fecha, date):
            return {"success": False, "message": "La fecha debe ser un valor válido de tipo 'date'."}
        return {"success": True, "message": "Fecha válida."}


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
        
        result = self._validarFecha(justificacion.fecha)
        if not result["success"]:
            return result

        # Inserción en la capa de datos
        return self.justificacionData.create_justificacion(justificacion)

    def modificarJustificacion(self, justificacion: Justificacion, old_asistencia_id):
        # Validar datos antes de actualizar en la capa de datos
        result = self._validarMotivo(justificacion.motivo)
        if not result["success"]:
            return result

        result = self._validarDescripcion(justificacion.descripcion)
        if not result["success"]:
            return result
        
        result = self._validarFecha(justificacion.fecha)
        if not result["success"]:
            return result

        # Actualización en la capa de datos
        return self.justificacionData.update_justificacion(justificacion, old_asistencia_id)

    def eliminarJustificacion(self, id_justificacion):
        return self.justificacionData.delete_justificacion(id_justificacion)

    def obtenerListaJustificacion(self, pagina=1, tam_pagina=10, ordenar_por="id_justificacion", tipo_orden="ASC", busqueda=None):
        return self.justificacionData.list_justificaciones(pagina, tam_pagina, ordenar_por, tipo_orden, busqueda)

    def obtenerJustificacionPorId(self, id_justificacion):
        return self.justificacionData.get_justificacion_by_id(id_justificacion)
