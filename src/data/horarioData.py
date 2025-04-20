from models.horario import Horario
from data.data import conection  # Importa la función para obtener la conexión
from settings.config import *


class HorarioData:

    def __init__(self):
        self.conn, self.resultado = conection()

    def obtener_conexion(self):

        try:
            # Verifica si la conexión está activa
            if not self.conn or not self.conn.is_connected():
                # Intenta reconectar
                self.conn, resultado = conection()
                if not resultado["success"]:
                    return (
                        None,
                        False,
                        "No se pudo establecer conexión a la Base de Datos.",
                    )

            return self.conn, True, "Conexión establecida correctamente."

        except Exception as e:
            # Maneja cualquier excepción durante la verificación o reconexión
            return None, False, f"Error al verificar la conexión: {e}"

    def validar_id_rol(self, id_rol):

        self.conn, success, message = self.obtener_conexion()
        if not success:
            return False, message

        try:
            with self.conn.cursor() as cursor:
                consulta = f"SELECT COUNT(*) FROM {TBROL} WHERE {TBROL_ID} = %s;"
                cursor.execute(consulta, (id_rol,))
                resultado = cursor.fetchone()

                # Verificar si el Id_Rol existe
                if resultado and resultado[0] > 0:
                    return True, None  # El Id_Rol existe
                else:
                    return False, f"El Id_Rol {id_rol} no existe."

        except Exception as e:
            # Manejo de errores si algo falla en la consulta
            return False, f"Error al verificar si existe el Id_Rol: {e}"

    def validar_datos_horario(self, horario, id_actual=None):
        # Convertir los valores a cadenas en caso de que sean None o de otro tipo
        dias_semanales = (
            str(horario.dias_semanales).strip() if horario.dias_semanales else ""
        )
        tipo_jornada = str(horario.tipo_jornada).strip() if horario.tipo_jornada else ""
        nombre_horario = (
            str(horario.nombre_horario).strip() if horario.nombre_horario else ""
        )

        if not nombre_horario:
            return False, "El nombre de horario es requerido"
        if not dias_semanales:
            return False, "El campo 'Dias Semanales' es requerido."
        if len(dias_semanales) > 30:
            return False, "El campo 'Dias Semanales' no debe exceder 30 caracteres."

        if not tipo_jornada:
            return False, "El campo 'Tipo Jornada' es requerido."
        if len(tipo_jornada) > 30:
            return False, "El campo 'Tipo Jornada' no debe exceder 30 caracteres."

        if horario.hora_inicio >= horario.hora_fin:
            return False, "La hora de inicio debe ser menor que la hora de fin."

        if horario.descripcion and len(horario.descripcion) > 100:
            return False, "La descripción no debe exceder los 100 caracteres."

        # Validación de unicidad SOLO si es inserción o si los campos clave cambiaron
        if id_actual is None:
            is_unique, message = self.validar_unicidad_jornada(
                nombre_horario, dias_semanales, tipo_jornada
            )
            if not is_unique:
                return False, message
        else:
            # Obtiene los datos actuales y compara para ver si realmente cambiaron
            actual_result = self.get_horario_by_id(id_actual)
            if not actual_result["success"]:
                return False, actual_result["message"]

            actual = actual_result["data"]
            if (
                actual["nombre_horario"] != nombre_horario
                or actual["dias_semanales"] != dias_semanales
                or actual["tipo_jornada"] != tipo_jornada
            ):
                is_unique, message = self.validar_unicidad_jornada(
                    nombre_horario, dias_semanales, tipo_jornada, id_actual
                )
                if not is_unique:
                    return False, message

        return True, "Datos válidos"

    def validar_unicidad_jornada(
        self, nombre_horario, dias_semanales, tipo_jornada, id=None
    ):
        """
        Verifica que no exista el mismo horario con el mismo Tipo de Jornada en el mismo rango de Dias Semanales,
        ignorando el registro actual si se está actualizando.
        """
        # Verificar la conexión
        conexion, resultado = conection()
        if not resultado["success"]:
            return resultado

        try:
            with self.conn.cursor() as cursor:
                # Construcción de la consulta base
                consulta = f"""
                SELECT COUNT(*) FROM {TBHORARIO}
                WHERE {TBHORARIO_NOMBRE_HORARIO} = %s
                AND {TBHORARIO_DIAS_SEMANALES} = %s 
                AND {TBHORARIO_TIPO_JORNADA} = %s
            """
                valores = [nombre_horario, dias_semanales, tipo_jornada]

                # Si estamos actualizando añadimos la condición para ignorarlo
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
                        "Ya existe un horario con el mismo nombre, días semanales y tipo de jornada.",
                    )
                # Todo está bien, no se encontró duplicado
                return True, "El horario es único"

        except Exception as e:
            # Manejo de errores si algo falla en la consulta
            return False, f"Error al verificar unicidad:del horario {e}"
        finally:
            conexion.close()

    def update_horario(self, horario: Horario, id_rol: int):
        """
        Actualiza un horario existente en la base de datos.
        """
        conexion, resultado = conection()
        if not resultado["success"]:
            return resultado

        # Validar los datos antes de la actualización
        datos_validos, mensaje = self.validar_datos_horario(
            horario, id_actual=horario.id
        )
        if not datos_validos:
            return {"success": False, "message": mensaje}

        id_rol_valido, mensaje_rol = self.validar_id_rol(id_rol)
        if not id_rol_valido:
            return {"success": False, "message": mensaje_rol}

        try:
            conexion.start_transaction()
            with self.conn.cursor() as cursor:
                query = f"""
            UPDATE {TBHORARIO} SET
                {TBHORARIO_NOMBRE_HORARIO} = %s,
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
                        horario.nombre_horario,
                        horario.dias_semanales,
                        horario.tipo_jornada,
                        horario.hora_inicio,
                        horario.hora_fin,
                        horario.descripcion,
                        horario.id,  # Condición para identificar el registro a actualizar
                    ),
                )
                query_rol_horario = f"""
                UPDATE {TBROLHORARIO} 
                SET {TBROLHORARIO_ID_ROL} = %s
                WHERE {TBROLHORARIO_ID_HORARIO} = %s
                """
                cursor.execute(
                    query_rol_horario,
                    (id_rol, horario.id),  # Nuevo id_rol y id_horario como condición
                )

                self.conn.commit()  # Confirmar los cambios en la base de datos

                # Cerrar el cursor
                cursor.close()

                return {"success": True, "message": "Horario actualizado exitosamente."}

        except Exception as e:
            conexion.rollback()
            return {"success": False, "message": f"Error al actualizar horario: {e}"}
        finally:
            conexion.close()

    def create_horario(self, horario: Horario, id_rol: int):
        conexion, resultado = conection()
        if not resultado["success"]:
            return resultado
        """
        Inserta un nuevo horario en la base de datos y su relación con el rol.
        """
        # Validar los datos antes de la inserción
        datos_validos, mensaje = self.validar_datos_horario(horario)
        if not datos_validos:
            return {"success": False, "message": mensaje}

        # Validar que el Id_Rol exista
        id_rol_valido, mensaje_rol = self.validar_id_rol(id_rol)
        if not id_rol_valido:
            return {"success": False, "message": mensaje_rol}

        try:

            conexion.start_transaction()
            with conexion.cursor() as cursor:

                # Insertar el horario en la tabla horario
                query_horario = f"""
            INSERT INTO {TBHORARIO} (
                {TBHORARIO_NOMBRE_HORARIO},
                {TBHORARIO_DIAS_SEMANALES},
                {TBHORARIO_TIPO_JORNADA},
                {TBHORARIO_HORA_INICIO},
                {TBHORARIO_HORA_FIN},
                {TBHORARIO_DESCRIPCION}
            ) VALUES (%s, %s, %s, %s, %s, %s)
            """
                cursor.execute(
                    query_horario,
                    (
                        horario.nombre_horario,
                        horario.dias_semanales,
                        horario.tipo_jornada,
                        horario.hora_inicio,
                        horario.hora_fin,
                        horario.descripcion,
                    ),
                )

                # Obtiene el ID del horario recién insertado
                id_horario = cursor.lastrowid

                # Inserta la relación en la tabla rol_horario
                query_rol_horario = f"""
                INSERT INTO {TBROLHORARIO} (
                    {TBROLHORARIO_ID_ROL},
                    {TBROLHORARIO_ID_HORARIO}
                ) VALUES (%s, %s)
                """
                cursor.execute(query_rol_horario, (id_rol, id_horario))
                conexion.commit()

                return {
                    "success": True,
                    "message": "Horario creado exitosamente.",
                    "id_horario": id_horario,
                }

        except Exception as e:
            # rollback
            conexion.rollback()
            return {"success": False, "message": f"Error al crear horario: {e}"}
        finally:
            conexion.close()

    def list_horarios(
        self,
        pagina=1,
        tam_pagina=10,
        ordenar_por=TBHORARIO_ID,
        tipo_orden="DESC",
        busqueda=None,
    ):
        conexion, resultado = conection()
        if not resultado["success"]:
            return resultado

        try:
            with conexion.cursor(dictionary=True) as cursor:

                # Validación de la columna por la cual ordenar
                columnas_validas = {
                    "id": TBHORARIO_ID,
                    "nombre": TBHORARIO_NOMBRE_HORARIO,
                    "rol": TBROL_NOMBRE,  # Permitir ordenar por el nombre del rol
                    "dias": TBHORARIO_DIAS_SEMANALES,
                    "tipo": TBHORARIO_TIPO_JORNADA,
                    "inicio": TBHORARIO_HORA_INICIO,
                    "fin": TBHORARIO_HORA_FIN,
                }
                ordenar_por = columnas_validas.get(ordenar_por, TBHORARIO_ID)

                if tipo_orden not in ["ASC", "DESC"]:
                    tipo_orden = "DESC"  # Valor por defecto si no es válido

                # Construcción de la consulta base con JOIN
                query = f"""
                SELECT 
                    h.{TBHORARIO_ID},
                    h.{TBHORARIO_NOMBRE_HORARIO},
                    r.{TBROL_NOMBRE} AS nombre_rol,
                    h.{TBHORARIO_DIAS_SEMANALES},
                    h.{TBHORARIO_TIPO_JORNADA},
                    h.{TBHORARIO_HORA_INICIO},
                    h.{TBHORARIO_HORA_FIN},
                    h.{TBHORARIO_DESCRIPCION}
                FROM {TBHORARIO} h
                LEFT JOIN {TBROLHORARIO} rh ON h.{TBHORARIO_ID} = rh.{TBROLHORARIO_ID_HORARIO}
                LEFT JOIN {TBROL} r ON rh.{TBROLHORARIO_ID_ROL} = r.{TBROL_ID}
                """

                # Añadir cláusula de búsqueda si se proporciona
                valores = []
                if busqueda:
                    query += f"""
                    WHERE h.{TBHORARIO_DIAS_SEMANALES} LIKE %s 
                    OR h.{TBHORARIO_TIPO_JORNADA} LIKE %s
                    OR r.{TBROL_NOMBRE} LIKE %s
                """
                    valores = [
                        f"%{busqueda}%"
                    ] * 3  # Para usar el valor de búsqueda en las columnas

                # Añadir la cláusula ORDER BY y LIMIT/OFFSET
                query += f" ORDER BY {ordenar_por} {tipo_orden} LIMIT %s OFFSET %s"
                valores.extend([tam_pagina, (pagina - 1) * tam_pagina])

                cursor.execute(query, valores)

                # Leyendo los registros de la consulta
                registros = cursor.fetchall()
                lista_horarios = []
                for registro in registros:
                    horario = {
                        "id": registro[TBHORARIO_ID],
                        "nombre_horario": registro[TBHORARIO_NOMBRE_HORARIO],
                        "nombre_rol": registro["nombre_rol"],  # Nombre del rol asociado
                        "dias_semanales": registro[TBHORARIO_DIAS_SEMANALES],
                        "tipo_jornada": registro[TBHORARIO_TIPO_JORNADA],
                        "hora_inicio": registro[TBHORARIO_HORA_INICIO],
                        "hora_fin": registro[TBHORARIO_HORA_FIN],
                        "descripcion": registro[TBHORARIO_DESCRIPCION],
                    }
                    lista_horarios.append(horario)

                # Obtener el total de registros para calcular el número total de páginas
                cursor.execute(f"SELECT COUNT(*) as total FROM {TBHORARIO}")
                total_registros = cursor.fetchone()["total"]
                total_paginas = (
                    total_registros + tam_pagina - 1
                ) // tam_pagina  # Redondeo hacia arriba

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
        finally:
            conexion.close()

    def delete_horario(self, horario_id):
        """
        Elimina un horario existente en la base de datos.
        """
        conexion, resultado = self.obtener_conexion()
        if not resultado["success"]:
            return resultado
        try:
            conexion.start_transaction()
            with conexion.cursor(dictionary=True) as cursor:

                query = f"DELETE FROM {TBHORARIO} WHERE {TBHORARIO_ID} = %s"

                # Ejecutar la consulta de eliminación
                cursor.execute(query, (horario_id,))
                self.conn.commit()  # Confirmar los cambios en la base de datos

                # Cerrar el cursor
                cursor.close()

                return {"success": True, "message": "Horario eliminado exitosamente."}

        except Exception as e:
            conexion.rollback()
            return {"success": False, "message": f"Error al eliminar horario: {e}"}
        finally:
            conexion.close()

    def get_horario_by_id(self, horario_id):
        """
        Obtiene un horario específico por su ID.
        """
        conexion, resultado = conection()
        if not resultado["success"]:
            return resultado

        try:

            with conexion.cursor(dictionary=True) as cursor:
                query = f"""
                SELECT 
                    h.*,
                    r.{TBROL_ID} AS rol_id,
                    r.{TBROL_NOMBRE} AS rol_nombre
                FROM {TBHORARIO} h
                LEFT JOIN {TBROLHORARIO} rh ON h.{TBHORARIO_ID} = rh.{TBROLHORARIO_ID_HORARIO}
                LEFT JOIN {TBROL} r ON rh.{TBROLHORARIO_ID_ROL} = r.{TBROL_ID}
                WHERE h.{TBHORARIO_ID} = %s
                """
                cursor.execute(query, (horario_id,))
                registro = cursor.fetchone()

                if registro:
                    return {
                        "success": True,
                        "data": {
                            "id": registro[TBHORARIO_ID],
                            "nombre_horario": registro.get(
                                TBHORARIO_NOMBRE_HORARIO, ""
                            ),
                            "dias_semanales": registro[TBHORARIO_DIAS_SEMANALES],
                            "tipo_jornada": registro[TBHORARIO_TIPO_JORNADA],
                            "hora_inicio": registro[TBHORARIO_HORA_INICIO],
                            "hora_fin": registro[TBHORARIO_HORA_FIN],
                            "descripcion": registro[TBHORARIO_DESCRIPCION],
                            "rol_id": registro.get("rol_id"),
                            "nombre_rol": registro.get("rol_nombre"),
                        },
                        "message": "Horario encontrado exitosamente.",
                    }
                else:
                    return {
                        "success": False,
                        "message": "No se encontró un horario con el ID proporcionado.",
                    }
        except Exception as e:

            return {"success": False, "message": f"Error al obtener el horario: {e}"}
        finally:
            conexion.close()

    def obtenerHorarioPorDiasYTipo(self, nombre_horario, dias_semanales, tipo_jornada):
        """
        Obtiene un horario específico por los días semanales y el tipo de jornada.
        """
        try:
            cursor = self.conn.cursor(dictionary=True)
            query = f"""
        SELECT * FROM {TBHORARIO} 
        WHERE {TBHORARIO_NOMBRE_HORARIO} = %s 
        AND {TBHORARIO_DIAS_SEMANALES} = %s 
        AND {TBHORARIO_TIPO_JORNADA} = %s
        LIMIT 1
        """
            cursor.execute(query, (nombre_horario, dias_semanales, tipo_jornada))
            registro = cursor.fetchone()
            cursor.close()

            if registro:
                return Horario(
                    nombre_horario=registro[TBHORARIO_NOMBRE_HORARIO],
                    dias_semanales=registro[TBHORARIO_DIAS_SEMANALES],
                    tipo_jornada=registro[TBHORARIO_TIPO_JORNADA],
                    hora_inicio=registro[TBHORARIO_HORA_INICIO],
                    hora_fin=registro[TBHORARIO_HORA_FIN],
                    descripcion=registro[TBHORARIO_DESCRIPCION],
                    id=registro[TBHORARIO_ID],
                )
            return None  # No se encontró ningún horario con el mismo nombre, días y tipo de jornada

        except Exception as e:
            print(f"Error al obtener horario por nombre, días y tipo: {e}")
            return None

    def delete_horario(self, horario_id):
        """
        Elimina un horario existente en la base de datos, incluyendo sus relaciones en Rol horario.
        """
        conexion, resultado = conection()
        if not resultado["success"]:
            return resultado

        try:
            conexion.start_transaction()
            with conexion.cursor(dictionary=True) as cursor:
                # 1. Primero eliminamos las relaciones en rol_horario del horario asociado
                delete_relaciones = f"""
                DELETE FROM {TBROLHORARIO} 
                WHERE {TBROLHORARIO_ID_HORARIO} = %s
                """
                cursor.execute(delete_relaciones, (horario_id,))

                # 2. Luego eliminamos el horario de horario
                delete_horario = f"""
                DELETE FROM {TBHORARIO} 
                WHERE {TBHORARIO_ID} = %s
                """
                cursor.execute(delete_horario, (horario_id,))

                conexion.commit()

                return {
                    "success": True,
                    "message": "Horario y sus relaciones eliminados exitosamente.",
                }

        except Exception as e:
            conexion.rollback()
            return {"success": False, "message": f"Error al eliminar horario: {e}"}
        finally:
            conexion.close()
