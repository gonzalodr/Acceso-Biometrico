from models.horario import Horario
from data.data import conection  # Importa la función para obtener la conexión
from settings.config import *


class HorarioData:

    def __init__(self):
        self.conn, self.resultado = conection()

    def validar_datos_horario(self, horario):

        # Convertir los valores a cadenas en caso de que sean None o de otro tipo
        dias_semanales = (
            str(horario.dias_semanales).strip() if horario.dias_semanales else ""
        )
        tipo_jornada = str(horario.tipo_jornada).strip() if horario.tipo_jornada else ""
        """
        Valida los datos del horario antes de la inserción.
        """
        if not dias_semanales:
            return False, "El campo 'Días Semanales' es requerido."
        if len(dias_semanales) > 50:
            return False, "El campo 'Días Semanales' no debe exceder 50 caracteres."

        if not tipo_jornada:
            return False, "El campo 'Tipo Jornada' es requerido."
        if len(tipo_jornada) > 30:
            return False, "El campo 'Tipo Jornada' no debe exceder 30 caracteres."

        if horario.hora_inicio >= horario.hora_fin:
            return False, "La hora de inicio debe ser menor que la hora de fin."

        if horario.descripcion and len(horario.descripcion) > 100:
            return False, "La descripción no debe exceder los 100 caracteres."

        # Validación de unicidad para Dias_Semanales y Tipo_Jornada
        is_unique, message = self.validar_unicidad_jornada(
            horario.dias_semanales, horario.tipo_jornada
        )
        if not is_unique:
            return False, message

        return True, "Datos válidos."

    def validar_unicidad_jornada(self, dias_semanales, tipo_jornada, id=None):
        """
        Verifica que no exista el mismo Tipo Jornada en el mismo rango de Dias_Semanales,
        ignorando el registro actual si se está actualizando.
        """
        # Verificar la conexión
        if not self.conn:
            self.conn, resultado = conection()
            if not resultado["success"]:
                return False, "No se pudo establecer conexión con la base de datos."

        try:
            with self.conn.cursor() as cursor:
                # Construcción de la consulta base
                consulta = f"""
                SELECT COUNT(*) FROM {TBHORARIO}
                WHERE {TBHORARIO_DIAS_SEMANALES} = %s 
                AND {TBHORARIO_TIPO_JORNADA} = %s
            """
                valores = [dias_semanales, tipo_jornada]

                # Si estamos actualizando (hay un id), añadimos la condición para ignorarlo
                if id is not None:
                    consulta += f" AND {TBHORARIO_ID} != %s"
                    valores.append(id)

                # Ejecutar la consulta con los valores
                cursor.execute(consulta, valores)
                count = cursor.fetchone()[0]

                if count > 0:
                    # Mensaje de error si ya existe un registro duplicado
                    return (
                        False,
                        "Ya existe un registro con el mismo tipo de jornada para el mismo rango de días.",
                    )
                # Todo está bien, no se encontró duplicado
                return True, "El tipo de jornada es único para el rango de días."

        except Exception as e:
            # Manejo de errores si algo falla en la consulta
            return False, f"Error al verificar unicidad: {e}"

    def update_horario(self, horario: Horario):
        """
        Actualiza un horario existente en la base de datos.
        """
        # Validar los datos antes de la actualización
        datos_validos, mensaje = self.validar_datos_horario(horario)
        if not datos_validos:
            return {"success": False, "message": mensaje}

        try:
            with self.conn.cursor() as cursor:
                query = f"""
        UPDATE {TBHORARIO} SET
            {TBHORARIO_DIAS_SEMANALES} = %s,
            {TBHORARIO_TIPO_JORNADA} = %s,
            {TBHORARIO_HORA_INICIO} = %s,
            {TBHORARIO_HORA_FIN} = %s,
            {TBHORARIO_DESCRIPCION} = %s
        WHERE {TBHORARIO_ID} = %s
        """
                # Ejecutar la consulta de actualización
                cursor.execute(
                    query,
                    (
                        horario.dias_semanales,
                        horario.tipo_jornada,
                        horario.hora_inicio,
                        horario.hora_fin,
                        horario.descripcion,
                        horario.id,  # Condición para identificar el registro a actualizar
                    ),
                )
                self.conn.commit()  # Confirmar los cambios en la base de datos

                # Cerrar el cursor
                cursor.close()

                return {"success": True, "message": "Horario actualizado exitosamente."}

        except Exception as e:
            return {"success": False, "message": f"Error al actualizar horario: {e}"}

    def create_horario(self, horario: Horario):
        """
        Inserta un nuevo horario en la base de datos.
        """
        # Validar los datos antes de la inserción
        datos_validos, mensaje = self.validar_datos_horario(horario)
        if not datos_validos:
            return {"success": False, "message": mensaje}

        try:
            cursor = self.conn.cursor()
            query = f"""
            INSERT INTO {TBHORARIO} (
                {TBHORARIO_DIAS_SEMANALES},
                {TBHORARIO_TIPO_JORNADA},
                {TBHORARIO_HORA_INICIO},
                {TBHORARIO_HORA_FIN},
                {TBHORARIO_DESCRIPCION}
            ) VALUES (%s, %s, %s, %s, %s)
            """
            # Ejecutar la consulta de inserción
            cursor.execute(
                query,
                (
                    horario.dias_semanales,
                    horario.tipo_jornada,
                    horario.hora_inicio,
                    horario.hora_fin,
                    horario.descripcion,
                ),
            )
            self.conn.commit()  # Confirmar los cambios en la base de datos

            # Obtener el ID del último registro insertado
            id_horario = cursor.lastrowid

            # Cerrar el cursor
            cursor.close()

            return {
                "success": True,
                "message": "Horario creado exitosamente.",
                "id_horario": id_horario,
            }

        except Exception as e:
            return {"success": False, "message": f"Error al crear horario: {e}"}

    def list_horarios(
        self,
        pagina=1,
        tam_pagina=10,
        ordenar_por=TBHORARIO_ID,
        tipo_orden="ASC",
        busqueda=None,
    ):
        """
        Lista los horarios con paginación, orden y búsqueda opcional.
        """
        try:
            cursor = self.conn.cursor(
                dictionary=True
            )  # Para devolver resultados como diccionarios
            # Validación de la columna por la cual ordenar
            columnas_validas = {
                "id": TBHORARIO_ID,
                "dias": TBHORARIO_DIAS_SEMANALES,
                "tipo": TBHORARIO_TIPO_JORNADA,
                "inicio": TBHORARIO_HORA_INICIO,
                "fin": TBHORARIO_HORA_FIN,
            }
            ordenar_por = columnas_validas.get(ordenar_por, TBHORARIO_ID)

            if tipo_orden not in ["ASC", "DESC"]:
                tipo_orden = "DESC"  # Valor por defecto si no es válido

            # Construcción de la consulta base
            query = f"SELECT * FROM {TBHORARIO}"

            # Añadir cláusula de búsqueda si se proporciona
            valores = []
            if busqueda:
                query += f"""
                WHERE {TBHORARIO_DIAS_SEMANALES} LIKE %s 
                OR {TBHORARIO_TIPO_JORNADA} LIKE %s
            """
                valores = [
                    f"%{busqueda}%"
                ] * 2  # Para usar el valor de búsqueda en ambas columnas

            # Añadir la cláusula ORDER BY y LIMIT/OFFSET
            query += f" ORDER BY {ordenar_por} {tipo_orden} LIMIT %s OFFSET %s"
            valores.extend([tam_pagina, (pagina - 1) * tam_pagina])

            cursor.execute(query, valores)

            # Leyendo los registros de la consulta
            registros = cursor.fetchall()
            lista_horarios = []
            for registro in registros:
                horario = Horario(
                    dias_semanales=registro[TBHORARIO_DIAS_SEMANALES],
                    tipo_jornada=registro[TBHORARIO_TIPO_JORNADA],
                    hora_inicio=registro[TBHORARIO_HORA_INICIO],
                    hora_fin=registro[TBHORARIO_HORA_FIN],
                    descripcion=registro[TBHORARIO_DESCRIPCION],
                    id=registro[TBHORARIO_ID],
                )
                lista_horarios.append(horario)

            # Obtener el total de registros para calcular el número total de páginas
            cursor.execute(f"SELECT COUNT(*) as total FROM {TBHORARIO}")
            total_registros = cursor.fetchone()["total"]
            total_paginas = (
                total_registros + tam_pagina - 1
            ) // tam_pagina  # Redondeo hacia arriba

            cursor.close()

            return {
                "success": True,
                "data": {
                    "listaHorarios": lista_horarios,
                    "pagina_actual": pagina,
                    "tam_pagina": tam_pagina,
                    "total_paginas": total_paginas,
                    "total_registros": total_registros,
                },
                "message": "Horarios listados exitosamente.",
            }

        except Exception as e:
            return {"success": False, "message": f"Error al listar horarios: {e}"}

    def delete_horario(self, horario_id):
        """
        Elimina un horario existente en la base de datos.
        """
        try:
            cursor = self.conn.cursor()
            query = f"DELETE FROM {TBHORARIO} WHERE {TBHORARIO_ID} = %s"

            # Ejecutar la consulta de eliminación
            cursor.execute(query, (horario_id,))
            self.conn.commit()  # Confirmar los cambios en la base de datos

            # Cerrar el cursor
            cursor.close()

            return {"success": True, "message": "Horario eliminado exitosamente."}

        except Exception as e:

            return {"success": False, "message": f"Error al eliminar horario: {e}"}

    def get_horario_by_id(self, horario_id):
        """
        Obtiene un horario específico por su ID.
        """
        try:
            cursor = self.conn.cursor(
                dictionary=True
            )  # Para devolver resultados como diccionario
            query = f"""
        SELECT * FROM {TBHORARIO}
        WHERE {TBHORARIO_ID} = %s
        """
            cursor.execute(query, (horario_id,))
            registro = cursor.fetchone()

            if registro:
                horario = Horario(
                    dias_semanales=registro[TBHORARIO_DIAS_SEMANALES],
                    tipo_jornada=registro[TBHORARIO_TIPO_JORNADA],
                    hora_inicio=registro[TBHORARIO_HORA_INICIO],
                    hora_fin=registro[TBHORARIO_HORA_FIN],
                    descripcion=registro[TBHORARIO_DESCRIPCION],
                    id=registro[TBHORARIO_ID],
                )
                cursor.close()

                return {
                    "success": True,
                    "data": horario,
                    "message": "Horario encontrado exitosamente.",
                }
            else:
                return {
                    "success": False,
                    "message": "No se encontró un horario con el ID proporcionado.",
                }

        except Exception as e:
            return {"success": False, "message": f"Error al obtener el horario: {e}"}

    def obtenerHorarioPorDiasYTipo(self, dias_semanales, tipo_jornada):
        """
        Obtiene un horario específico por los días semanales y el tipo de jornada.
        """
        try:
            cursor = self.conn.cursor(dictionary=True)
            query = f"""
        SELECT * FROM {TBHORARIO} 
        WHERE {TBHORARIO_DIAS_SEMANALES} = %s 
        AND {TBHORARIO_TIPO_JORNADA} = %s
        LIMIT 1
        """
            cursor.execute(query, (dias_semanales, tipo_jornada))
            registro = cursor.fetchone()
            cursor.close()

            if registro:
                return Horario(
                    dias_semanales=registro[TBHORARIO_DIAS_SEMANALES],
                    tipo_jornada=registro[TBHORARIO_TIPO_JORNADA],
                    hora_inicio=registro[TBHORARIO_HORA_INICIO],
                    hora_fin=registro[TBHORARIO_HORA_FIN],
                    descripcion=registro[TBHORARIO_DESCRIPCION],
                    id=registro[TBHORARIO_ID],
                )
            return None  # No se encontró ningún horario con los mismos días y tipo

        except Exception as e:
            print(f"Error al obtener horario por días y tipo: {e}")
            return None
