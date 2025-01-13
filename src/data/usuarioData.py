from models.usuario import Usuario
from data.data import conection
from settings.config import *
from settings.logger import logger
import bcrypt

class UsuarioData:
    
    def create_usuario(self, usuario: Usuario, conexionEx = None):
        #manejando la conexion exterior
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
                    conexion.commit() #confirma la inserccion solo si no se recive conexion externa

                return{'success':True, 'message':'Usuario creado exitosamente', 'id_usuario':id_usuario}
        except Exception as e:
            logger.error(f'{e}')
            return {'success':False, 'message':'Ocurrio un error al crear el usuario'}
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
                query = f"""UPDATE {TBUSUARIO} SET 
                {TBUSUARIO_USUARIO} = %s,
                {TBUSUARIO_CONTRASENA} = %s
                WHERE {TBUSUARIO_ID} = %s"""
            
                cursor.execute(query, (
                    usuario.usuario,
                    usuario.contrasena,
                    usuario.id
                ))
                if conexionEx is None:
                    conexion.commit()
                return {'success':True, 'message':'Usuario actualizado exitosamente'}
        except Exception as e:
            logger.error(f'{e}')
            return {'success':False,'message':'Ocurrio un error al actualizar el usuario.'}
        finally:
            if conexion and conexionEx is None:
                conexion.close()
       
    def delete_usuario(self, usuario_id):
        conexion, resultado = conection()
        if not resultado["success"]:
            return resultado
        
        try:
            cursor = conexion.cursor()
            query = f"DELETE FROM {TBUSUARIO} WHERE {TBUSUARIO_ID} = %s "
            
            cursor.execute(query, (usuario_id,))
            conexion.commit()
            
            resultado["success"] = True
            resultado["message"] = "Usuario eliminado exitosamente"
        except Exception as e:
            resultado["success"] = False
            resultado["message"] = f"Error al eliminar usuario: {e}"
        finally:
            if conexion:
                conexion.close()
        return resultado

    def list_usuarios(self, pagina=1, tam_pagina=10, ordenar_por = TBUSUARIO_ID, tipo_orden="ASC", busqueda = None):
        conexion, resultado = conection()
        cursor = None
        if not resultado["success"]:
            return resultado
        
        listaUsuarios = []
        try:
            cursor = conexion.cursor(dictionary=True)  
            columna_orden = { 
                "usuario":TBUSUARIO_USUARIO, 
                "id_persona":TBUSUARIO_ID_PERSONA, 
            }
            ordenar_por = columna_orden[ordenar_por] if ordenar_por in columna_orden else TBUSUARIO_ID
                
            if tipo_orden != "ASC":
                tipo_orden = "DESC"
                
            query = f"SELECT * FROM {TBUSUARIO} "
            
            valores = []
            if busqueda:
                query += f"""
                    WHERE {TBUSUARIO_USUARIO} LIKE %s 
                    OR {TBUSUARIO_CONTRASENA} LIKE %s
                """
                valores = [f"%{busqueda}%"] * 5 
            
            query += f" ORDER BY {ordenar_por} {tipo_orden} LIMIT %s OFFSET %s"
            valores.extend([tam_pagina, (pagina - 1) * tam_pagina])

            cursor.execute(query, valores)
            
            registros = cursor.fetchall()
            for registro in registros:
                usuario = Usuario(
                    registro[TBUSUARIO_USUARIO],
                    registro[TBUSUARIO_CONTRASENA],
                    registro[TBUSUARIO_ID],
                    registro[TBUSUARIO_ID_PERSONA],
                )
                listaUsuarios.append(usuario)
                
            cursor.execute(f"SELECT COUNT(*) as total FROM {TBUSUARIO}")
            total_registros = cursor.fetchone()["total"]
            total_paginas = (total_registros + tam_pagina - 1) // tam_pagina  

            resultado["data"] = {
                "listaUsuarios": listaUsuarios,
                "pagina_actual": pagina,
                "tam_pagina": tam_pagina,
                "total_paginas": total_paginas,
                "total_registros": total_registros
            }
            resultado["success"] = True
            resultado["message"] = "Usuarios listados exitosamente."
        except Exception as e:
            resultado["success"] = False
            resultado["message"] = f"Error al listar usuarios: {e}"
        finally:
            if cursor:
                cursor.close()
            if conexion:
                conexion.close()
        return resultado

    def get_usuario_by_correo_o_usuario(self, identificador):
        conexion, resultado = conection()
        cursor = None
        if not resultado["success"]:
            return resultado
        try:
            cursor = conexion.cursor();
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
            cursor.execute(query,[identificador,identificador])# ingresa los parametros
            usuarioPass = cursor.fetchone()#obtiene la unica contraseña
            
            if usuarioPass:
                usuario = Usuario(usuario=usuarioPass[0],id_persona=usuarioPass[2])
                resultado = {"success":True,"password":usuarioPass[1], "usuario":usuario}
            else:
                resultado = {"success":True,"message":"Usuario o contraseña incorrecta"}
        except Exception as e:
            resultado["success"] = False
            resultado["message"] = f"Error al buscar usuario y contraseñas: {e}"
        finally:
            if conexion:
                conexion.close()
        return resultado
           
    def verificar_usuario_contrasena(self, identificador, contrasena):
        try:
            # Buscar el usuario por correo o nombre de usuario
            usuario = self.get_usuario_by_correo_o_usuario(identificador)
            # Verifica si el usuario existe
            if usuario["success"]:
                # Comparar la contraseña encriptada
                if "password" in usuario:
                    if bcrypt.checkpw(contrasena.encode('utf-8'), usuario["password"].encode('utf-8')):
                        return {"success": True, "login":True, "message": "Inicio de sesión exitoso","usuario":usuario["usuario"]}
                    else:
                        return {"success":True, "login":False,"message":"Usuario o contraseña incorrecta"}
                else:
                    return {"success":True, "login":False,"message":"Usuario o contraseña incorrecta"}
            else:
                raise ValueError(usuario["message"])
        except Exception as e:
            return {"success":False,"message":f"Error al verificar usuario y contrasena {e}"}

            
