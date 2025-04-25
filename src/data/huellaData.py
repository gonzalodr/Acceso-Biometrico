from data.data import conection
from settings.logger import logger


class HuellaData:

    def registrar_huella(
        self,
        id_empleado: int,
        user_id_dispositivo: str,
        privilegio: int = 0,
    ):
        conexion, resultado = conection()
        if not resultado["success"]:
            return resultado

        try:
            with conexion.cursor() as cursor:
                query = """
                INSERT INTO huella 
                (id_empleado, user_id_dispositivo, privilegio,)
                VALUES (%s, %s, %s)
            """
            valores = (
                id_empleado,
                user_id_dispositivo,
                privilegio,
            )
            cursor.execute(query, valores)
            conexion.commit()
            return {"success": True, "message": "Huella registrada correctamente."}
        except Exception as e:
            logger.error(f"Error al registrar huella: {e}")
            return {"success": False, "message": "Error al registrar la huella."}
        finally:
            if conexion:
                cursor.close()
                conexion.close()
