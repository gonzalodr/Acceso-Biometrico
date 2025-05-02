from data.data import conection  # Asegúrate de que este sea el path correcto
from settings.logger import logger
from models.huella import Huella
from mysql.connector import Error
from settings.config import *

class HuellaData:
    @staticmethod
    def registrar_huella(
        id_empleado: int,
        uid_dispositivo: int,
        user_id_dispositivo: str,
        nombre_guardado: str,
        privilegio: int = 0,
        tiene_huella: bool = True,
    ):
        conexion, resultado = conection()
        if not resultado["success"]:
            return resultado

        try:
            with conexion.cursor() as cursor:
                query = """
                INSERT INTO huella 
                (id_empleado, uid_dispositivo, user_id_dispositivo, nombre_guardado, privilegio, tiene_huella)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            valores = (
                id_empleado,
                uid_dispositivo,
                user_id_dispositivo,
                nombre_guardado,
                privilegio,
                tiene_huella,
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


    def create_huella(self, huella: Huella):
        conexion, resultado = conection()
        if not resultado["success"]:
            return resultado
        
        try:
            with conexion.cursor() as cursor:
                query = f"""INSERT INTO {TBHUELLA}(
                {TBHUELLA_ID_EMPLEADO},
                {TBHUELLA_HUELLA})
                VALUES (%s, %s)"""
                
                cursor.execute(query, (
                    huella.id_empleado,
                    huella.id_huella  # Asegúrate de que este campo contenga la huella en el formato correcto
                ))
                conexion.commit()
                return {'success': True, 'message': 'La huella se guardó correctamente.'}
        except Error as e:
            logger.error(f'Error: {e}')
            return {'success': False, 'message': 'Ocurrió un error al guardar la huella.'}
        finally:
            if conexion:
                conexion.close()
