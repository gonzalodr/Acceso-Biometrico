from models.usuario import Usuario
from data.data import conection
from settings.config import *
import bcrypt

class UsuarioData:
    
    def create_usuario(self, usuario: Usuario):
        conexion, resultado = conection()
        if not resultado["success"]:
            return resultado
        
        try:
            cursor = conexion.cursor()
            query = f"""INSERT INTO {TBUSUARIO}(
            {TBUSUARIO_ID_PERSONA},
            {TBUSUARIO_USUARIO},
            {TBUSUARIO_CONTRASENA})
            VALUES (%s, %s, %s)"""
            
            cursor.execute(query, (
            usuario.id_persona,
            usuario.usuario,
            usuario.contrasena
            ))
            conexion.commit()
            resultado["success"] = True
            resultado["message"] = "Usuario creado exitosamente"
        except Exception as e:
            resultado["success"] = False
            resultado["message"] = f"Error al crear usuario: {e}"
        finally:
            if conexion:
                conexion.close()
        return resultado
            
    def update_usuario(self, usuario: Usuario):
        conexion, resultado = conection()
        cursor = None
        if not resultado["success"]:
            return resultado
        try:
            cursor = conexion.cursor()
            query = f"""UPDATE {TBUSUARIO} SET 
            {TBUSUARIO_USUARIO} = %s,
            {TBUSUARIO_CONTRASENA} = %s
            WHERE {TBUSUARIO_ID} = %s"""
        
            cursor.execute(query, (
                usuario.usuario,
                usuario.contrasena,
                usuario.id
            ))
            conexion.commit()
            resultado["success"] = True
            resultado["message"] = "Usuario actualizado exitosamente."
        except Exception as e:
            resultado["success"] = False
            resultado["message"] = f"Error al actualizar usuario: {e}"
        finally:
            if cursor:
                cursor.close()
            if conexion:
                conexion.close()
        return resultado
       
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
        try:
            # Busca el usuario tanto por correo como por nombre de usuario
            usuario = db_session.query(Usuario).filter(
                (Usuario.correo == identificador) | (Usuario.usuario == identificador)
            ).first()
            return usuario if usuario else None
        except Exception as e:
            print(f"Error al buscar el usuario: {e}")
            return None
    
    def verificar_usuario_contrasena(self, identificador, contrasena):
        try:
            # Buscar el usuario por correo o nombre de usuario
            usuario = self.get_usuario_by_correo_o_usuario(identificador)
            # Verifica si el usuario existe
            if usuario:
                # Comparar la contraseña encriptada
                if bcrypt.checkpw(contrasena.encode('utf-8'), usuario.contrasena.encode('utf-8')):
                    return {"success": True, "usuario": usuario, "message": "Inicio de sesión exitoso"}
        except Exception as e:
            print(f"Error en la base de datos: {e}")
            return {"success": False, "message": f"Error: {str(e)}"}
