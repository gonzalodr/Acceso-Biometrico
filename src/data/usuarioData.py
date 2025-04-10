from mysql.connector import Error
from models.usuario import Usuario
from data.data import conection
from settings.config import *
from settings.logger import logger
from settings.tablas import TBUSUARIOPERFIL,TBUSUARIOPERFIL_ID_USER
import bcrypt

class UsuarioData:
    def verificar_usuario(self,usuario:str,id_usuario:int= None):
        
        conexion, resultado = conection()
        if not resultado["success"]:
            return True  
        
        try:
            cursor = conexion.cursor()
            
            # Consulta para verificar la existencia de la cédula
            query = f"SELECT COUNT(*) FROM {TBUSUARIO} WHERE {TBUSUARIO_USUARIO} = %s"
            
            # Agregamos una cláusula para ignorar el ID proporcionado
            if id_usuario is not None and id_usuario > 0:
                query += f" AND {TBUSUARIO_ID} != %s"
                cursor.execute(query, (usuario, id_usuario))
            else:
                cursor.execute(query, (usuario,))
            
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


    def create_usuario(self, usuario: Usuario, conexionEx = None):
        #manejando la conexión exterior
        if conexionEx is None:
            conexion, resultado = conection()
            if not resultado["success"]:
                return resultado
        else:
            conexion = conexionEx
        
        try:
            with conexion.cursor() as cursor:
                query = f"""INSERT INTO {TBUSUARIO}(
                {TBUSUARIO_ID_PERSONA},
                {TBUSUARIO_USUARIO},
                {TBUSUARIO_CONTRASENA}
                )VALUES (%s, %s, %s)"""
                
                cursor.execute(query, (
                    usuario.id_persona,
                    usuario.usuario,
                    usuario.contrasena
                    ))
                
                id_usuario = cursor.lastrowid

                if conexionEx is None:
                    conexion.commit() #confirma la inserción solo si no se recibe conexión externa

                return{'success':True, 'message':'Usuario creado exitosamente', 'id_usuario':id_usuario}
        except Exception as e:
            logger.error(f'{e}')
            return {'success':False, 'message':'Ocurrió un error al crear el usuario'}
        finally:
            if conexion and conexionEx is None:
                conexion.close()
            
    def update_usuario(self, usuario: Usuario, conexionEx = None):
        if conexionEx is None:
            conexion, resultado = conection()
            if not resultado["success"]:
                return resultado
        else:
            conexion = conexionEx
        
        try:
            with conexion.cursor() as cursor:
                # Construir la consulta SQL dinámicamente
                if usuario.contrasena is None:
                    query = f"""UPDATE {TBUSUARIO} SET 
                    {TBUSUARIO_USUARIO} = %s
                    WHERE {TBUSUARIO_ID} = %s"""
                    params = (usuario.usuario, usuario.id)
                else:
                    query = f"""UPDATE {TBUSUARIO} SET 
                    {TBUSUARIO_USUARIO} = %s,
                    {TBUSUARIO_CONTRASENA} = %s
                    WHERE {TBUSUARIO_ID} = %s"""
                    params = (usuario.usuario, usuario.contrasena, usuario.id)
                
                cursor.execute(query, params)
                
                if conexionEx is None:
                    conexion.commit()
                
                return {'success': True, 'message': 'Usuario actualizado exitosamente'}
        
        except Exception as e:
            logger.error(f'{e}')
            return {'success': False, 'message': 'Ocurrió un error al actualizar el usuario.'}
        
        finally:
            if conexion and conexionEx is None:
                conexion.close()
       
    def delete_usuario(self, usuario_id:int, conexionEx = None):
        if conexionEx is None:
            conexion, resultado = conection()
            if not resultado["success"]:
                return resultado
        else:
            conexion = conexionEx
        try:
            with conexion.cursor() as cursor:
                cursor.execute(f"DELETE FROM {TBUSUARIOPERFIL} WHERE {TBUSUARIOPERFIL_ID_USER} = %s",(usuario_id,))
                cursor.execute(f"DELETE FROM {TBUSUARIO} WHERE {TBUSUARIO_ID} = %s ", (usuario_id,))
                
                if conexionEx is None:
                    conexion.commit()

                return {'success':True, 'message':'Usuario eliminado exitosamente.'}
        except Error as e:
            if conexionEx is None:
                conexion.rollback()

            logger.error(f'{e}')
            return {'success':False, 'message':'Ocurrió un error al eliminar el usuario.'}
        finally:
            if conexion and conexionEx is None:
                conexion.close()

    def list_usuarios(self, pagina=1, tam_pagina=10, ordenar_por="id_usuario", tipo_orden="ASC", busqueda=None):
        conexion, resultado = conection()
        cursor = None
        if not resultado["success"]:
            return resultado

        listaUsuarios = []
        try:
            with conexion.cursor(dictionary=True) as cursor:
                # Validación de la columna de ordenamiento
                columna_orden = {
                    "usuario": TBUSUARIO_USUARIO,
                    "id_persona": TBUSUARIO_ID_PERSONA,
                    "nombre": TBPERSONA_NOMBRE  # Permitir ordenar por nombre
                }
                ordenar_por = columna_orden.get(ordenar_por, TBUSUARIO_ID)

                # Asigna el tipo de orden ascendente o descendente
                tipo_orden = "DESC" if tipo_orden != "ASC" else "ASC"

                # Construcción de la consulta base con INNER JOIN para obtener el nombre de la persona
                query = f"""
                    SELECT U.{TBUSUARIO_ID}, U.{TBUSUARIO_USUARIO}, U.{TBUSUARIO_CONTRASENA}, 
                        U.{TBUSUARIO_ID_PERSONA}, P.{TBPERSONA_NOMBRE} AS nombre_persona, 
                        P.{TBPERSONA_APELLIDOS} AS apellido_persona
                    FROM {TBUSUARIO} U
                    INNER JOIN {TBPERSONA} P ON U.{TBUSUARIO_ID_PERSONA} = P.{TBPERSONA_ID}
                """

                # Añadir cláusula de búsqueda si se proporciona
                valores = []
                if busqueda:
                    query += f"""
                        WHERE U.{TBUSUARIO_USUARIO} LIKE %s 
                        OR P.{TBPERSONA_NOMBRE} LIKE %s
                        OR P.{TBPERSONA_APELLIDOS} LIKE %s
                    """
                    valores = [f"%{busqueda}%", f"%{busqueda}%", f"%{busqueda}%"]

                # Añadir la cláusula ORDER BY y LIMIT/OFFSET
                query += f" ORDER BY {ordenar_por} {tipo_orden} LIMIT %s OFFSET %s"
                valores.extend([tam_pagina, (pagina - 1) * tam_pagina])

                # Ejecutar la consulta con los parámetros de forma segura
                cursor.execute(query, valores)

                # Leer los registros
                registros = cursor.fetchall()
                for registro in registros:
                    usuario = {
                        "id_usuario": registro[TBUSUARIO_ID],
                        "usuario": registro[TBUSUARIO_USUARIO],
                        "contrasena": registro[TBUSUARIO_CONTRASENA],
                        "id_persona": registro[TBUSUARIO_ID_PERSONA],
                        "nombre_completo": f"{registro['nombre_persona']} {registro['apellido_persona']}"  # Unir nombre y apellido
                    }
                    listaUsuarios.append(usuario)

                # Obtener el total de registros para calcular el número total de páginas
                cursor.execute(f"SELECT COUNT(*) as total FROM {TBUSUARIO}")
                total_registros = cursor.fetchone()["total"]
                total_paginas = (total_registros + tam_pagina - 1) // tam_pagina  # Redondear hacia arriba

                resultado["data"] = {
                    "listaUsuarios": listaUsuarios,
                    "pagina_actual": pagina,
                    "tam_pagina": tam_pagina,
                    "total_paginas": total_paginas,
                    "total_registros": total_registros
                }
                resultado["success"] = True
                resultado["message"] = "Usuarios listados exitosamente."
                return resultado
        except Exception as e:
            resultado["success"] = False
            resultado["message"] = f"Error al listar usuarios: {e}"
        finally:
            if conexion:
                conexion.close()
        
        return resultado

   
    def get_usuario_by_id(self, persona_id:int, conexionEx = None):
        conexion, resultado = conection() if conexionEx is None else (conexionEx, {"success": True})
        if not resultado["success"]:
            return resultado
        try:
            with conexion.cursor(dictionary=True) as cursor:
                query = f"""SELECT
                                {TBUSUARIO_ID},
                                {TBUSUARIO_ID_PERSONA},
                                {TBUSUARIO_USUARIO}
                            FROM {TBUSUARIO} WHERE {TBUSUARIO_ID_PERSONA} = %s"""
                cursor.execute(query, (persona_id,))
                data = cursor.fetchone()
                if data:
                    usuario = Usuario(
                        usuario = data[TBUSUARIO_USUARIO],
                        id      = data[TBUSUARIO_ID],
                        id_persona = data[TBUSUARIO_ID_PERSONA]
                    )
                    return {"success":True,"exists":True, "message":"Usuario obtenido exitosamente", "usuario":usuario}
                else:
                    return {"success":True,"exists":False,"message":"Usuario no encontrado"}
        except Error as error:
            logger.error(f'{error}')
            return {'success':False, 'message':'Ocurrió un error al obtener el usuario.'}
        finally:
            if conexion and conexionEx is None:
                conexion.close()
   
    def get_usuario_by_correo_o_usuario(self, identificador):
        conexion, resultado = conection()
        if not resultado["success"]:
            return resultado
        try:
            with conexion.cursor() as cursor:
                query = f"""
                        SELECT 
                            U.{TBUSUARIO_USUARIO},
                            U.{TBUSUARIO_CONTRASENA},
                            P.{TBPERSONA_ID}
                        FROM {TBUSUARIO} U
                        INNER JOIN {TBPERSONA} P ON P.{TBPERSONA_ID} =  U.{TBUSUARIO_ID_PERSONA}
                        WHERE
                            P.{TBPERSONA_CORREO} = %s OR U.{TBUSUARIO_USUARIO} = %s 
                        """
                cursor.execute(query,[identificador,identificador])# ingresa los parámetros
                usuarioPass = cursor.fetchone()#obtiene la única contraseña
                
                if usuarioPass:
                    usuario = Usuario(usuario=usuarioPass[0],id_persona=usuarioPass[2])
                    return {"success":True,"password":usuarioPass[1], "usuario":usuario}
                else:
                    return {"success":True,"message":"Usuario o contraseña incorrecta"}
        except Exception as e:
            logger.error(f'{e}')
            return {'success':False, 'message': 'Ocurrió un error de verificación'}
        finally:
            if conexion:
                conexion.close()
      
    def verificar_usuario_contrasena(self, identificador, contrasena):
        try:
            # Buscar el usuario por correo o nombre de usuario
            result = self.get_usuario_by_correo_o_usuario(identificador)
            # Verifica si el usuario existe
            if result["success"]:
                # Comparar la contraseña encriptada
                if "password" in result:
                    if bcrypt.checkpw(contrasena.encode('utf-8'), result["password"].encode('utf-8')):
                        return {"success": True, "login":True, "message": "Inicio de sesión exitoso","usuario":result["usuario"]}
                    else:
                        return {"success":True, "login":False,"message":"Usuario o contraseña incorrecta"}
                else:
                    return {"success":True, "login":False,"message":"Usuario o contraseña incorrecta"}
            else:
                return result
        except Exception as e:
            logger.error(f'{e}')
            return {"success":False,"message":f"Error al verificar usuario y contrasena."}

            
