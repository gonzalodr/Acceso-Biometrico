from models.horario import Horario
from data.horarioData import HorarioData
from datetime import datetime


class HorarioService:

    def __init__(self):
        self.horarioData = HorarioData()

    def _validarHoras(self, hora_inicio, hora_fin):
        """
        Valida que la hora de inicio sea menor que la hora de fin.
        """
        if hora_inicio >= hora_fin:
            return {
                "success": False,
                "message": "La hora de inicio debe ser menor que la hora de fin.",
            }
        return {"success": True}

    def insertarHorario(self, horario: Horario, id_rol: int):
        """
        Inserta un nuevo horario después de validar los datos.
        """
        # Validar las horas de inicio y fin
        result = self._validarHoras(horario.hora_inicio, horario.hora_fin)
        if not result["success"]:
            return result

        # Insertar el horario usando la capa de datos
        return self.horarioData.create_horario(horario, id_rol)

    def _existe_horario_duplicado(self, horario: Horario):
        """
        Verifica si ya existe un horario con el mismo nombre, rango de días y tipo de jornada,
        excluyendo el ID actual en caso de actualización.
        """
        horario_existente = self.horarioData.obtenerHorarioPorDiasYTipo(
            horario.nombre_horario, horario.dias_semanales, horario.tipo_jornada
        )
        # Si existe un horario duplicado y no es el mismo que se está actualizando
        if horario_existente and horario_existente.id != horario.id:
            return True
        return False

    def modificarHorario(self, horario: Horario, id_rol: int):
        """
        Modifica un horario existente después de validar los datos.
        """
        # Validar las horas de inicio y fin
        result = self._validarHoras(horario.hora_inicio, horario.hora_fin)
        if not result["success"]:
            return result

        # Obtener el horario actual de la base de datos
        result_actual = self.horarioData.get_horario_by_id(horario.id)
        if not result_actual["success"]:
            return result_actual

        horario_actual = result_actual["data"]

        if (
            horario.nombre_horario != horario_actual["nombre_horario"]
            or horario.dias_semanales != horario_actual["dias_semanales"]
            or horario.tipo_jornada != horario_actual["tipo_jornada"]
        ):

            # Validar duplicado ignorando el registro actual
            is_unique, message = self.horarioData.validar_unicidad_jornada(
                nombre_horario=horario.nombre_horario,
                dias_semanales=horario.dias_semanales,
                tipo_jornada=horario.tipo_jornada,
                id=horario.id,  # Pasar el ID actual para ignorarlo en la validación
            )

            if not is_unique:
                return {"success": False, "message": message}

        # Modificar el horario usando la capa de datos
        return self.horarioData.update_horario(horario, id_rol)

    def eliminarHorario(self, id):
        """
        Elimina un horario por su ID.
        """
        return self.horarioData.delete_horario(id)

    def obtenerListaHorarios(
        self,
        pagina=1,
        tam_pagina=10,
        ordenar_por="id",
        tipo_orden="DESC",
        busqueda=None,
    ):
        """
        Obtiene una lista de horarios con paginación y búsqueda opcional.
        """
        return self.horarioData.list_horarios(
            pagina, tam_pagina, ordenar_por, tipo_orden, busqueda
        )

    def obtenerHorarioPorId(self, id):
        """
        Obtiene un horario específico por su ID.
        """
        return self.horarioData.get_horario_by_id(id)
