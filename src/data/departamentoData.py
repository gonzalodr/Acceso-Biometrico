from mysql.connector import Error 

from models.departamento import Departamento
from data.data import conection
from settings.config import *
from settings.logger import logger

class DepartamentoData:
    
    def create_departamento(self, departamento: Departamento):
        conexion, resultado = conection()
        if not resultado["success"]:
            return resultado
        
        try:
            with conexion.cursor() as cursor:
                
                # Primero verificamos si el departamento ya existe
                check_query = f"""SELECT COUNT(*) FROM {TBDEPARTAMENTO} 
                                 WHERE {TBDEPARTAMENTO_NOMBRE} = %s"""
                cursor.execute(check_query, (departamento.nombre,))
                count = cursor.fetchone()[0]
            
                if count > 0:
                    return {'success': False, 'message': 'El departamento ya existe y no puede ser creado nuevamente.'}
                
                insert_query = f"""INSERT INTO {TBDEPARTAMENTO}(
                                {TBDEPARTAMENTO_NOMBRE},
                                {TBDEPARTAMENTO_DESCRIPCION})
                                VALUES (%s, %s)"""
                
                cursor.execute(insert_query, (
                    departamento.nombre,
                    departamento.descripcion
                ))
                conexion.commit()
                return {'success':True, 'message':'El departamento se guardo correctamente.'}
        except Error as e:
            logger.error(f'Error: {e}')
            return {'success':False, 'message':'Ocurrió un error al guardar el departamento.'}
        finally:
            if conexion:
                conexion.close()
            
    def update_departamento(self, departamento: Departamento):
        conexion, resultado = conection()
        cursor = None
        if not resultado["success"]:
            return resultado
        try:
            with conexion.cursor() as cursor:
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
                return{'success':True, 'message':'Departamento actualizado exitosamente.'}
        except Error as e:
            logger.error(f'Erro: {e}')
            return {'success':False, 'message': 'Ocurrió un error al actualizar el departamento.'}
        finally:
            if conexion:
                conexion.close()
       
    def delete_departamento(self, departamento_id):
        conexion, resultado = conection()
        if not resultado["success"]:
            return resultado
        
        try:
            with conexion.cursor() as cursor:
                query = f"DELETE FROM {TBDEPARTAMENTO} WHERE {TBDEPARTAMENTO_ID} = %s "
                cursor.execute(query, (departamento_id,))
                conexion.commit()
                return {'success':True, 'message':'El departamento se elimino correctamente.'}
        except Error as e:
            return {'success':False, 'message':'Ocurrió un error al eliminar el departamento.'}
        finally:
            if conexion:
                conexion.close()
              
    def list_departamentos(self, pagina=1, tam_pagina=10, ordenar_por = TBDEPARTAMENTO_ID, tipo_orden="ASC", busqueda = None):
        conexion, resultado = conection()
        cursor = None
        if not resultado["success"]:
            return resultado
        
        listaDepartamentos = []
        try:
            with conexion.cursor(dictionary=True) as cursor:  
                #validacion de por que columna ordenar
                columna_orden = { 
                    "nombre":TBDEPARTAMENTO_NOMBRE, 
                    "descripción":TBDEPARTAMENTO_DESCRIPCION, 
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
                    valores = [f"%{busqueda}%", f"%{busqueda}%"]  # Para usar el valor de búsqueda con LIKE en todas las columnas
                
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
                return resultado
        except Error as e:
            logger.error(f'Error: {e}')
            return {'success':False, 'message':'Ocurrió un error al cargar la lista de departamentos.'}
        finally:
            if conexion:
                conexion.close()
    
    def get_departamento_by_id(self, departamento_id):
        conexion, resultado = conection()
        if not resultado["success"]:
            return resultado
        
        try:
            with conexion.cursor() as cursor:
                query = f"""SELECT
                                {TBDEPARTAMENTO_NOMBRE}, 
                                {TBDEPARTAMENTO_DESCRIPCION}, 
                                {TBDEPARTAMENTO_ID} 
                            FROM {TBDEPARTAMENTO} 
                            WHERE id = %s"""
                
                cursor.execute(query, (departamento_id,))
                data = cursor.fetchone()
                
                if data:
                    departamento = Departamento(   
                        nombre=data[0],
                        descripcion=data[1],
                        id=data[2]
                    )
                    return {'success':True, 'exists':False, 'departamento':departamento}
                else:
                    return {'success':True, 'exists':False, 'message':'No se encontró el departamento.'}
        except Error as e:
            logger.error(f'{e}')
            return {'success':False,'message':'Ocurrió un error al obtener el departamento'}
        finally:
            if conexion:
                conexion.close()

    def obtener_todo_departamentos(self):
        conexion, resultado = conection()
        if not resultado["success"]:
            return resultado
        try:
            with conexion.cursor(dictionary=True) as cursor:
                query=f"SELECT * FROM {TBDEPARTAMENTO}"
                cursor.execute(query)
                data = cursor.fetchall()
                listaDepa = []
                for depa in data:
                    departamento = Departamento(depa[TBDEPARTAMENTO_NOMBRE], depa[TBDEPARTAMENTO_DESCRIPCION],depa[TBDEPARTAMENTO_ID])
                    listaDepa.append(departamento)

                return {'success':True, 'listaDepa':listaDepa,'message':'Se obtuvieron todos los departamentos registrados.'}
        except Error as e:
            logger.error(f'{e}')
            return{'success':False,'message':'Ocurrio un error al listar todos los departamentos.'}
        finally:
            if conexion:
                conexion.close()

                    