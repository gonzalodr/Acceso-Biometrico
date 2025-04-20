from models.perfil import Perfil
from data.data import conection
from settings.config import *
from settings.logger import logger
from data.permisosPerfilData import PermisosPerfilData
import traceback


class PerfilData:
    def __init__(self):
        self.permisoPerfilData = PermisosPerfilData()

    def verificar_nombre_perfil(
        self, nombre_perfil: str, id_perfil_excluir: int = None
    ) -> dict:
        conexion, resultado = conection()
        if not resultado["success"]:
            return resultado

        try:
            with conexion.cursor() as cursor:
                if id_perfil_excluir:
                    # Consulta que excluye el perfil que se está actualizando
                    query = f"""
                            SELECT 
                                COUNT(*) 
                            FROM  {TBPERFIL} 
                            WHERE {TBPERFIL_NOMBRE} = %s 
                            AND {TBPERFIL_ID} != %s"""
                    cursor.execute(query, (nombre_perfil, id_perfil_excluir))
                else:
                    # Consulta normal para creación de nuevo perfil
                    query = f"""
                            SELECT 
                                COUNT(*) 
                            FROM {TBPERFIL} 
                            WHERE {TBPERFIL_NOMBRE} = %s"""
                    cursor.execute(query, (nombre_perfil,))

                count = cursor.fetchone()[0]

                return {
                    "exists": count > 0,
                    "success": True,
                    "message": "Verificación completada",
                }
        except Exception as e:
            logger.error(f"{e} - {traceback.format_exc()}")
            return {
                "exists": False,
                "success": False,
                "message": "Ocurrió un error al verificar el nombre del perfil",
            }
        finally:
            if conexion:
                conexion.close()

    def create_perfil(
        self, perfil: Perfil, listaPermisos
    ):  # metodo para crear el perfil en la base de datos
        conexion, resultado = conection()
        if not resultado["success"]:  # si falla la conexion retorna error
            return resultado
        try:
            with conexion.cursor() as cursor:  # se utiliza el cursor para las consultas a la base de datos
                query = f"""INSERT INTO {TBPERFIL}(
                {TBPERFIL_NOMBRE},
                {TBPERFIL_DESCRIPCION})
                VALUES (%s, %s)"""  # campos o posciones

                cursor.execute(query, (perfil.nombre, perfil.descripcion))
                id_perfil = cursor.lastrowid
                ##registrar los accesos
                if listaPermisos:
                    for permiso in listaPermisos:
                        permiso.perfil_id = id_perfil
                        result = self.permisoPerfilData.create_permiso_perfil(
                            permiso, conexion
                        )
                        if not result["success"]:
                            conexion.rollback()
                            return result
                conexion.commit()
                return {
                    "success": True,
                    "message": "El perfil se guardo correctamente.",
                }
        except Exception as e:
            logger.error(f"{e}  - {traceback.format_exc()}")
            conexion.rollback()
            return {
                "success": False,
                "message": "Ocurrio un error al guardar el perfil.",
            }
        finally:
            if conexion:
                conexion.close()

    def update_perfil(
        self, perfil: Perfil, listaPermisos
    ):  # metodo para actualizar perfil
        conexion, resultado = conection()  # obtiene el estado de la conexion
        if not resultado["success"]:  # error
            return resultado

        try:
            with conexion.cursor() as cursor:
                conexion.start_transaction()
                query = f"""UPDATE {TBPERFIL} SET 
                {TBPERFIL_NOMBRE} = %s,
                {TBPERFIL_DESCRIPCION} = %s
                WHERE {TBPERFIL_ID} = %s"""

                cursor.execute(query, (perfil.nombre, perfil.descripcion, perfil.id))
                if listaPermisos:
                    for permiso in listaPermisos:
                        permiso.perfil_id = perfil.id
                        if permiso.id:
                            result = self.permisoPerfilData.update_permiso_perfil(
                                permiso, conexion
                            )
                            if not result["success"]:
                                conexion.rollback()
                                return result
                        else:
                            result = self.permisoPerfilData.create_permiso_perfil(
                                permiso, conexion
                            )
                            if not result["success"]:
                                conexion.rollback()
                                return result

                conexion.commit()
                return {
                    "success": True,
                    "message": "Se actualizo correctamente el perfil",
                }
        except Exception as e:
            logger.error(f"{e} - {traceback.format_exc()}")
            conexion.rollback()
            return {
                "succcess": False,
                "message": "Ocurrio un error al actualizar los perfiles.",
            }
        finally:
            if conexion:
                conexion.close()

    def delete_perfil(self, perfil_id):
        conexion, resultado = conection()
        if not resultado["success"]:
            return resultado

        try:
            with conexion.cursor() as cursor:
                # Verificar si hay usuarios vinculados
                cursor.execute(
                    f"""SELECT 1
                                FROM {TBUSUARIOPERFIL} 
                                WHERE {TBUSUARIOPERFIL_ID_PERF} = %s""",
                    (perfil_id,),
                )
                row = cursor.fetchone()  # Solo llamamos a fetchone() una vez
                if row is not None:  # Si hay resultados
                    return {
                        "success": False,
                        "message": "Este perfil tiene usuarios vinculados.",
                    }

                # Eliminar permisos del perfil
                cursor.execute(
                    f"DELETE FROM {TBPERMISOPERFIL} WHERE {TBPERMISOPERFIL_PERFIL_ID} = %s",
                    (perfil_id,),
                )

                # Eliminar el perfil
                cursor.execute(
                    f"DELETE FROM {TBPERFIL} WHERE {TBPERFIL_ID} = %s", (perfil_id,)
                )

                conexion.commit()
                return {
                    "success": True,
                    "message": "El perfil se eliminó exitosamente.",
                }

        except Exception as e:
            conexion.rollback()
            logger.error(f"{e} - {traceback.format_exc()}")
            return {
                "success": False,
                "message": "Ocurrió un error al eliminar el perfil",
            }
        finally:
            if conexion:
                conexion.close()

    def list_perfiles(
        self,
        pagina=1,
        tam_pagina=10,
        ordenar_por=TBPERFIL_ID,
        tipo_orden="ASC",
        busqueda=None,
    ):
        conexion, resultado = conection()
        if not resultado["success"]:
            return resultado

        listaPerfiles = []  # lista donde se almacenan los perfiles
        try:
            with conexion.cursor(dictionary=True) as cursor:

                columna_orden = {
                    "nombre": TBPERFIL_NOMBRE,
                    "descripcion": TBPERFIL_DESCRIPCION,
                }

                ordenar_por = columna_orden.get(ordenar_por, TBPERFIL_ID)
                tipo_orden = "DESC" if tipo_orden != "ASC" else "ASC"

                query = f"SELECT * FROM {TBPERFIL}"
                valores = []

                if busqueda:
                    query += f" WHERE {TBPERFIL_NOMBRE} LIKE %s OR {TBPERFIL_DESCRIPCION} LIKE %s"
                    valores = [f"%{busqueda}%", f"%{busqueda}%"]

                query += f" ORDER BY {ordenar_por} {tipo_orden} LIMIT %s OFFSET %s"
                valores.extend([tam_pagina, (pagina - 1) * tam_pagina])

                cursor.execute(query, valores)
                registros = cursor.fetchall()
                for registro in registros:
                    perfil = Perfil(
                        nombre=registro[TBPERFIL_NOMBRE],
                        descripcion=registro[TBPERFIL_DESCRIPCION],
                        id=registro[TBPERFIL_ID],
                    )
                    result = self.permisoPerfilData.get_permisos_perfil_ByPerfilId(
                        perfil.id
                    )
                    if not result["success"]:
                        return result
                    listaPerfiles.append(
                        {"perfil": perfil, "listaPermisos": result["listaPermiso"]}
                    )

                cursor.execute(f"SELECT COUNT(*) as total FROM {TBPERFIL}")
                total_registros = cursor.fetchone()["total"]
                total_paginas = (total_registros + tam_pagina - 1) // tam_pagina

                return {
                    "success": True,
                    "message": "Perfiles listados correctamente.",
                    "data": {
                        "listaPerfiles": listaPerfiles,
                        "pagina_actual": pagina,
                        "tam_pagina": tam_pagina,
                        "total_paginas": total_paginas,
                        "total_registros": total_registros,
                    },
                }

        except Exception as e:
            logger.error(f"{e}-Traceback: {traceback.format_exc()}")
            return {
                "success": False,
                "message": "Ocurrio un error al listar los perfiles.",
            }
        finally:
            if conexion:
                conexion.close()

    def get_perfil_by_id(self, perfil_id):
        conexion, resultado = conection()
        if not resultado["success"]:
            return resultado

        try:
            with conexion.cursor(dictionary=True) as cursor:
                # Consulta SQL para obtener el perfil por su ID
                query = f"""SELECT
                            {TBPERFIL_NOMBRE}, 
                            {TBPERFIL_DESCRIPCION}, 
                            {TBPERFIL_ID} 
                        FROM {TBPERFIL} 
                        WHERE {TBPERFIL_ID} = %s"""

                cursor.execute(query, (perfil_id,))  # busca segun el id
                data = cursor.fetchone()  # se obtiene el resultado

                if data:  # si se encuentra el perfil
                    perfil = Perfil(
                        nombre=data[TBPERFIL_NOMBRE],
                        descripcion=data[TBPERFIL_DESCRIPCION],
                        id=data[TBPERFIL_ID],
                    )
                    result = self.permisoPerfilData.get_permisos_perfil_ByPerfilId(
                        perfil.id
                    )
                    if not result["success"]:
                        return result
                    return {
                        "success": True,
                        "exists": True,
                        "data": {
                            "perfil": perfil,
                            "listaPermisos": result["listaPermiso"],
                        },
                        "message": "Se obtuvo el perfil con sus accesos exitosamente.",
                    }
                else:
                    return {
                        "success": True,
                        "exists": False,
                        "message": "No se encontro el perfil.",
                    }
        except Exception as e:
            logger.error(f"{e}")
            return {
                "success": False,
                "message": "Ocurrio un error al obtener el perfil.",
            }
        finally:
            if conexion:
                conexion.close()

    def obtener_todo_perfiles(self):
        conexion, resultado = conection()
        if not resultado["success"]:
            return resultado

        listaPerfiles = []  # Lista donde se almacenarán los perfiles ob
        try:
            with conexion.cursor(dictionary=True) as cursor:
                query = f"SELECT * FROM {TBPERFIL}"
                cursor.execute(query)
                registros = cursor.fetchall()

                # Se convierten los registros en objetos de tipo Perfil y se almacenan en la lista
                for registro in registros:
                    perfil = Perfil(
                        nombre=registro[TBPERFIL_NOMBRE],
                        descripcion=registro[TBPERFIL_DESCRIPCION],
                        id=registro[TBPERFIL_ID],
                    )
                    listaPerfiles.append(perfil)

                resultado["data"] = {
                    "listaPerfiles": listaPerfiles,
                }
                resultado["success"] = True
                resultado["message"] = "Perfiles listados exitosamente."
        except Exception as e:
            resultado["success"] = False
            resultado["message"] = f"Error al listar perfiles: {e}"
        finally:
            if cursor:
                cursor.close()  # Se cierra el cursor
            if conexion:
                conexion.close()  # Se cierra la conexión a la base de datos

        return resultado
