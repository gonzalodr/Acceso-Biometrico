import mysql.connector
from mysql.connector import Error
from settings.config import DATABASE_CONFIG
from settings.logger import logger

def conection():
    conexion = None
    try:
        conexion = mysql.connector.connect(
            host = DATABASE_CONFIG["host"],
            user = DATABASE_CONFIG["user"],
            password = DATABASE_CONFIG["password"],
            database = DATABASE_CONFIG["database"]
        )
        return conexion, {'success':True}
    except Error as e:
        logger.error(f'{e}')
        return conexion, {'success':False,'message':'Ocurrió un error de conexión.'}
