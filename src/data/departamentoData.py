from models.departamento import Departamento
from data.data import conection
from settings.config import *

class DepartamentoData:
    
    def create_departamento(self, departamento: Departamento):
        conexion, resultado = conection()
        if not resultado["success"]:
            return resultado
        
        try:
            cursor = conexion.cursor()
            query = f"""INSERT INTO {TBDEPARTAMENTO}(
            {TBDEPARTAMENTO_NOMBRE},
            {TBDEPARTAMENTO_DESCRIPCION})
            VALUES (%s, %s)"""
            
            cursor.execute(query, (
            departamento.nombre,
            departamento.descripcion
            ))
            conexion.commit()
            resultado["success"] = True
            resultado["success"] = "Departamento creado exitosamente"
        except Exception as e:
            resultado["success"] = False
            resultado["success"] = f"Error al crear departamento: {e}"
        finally:
            if conexion:
                conexion.close()
                return resultado
            
    def update_departamento(self, departamento: Departamento):
        conexion, resultado = conection()
        cursor = None
        if not resultado["success"]:
            return resultado
        try:
            cursor = conexion.cursor()
            query = f"""UPDATE {TBDEPARTAMENTO} SET 
            {TBDEPARTAMENTO_NOMBRE} = %s,
            {TBDEPARTAMENTO_DESCRIPCION} = %s
            WHERE {TBDEPARTAMENTO_ID} = %s"""
        
            cursor.execute(query, (
                departamento.nombre,
                departamento.descripcion,
                departamento.id
            ))
            conexion.commit()
            resultado["success"] = True
            resultado["message"] = "Departamento actualizado exitosamente."
        except Exception as e:
            resultado["success"] = False
            resultado["message"] = f"Error al actualizar departamento: {e}"
        finally:
            if cursor:
                cursor.close()
            if conexion:
                conexion.close()
        return resultado
       
    def delete_departamento(self, departamento_id):
        conexion, resultado = conection()
        if not resultado["success"]:
            return resultado
        
        try:
            cursor = conexion.cursor()
            query = f"DELETE FROM {TBDEPARTAMENTO} WHERE {TBDEPARTAMENTO_ID} = %s "
            
            cursor.execute(query, (departamento_id,))
            conexion.commit()
            
            resultado["success"] = True
            resultado["message"] = "Departamento eliminado exitosamente"
        except Exception as e:
            resultado["success"] = False
            resultado["message"] = f"Error al eliminar departamento: {e}"
        finally:
            if conexion:
                conexion.close()
        return resultado
              
    def list_departamentos(self, pagina=1, tam_pagina=10, ordenar_por = TBDEPARTAMENTO_ID, tipo_orden="ASC", busqueda = None):
        conexion, resultado = conection()
        cursor = None
        if not resultado["success"]:
            return resultado
        
        listaDepartamentos = []
        try:
            cursor = conexion.cursor(dictionary=True)  
            #validacion de por que columna ordenar
            columna_orden = { 
                "nombre":TBDEPARTAMENTO_NOMBRE, 
                "descripcion":TBDEPARTAMENTO_DESCRIPCION, 
            }
            ## asigna sobre que tabla realizar el orden
            ordenar_por = columna_orden[ordenar_por] if ordenar_por in columna_orden else TBDEPARTAMENTO_ID
                
            ## asigna el tipo de orden ascendente o descendente
            if tipo_orden != "ASC":
                tipo_orden = "DESC"
                
            # Construcción de la consulta base
            query = f"SELECT * FROM {TBDEPARTAMENTO} "
            
            # Añadir cláusula de búsqueda si se proporciona
            valores = []
            if busqueda:
                query += f"""
                    WHERE {TBDEPARTAMENTO_NOMBRE} LIKE %s 
                    OR {TBDEPARTAMENTO_DESCRIPCION} LIKE %s
                """
                valores = [f"%{busqueda}%"] * 5  # Para usar el valor de búsqueda con LIKE en todas las columnas
            
            # Añadir la cláusula ORDER BY y LIMIT/OFFSET
            query += f" ORDER BY {ordenar_por} {tipo_orden} LIMIT %s OFFSET %s"
            valores.extend([tam_pagina, (pagina - 1) * tam_pagina])

            # Ejecutar la consulta con los parámetros de forma segura
            cursor.execute(query, valores)
            
            #Leyendo los registros de 
            registros = cursor.fetchall()
            for registro in registros:
                departamento = Departamento(
                    registro[TBDEPARTAMENTO_NOMBRE],
                    registro[TBDEPARTAMENTO_DESCRIPCION],
                    registro[TBDEPARTAMENTO_ID],
                )
                listaDepartamentos.append(departamento)
                
            # Obtener el total de registros para calcular el número total de páginas
            cursor.execute(f"SELECT COUNT(*) as total FROM {TBDEPARTAMENTO}")
            total_registros = cursor.fetchone()["total"]
            total_paginas = (total_registros + tam_pagina - 1) // tam_pagina  # Redondear hacia arriba

            resultado["data"] = {
                "listaDepartamentos": listaDepartamentos,
                "pagina_actual": pagina,
                "tam_pagina": tam_pagina,
                "total_paginas": total_paginas,
                "total_registros": total_registros
            }
            resultado["success"] = True
            resultado["message"] = "Departamentos listadas exitosamente."
        except Exception as e:
            resultado["success"] = False
            resultado["message"] = f"Error al listar departamentos: {e}"
        finally:
            if cursor:
                cursor.close()
            if conexion:
                conexion.close()
        return resultado