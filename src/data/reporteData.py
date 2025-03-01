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
    
    def update_perfil(self, reporte: Reporte):
        conexion, resultado = conection()
        if not resultado["success"]:
            return resultado
        
        try:
            cursor = conexion.cursor()
            query = f"""UPDATE {TBREPORTE} SET
            {TBREPORTE_ID_EMPLEADO} = %s,
            {TBREPORTE_FECHA_GENERACION} = %s,
            {TBREPORTE_TIPO_REPORTE} = %s,
            {TBREPORTE_CONTENIDO} = %s
            WHERE {TBREPORTE_ID} = %s"""
            
            cursor.execute(query, (
                reporte.id_empleado,
                reporte.fecha_generacion,
                reporte.tipo_reporte,
                reporte.contenido,
                reporte.id
            ))
            conexion.commit()
            resultado["success"] = True
            resultado["message"] = "Reporte actualizado exitosamente."
        except Exception as e:
            resultado["success"] = False
            resultado["message"] = f"Error al actualizar reporte: {e}"
        finally:
            if conexion:
                conexion.close()
        return resultado
    
    def delete_reporte(self, id):
        conexion, resultado = conection()
        if not resultado["success"]:
            return resultado
        
        try:
            cursor = conexion.cursor()
            query = f"DELETE FROM {TBREPORTE} WHERE {TBREPORTE_ID} = %s"
            cursor.execute(query, (id,))
            conexion.commit()
            
            resultado["success"] = True
            resultado["message"] = "Reporte eliminado exitosamente."
        except Exception as e:
            resultado["success"] = False
            resultado["message"] = f"Error al eliminar reporte: {e}"
        finally:
            if conexion:
                conexion.close()
        return resultado