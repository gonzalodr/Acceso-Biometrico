from mysql.connector        import Error
from models.usuario         import Usuario
from models.perfil          import Perfil
from models.permiso_perfil  import Permiso_Perfil
from data.data              import conection
from settings.config        import *
from settings.logger        import logger
from settings.config        import TBUSUARIOPERFIL, TBUSUARIOPERFIL_ID_USER
import bcrypt


class UsuarioData:
    def verificar_usuario(self, usuario: str, id_usuario: int = None):

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

    def create_usuario(self, usuario: Usuario, conexionEx=None):
        # manejando la conexión exterior
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

                cursor.execute(
                    query, (usuario.id_persona, usuario.usuario, usuario.contrasena)
                )

                id_usuario = cursor.lastrowid

                if conexionEx is None:
                    conexion.commit()  # confirma la inserción solo si no se recibe conexión externa

                return {
                    "success": True,
                    "message": "Usuario creado exitosamente",
                    "id_usuario": id_usuario,
                }
        except Exception as e:
            logger.error(f"{e}")
            return {"success": False, "message": "Ocurrió un error al crear el usuario"}
        finally:
            if conexion and conexionEx is None:
                conexion.close()

    def update_usuario(self, usuario: Usuario, conexionEx=None):
        print("Usuario en la base de datos: " + usuario.mostrar())
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
                                {TBUSUARIO_USUARIO} = %s,
                                {TBUSUARIO_ID_PERSONA} = %s
                                WHERE {TBUSUARIO_ID} = %s"""
                    params = (usuario.usuario, usuario.id_persona, usuario.id)
                else:
                    query = f"""UPDATE {TBUSUARIO} SET 
                                {TBUSUARIO_USUARIO} = %s,
                                {TBUSUARIO_ID_PERSONA} = %s,
                                {TBUSUARIO_CONTRASENA} = %s
                                WHERE {TBUSUARIO_ID} = %s"""
                    params = (
                        usuario.usuario,
                        usuario.id_persona,
                        usuario.contrasena,
                        usuario.id,
                    )

                cursor.execute(query, params)

                if conexionEx is None:
                    conexion.commit()

                return {"success": True, "message": "Usuario actualizado exitosamente"}

        except Exception as e:
            logger.error(f"{e}")
            return {
                "success": False,
                "message": "Ocurrió un error al actualizar el usuario.",
            }

        finally:
            if conexion and conexionEx is None:
                conexion.close()

    def delete_usuario(self, usuario_id: int, conexionEx=None):
        if conexionEx is None:
            conexion, resultado = conection()
            if not resultado["success"]:
                return resultado
        else:
            conexion = conexionEx
        try:
            with conexion.cursor() as cursor:
                cursor.execute(
                    f"DELETE FROM {TBUSUARIOPERFIL} WHERE {TBUSUARIOPERFIL_ID_USER} = %s",
                    (usuario_id,),
                )
                cursor.execute(
                    f"DELETE FROM {TBUSUARIO} WHERE {TBUSUARIO_ID} = %s ", (usuario_id,)
                )

                if conexionEx is None:
                    conexion.commit()

                return {"success": True, "message": "Usuario eliminado exitosamente."}
        except Error as e:
            if conexionEx is None:
                conexion.rollback()

            logger.error(f"{e}")
            return {
                "success": False,
                "message": "Ocurrió un error al eliminar el usuario.",
            }
        finally:
            if conexion and conexionEx is None:
                conexion.close()

    def list_usuarios(
        self,
        pagina=1,
        tam_pagina=10,
        ordenar_por="id_usuario",
        tipo_orden="ASC",
        busqueda=None,
    ):
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
                    "nombre": TBPERSONA_NOMBRE,  # Permitir ordenar por nombre
                }
                ordenar_por = columna_orden.get(ordenar_por, TBUSUARIO_ID_PERSONA)

                # Asigna el tipo de orden ascendente o descendente
                tipo_orden = "DESC" if tipo_orden != "ASC" else "ASC"

                # Construcción de la consulta base con INNER JOIN para obtener el nombre de la persona y el perfil
                query = f"""
                    SELECT 
                        U.id AS id_usuario, 
                        U.usuario, 
                        P.nombre AS nombre_persona, 
                        P.apellidos AS apellido_persona, 
                        UP.{TBUSUARIOPERFIL_ID} AS id_usuario_perfil,  -- ID de la tabla usuario_perfil
                        UP.{TBUSUARIOPERFIL_ID_PERF} AS id_perfil,  -- ID del perfil (llave foránea)
                        PF.nombre AS nombre_perfil 
                    FROM 
                        {TBUSUARIO} U 
                    INNER JOIN 
                        {TBPERSONA} P ON U.id_persona = P.id 
                    LEFT JOIN 
                        {TBUSUARIOPERFIL} UP ON U.id = UP.{TBUSUARIOPERFIL_ID_USER} 
                    LEFT JOIN 
                        {TBPERFIL} PF ON UP.{TBUSUARIOPERFIL_ID_PERF} = PF.id 
                """

                # Añadir cláusula de búsqueda si se proporciona
                valores = []
                if busqueda:
                    query += f"""
                        WHERE U.usuario LIKE %s 
                        OR CONCAT(P.nombre, ' ', P.apellidos) LIKE %s  
                        OR PF.nombre LIKE %s
                        OR (PF.nombre IS NULL AND LOWER(%s) = 'Sin perfil')  
                    """
                    valores = [
                        f"%{busqueda}%",
                        f"%{busqueda}%",
                        f"%{busqueda}%",
                        busqueda.lower(),
                    ]

                # Añadir la cláusula ORDER BY y LIMIT/OFFSET
                query += f" ORDER BY {ordenar_por} {tipo_orden} LIMIT %s OFFSET %s"
                valores.extend([tam_pagina, (pagina - 1) * tam_pagina])

                # Ejecutar la consulta con los parámetros de forma segura
                cursor.execute(query, valores)

                # Leer los registros
                registros = cursor.fetchall()
                for registro in registros:
                    usuario = {
                        "id_usuario": registro["id_usuario"],  # ID del usuario
                        "usuario": registro["usuario"],
                        "nombre_completo": f"{registro['nombre_persona']} {registro['apellido_persona']}",  # Unir nombre y apellido
                        "id_usuario_perfil": registro[
                            "id_usuario_perfil"
                        ],  # ID de la tabla usuario_perfil
                        "id_perfil": registro[
                            "id_perfil"
                        ],  # ID del perfil (llave foránea)
                        "nombre_perfil": (
                            registro["nombre_perfil"]
                            if registro["nombre_perfil"]
                            else "Sin perfil"
                        ),  # Manejo de caso sin perfil
                    }
                    listaUsuarios.append(usuario)

                # Obtener el total de registros para calcular el número total de páginas
                cursor.execute(f"SELECT COUNT(*) as total FROM {TBUSUARIO}")
                total_registros = cursor.fetchone()["total"]
                total_paginas = (
                    total_registros + tam_pagina - 1
                ) // tam_pagina  # Redondear hacia arriba

                resultado["data"] = {
                    "listaUsuarios": listaUsuarios,
                    "pagina_actual": pagina,
                    "tam_pagina": tam_pagina,
                    "total_paginas": total_paginas,
                    "total_registros": total_registros,
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

    def get_usuario_by_id(self, id_usuario: int, conexionEx=None):
        conexion, resultado = (
            conection() if conexionEx is None else (conexionEx, {"success": True})
        )
        if not resultado["success"]:
            return resultado
        try:
            with conexion.cursor(dictionary=True) as cursor:
                query = f"""
                    SELECT
                        U.{TBUSUARIO_ID},
                        U.{TBUSUARIO_ID_PERSONA},
                        U.{TBUSUARIO_USUARIO},
                        UP.{TBUSUARIOPERFIL_ID_PERF} AS id_perfil
                    FROM {TBUSUARIO} U
                    LEFT JOIN {TBUSUARIOPERFIL} UP ON U.{TBUSUARIO_ID} = UP.{TBUSUARIOPERFIL_ID_USER}
                    WHERE U.{TBUSUARIO_ID} = %s  -- Cambiar a buscar por id_usuario
                """
                cursor.execute(query, (id_usuario,))
                data = cursor.fetchone()
                if data:
                    usuario = Usuario(
                        usuario=data[TBUSUARIO_USUARIO],
                        id=data[TBUSUARIO_ID],
                        id_persona=data[TBUSUARIO_ID_PERSONA],
                    )
                    return {
                        "success": True,
                        "exists": True,
                        "message": "Usuario obtenido exitosamente",
                        "usuario": usuario,
                        "id_perfil": data[
                            "id_perfil"
                        ],  # Agregar el id_perfil a la respuesta
                    }
                else:
                    return {
                        "success": True,
                        "exists": False,
                        "message": "Usuario no encontrado",
                    }
        except Error as error:
            logger.error(f"{error}")
            return {
                "success": False,
                "message": "Ocurrió un error al obtener el usuario.",
            }
        finally:
            if conexion and conexionEx is None:
                conexion.close()

    def get_usuario_by_correo_o_usuario(self, identificador):
        conexion, resultado = conection()
        if not resultado["success"]:
            return resultado
        try:
            with conexion.cursor(dictionary=True) as cursor:
                query = f"""
                        SELECT 
                            U.{TBUSUARIO_ID} as usuario_id,
                            U.{TBUSUARIO_USUARIO},
                            U.{TBUSUARIO_CONTRASENA},
                            P.{TBPERSONA_ID}
                        FROM {TBUSUARIO} U
                        INNER JOIN {TBPERSONA} P ON P.{TBPERSONA_ID} =  U.{TBUSUARIO_ID_PERSONA}
                        WHERE
                            P.{TBPERSONA_CORREO} = %s OR U.{TBUSUARIO_USUARIO} = %s 
                        """
                cursor.execute(
                    query, [identificador, identificador]
                )  # ingresa los parámetros
                usuarioPass = cursor.fetchone()  # obtiene la única contraseña

                if usuarioPass:
                    usuario = Usuario(usuario=usuarioPass[TBUSUARIO_USUARIO], id_persona=usuarioPass[TBPERSONA_ID])
                    queryPerfil = f"""SELECT 
                    PF.{TBPERFIL_ID} as perfil_id,
                    PF.{TBPERFIL_NOMBRE},
                    PF.{TBPERFIL_DESCRIPCION},
                    PP.{TBPERMISOPERFIL_ID} as permisoperfil_id,
                    PP.{TBPERMISOPERFIL_PERFIL_ID},
                    PP.{TBPERMISOPERFIL_TABLA},
                    PP.{TBPERMISOPERFIL_VER},
                    PP.{TBPERMISOPERFIL_INSERTAR},
                    PP.{TBPERMISOPERFIL_EDITAR},
                    PP.{TBPERMISOPERFIL_ELIMINAR}
                    
                    FROM {TBPERFIL} PF
                    INNER JOIN {TBUSUARIOPERFIL} UP ON UP.{TBUSUARIOPERFIL_ID_PERF} = PF.{TBPERFIL_ID}
                    INNER JOIN {TBPERMISOPERFIL} PP ON PP.{TBPERMISOPERFIL_PERFIL_ID} = PF.{TBPERFIL_ID}
                    WHERE UP.{TBUSUARIOPERFIL_ID_USER} = %s
                    """
                    cursor.execute(queryPerfil,(usuarioPass["usuario_id"],))
                    usuarioPerfil = cursor.fetchall()

                    if usuarioPerfil:   
                        perfil = Perfil(
                            nombre      = usuarioPerfil[0][TBPERFIL_NOMBRE],
                            descripcion = usuarioPerfil[0][TBPERFIL_DESCRIPCION],
                            id          = usuarioPerfil[0]["perfil_id"]
                        )
                        listaPermisosPerfil=[]
                        for permiso in usuarioPerfil:
                            perm = Permiso_Perfil(
                                id          = permiso["permisoperfil_id"],
                                perfil_id   = permiso[TBPERMISOPERFIL_PERFIL_ID],
                                tabla       = permiso[TBPERMISOPERFIL_TABLA],
                                ver         = permiso[TBPERMISOPERFIL_VER],
                                crear       = permiso[TBPERMISOPERFIL_INSERTAR],
                                editar      = permiso[TBPERMISOPERFIL_EDITAR],
                                eliminar    = permiso[TBPERMISOPERFIL_ELIMINAR]
                            )
                            listaPermisosPerfil.append(perm)
                            
                        print(perfil)
                        print("------------------")
                        print(listaPermisosPerfil) 
                        
                    return {
                        "success": True,
                        "password": usuarioPass[TBUSUARIO_CONTRASENA],
                        "usuario": usuario,
                    }
                else:
                    return {
                        "success": True,
                        "message": "Usuario o contraseña incorrecta",
                    }
        except Exception as e:
            logger.error(f"{e}")
            return {"success": False, "message": "Ocurrió un error de verificación"}
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
                    if bcrypt.checkpw(
                        contrasena.encode("utf-8"), result["password"].encode("utf-8")
                    ):
                        return {
                            "success": True,
                            "login": True,
                            "message": "Inicio de sesión exitoso",
                            "usuario": result["usuario"],
                        }
                    else:
                        return {
                            "success": True,
                            "login": False,
                            "message": "Usuario o contraseña incorrecta",
                        }
                else:
                    return {
                        "success": True,
                        "login": False,
                        "message": "Usuario o contraseña incorrecta",
                    }
            else:
                return result
        except Exception as e:
            logger.error(f"{e}")
            return {
                "success": False,
                "message": f"Error al verificar usuario y contrasena.",
            }
