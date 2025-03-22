from mysql.connector import Error
from models.asistencia import Asistencia
from data.data import conection
from settings.config import *
from settings.logger import logger

class AsistenciaData:

    
    def listar_asistencia_por_empleado(self, id_empleado: int):
        conexion, resultado = conection()
        if not resultado["success"]:
            return resultado
        
        listaAsistencias = []
        try:
            with conexion.cursor(dictionary=True) as cursor:
                query = f'''
                    SELECT Id, Id_Empleado, Fecha, Estado_Asistencia 
                    FROM Asistencia 
                    WHERE Id_Empleado = %s AND Estado_Asistencia = 'No_Justificada'
                    ORDER BY Fecha DESC
                '''
                cursor.execute(query, (id_empleado,))
                registros = cursor.fetchall()
                
                for data in registros:
                    asistencia = Asistencia(
                        id_asistencia=data["Id"],
                        id_empleado=data["Id_Empleado"],
                        fecha=data["Fecha"],
                        estado_asistencia=data["Estado_Asistencia"]
                    )
                    listaAsistencias.append(asistencia)
                
                return {
                    "data": listaAsistencias,
                    "success": True,
                    "message": "Asistencias listadas exitosamente."
                }
        except Error as e:
            logger.error(f"Error al listar asistencias: {e}")
            return {"success": False, "message": "Ocurrió un error al listar las asistencias."}
        finally:
            if conexion:
                conexion.close()
