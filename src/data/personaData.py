
from models.persona import Persona
from data.data import conection  # Importa la función para obtener la conexión
from settings.config import * 
from settings.logger import logger

class PersonaData:
    
    def cedula_exists(self, cedula: str, persona_id: int = None) -> bool:
        """Verifica si la cédula ya existe en la base de datos."""
        conexion, resultado = conection()  # Asegúrate de tener una función de conexión adecuada
        if not resultado["success"]:
            return True  # Retorna True si la conexión falla para evitar continuar
        
        try:
            cursor = conexion.cursor()
            
            # Consulta para verificar la existencia de la cédula
            query = f"SELECT COUNT(*) FROM {TBPERSONA} WHERE {TBPERSONA_CEDULA} = %s"
            
            # Agregamos una cláusula para ignorar el ID proporcionado
            if persona_id is not None and persona_id > 0:
                query += f" AND id != %s"
                cursor.execute(query, (cedula, persona_id))
            else:
                cursor.execute(query, (cedula,))
            
            count = cursor.fetchone()[0]
            return count > 0  # Retorna True si hay al menos una cédula encontrada
        except Exception as e:
            print(f"Error al verificar la cédula: {e}")
            return True  # Retorna True en caso de error para evitar duplicados
        finally:
            if cursor:
                cursor.close()
            if conexion:
                conexion.close()
    
    
    def email_exists(self, email: str, persona_id: int = None) -> bool:
        """Verifica si el correo electrónico ya existe en la base de datos."""
        conexion, resultado = conection()  # Asegúrate de tener una función de conexión adecuada
        if not resultado["success"]:
            return True  # Retorna True si la conexión falla para evitar continuar
        
        try:
            cursor = conexion.cursor()
            # Consulta para verificar la existencia del correo
            query = f"SELECT COUNT(*) FROM {TBPERSONA} WHERE {TBPERSONA_CORREO} = %s"
            # Agregamos una cláusula para ignorar el ID proporcionado
            if persona_id is not None and persona_id > 0:
                query += f" AND id != %s"
                cursor.execute(query, (email, persona_id))
            else:
                cursor.execute(query, (email,))
            
            count = cursor.fetchone()[0]
            return count > 0  # Retorna True si hay al menos un correo encontrado
        except Exception as e:
            print(f"Error al verificar el correo: {e}")
            return True  # Retorna True en caso de error para evitar duplicados
        finally:
            if cursor:
                cursor.close()
            if conexion:
                conexion.close()
    ##
    # Se guarda un objeto persona
    # ##
    def create_persona(self, persona: Persona, conexionEx = None):
        conexion, resultado = conection() if conexionEx is None else (conexionEx, {"success": True})
        if not resultado["success"]:
            return resultado
        
        try:
            with conexion.cursor() as cursor:
                query = f"""INSERT INTO {TBPERSONA} (
                    {TBPERSONA_FOTO} , 
                    {TBPERSONA_NOMBRE} ,  
                    {TBPERSONA_APELLIDOS} ,
                    {TBPERSONA_NACIMIENTO} ,
                    {TBPERSONA_CEDULA} ,
                    {TBPERSONA_ESTADO_CIVIL} ,
                    {TBPERSONA_CORREO} , 
                    {TBPERSONA_DIRECCION}) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
        
                cursor.execute(query, (
                    persona.foto,
                    persona.nombre,
                    persona.apellidos,
                    persona.fecha_nacimiento,
                    persona.cedula,
                    persona.estado_civil,
                    persona.correo,
                    persona.direccion
                ))

                id_persona = cursor.lastrowid

                if conexionEx is None:
                    conexion.commit()

                return {'success':True, 'message': 'Persona guardada exitosamente', 'id_persona':id_persona}
        except Exception as e:
            logger.error(f'{e}')
            return{'success':False, 'message':'Ocurrió un error al registrar a la persona'}
        finally:
            if conexion and conexionEx is None:
                conexion.close()

    ##
    # Se guarda los cambios
    # ##
    def update_persona(self, persona:Persona, conexionEx = None):
        conexion, resultado = conection() if conexionEx is None else (conexionEx, {"success": True})
        if not resultado["success"]:
            return resultado

        try:
            with conexion.cursor() as cursor:
                query = f"""UPDATE {TBPERSONA} SET 
                {TBPERSONA_FOTO} = %s,
                {TBPERSONA_NOMBRE} = %s,
                {TBPERSONA_APELLIDOS} = %s,
                {TBPERSONA_NACIMIENTO} = %s,
                {TBPERSONA_CEDULA} = %s,
                {TBPERSONA_ESTADO_CIVIL} = %s,
                {TBPERSONA_CORREO} = %s,
                {TBPERSONA_DIRECCION} = %s
                WHERE {TBPERSONA_ID} = %s"""
                
                cursor.execute(query, (
                    persona.foto,
                    persona.nombre,
                    persona.apellidos,
                    persona.fecha_nacimiento,
                    persona.cedula,
                    persona.estado_civil,
                    persona.correo,
                    persona.direccion,
                    persona.id
                ))
                if conexionEx is None:
                    conexion.commit()
                return {'success':True, 'message':'Persona actualizada exitosamente'}
        except Exception as e:
            logger.error(f'{e}')
            return {'success':False, 'message':'Ocurrió un error al actualizar la persona'}
        finally:
            if conexion and conexionEx is None:
                conexion.close()

    ##
    # Se elimina la persona
    # ##
    def delete_persona(self, persona_id, conexionEx = None):
        conexion, resultado = conection() if conexionEx is None else (conexionEx, {"success": True})
        if not resultado["success"]:
            return resultado
        
        try:
            with conexion.cursor() as cursor:
                query = f"DELETE FROM {TBPERSONA} WHERE {TBPERSONA_ID} = %s "
                cursor.execute(query, (persona_id,))

                if conexionEx is None:
                    conexion.commit()

                return {'success':True, 'message':'Persona eliminada exitosamente'}
        except Exception as e:
            logger.error(f'{e}')
            return {'success':False,'message':'Ocurrió un error al eliminar esta persona'}
        finally:
            if conexion and conexionEx is None:
                conexion.close()
    
    ##
    # Se lista las personas
    # tipo de orden ASC o DESC
    # ##
    def list_personas(self, pagina=1, tam_pagina=10, ordenar_por = TBPERSONA_ID, tipo_orden="ASC", busqueda = None):
        conexion, resultado = conection()
        cursor = None
        if not resultado["success"]:
            return resultado
        
        listaPersonas = []
        try:
            cursor = conexion.cursor(dictionary=True)  
            #validacion de por que columna ordenar
            columna_orden = { 
                "cedula":TBPERSONA_CEDULA, 
                "fechaNacimiento":TBPERSONA_NACIMIENTO, 
                "apellido":TBPERSONA_APELLIDOS, 
                "nombre":TBPERSONA_NOMBRE
            }
            ## asigna sobre que tabla realizar el orden
            ordenar_por = columna_orden[ordenar_por] if ordenar_por in columna_orden else TBPERSONA_ID
                
            ## asigna el tipo de orden ascendente o descendente
            if tipo_orden != "ASC":
                tipo_orden = "DESC"
                
            # Construcción de la consulta base
            query = f"SELECT * FROM {TBPERSONA} "
            
            # Añadir cláusula de búsqueda si se proporciona
            valores = []
            if busqueda:
                query += f"""
                    WHERE {TBPERSONA_NOMBRE} LIKE %s 
                    OR {TBPERSONA_APELLIDOS} LIKE %s
                    OR {TBPERSONA_CEDULA} LIKE %s 
                    OR {TBPERSONA_CORREO} LIKE %s
                """
                valores = [f"%{busqueda}%"] * 5  # Para usar el valor de búsqueda con LIKE en todas las columnas
            
            # Añadir la cláusula ORDER BY y LIMIT/OFFSET
            query += f" ORDER BY {ordenar_por} {tipo_orden} LIMIT %s OFFSET %s"
            valores.extend([tam_pagina, (pagina - 1) * tam_pagina])

            cursor.execute(query, valores)
            
            #Leyendo los registros de 
            registros = cursor.fetchall()
            for registro in registros:
                persona = Persona(
                    registro[TBPERSONA_NOMBRE],
                    registro[TBPERSONA_APELLIDOS],
                    registro[TBPERSONA_NACIMIENTO],
                    registro[TBPERSONA_CEDULA],
                    registro[TBPERSONA_ESTADO_CIVIL],
                    registro[TBPERSONA_CORREO],
                    registro[TBPERSONA_DIRECCION],
                    registro[TBPERSONA_ID],
                    registro[TBPERSONA_FOTO]
                )
                listaPersonas.append(persona)
                
            # Obtener el total de registros para calcular el número total de páginas
            cursor.execute(f"SELECT COUNT(*) as total FROM {TBPERSONA}")
            total_registros = cursor.fetchone()["total"]
            total_paginas = (total_registros + tam_pagina - 1) // tam_pagina  # Redondear hacia arriba

            resultado["data"] = {
                "listaPersonas": listaPersonas,
                "pagina_actual": pagina,
                "tam_pagina": tam_pagina,
                "total_paginas": total_paginas,
                "total_registros": total_registros
            }
            resultado["success"] = True
            resultado["message"] = "Personas listadas exitosamente."
        except Exception as e:
            resultado["success"] = False
            resultado["message"] = f"Error al listar personas: {e}"
        finally:
            if cursor:
                cursor.close()
            if conexion:
                conexion.close()
        return resultado
   
    ##
    # Obtiene el objeto por persona
    # ##
    def get_persona_by_id(self, persona_id:int,conexionEx = None):
        conexion, resultado = conection() if conexionEx is None else (conexionEx, {"success": True})
        if not resultado["success"]:
            return resultado
        try:
            with conexion.cursor() as cursor:
                query = f"""SELECT
                                {TBPERSONA_FOTO}, 
                                {TBPERSONA_NOMBRE}, 
                                {TBPERSONA_APELLIDOS}, 
                                {TBPERSONA_NACIMIENTO}, 
                                {TBPERSONA_CEDULA}, 
                                {TBPERSONA_ESTADO_CIVIL}, 
                                {TBPERSONA_CORREO}, 
                                {TBPERSONA_DIRECCION},
                                {TBPERSONA_ID} 
                            FROM {TBPERSONA} 
                            WHERE id = %s"""
                
                cursor.execute(query, (persona_id,))
                data = cursor.fetchone()
                
                if data:
                    persona = Persona(
                        foto            = data[0],
                        nombre          = data[1],
                        apellidos       = data[2],
                        fecha_nacimiento= data[3],
                        cedula          = data[4],
                        estado_civil    = data[5],
                        correo          = data[6],
                        direccion       = data[7],
                        id              = data[8]
                    )
                    return {'success':True,'exists':True, 'message':'Se encontro a la persona.','persona':persona}
                else:
                    return {'success':True,'exists':False, 'message':'No se encontro a la persona.'}
        except Exception as e:
            logger.error(f'{e}')
            return {'success':False, 'message':'Ocurrio un error al buscar la persona'}
        finally:
            if conexion and conexionEx is None:
                conexion.close()

