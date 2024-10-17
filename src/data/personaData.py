
from models.persona import Persona
from data.data import conection  # Importa la función para obtener la conexión
from settings.config import * 


class PersonaData:
    ##
    # Se guarda un objeto persona
    # ##
    def create_persona(self, persona: Persona):
        conexion, resultado = conection()
        if not resultado["success"]:
            return resultado
        
        try:
            cursor = conexion.cursor()
            query = f"""INSERT INTO {TBPERSONA} (
                {TBPERSONA_FOTO} , 
                {TBPERSONA_NOMBRE} ,  
                {TBPERSONA_APELLIDO1} ,
                {TBPERSONA_APELLIDO2} ,
                {TBPERSONA_NACIMIENTO} ,
                {TBPERSONA_CEDULA} ,
                {TBPERSONA_ESTADO_CIVIL} ,
                {TBPERSONA_CORREO} , 
                {TBPERSONA_DIRECCION}) 
                VALUES (%s, %s, %s, %s, %s,%s, %s, %s, %s)"""
            
            cursor.execute(query, (
                persona.foto,
                persona.nombre,
                persona.apellido1,
                persona.apellido2,
                persona.fecha_nacimiento,
                persona.cedula,
                persona.estado_civil,
                persona.correo,
                persona.direccion
            ))
            
            conexion.commit()
            resultado["success"] = True
            resultado["message"] = "Persona creada exitosamente."
        except Exception as e:
            resultado["success"] = False
            resultado["message"] = f"Error al crear persona: {e}"
        finally:
            if conexion:
                conexion.close()
        return resultado

    ##
    # Se guarda los cambios
    # ##
    def update_persona(self, persona:Persona):
        conexion, resultado = conection()
        cursor = None
        if not resultado["success"]:
            return resultado
        try:
            cursor = conexion.cursor()
            query = f"""UPDATE {TBPERSONA} SET 
            {TBPERSONA_FOTO} = %s,
            {TBPERSONA_NOMBRE} = %s,
            {TBPERSONA_APELLIDO1} = %s,
            {TBPERSONA_APELLIDO2} = %s,
            {TBPERSONA_NACIMIENTO} = %s,
            {TBPERSONA_CEDULA} = %s,
            {TBPERSONA_ESTADO_CIVIL} = %s,
            {TBPERSONA_CORREO} = %s,
            {TBPERSONA_DIRECCION} = %s
             WHERE {TBPERSONA_ID} = %s"""
            
            cursor.execute(query, (
                persona.foto,
                persona.nombre,
                persona.apellido1,
                persona.apellido2,
                persona.fecha_nacimiento,
                persona.cedula,
                persona.estado_civil,
                persona.correo,
                persona.direccion,
                persona.id
            ))
            conexion.commit()
            resultado["success"] = True
            resultado["message"] = "Persona actualizada exitosamente."
        except Exception as e:
            resultado["success"] = False
            resultado["message"] = f"Error al actualizar persona: {e}"
        finally:
            if cursor:
                cursor.close()
            if conexion:
                conexion.close()
        return resultado

    ##
    # Se elimina la persona
    # ##
    def delete_persona(self, persona_id):
        conexion, resultado = conection()
        cursor = None
        if not resultado["success"]:
            return resultado
        try:
            cursor = conexion.cursor()
            query = f"DELETE FROM {TBPERSONA} WHERE {TBPERSONA_ID} = %s "
            
            cursor.execute(query, (persona_id,))
            conexion.commit()
            
            resultado["success"] = True
            resultado["message"] = "Persona eliminada exitosamente."
        except Exception as e:
            resultado["success"] = False
            resultado["message"] = f"Error al eliminar persona: {e}"
        finally:
            if cursor:
                cursor.close()
            if conexion:
                conexion.close()

        return resultado
    
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
                "apellido":TBPERSONA_APELLIDO1, 
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
                    OR {TBPERSONA_APELLIDO1} LIKE %s
                    OR {TBPERSONA_APELLIDO2} LIKE %s 
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
                    registro[TBPERSONA_APELLIDO1],
                    registro[TBPERSONA_APELLIDO2],
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
   
# sql
# SELECT * 
# FROM persona 
# WHERE columna1 LIKE '%tu_texto_a_buscar%' 
#    OR columna2 LIKE '%tu_texto_a_buscar%' 
#    OR columna3 LIKE '%tu_texto_a_buscar%';
