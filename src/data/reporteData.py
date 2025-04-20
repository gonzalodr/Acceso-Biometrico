from data.EmpleadoData  import Empleado
from settings.config    import *      

from data.data          import conection
from mysql.connector    import Error 
from settings.config    import *
from settings.logger    import logger
from datetime           import date,datetime

from models.reporte     import Reporte 
from models.asistencia  import Asistencia
from models.rol         import Rol
from models.departamento        import Departamento
from models.solicitud_permisos  import SolicitudPermiso
from models.justificacion       import Justificacion

import traceback
import sys




class ReporteData:
    
    #metodo para crear reporte en la base de datos
    def create_reporte(self, reporte: Reporte):
        #llama a la funcion conection para tener conexion a la base datos
        conexion, resultado = conection() 
        # verifica si la conexion falló
        if not resultado["success"]:
            return resultado
        
        try:
            #se crea el cursor para ejecutar las consultas SQL
            cursor = conexion.cursor()
            query = f"""INSERT INTO {TBREPORTE}(
            {TBREPORTE_ID_EMPLEADO},
            {TBREPORTE_FECHA_GENERACION},
            {TBREPORTE_TIPO_REPORTE},
            {TBREPORTE_CONTENIDO})
            VALUES (%s, %s, %s, %s)"""
            
            #define la consulta SQL pasando los objetos del reporte
            cursor.execute(query,(
                reporte.id_empleado,
                reporte.fecha_generacion,
                reporte.tipo_reporte,
                reporte.contenido
            ))
            #confirma los cambios en la base de datos
            conexion.commit()
            #actualiza el resultado indicando que la operacion fue exitosa
            resultado["success"] = True
            resultado["message"] = "Reporte creado exitosamente"
            #captura cualquier excepcion que ocurra duante la consulta
        except Exception as e :
            resultado["success"] = False
            #guarda el mensaje de error
            resultado["message"] = f"Erorr al crear reporte:  {e}"
            #cierra la conexion si esta abierta
        finally:
            if conexion:
                conexion.close()
        return resultado 
    
    #metodo para actualizar el reporte
    def update_reporte(self, reporte: Reporte):
        #llama a la funcion conection para tener conexion a la base datos
        conexion, resultado = conection()
        # verifica si la conexion falló
        if not resultado["success"]:
            return resultado
        
        try:
            #se crea el cursor para ejecutar las consultas SQL
            cursor = conexion.cursor()
            
            #consulta SQL para actualizar un reporte en la tabla TBREPORTE
            query = f"""UPDATE {TBREPORTE} SET
            {TBREPORTE_ID_EMPLEADO} = %s,
            {TBREPORTE_FECHA_GENERACION} = %s,
            {TBREPORTE_TIPO_REPORTE} = %s,
            {TBREPORTE_CONTENIDO} = %s
            WHERE {TBREPORTE_ID} = %s"""
            
            #define la consulta SQL pasando los valores actualizados del  objetos reporte
            cursor.execute(query, (
                reporte.id_empleado,
                reporte.fecha_generacion,
                reporte.tipo_reporte,
                reporte.contenido,
                reporte.id
            ))
            #confirma los cambios en la base de datos
            conexion.commit()
            #indica que la operacion fue exitosa
            resultado["success"] = True
            resultado["message"] = "Reporte actualizado exitosamente."
            #captura cualquier excepcion que ocurra duante la consulta
        except Exception as e:
            resultado["success"] = False
            #guarda el mensaje de error
            resultado["message"] = f"Error al actualizar reporte: {e}"
        #cierra la conexion si esta abierta    
        finally:
            if conexion:
                conexion.close()
        return resultado
    
    #metodo de eliminar un reporte
    def delete_reporte(self, id):
        #llama a la funcion conection para tener conexion a la base datos
        conexion, resultado = conection()
        # verifica si la conexion falló
        if not resultado["success"]:
            return resultado
        
        try:
            #se crea el cursor para ejecutar las consultas SQL
            cursor = conexion.cursor()
            #define la consulta SQL, pasando el ID del reporte a eliminar
            query = f"DELETE FROM {TBREPORTE} WHERE {TBREPORTE_ID} = %s"
            # Ejecuta la consulta SQL pasando el ID del reporte a eliminar
            cursor.execute(query, (id,))
            # Confirma los cambios en la base de datos
            conexion.commit()
            # Indica que la eliminacion fue exitosa
            resultado["success"] = True
            resultado["message"] = "Reporte eliminado exitosamente."
        # Captura cualquier excepcion que ocurra durante la eliminacion
        except Exception as e:
            resultado["success"] = False
            #gaurda el mensaje de error
            resultado["message"] = f"Error al eliminar reporte: {e}"
        #cierra la conexion si esta abierta
        finally:
            if conexion:
                conexion.close()
        return resultado
    
    def list_reportes(self, pagina=1, tam_pagina=10, ordenar_por=TBREPORTE_ID, tipo_orden="ASC", busqueda=None):
        conexion, resultado = conection()
        if not resultado["success"]:
            return resultado
        
        listaReportes = [] #lista donde se almacenan los perfiles
        try:
            cursor = conexion.cursor(dictionary=True) #cursor para ejecutar las consultas
            #diccionario para  mapear los nombres de las columnas
            columna_orden = {
                "id_empleado": TBREPORTE_ID_EMPLEADO,
                "fecha_generacion": TBREPORTE_FECHA_GENERACION,
                "tipo_reporte": TBREPORTE_TIPO_REPORTE,
                "contenido": TBREPORTE_CONTENIDO
            }
            # si la columna esta desordenada se ordena por id
            ordenar_por = columna_orden.get(ordenar_por, TBREPORTE_ID)
            #se ajusta
            tipo_orden = "DESC" if tipo_orden != "ASC" else "ASC"
            
            query = f"""SELECT 
                    r.*,
                    p.{TBPERSONA_NOMBRE} AS nombre_persona
                FROM {TBREPORTE} r
                INNER JOIN {TBEMPLEADO} e ON r.{TBREPORTE_ID_EMPLEADO} = e.{TBEMPLEADO_ID}
                INNER JOIN {TBPERSONA} p ON e.{TBEMPLEADO_PERSONA} = p.{TBPERSONA_ID}"""
            valores = []
            
            if busqueda:
                query += f""" WHERE p.{TBPERSONA_NOMBRE} LIKE %s 
                              OR r.{TBREPORTE_ID_EMPLEADO} LIKE %s 
                              OR r.{TBREPORTE_FECHA_GENERACION} LIKE %s 
                              OR r.{TBREPORTE_TIPO_REPORTE} LIKE %s 
                              OR r.{TBREPORTE_CONTENIDO} LIKE %s """
                valores = [f"%{busqueda}%", f"%{busqueda}%", f"%{busqueda}%", f"%{busqueda}%", f"%{busqueda}%"]
            
            query += f" ORDER BY {ordenar_por} {tipo_orden} LIMIT %s OFFSET %s"
            valores.extend([tam_pagina, (pagina - 1) * tam_pagina])
            
            cursor.execute(query, valores) # Ejecuta la consulta SQL
            registros = cursor.fetchall()# Obtiene todos los registros
            for registro in registros:        # Se iteran los registros obtenidos y se convierten en objetos de tipo Perfil
                reporte = Reporte(
                    id_empleado=registro[TBREPORTE_ID_EMPLEADO],
                    fecha_generacion=registro[TBREPORTE_FECHA_GENERACION],
                    tipo_reporte=registro[TBREPORTE_TIPO_REPORTE],
                    contenido=registro[TBREPORTE_CONTENIDO],
                    id=registro[TBREPORTE_ID]
                )
                listaReportes.append({'reporte': reporte,'nombre_empleado': registro['nombre_persona'] })# Se añade el perfil a la lista
            
            cursor.execute(f"SELECT COUNT(*) as total FROM {TBREPORTE}") #TBROL
            total_registros = cursor.fetchone()["total"]  # Se obtiene el número total de registros
            total_paginas = (total_registros + tam_pagina - 1) // tam_pagina
            
            resultado["data"] = {
                "listaReportes": listaReportes,
                "pagina_actual": pagina,
                "tam_pagina": tam_pagina,
                "total_paginas": total_paginas,
                "total_registros": total_registros
            }
            resultado["success"] = True
            resultado["message"] = "Reportes listados exitosamente."
        except Exception as e:
            resultado["success"] = False
            resultado["message"] = f"Error al listar reportes: {e}"
        finally:
            if cursor:
                cursor.close()
            if conexion:
                conexion.close()
        return resultado
    
    def get_reporte_by_id(self, reporte_id):
        conexion, resultado = conection()
        if not resultado["success"]:
            return resultado

        try:
            cursor = conexion.cursor()
              # Consulta SQL para obtener el perfil por su ID
            query = f"""SELECT
                            {TBREPORTE_ID_EMPLEADO}, 
                            {TBREPORTE_FECHA_GENERACION}, 
                            {TBREPORTE_TIPO_REPORTE}, 
                            {TBREPORTE_CONTENIDO},
                            {TBREPORTE_ID} 
                        FROM {TBREPORTE} 
                        WHERE {TBREPORTE_ID} = %s"""
            
            cursor.execute(query, (reporte_id,)) #busca segun el id
            data = cursor.fetchone() # se obtiene el resultado
            
            if data: #si se encuentra el perfil
                reporte = Reporte(
                    id_empleado=data[0],
                    fecha_generacion=data[1],
                    tipo_reporte=data[2],
                    contenido=data[3],
                    id=data[4]
                )
                resultado["success"] = True
                resultado["data"] = reporte
            else:
                resultado["success"] = False
                resultado["message"] = "No se encontró ningún reporte con el ID proporcionado."
        except Exception as e:
            resultado["success"] = False
            resultado["message"] = f"Error al obtener reporte: {e}"
        finally:
            if conexion:
                conexion.close()
        return resultado
    
    def obtener_todo_reportes(self):
        conexion, resultado = conection()
        if not resultado["success"]:
            return resultado
        
        listaReportes = []  # Lista donde se almacenarán los perfiles ob
        try:
            with conexion.cursor(dictionary=True) as cursor:
                query = f"SELECT * FROM {TBREPORTE}"
                cursor.execute(query)
                registros = cursor.fetchall()
                
           # Se convierten los registros en objetos de tipo Reporte y se almacenan en la lista
                for registro in registros:
                    reporte = Reporte(
                        id_empleado=registro[TBREPORTE_ID_EMPLEADO],
                        fecha_generacion=registro[TBREPORTE_FECHA_GENERACION],
                        tipo_reporte=registro[TBREPORTE_TIPO_REPORTE],
                        contenido=registro[TBREPORTE_CONTENIDO],
                        id=registro[TBREPORTE_ID],
                    )
                    listaReportes.append(reporte)
                
                resultado["data"] = {
                    "listaReportes": listaReportes,
                }
                resultado["success"] = True
                resultado["message"] = "Reportes listados exitosamente."
        except Exception as e:
            resultado["success"] = False
            resultado["message"] = f"Error al listar reportes: {e}"
        finally:
            if cursor:
                cursor.close()# Se cierra el cursor
            if conexion:
                conexion.close()# Se cierra la conexión a la base de datos
        
        return resultado
        
    def obtener_datos_para_reporte(self, limit: int= None, offset: int = None, tipoReporte: list = ['todo'], id_departamento: int = None, id_rol: int = None, id_empleado: int = None, rangoFechas: dict[str, date] = None):
        conexion, resultado = conection()
        if not resultado['success']:
            return resultado
        try:
            
            if rangoFechas:
                if len(rangoFechas) != 2:
                    return {'success': False, 'message': 'Error: Se requieren exactamente 2 fechas (inicio y fin)'}
                try:
                    # Convertir strings a objetos date
                    fecha_inicio    = datetime.strptime(rangoFechas[0], '%Y-%m-%d').date()
                    fecha_fin       = datetime.strptime(rangoFechas[1], '%Y-%m-%d').date()
                    
                    if fecha_inicio > fecha_fin:
                        return {'success': False, 'message': 'La fecha de inicio no puede ser mayor que la fecha fin'}
                    rangoFechas = [fecha_inicio,fecha_fin]
                except ValueError:
                    return {'success': False, 'message': 'Formato de fecha inválido. Use YYYY-MM-DD'}
            
            REPORTES_VALIDOS = ['todo','justificacion','asistencias','permisos']
            
            if not all(reporte in REPORTES_VALIDOS for reporte in tipoReporte):
                return {'success':False,'message':f'El tipo de reporte no es valido. Tipos de reportes \'{', '.join(REPORTES_VALIDOS)}\''}
            
            with conexion.cursor(dictionary=True) as cursor:
                datosSelect = []
                leftJoin    = []
                condicion   = []
                valores     = ()

                if tipoReporte:
                    if any(reporte in ['justificacion', 'todo'] for reporte in tipoReporte) :
                        leftJoin.append(f'LEFT JOIN {TBJUSTIFICACION} J ON J.{TBJUSTIFICACION_ID_EMPLEADO} = E.{TBEMPLEADO_ID}')
                        if rangoFechas:
                            leftJoin[-1] += f' AND (J.{TBJUSTIFICACION_FECHA} >= %s AND J.{TBJUSTIFICACION_FECHA} <= %s )'
                            valores += (rangoFechas[0], rangoFechas[1])
                        
                        datosSelect.extend([
                            f'J.{TBJUSTIFICACION_ID}            AS JustificacionId',
                            f'J.{TBJUSTIFICACION_ID_EMPLEADO}   AS JustificacionIdEmpleado',
                            f'J.{TBJUSTIFICACION_ID_ASISTENCIA} AS JustificacionIdAsistencia',
                            f'J.{TBJUSTIFICACION_FECHA}         AS JustificacionFecha',
                            f'J.{TBJUSTIFICACION_MOTIVO}        AS JustificacionMotivo',
                            f'J.{TBJUSTIFICACION_DESCRIPCION}   AS JustificacionDescripcion'
                        ])

                    if any(reporte in ['asistencias', 'todo']   for reporte in tipoReporte) :
                        leftJoin.append(f'LEFT JOIN {TBASISTENCIA} A ON A.{TBASISTENCIA_ID_EMPLEADO} = E.{TBEMPLEADO_ID}')
                        if rangoFechas:
                            leftJoin[-1] += f' AND (A.{TBASISTENCIA_FECHA} >= %s AND A.{TBASISTENCIA_FECHA} <= %s)'
                            valores += (rangoFechas[0],rangoFechas[1])
                        
                        datosSelect.extend([
                            f'A.{TBASISTENCIA_ID}                   AS AsistenciaId',
                            f'A.{TBASISTENCIA_ID_EMPLEADO}          AS AsistenciaIdEmpleado',
                            f'A.{TBASISTENCIA_FECHA}                AS AsistenciaFecha',
                            f'A.{TBASISTENCIA_ESTADO_ASISTENCIA}    AS AsistenciaEstado'
                        ])
                                
                    if any(reporte in ['permisos', 'todo']      for reporte in tipoReporte) :
                        leftJoin.append(f'LEFT JOIN {TBSOLICITUDPERMISOS} SP ON SP.{TBSOLICITUDPERMISOS_ID_EMPLEADO} = E.{TBEMPLEADO_ID}')
                        if rangoFechas:
                            leftJoin[-1] += f' AND (SP.{TBSOLICITUDPERMISOS_FECHA_INICIO} <= %s AND SP.{TBSOLICITUDPERMISOS_FECHA_FIN} >= %s)'
                            valores += (rangoFechas[1], rangoFechas[0])  # Nota el orden invertido para el solapamiento
                        
                        datosSelect.extend([
                            f'SP.{TBSOLICITUDPERMISOS_ID}           AS PermisoId',
                            f'SP.{TBSOLICITUDPERMISOS_ID_EMPLEADO}  AS PermisoIdEmpleado',
                            f'SP.{TBSOLICITUDPERMISOS_TIPO}         AS PermisoTipo',
                            f'SP.{TBSOLICITUDPERMISOS_FECHA_INICIO} AS PermisoFechaInicio',
                            f'SP.{TBSOLICITUDPERMISOS_FECHA_FIN}    AS PermisoFechaFin',
                            f'SP.{TBSOLICITUDPERMISOS_DESCRIPCION}  AS PermisoDescripcion',
                            f'SP.{TBSOLICITUDPERMISOS_ESTADO}       AS PermisoEstado'
                        ])
                        
                leftJoin.append(F'INNER JOIN {TBDEPARTAMENTO} D ON D.{TBDEPARTAMENTO_ID} = E.{TBEMPLEADO_DEPARTAMENTO} ')
                if id_departamento:
                    leftJoin[-1] += f' AND D.{TBDEPARTAMENTO_ID} = %s'
                    valores += (id_departamento,)
                    
                datosSelect.extend([
                    f'D.{TBDEPARTAMENTO_ID}     AS DepartamentoId',
                    f'D.{TBDEPARTAMENTO_NOMBRE} AS DepartamentoNombre',
                    f'D.{TBDEPARTAMENTO_DESCRIPCION} AS DepartamentoDescripcion'
                ])
                

                leftJoin.append(f'INNER JOIN {TBROLEMPLEADO} RE ON RE.{TBROLEMPLEADO_ID_EMPLEADO} = E.{TBEMPLEADO_ID}')
                leftJoin.append(f'INNER JOIN {TBROL} R ON R.{TBROL_ID} = RE.{TBROLEMPLEADO_ID_ROL}')
                if id_rol:
                    leftJoin[-1] += f' AND RE.{TBROLEMPLEADO_ID_ROL} = %s'
                    valores += (id_rol,)
                
                datosSelect.extend([
                    f'R.{TBROL_ID}          AS RolId',
                    f'R.{TBROL_NOMBRE}      AS RolNombre',
                    f'R.{TBROL_DESCRIPCION} AS RolDescripcion'
                ])
                
                if id_empleado: #siempre tiene que ir de ultimo por que es lo que va en el where
                    condicion.append(f'E.{TBEMPLEADO_ID} = %s')
                    valores += (id_empleado,)

                # Construcción de la consulta
                query = f'''SELECT 
                            E.{TBEMPLEADO_ID}       AS EmpleadoId,
                            P.{TBPERSONA_CEDULA}    AS CedulaPersona,
                            P.{TBPERSONA_NOMBRE}    AS NombrePersona,
                            P.{TBPERSONA_APELLIDOS} AS ApellidosPersona,
                                
                            {',\n'.join(datosSelect) if datosSelect else ''} 
                            FROM {TBEMPLEADO} E 
                            INNER JOIN {TBPERSONA} P ON P.{TBPERSONA_ID} = E.{TBEMPLEADO_PERSONA}
                            {'\n'.join(leftJoin)}'''
                
                if condicion:
                    query += f'\nWHERE {" AND ".join(condicion)}'
                
                # Agregar paginación
                if limit and offset: query += f'\nLIMIT {limit} OFFSET {offset}'

                cursor.execute(query,valores)
                datos = cursor.fetchall()

                datosReporte = []
                if datos:
                    for reporte in datos:                        
                        datosEmpleadoReporte = {}
                        datosEmpleadoReporte['id_empleado'] = reporte['EmpleadoId']
                        datosEmpleadoReporte['nombre']      = reporte['NombrePersona']
                        datosEmpleadoReporte['apellidos']   = reporte['ApellidosPersona']
                        datosEmpleadoReporte['cedula']      = reporte['ApellidosPersona']
                        
                        if (any(reporte in ['justificacion', 'todo'] for reporte in tipoReporte)) and reporte['JustificacionId']:
                            justificacion = Justificacion(
                                id              = reporte['JustificacionId'],
                                id_empleado     = reporte['JustificacionIdEmpleado'],
                                id_asistencia   = reporte['JustificacionIdAsistencia'],
                                fecha           = reporte['JustificacionFecha'],
                                motivo          = reporte['JustificacionMotivo'],
                                descripcion     = reporte['JustificacionDescripcion']
                            )
                            datosEmpleadoReporte['justificacion'] =justificacion
                        
                        if (any(reporte in ['asistencias', 'todo']   for reporte in tipoReporte)) and reporte['AsistenciaId']:
                            asistencia = Asistencia(
                                id          = reporte['AsistenciaId'],
                                id_empleado = reporte['AsistenciaIdEmpleado'],
                                fecha       = reporte['AsistenciaFecha'],
                                estado_asistencia = reporte['AsistenciaEstado']
                            )
                            datosEmpleadoReporte['asistencia'] = asistencia
                        
                        if (any(reporte in ['permisos', 'todo']      for reporte in tipoReporte)) and reporte['PermisoId']:
                            permiso = SolicitudPermiso(
                                id          = reporte['PermisoId'],
                                id_empleado = reporte['PermisoIdEmpleado'],
                                tipo        = reporte['PermisoTipo'],
                                fecha_inicio= reporte['PermisoFechaInicio'],
                                fecha_fin   = reporte['PermisoFechaFin'],
                                descripcion = reporte['PermisoDescripcion'],
                                estado      = reporte['PermisoEstado']
                            )
                            datosEmpleadoReporte['permisos'] = permiso
                        
                        if reporte['DepartamentoId']:
                            departamento = Departamento(
                                id          = reporte['DepartamentoId'],
                                nombre      = reporte['DepartamentoNombre'],
                                descripcion = reporte['DepartamentoDescripcion']
                            )
                            datosEmpleadoReporte['departamento'] = departamento
                            
                        if reporte['RolId']:
                            rol = Rol(
                                id      = reporte['RolId'],
                                nombre  = reporte['RolNombre'],
                                descripcion = reporte['RolDescripcion']
                            )
                            datosEmpleadoReporte['rol'] = rol
                            
                        datosReporte.append(datosEmpleadoReporte)
                        
                    return{
                        'success':True,
                        'reporte':datosReporte,
                        'message':'Se obtuvieron los datos correctamente.'
                    }
                else:
                    return {'success': True,'reporte':datosReporte,'message': 'No se encontraron datos'}
        except Exception as e:
            
            exc_type, exc_value, exc_traceback = sys.exc_info()
            errores = traceback.extract_tb(exc_traceback)[-1]
            logger.error(f'{e} - LIN&COL {errores.lineno}:{errores.colno if hasattr(errores, 'colno') else 'N/A'}')
            return {'success': False, 'message': 'Ocurrió un error al obtener los datos para el reporte.'}
        finally:
            if conexion: conexion.close()
        