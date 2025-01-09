import mysql.connector
from mysql.connector import Error
from settings.config import DATABASE_CONFIG
from settings.logger import logger

def conection():
    conexion = None
    resultado = { "success" : False, "message" : "" }
    try:
        conexion = mysql.connector.connect(
            host = DATABASE_CONFIG["host"],
            user = DATABASE_CONFIG["user"],
            password = DATABASE_CONFIG["password"],
            database = DATABASE_CONFIG["database"]
        )
        resultado["success"] = True
    except Error as e:
        logger.error(f'Error de conexion : {e}')
        resultado["message"] = f"Error '{e}' ocurrió al conectar a la base de datos"
    return conexion, resultado #devuelve la conexion y los resultados
