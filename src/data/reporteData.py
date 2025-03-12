from models.reporte import Reporte #importa la clase de reportes 
from data.data import conection # importa la funcion de conection para crear la conexion enla base de datos
from settings.config import * 

class ReporteData:
    
    #metodo para crear reporte en la base de datos
    def create_reporte(self, reporte: Reporte):
        #llama a la funcion conection para tener conexion a la base datos
        conexion, resultado = conection() 
        # verifica si la conexion falló
        if not resultado["success"]:
            return resultado
        
        try:
            #se crea el cursor para ejecutar las consultas SQL
            cursor = conexion.cursor()
            query = f"""INSERT INTO {TBREPORTE}(
            {TBREPORTE_ID_EMPLEADO},
            {TBREPORTE_FECHA_GENERACION},
            {TBREPORTE_TIPO_REPORTE},
            {TBREPORTE_CONTENIDO})
            VALUES (%s, %s, %s, %s)"""
            
            #define la consulta SQL pasando los objetos del reporte
            cursor.execute(query,(
                reporte.id_empleado,
                reporte.fecha_generacion,
                reporte.tipo_reporte,
                reporte.contenido
            ))
            #confirma los cambios en la base de datos
            conexion.commit()
            #actualiza el resultado indicando que la operacion fue exitosa
            resultado["success"] = True
            resultado["message"] = "Reporte creado exitosamente"
            #captura cualquier excepcion que ocurra duante la consulta
        except Exception as e :
            resultado["success"] = False
            #guarda el mensaje de error
            resultado["message"] = f"Erorr al crear reporte:  {e}"
            #cierra la conexion si esta abierta
        finally:
            if conexion:
                conexion.close()
        return resultado 
    
    #metodo para actualizar el reporte
    def update_reporte(self, reporte: Reporte):
        #llama a la funcion conection para tener conexion a la base datos
        conexion, resultado = conection()
        # verifica si la conexion falló
        if not resultado["success"]:
            return resultado
        
        try:
            #se crea el cursor para ejecutar las consultas SQL
            cursor = conexion.cursor()
            
            #consulta SQL para actualizar un reporte en la tabla TBREPORTE
            query = f"""UPDATE {TBREPORTE} SET
            {TBREPORTE_ID_EMPLEADO} = %s,
            {TBREPORTE_FECHA_GENERACION} = %s,
            {TBREPORTE_TIPO_REPORTE} = %s,
            {TBREPORTE_CONTENIDO} = %s
            WHERE {TBREPORTE_ID} = %s"""
            
            #define la consulta SQL pasando los valores actualizados del  objetos reporte
            cursor.execute(query, (
                reporte.id_empleado,
                reporte.fecha_generacion,
                reporte.tipo_reporte,
                reporte.contenido,
                reporte.id
            ))
            #confirma los cambios en la base de datos
            conexion.commit()
            #indica que la operacion fue exitosa
            resultado["success"] = True
            resultado["message"] = "Reporte actualizado exitosamente."
            #captura cualquier excepcion que ocurra duante la consulta
        except Exception as e:
            resultado["success"] = False
            #guarda el mensaje de error
            resultado["message"] = f"Error al actualizar reporte: {e}"
        #cierra la conexion si esta abierta    
        finally:
            if conexion:
                conexion.close()
        return resultado
    
    #metodo de eliminar un reporte
    def delete_reporte(self, id):
        #llama a la funcion conection para tener conexion a la base datos
        conexion, resultado = conection()
        # verifica si la conexion falló
        if not resultado["success"]:
            return resultado
        
        try:
            #se crea el cursor para ejecutar las consultas SQL
            cursor = conexion.cursor()
            #define la consulta SQL, pasando el ID del reporte a eliminar
            query = f"DELETE FROM {TBREPORTE} WHERE {TBREPORTE_ID} = %s"
            # Ejecuta la consulta SQL pasando el ID del reporte a eliminar
            cursor.execute(query, (id,))
            # Confirma los cambios en la base de datos
            conexion.commit()
            # Indica que la eliminacion fue exitosa
            resultado["success"] = True
            resultado["message"] = "Reporte eliminado exitosamente."
        # Captura cualquier excepcion que ocurra durante la eliminacion
        except Exception as e:
            resultado["success"] = False
            #gaurda el mensaje de error
            resultado["message"] = f"Error al eliminar reporte: {e}"
        #cierra la conexion si esta abierta
        finally:
            if conexion:
                conexion.close()
        return resultado