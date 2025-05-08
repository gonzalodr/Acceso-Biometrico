from data.data import conection  # obtener la conexión
from mysql.connector import Error
from settings.config import (
    TBTELEFONO,
    TBTELEFONO_ID,
    TBTELEFONO_TIPO_CONTACTO,
    TBTELEFONO_ID_PERSONA,
    TBTELEFONO_NUMERO,
)  # obtener los nombres de tablas
from settings.logger import logger  # recolectar los errores

from models.telefono import Telefono


class TelefonoData:

    def verificarExistenciaTelefono(
        self, telefono: str, id_telefono: int = None, conexionEx=None
    ):
        conexion, resultado = (
            conection() if conexionEx is None else (conexionEx, {"success": True})
        )
        if not resultado["success"]:
            return resultado
        try:
            with conexion.cursor() as cursor:
                query = (
                    f"SELECT COUNT(*) FROM {TBTELEFONO} WHERE {TBTELEFONO_NUMERO} = %s "
                )
                if id_telefono is not None and id_telefono > 0:
                    query += f" AND {TBTELEFONO_ID} != %s"
                    cursor.execute(query, (telefono, id_telefono))
                else:
                    cursor.execute(query, (telefono,))
                count = cursor.fetchone()[0]
                return {"success": True, "isValid": count == 0}
        except Error as e:
            logger.error(f"{e}")
            return {"success": True, "isValid": False}
        finally:
            if conexion and conexionEx is None:
                conexion.close()

    def create_telefono(self, telefono: Telefono, conexionEx=None):
        conexion, resultado = (
            conection() if conexionEx is None else (conexionEx, {"success": True})
        )
        if not resultado["success"]:
            return resultado

        try:
            with conexion.cursor() as cursor:
                query = f""" INSERT INTO {TBTELEFONO} (
                            {TBTELEFONO_ID_PERSONA},
                            {TBTELEFONO_NUMERO},
                            {TBTELEFONO_TIPO_CONTACTO}
                            ) VALUES (%s,%s,%s)"""
                cursor.execute(
                    query, (telefono.id_persona, telefono.numero, telefono.tipo)
                )
                if conexionEx is None:
                    conexion.commit()
                return {
                    "success": True,
                    "message": "Se guardo el numero de telefono correctamente.",
                }
        except Error as e:
            logger.error(f"{e}")
            return {
                "success": False,
                "message": "Ocurrió un error al registrar el numero de telefono.",
            }
        finally:
            if conexion and conexionEx is None:
                conexion.close()

    def update_telefono(self, telefono: Telefono, conexionEx=None):
        conexion, resultado = (
            conection() if conexionEx is None else (conexionEx, {"success": True})
        )
        if not resultado["success"]:
            return resultado

        try:
            with conexion.cursor() as cursor:
                query = f"""UPDATE {TBTELEFONO} SET
                        {TBTELEFONO_ID_PERSONA} = %s,
                        {TBTELEFONO_NUMERO} = %s,
                        {TBTELEFONO_TIPO_CONTACTO} = %s
                        WHERE {TBTELEFONO_ID} = %s """
                cursor.execute(
                    query,
                    (telefono.id_persona, telefono.numero, telefono.tipo, telefono.id),
                )
                if conexionEx is None:
                    conexion.commit()
                return {
                    "success": True,
                    "message": "Se actualizo el telefono correctamente.",
                }
        except Error as e:
            logger.error(f"{e}")
            return {
                "success": False,
                "message": "Ocurrió un error al actualizar el telefono.",
            }
        finally:
            if conexion and conexionEx is None:
                conexion.close()

    def delete_telefono(self, id_telefono: int, conexionEx=None):
        conexion, resultado = (
            conection() if conexionEx is None else (conexionEx, {"success": True})
        )
        if not resultado["success"]:
            return resultado

        try:
            with conexion.cursor() as cursor:
                query = f"""DELETE FROM {TBTELEFONO} WHERE {TBTELEFONO_ID} = %s """
                cursor.execute(query, (id_telefono,))
                if conexionEx is None:
                    conexion.commit()
                return {
                    "success": True,
                    "message": "Se elimino el numero de telefono correctamente.",
                }
        except Error as e:
            logger.error(f"{e}")
            return {
                "success": False,
                "message": "Ocurrió un error al eliminar el telefono.",
            }
        finally:
            if conexion and conexionEx is None:
                conexion.close()

    def get_telefono_by_id(self, id_telefono: int):
        conexion, resultado = conection()
        if not resultado["success"]:
            return resultado
        try:
            with conexion.cursor(dictionary=True) as cursor:
                query = f"""SELECT 
                    {TBTELEFONO_ID},
                    {TBTELEFONO_ID_PERSONA},
                    {TBTELEFONO_NUMERO},
                    {TBTELEFONO_TIPO_CONTACTO}
                    FROM {TBTELEFONO}
                    WHERE {TBTELEFONO_ID} = %s
                """
                cursor.execute(query, (id_telefono,))

                data = cursor.fetchone()

                if data:
                    telefono = Telefono(
                        data[TBTELEFONO_ID_PERSONA],
                        data[TBTELEFONO_NUMERO],
                        data[TBTELEFONO_TIPO_CONTACTO],
                        data[TBTELEFONO_ID],
                    )
                    return {
                        "data": telefono,
                        "success": True,
                        "exists": True,
                        "message": "Se encontró el numero de telefono.",
                    }
                else:
                    return {
                        "success": True,
                        "exists": False,
                        "message": "No se encontró el numero de telefono.",
                    }
        except Error as e:
            logger.error(f"{e}")
            return {
                "success": False,
                "message": "Ocurrió un error al obtener el telefono.",
            }
        finally:
            if conexion:
                conexion.close()

    def get_Telefono_by_id_persona(self, id_persona: int, conexionEx=None):
        conexion, resultado = (
            conection() if conexionEx is None else (conexionEx, {"success": True})
        )
        if not resultado["success"]:
            return resultado
        try:
            listaTelefonos = []
            with conexion.cursor(dictionary=True) as cursor:
                query = f"""SELECT 
                        {TBTELEFONO_ID},
                        {TBTELEFONO_ID_PERSONA},
                        {TBTELEFONO_NUMERO},
                        {TBTELEFONO_TIPO_CONTACTO}
                        FROM {TBTELEFONO}
                        WHERE {TBTELEFONO_ID_PERSONA} = %s
                    """
                cursor.execute(query, (id_persona,))

                registros = cursor.fetchall()

                if registros:
                    for data in registros:
                        telefono = Telefono(
                            data[TBTELEFONO_ID_PERSONA],
                            data[TBTELEFONO_NUMERO],
                            data[TBTELEFONO_TIPO_CONTACTO],
                            data[TBTELEFONO_ID],
                        )
                        listaTelefonos.append(telefono)

                    return {
                        "listaTelefonos": listaTelefonos,
                        "success": True,
                        "exists": True,
                        "message": "Se encontró el numero de telefono.",
                    }
                else:
                    return {
                        "success": True,
                        "exists": False,
                        "message": "No se encontró el numero de telefono.",
                    }
        except Error as e:
            logger.error(f"{e}")
            return {
                "success": False,
                "message": "Ocurrio un error al buscar los numeros telefonicos.",
            }
        finally:
            if conexion and conexionEx is None:
                conexion.close()
