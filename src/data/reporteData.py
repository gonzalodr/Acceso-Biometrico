from models.reporte import Reporte
from data.data import conection
from settings.config import *

class ReporteData:
    
    def create_reporte(self, reporte: Reporte): #crear reporte en la base de datos
        conexion, resultado = conection() #conexiona la base datos
        if not resultado["success"]:# si falla
            return resultado
        
        try:
            cursor = conexion.cursor()
            query = f"""INSERT INTO {TBREPORTE}(
            {TBREPORTE_ID_EMPLEADO},
            {TBREPORTE_FECHA_GENERACION},
            {TBREPORTE_TIPO_REPORTE},
            {TBREPORTE_CONTENIDO})
            VALUES (%s, %s, %s, %s)"""
            
            cursor.execute(query,(
                reporte.id_empleado,
                reporte.fecha_generacion,
                reporte.tipo_reporte,
                reporte.contenido
            ))
            conexion.commit()
            resultado["success"] = True
            resultado["message"] = "Reporte creado exitosamente"
        except Exception as e :
            resultado["success"] = False
            resultado["message"] = f"Erorr al crear reporte:  {e}"
        finally:
            if conexion:
                conexion.close()
        return resultado 