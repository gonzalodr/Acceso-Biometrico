from data.data import conection     #obtener la conexión
from settings.tablas import *       #obtener los nombres de tablas
from settings.logger import logger  #recolectar los errores 
from mysql.connector import Error

#importando clases
from typing import Dict, Any        #clase diccionario
from models.persona import Persona  #clase persona
from models.usuario import Usuario  #clase usuario
from models.telefono import Telefono#clase teléfono
from models.empleado import Empleado

#importando la clases data de usuarioData, personaData, usuarioPerfilData y empleadoRolData
from data.personaData import PersonaData
from data.usuarioData import UsuarioData
from data.telefonoData import TelefonoData
from data.empleado_RolData import EmpleadoRolData
from data.departamentoData import DepartamentoData
from data.usuario_PerfilData import UsuarioPerfilData
from data.rolData import RolData



class EmpleadoData:
    def __init__(self):
        self.personadata = PersonaData()
        self.usuariodata = UsuarioData()
        self.emplRolData = EmpleadoRolData()
        self.userPerfilData = UsuarioPerfilData()
        self.telefonoData = TelefonoData()
        self.depaData   = DepartamentoData()
        self.rolData    = RolData()

    '''
    Registra los datos del empleado, persona, creación de usuarios, asignación de rol y de departamento
    '''
    def create_Empleado(self, datos: Dict[str, Any])->Dict[str,Any]:
        conexion, resultado = conection()
        if not resultado["success"]:
            return resultado
        try:
            #obteniendo persona, telefonos, usuarios
            persona:Persona = datos.get('persona')
            listaTel:list   = datos.get('listaTelefonos')
            usuario:Usuario = datos.get('usuario')
          
            #recibiendo perfil, departamento, rol
            id_dep:int = datos.get('id_departamento')
            id_rol:int = datos.get('id_rol')
            id_per:int = datos.get('id_perfil')
            
            #iniciando transaccion
            conexion.start_transaction()

            #registrando la persona
            result = self.personadata.create_persona(persona,conexion)
            if not result['success']:
                conexion.rollback()
                return result
            id_persona = result['id_persona'] #obtenemos el id
            
            #registrando el o los teléfonos
            if listaTel:
                for telefono in listaTel:
                    telefono.id_persona = id_persona
                    print(telefono)
                    result = self.telefonoData.create_telefono(telefono,conexion)
                    print(result)
                    if not result['success']:
                        conexion.rollback()
                        return result

            #registrando empleado, (Asociacion de tb persona, tb departamento en tb empleado)
            #departamento es opcional
            result = self.registrar_empleado(id_persona,id_dep,conexion)
            if not result['success']:
                conexion.rollback()
                return result
            id_empleado = result['id_empleado']

            #registrando rol empleado opcional
            if id_rol:
                result = self.emplRolData.create_rol_empleado(id_empleado, id_rol, conexion)
                if not result['success']:
                    conexion.rollback()
                    return result
            
            #ingresando el usuario y su perfil
            if usuario:
                usuario.id_persona = id_persona
                result = self.usuariodata.create_usuario(usuario,conexion)
                if not result['success']:
                    conexion.rollback()
                    return result
                id_usuario = result['id_usuario']
                
                #registrando el perfil
                if id_per:
                    result = self.userPerfilData.create_usuario_perfil(id_usuario,id_per,conexion)
                    if not result['success']:
                        conexion.rollback()
                        return result

            #confirmando los registros
            conexion.commit()
            return {'success':True, 'message':'Se registro el empleado correctamente.'}
        except Exception as e:
            conexion.rollback()
            logger.error(f'{e}') 
            return {'success':False, 'message':f'Ocurrió un error al registrar el empleado'}
        finally:
            if conexion:
                conexion.close()
    '''
    Creando registro empleado_persona
    '''
    def registrar_empleado(self, id_persona:int, id_departamento:int, conexionEx = None)->Dict[str,Any]:
        conexion, resultado = conection() if conexionEx is None else (conexionEx, {"success": True})
        if not resultado["success"]:
            return resultado
        
        try:
            with conexion.cursor() as cursor:
                queryEmpleado = f'''INSERT INTO {TBEMPLEADO} (
                    {TBEMPLEADO_PERSONA},
                    {TBEMPLEADO_DEPARTAMENTO}
                    )VALUES(%s, %s)
                '''
                cursor.execute(queryEmpleado,(id_persona, id_departamento))
                
                id_empleado = cursor.lastrowid
                if conexionEx is None:
                    conexion.commit()

                return {'success':True, 'message':'Empleado registrado exitosamente','id_empleado':id_empleado}
        except Exception as e:
            logger.error(f'{e}')
            return {'success':False, 'message':'Ocurrió un error al registrar al empleado'}
        finally:
            if conexion and conexionEx is None:
                conexion.close()
    
    '''
    Actualizacion de los datos del empleado, persona, creación de usuarios, asignación de rol y de departamento
    '''
    def update_Empleado(self,id_empledo:int,datos:Dict[str,Any]):
        conexion, resultado = conection()
        if not resultado["success"]:
            return resultado
        try:
            persona:Persona = datos.get('persona')
            listaTel        = datos.get('listaTelefonos')
            usuario:Usuario = datos.get('usuario')

            id_dep:int = datos.get('id_departamento')
            id_rol:int = datos.get('id_rol')            #obtener por empleado    
            id_per:int = datos.get('id_perfil')         #obtener por por usuario para la relacion usuario perfil

            conexion.start_transaction()
            with conexion.cursor() as cursor:
                #actualizar empleado (persona, departamento)
                queryEmpleado = f'''UPDATE {TBEMPLEADO} SET
                    {TBEMPLEADO_DEPARTAMENTO} = %s
                    WHERE {TBEMPLEADO_ID} = %s
                '''
                cursor.execute(queryEmpleado,(id_dep,id_empledo))
                #actualizar persona Objeto Persona
                result = self.personadata.update_persona(persona,conexion)
                if not result['success']:
                    conexion.rollback()
                    return result

                #actualizar telefonos o crear telefonos Objeto Telefono
                if listaTel:
                    for telefono in listaTel:
                        telefono.id_persona = persona.id
                        print(telefono)
                        if telefono.id: #actualiza
                            result = self.telefonoData.update_telefono(telefono,conexion)
                            if not result['success']:
                                conexion.rollback()
                                return result
                        else:           #crea
                            result = self.telefonoData.create_telefono(telefono,conexion)
                            if not result['success']:
                                conexion.rollback()
                                return result
                            
                #actualizar rolEmpleado id_rol id_empleado si existe rolEmpleado crear rolEmpleado
                #buscando rolEmpleado

                result = self.emplRolData.get_roles_empleado_by_id_empleado(id_empledo,conexion)
                if not result['success']:
                    conexion.rollback()
                    return result
                
                #comprobando si existe rolEmpleado y si id_rol es None eliminar rolEmpleado
                #Explicacion sin en frond paso de de algun rol a ningun rol se elimina el rolEmpleado
                if result['exists'] and id_rol is None:
                    #eliminar rolEmpleado
                    resultAux = self.emplRolData.delete_rol_empleado(result['rolesEmpleado']['id'],conexion)
                    if not resultAux['success']:
                        conexion.rollback()
                        return resultAux     
                             
                #si existe rolEmpleado y id_rol no es None se procede a actualizar
                elif result['exists'] and id_rol:
                    #actualizar rolEmpleado
                    resultAux = self.emplRolData.update_rol_empleado(result['rolesEmpleado']['id'],id_empledo,id_rol,conexion)
                    if not resultAux['success']:
                        conexion.rollback()
                        return resultAux
                #si no existe rolEmpleado y id_rol no es None se procede a crear
                elif result['exists'] is False and id_rol:
                    #crear rolEmpleado
                    resultAux = self.emplRolData.create_rol_empleado(id_empledo,id_rol,conexion)
                    if not resultAux['success']:
                        conexion.rollback()
                        return resultAux

                #actualizar usuario o crear usuario Objeto Usuario
                if usuario:
                    usuario.id_persona = persona.id
                    if usuario.id:  #si el usuario tiene id actualiza
                        result = self.usuariodata.update_usuario(usuario,conexion)
                        if not result['success']: 
                            conexion.rollback()
                            return result
                        
                        result = self.userPerfilData.get_usuario_perfil_by_id_usurio(usuario.id,conexion)
                        if not result['success']:
                            conexion.rollback()
                            return result
                        if result['exists'] and id_per:
                            #actualizar id_perfil en la tabla usuarioPerfil
                            result = self.userPerfilData.update_usuario_perfil(result['usuarioPerfil']['id'],usuario.id,id_per,conexion)
                            if not result['success']:
                                conexion.rollback()
                                return result
                        elif result['exists'] and id_per is None:
                            result = self.userPerfilData.delete_usuario_perfil(result['usuarioPerfil']['id'])
                            if not result['success']:
                                conexion.rollback()
                                return result
                        elif result['exists'] is False and id_per:
                            result = self.userPerfilData.create_usuario_perfil(usuario.id,id_per, conexion)
                            if not result['success']:
                                conexion.rollback()
                                return result
                        
                    else:          #si el usuario no tiene id lo crea crea
                        result = self.usuariodata.create_usuario(usuario,conexion)
                        if not result['success']:
                            conexion.rollback()
                            return result
                        id_usuario = result['id_usuario']
                        #registrando el perfil
                        if id_per:
                            result = self.userPerfilData.create_usuario_perfil(id_usuario,id_per,conexion)
                            if not result['success']:
                                conexion.rollback()
                                return result
                        
                #confirmar los cambios
                conexion.commit()
                return {'success':True, 'message':'Se actualizo el empleado correctamente.'}
        except Error as e:
            logger.error(f"{e}")
            conexion.rollback()
            return {"success": False, "message": "Ocurrió un error al actualizar el empleado."}
        finally:
            if conexion:
                conexion.close()

    '''
    Eliminación de los datos del empleado, persona, creación de usuarios, asignación de rol y de departamento
    '''  
    def delete_Empleado(self, id_empleado:int):
        conexion, resultado = conection()
        if not resultado["success"]:
            return resultado
        try:
            with conexion.cursor() as cursor:
                conexion.start_transaction() #Iniciar transaccion

                # Obtener el Id_Persona del empleado
                cursor.execute("SELECT Id_Persona FROM Empleado WHERE Id = %s;", (id_empleado,))
                resultado = cursor.fetchone()
                if not resultado:
                    logger.error('No se encontro los datos personales del empleado.')
                    return {'success':False,'message':'Ocurrio un error al eliminar el empleado.'}
                id_persona = resultado[0]  # Obtener el valor de Id_Persona

                # Obtener el Id_Usuario relacionado con la persona
                cursor.execute("SELECT Id FROM Usuario WHERE Id_Persona = %s;", (id_persona,))
                resultado = cursor.fetchone()

                id_usuario = None
                if resultado:
                    id_usuario = resultado[0]  # Obtener el valor de Id_Usuario si existe

                # Si existe un usuario, eliminar registros dependientes
                if id_usuario:
                    # Eliminar registros en Mantenimiento
                    cursor.execute("DELETE FROM Mantenimiento WHERE Id_usuario = %s;", (id_usuario,))

                    # Eliminar registros en Usuario_Perfil
                    cursor.execute("DELETE FROM Usuario_Perfil WHERE Id_Usuario = %s;", (id_usuario,))

                    # Eliminar registros en Usuario
                    cursor.execute("DELETE FROM Usuario WHERE Id = %s;", (id_usuario,))

                # Eliminar registros en Telefono
                cursor.execute("DELETE FROM Telefono WHERE Id_Persona = %s;", (id_persona,))

                # Eliminar registros en Huella
                cursor.execute("DELETE FROM Huella WHERE Id_Empleado = %s;", (id_empleado,))

                # Eliminar registros en Justificacion
                cursor.execute("DELETE FROM Justificacion WHERE Id_Empleado = %s;", (id_empleado,))

                # Eliminar registros en Solicitud_Permiso
                cursor.execute("DELETE FROM Solicitud_Permiso WHERE Id_Empleado = %s;", (id_empleado,))

                # Eliminar registros en Reporte
                cursor.execute("DELETE FROM Reporte WHERE Id_Empleado = %s;", (id_empleado,))

                # Eliminar registros en Detalle_Asistencia
                cursor.execute("""
                    DELETE FROM Detalle_Asistencia 
                    WHERE Id_Asistencia IN (
                        SELECT Id FROM Asistencia WHERE Id_Empleado = %s
                    );
                """, (id_empleado,))

                # Eliminar registros en Asistencia
                cursor.execute("DELETE FROM Asistencia WHERE Id_Empleado = %s;", (id_empleado,))

                # Eliminar registros en Empleado_Rol
                cursor.execute("DELETE FROM Empleado_Rol WHERE Id_Empleado = %s;", (id_empleado,))

                # Eliminar registros en Empleado
                cursor.execute("DELETE FROM Empleado WHERE Id = %s;", (id_empleado,))

                # Eliminar registros en Persona
                cursor.execute("DELETE FROM Persona WHERE Id = %s;", (id_persona,))

                # Confirmar la transacción
                conexion.commit()
                return {'success':True,'message':'Se elimino el empleado correctamente.'}
        except Error as e:
            logger.error(f"{e}")
            return {"success": False, "message": "Ocurrió un error al eliminar al empleado."}
        finally:
            if conexion:
                conexion.close()
    '''
    Listado de los datos del empleado, los datos personales
    '''
    def list_Empleados(self, pagina=1, tam_pagina=10, ordenar_por=TBPERSONA_ID, tipo_orden="ASC", busqueda=None):
        conexion, resultado = conection()
        if not resultado["success"]:
            return resultado

        listaPersonas = []
        try:
            with conexion.cursor(dictionary=True) as cursor:
                # Mapeo de columnas para ordenar
                columnas_validas = {
                    "cedula": TBPERSONA_CEDULA,
                    "fechaNacimiento": TBPERSONA_NACIMIENTO,
                    "apellido": TBPERSONA_APELLIDOS,
                    "nombre": TBPERSONA_NOMBRE
                }
                
                # Validar columna de ordenamiento
                ordenar_por = columnas_validas.get(ordenar_por, TBPERSONA_ID)
                tipo_orden = "DESC" if tipo_orden.upper() != "ASC" else "ASC"

                # Construcción de la consulta base
                query_base = f"""
                    SELECT 
                        EMP.{TBEMPLEADO_ID} AS EMPLEADO_ID,
                        P.{TBPERSONA_ID} AS PERSONA_ID,
                        P.{TBPERSONA_NOMBRE}, 
                        P.{TBPERSONA_APELLIDOS}, 
                        P.{TBPERSONA_NACIMIENTO}, 
                        P.{TBPERSONA_CEDULA}, 
                        P.{TBPERSONA_ESTADO_CIVIL}, 
                        P.{TBPERSONA_CORREO}, 
                        P.{TBPERSONA_DIRECCION}
                    FROM {TBPERSONA} P
                    INNER JOIN {TBEMPLEADO} EMP ON EMP.{TBEMPLEADO_PERSONA} = P.{TBPERSONA_ID}
                """

                # Construcción de la condición de búsqueda
                valores = []
                condicion = ""
                if busqueda:
                    condicion = " WHERE (P.{0} LIKE %s OR P.{1} LIKE %s OR P.{2} LIKE %s OR P.{3} LIKE %s)".format(
                        TBPERSONA_NOMBRE, TBPERSONA_APELLIDOS, TBPERSONA_CEDULA, TBPERSONA_CORREO
                    )
                    valores.extend([f"%{busqueda}%"] * 4)

                # Obtener el total de registros que cumplen la condición
                query_count = f"""
                    SELECT COUNT(*) as total FROM {TBPERSONA} P
                    INNER JOIN {TBEMPLEADO} EMP ON EMP.{TBEMPLEADO_PERSONA} = P.{TBPERSONA_ID}
                    {condicion}
                """
                cursor.execute(query_count, valores)
                total_registros = cursor.fetchone()["total"]
                total_paginas = (total_registros + tam_pagina - 1) // tam_pagina

                # Agregar orden y paginación
                query_final = f"""
                    {query_base} {condicion} 
                    ORDER BY P.{ordenar_por} {tipo_orden} 
                    LIMIT %s OFFSET %s
                """
                valores.extend([tam_pagina, (pagina - 1) * tam_pagina])
                cursor.execute(query_final, valores)
                registros = cursor.fetchall()

                # Procesar resultados
                for data in registros:
                    persona:Persona = Persona(
                        nombre      = data[TBPERSONA_NOMBRE],
                        apellidos   = data[TBPERSONA_APELLIDOS],
                        cedula      = data[TBPERSONA_CEDULA],
                        fecha_nacimiento= data[TBPERSONA_NACIMIENTO],
                        estado_civil= data[TBPERSONA_ESTADO_CIVIL],
                        correo      = data[TBPERSONA_CORREO],
                        direccion   = data[TBPERSONA_DIRECCION],
                        id          = data['PERSONA_ID']
                    )
                    listaPersonas.append({ 'id_empleado': data['EMPLEADO_ID'],'persona': persona })

                return {
                    "data": {
                        "listaPersonas": listaPersonas,
                        "pagina_actual": pagina,
                        "tam_pagina": tam_pagina,
                        "total_paginas": total_paginas,
                        "total_registros": total_registros
                    },
                    "success": True,
                    "message": "Personas listadas exitosamente."
                }
        except Error as e:
            logger.error(f"Error al listar empleados: {e}")
            return {"success": False, "message": "Ocurrió un error al listar los empleados."}
        finally:
            if conexion:
                conexion.close()
    '''
    Obtener la información de un empleado por su ID
    Datos personales
    Usuario->perfil asignado
    Departamento
    Rol asignado
    '''
    def getEmpleadoById(self,id_empleado:int,conexionEx=None):
        conexion, resultado = conection() if conexionEx is None else (conexionEx, {"success": True})
        if not resultado["success"]:
            return resultado
        try:
            with conexion.cursor(dictionary=True) as cursor:
                query = f"""SELECT 
                                {TBEMPLEADO_ID},
                                {TBEMPLEADO_PERSONA},
                                {TBEMPLEADO_DEPARTAMENTO}
                            FROM {TBEMPLEADO}
                            WHERE {TBEMPLEADO_ID} = %s
                """
                cursor.execute(query, (id_empleado,))
                data = cursor.fetchone()
                if data:
                    #departamento
                    departamento = data[TBEMPLEADO_DEPARTAMENTO]
                    
                    #extraer la persona
                    result = self.personadata.get_persona_by_id(data[TBEMPLEADO_PERSONA],conexion)
                    if not result['success']:
                        return result
                    if not result['exists']:
                        return {'success':False, 'message':'No se obtuvieron los datos personales exitosamente'}
                    persona = result['persona']

                    #traer telefonos
                    result = self.telefonoData.get_Telefono_by_id_persona(persona.id,conexion)
                    if not result['success']:
                        return result
                    listaTelefonos = result.get('listaTelefonos')

                    #extraer el usuario si es que existe alguno
                    result = self.usuariodata.get_usuario_by_id(data[TBEMPLEADO_PERSONA],conexion)
                    if not result['success']:
                        return result
                    usuario = result.get('usuario')

                    #extraer relacion perfil usuario si existe usuario existe perfil asociado
                    perfilUsuario = None
                    if usuario:
                        result = self.userPerfilData.get_usuario_perfil_by_id_usurio(usuario.id,conexion)
                        if not result['success']:
                            return result

                        perfilUsuario = result.get('usuarioPerfil')


                    #extraer relacion rolEmpleado
                    result = self.emplRolData.get_roles_empleado_by_id_empleado(id_empleado,conexion)
                    if not result['success']:
                        return result
                    rolEmpleado =  result.get('rolesEmpleado')

                    
                    return {
                        'empleado':{
                            'persona':persona,
                            'usuario':usuario,
                            'pefilUsuario':perfilUsuario,
                            'rolEmpleado':rolEmpleado,
                            'departamento':departamento,
                            'listaTelefonos':listaTelefonos
                        },
                        'success':True,
                        'exists':True,
                        'message':'Se obtuvo los datos del empleado correctamente.'
                    }
                else:
                    return {'success':True,'exists':False, 'message':'No existe el empleado.'}
        except Error as e:
            logger.error(f'{e}')
            return {'success':False, 'message':'Ocurrio un problema al obtener el empleado.'}
        finally:
            if conexion and conexionEx is None:
                conexion.close()

    def getAll_info_empleado_by_id(self, id_empleado:int, conexionEx ):
        conexion, resultado = conection() if conexionEx is None else (conexionEx, {"success": True})
        if not resultado["success"]:
            return resultado
        try:
            with conexion.cursor(dictionary=True) as cursor:
                query =f'''
                        SELECT 
                            {TBEMPLEADO_ID},
                            {TBEMPLEADO_PERSONA},
                            {TBEMPLEADO_DEPARTAMENTO}
                        FROM {TBEMPLEADO} 
                        WHERE {TBEMPLEADO_ID} = %s
                        '''
                cursor.execute(query,(id_empleado,))
                data = cursor.fetchone()
                if data:
                    pass
                else:
                    return{'success':True, 'exists':False, 'message':'No se encontro el empleado.'}
        except Error as e:
            logger.error(f'{e}')
            return {'success':False,'message':'Ocurrio un problema al obtener la informacion del empleado.'}
        finally:
            if conexion and conexionEx:
                conexion.close()
                
                
    """   def obtener_todo_empleados(self):
        conexion, resultado = conection()
        if not resultado["success"]:
            return resultado
        
        listaEmpleados = []  # Lista donde se almacenarán los perfiles ob
        try:
            with conexion.cursor(dictionary=True) as cursor:
                query = f"SELECT * FROM {TBEMPLEADO}"
                cursor.execute(query)
                registros = cursor.fetchall()
                
                 # Se convierten los registros en objetos de tipo Perfil y se almacenan en la lista
                for registro in registros:
                    empleado = Empleado(
                        id_persona=registro[TBEMPLEADO_PERSONA],
                        id_departamento=registro[TBEMPLEADO_DEPARTAMENTO],
                        id=registro[TBEMPLEADO_ID]
                    )
                    listaEmpleados.append(empleado)
                
                resultado["data"] = {
                    "listaEmpleados": listaEmpleados,
                }
                resultado["success"] = True
                resultado["message"] = "Empleados listados exitosamente."
        except Exception as e:
            resultado["success"] = False
            resultado["message"] = f"Error al listar empleado: {e}"
        finally:
            if cursor:
                cursor.close()# Se cierra el cursor
            if conexion:
                conexion.close()# Se cierra la conexión a la base de datos

        return resultado
        
    
     """
     
    def obtener_todo_empleados(self):
        conexion, resultado = conection()
        if not resultado["success"]:
            return resultado
        
        """listaEmpleados = []  # Lista donde se almacenarán los perfiles ob
        try:
            with conexion.cursor(dictionary=True) as cursor:
                query = f"SELECT * FROM {TBEMPLEADO}"
                cursor.execute(query)
                registros = cursor.fetchall()
                """
                
        listaEmpleados = []  # Lista donde se almacenarán los empleados
        try:
            with conexion.cursor(dictionary=True) as cursor:
                query = f"""
                    SELECT 
                        e.{TBEMPLEADO_ID}, 
                        e.{TBEMPLEADO_PERSONA}, 
                        e.{TBEMPLEADO_DEPARTAMENTO}, 
                        p.{TBPERSONA_NOMBRE} AS nombre_persona  -- Obtener el nombre de la persona
                    FROM {TBEMPLEADO} e
                    INNER JOIN {TBPERSONA} p ON e.{TBEMPLEADO_PERSONA} = p.{TBPERSONA_ID}
                """
                cursor.execute(query)
                registros = cursor.fetchall()
            
                 # Se convierten los registros en objetos de tipo Perfil y se almacenan en la lista
                for registro in registros:
                    empleado = Empleado(
                        id_persona=registro[TBEMPLEADO_PERSONA],
                        id_departamento=registro[TBEMPLEADO_DEPARTAMENTO],
                        id=registro[TBEMPLEADO_ID],
                        nombre_persona=registro["nombre_persona"]
                    )
                    listaEmpleados.append(empleado)
                
                resultado["data"] = {
                    "listaEmpleados": listaEmpleados,
                }
                resultado["success"] = True
                resultado["message"] = "Empleados listados exitosamente."
        except Exception as e:
            resultado["success"] = False
            resultado["message"] = f"Error al listar empleado: {e}"
        finally:
            if cursor:
                cursor.close()# Se cierra el cursor
            if conexion:
                conexion.close()# Se cierra la conexión a la base de datos

        return resultado