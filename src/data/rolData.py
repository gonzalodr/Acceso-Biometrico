from models.rol import Rol
from data.data import conection
from settings.logger import logger
from settings.config import TBROL, TBROL_ID, TBROL_NOMBRE, TBROL_DESCRIPCION


class RolData:

    def create_rol(self, rol: Rol):
        conexion, resultado = conection()
        if not resultado["success"]:
            return resultado

        try:
            with conexion.cursor() as cursor:
                query = f"""INSERT INTO {TBROL}( {TBROL_NOMBRE}, {TBROL_DESCRIPCION} ) VALUES (%s, %s)"""
                cursor.execute(query, (rol.nombre, rol.descripcion))
                conexion.commit()
                return {"success": True, "message": "Se guardo el rol correctamente."}
        except Exception as e:
            logger.error(f"{e}")
            return {
                "success": False,
                "message": "Ocurrió un error al registrar el rol.",
            }
        finally:
            if conexion:
                conexion.close()

    def update_rol(self, rol: Rol):
        conexion, resultado = conection()
        if not resultado["success"]:
            return resultado

        try:
            with conexion.cursor() as cursor:
                query = f"""UPDATE {TBROL} SET {TBROL_NOMBRE} = %s, {TBROL_DESCRIPCION} = %s
                        WHERE {TBROL_ID} = %s"""

                cursor.execute(query, (rol.nombre, rol.descripcion, rol.id))
                conexion.commit()
                return {
                    "success": True,
                    "message": "Se actualizo correctamente el rol.",
                }
        except Exception as e:
            logger.error(f"{e}")
            return {
                "success": True,
                "message": "Ocurrió un error al actualizar el rol.",
            }
        finally:
            if conexion:
                conexion.close()

    def delete_rol(self, rol_id):
        conexion, resultado = conection()
        if not resultado["success"]:
            return resultado

        try:
            with conexion.cursor() as cursor:
                query = f"DELETE FROM {TBROL} WHERE {TBROL_ID} = %s"

                cursor.execute(query, (rol_id,))
                conexion.commit()

                return {"success": True, "message": "Se elimino correctamente el rol."}
        except Exception as e:
            logger.error(f"{e}")
            return {
                "success": False,
                "message": "Ocurrió un error al actualizar el rol.",
            }
        finally:
            if conexion:
                conexion.close()

    def list_roles(
        self,
        pagina=1,
        tam_pagina=10,
        ordenar_por=TBROL_ID,
        tipo_orden="ASC",
        busqueda=None,
    ):
        conexion, resultado = conection()
        if not resultado["success"]:
            return resultado

        listaRoles = []
        try:
            with conexion.cursor(dictionary=True) as cursor:
                columna_orden = {
                    "nombre": TBROL_NOMBRE,
                    "descripcion": TBROL_DESCRIPCION,
                }

                ordenar_por = columna_orden.get(ordenar_por, TBROL_ID)
                tipo_orden = "DESC" if tipo_orden != "ASC" else "ASC"

                query = f"SELECT * FROM {TBROL}"
                valores = []
                if busqueda:
                    query += (
                        f" WHERE {TBROL_NOMBRE} LIKE %s OR {TBROL_DESCRIPCION} LIKE %s"
                    )
                    valores = [f"%{busqueda}%", f"%{busqueda}%"]

                query += f" ORDER BY {ordenar_por} {tipo_orden} LIMIT %s OFFSET %s"
                valores.extend([tam_pagina, (pagina - 1) * tam_pagina])

                cursor.execute(query, valores)
                registros = cursor.fetchall()
                for registro in registros:
                    rol = Rol(
                        nombre=registro[TBROL_NOMBRE],
                        descripcion=registro[TBROL_DESCRIPCION],
                        id=registro[TBROL_ID],
                    )
                    listaRoles.append(rol)

                cursor.execute(f"SELECT COUNT(*) as total FROM {TBROL}")
                total_registros = cursor.fetchone()["total"]
                total_paginas = (total_registros + tam_pagina - 1) // tam_pagina

                resultado["data"] = {
                    "listaRoles": listaRoles,
                    "pagina_actual": pagina,
                    "tam_pagina": tam_pagina,
                    "total_paginas": total_paginas,
                    "total_registros": total_registros,
                }
                resultado["success"] = True
                resultado["message"] = "Roles listados exitosamente."
        except Exception as e:
            logger.error(f"{e}")
            resultado["success"] = False
            resultado["message"] = f"Error al listar roles: {e}"
        finally:
            if conexion:
                conexion.close()
        return resultado

    def get_rol_by_id(self, rol_id):
        conexion, resultado = conection()
        if not resultado["success"]:
            return resultado

        try:
            with conexion.cursor() as cursor:
                query = f"""SELECT
                                {TBROL_NOMBRE}, 
                                {TBROL_DESCRIPCION}, 
                                {TBROL_ID} 
                            FROM {TBROL} 
                            WHERE {TBROL_ID} = %s"""

                cursor.execute(query, (rol_id,))
                data = cursor.fetchone()

                if data:
                    rol = Rol(nombre=data[0], descripcion=data[1], id=data[2])
                    return {
                        "success": True,
                        "exists": True,
                        "message": "Se encontró el rol buscado.",
                        "data": rol,
                    }
                else:
                    return {
                        "success": True,
                        "exists": False,
                        "message": "No se encontró el rol.",
                    }
        except Exception as e:
            logger.error(f"{e}")
            return {"success": False, "message": "No se encontró el rol."}
        finally:
            if conexion:
                conexion.close()

    def obtener_todo_roles(self):
        conexion, resultado = conection()
        if not resultado["success"]:
            return resultado

        listaRoles = []
        try:
            with conexion.cursor(dictionary=True) as cursor:
                query = f"SELECT * FROM {TBROL}"
                cursor.execute(query)
                registros = cursor.fetchall()
                for registro in registros:
                    rol = Rol(
                        registro[TBROL_NOMBRE],
                        registro[TBROL_DESCRIPCION],
                        registro[TBROL_ID],
                    )
                    listaRoles.append(rol)
                return {
                    "data": {"listaRoles": listaRoles},
                    "success": True,
                    "message": "Roles listados exitosamente",
                }

        except Exception as e:
            logger.error(f"{e}")
            return {
                "success": True,
                "message": "Ocurrió un error al listar todos los roles",
            }
        finally:
            if conexion:
                conexion.close()

    def get_all_roles(self):
        """
        Obtiene todos los roles (nombre e ID) de la tabla Rol.
        Retorna un diccionario el nombre y ID
        """
        conexion, resultado = conection()
        if not resultado["success"]:
            return resultado

        try:
            with conexion.cursor() as cursor:
                query = f"""
                SELECT
                    {TBROL_NOMBRE}, 
                    {TBROL_ID} 
                FROM {TBROL}
            """
                cursor.execute(query)
                roles = cursor.fetchall()  # Obtiene todos los registros

                if roles:
                    # Convertir los resultados en una lista de diccionarios
                    lista_roles = [{"nombre": rol[0], "id": rol[1]} for rol in roles]
                    return {
                        "success": True,
                        "message": "Roles obtenidos correctamente.",
                        "data": lista_roles,
                    }
                else:
                    return {
                        "success": True,
                        "message": "No se encontraron roles.",
                        "data": [],
                    }
        except Exception as e:
            logger.error(f"Error al obtener los roles: {e}")
            return {
                "success": False,
                "message": "Error al obtener los roles.",
                "data": None,
            }
        finally:
            if conexion:
                conexion.close()
