from data.data import conection     #obtener la conexión
from settings.tablas import *       #obtener los nombres de tablas
from settings.logger import logger  #recolectar los errores 
from mysql.connector import Error

#importando clases
from typing import Dict, Any        #clase diccionario
from models.persona import Persona  #clase persona
from models.usuario import Usuario  #clase usuario
from models.telefono import Telefono#clase teléfono

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
                    result = self.telefonoData.create_telefono(telefono,conexion)
                    if not result['success']:
                        conexion.rollback()
                        return result

            #registrando empleado, (Asociacion de tb persona, tb departamento en tb empleado)
            result = self.registrar_empleado(id_persona,id_dep,conexion)
            if not result['success']:
                conexion.rollback()
                return result
            id_empleado = result['id_empleado']

            #registrando rol empleado
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
    def update_Empleado(self,datos:Dict[str,Any]):
        conexion, resultado = conection()
        if not resultado["success"]:
            return resultado
        try:
            persona:Persona = datos.get('persona')
            listaTel = datos.get('listaTelefonos')
            usuario:Usuario = datos.get('usuario')

            id_dep:int = datos.get('id_departamento') if datos.get('id_departamento') else None
            id_rol:int = datos.get('id_rol') if datos.get('id_rol') else None
            id_per:int = datos.get('id_perfil') if datos.get('id_perfil') else None #perfiles
             
            with conexion.cursor() as cursor:
                pass

        except Error as e:
            logger.error(f"{e}")
            return {"success": False, "message": "Ocurrió un error al actualizar el empleado."}
        finally:
            if conexion:
                conexion.close()

    '''
    Eliminación de los datos del empleado, persona, creación de usuarios, asignación de rol y de departamento
    '''  
    def delete_Empleado(self, id_empleado):
        conexion, resultado = conection()
        if not resultado["success"]:
            return resultado
        try:
            with conexion.cursor() as cursor:
                pass
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
                        return result
                    persona = result['persona']


                    #extraer el usuario si es que existe alguno
                    result = self.usuariodata.get_usuario_by_id(data[TBEMPLEADO_PERSONA],conexion)
                    if not result['success']:
                        return result
                    usuario = result.get('usuario')

                    #extraer relacion perfil usuario si existe usuario existe perfil asociado
                    perfilUsuario = None
                    if usuario:
                        result = self.userPerfilData.get_usuario_by_id_usurio(usuario.id,conexion)
                        if not result['success']:
                            return result
                        if not result['exists']:
                            return result
                        perfilUsuario = result['usuarioPerfil']


                    #extraer relacion rolEmpleado
                    result = self.emplRolData.get_rol_empleado_by_id(data[TBEMPLEADO_ID],conexion)
                    if not result['success']:
                        return result
                    rolEmpleado =  result.get('rolEmpleado')
                    
                    return {
                        'empleado':{
                            'persona':persona,
                            'usuario':usuario,
                            'pefilUsuario':perfilUsuario,
                            'rolEmpleado':rolEmpleado,
                            'departamento':departamento
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