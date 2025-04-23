import time 
from settings.config import ZKTECA_CONFIG
from settings.logger import logger
from zk              import ZK
from datetime        import date
from datetime        import time as dt_time

from typing import Optional, List, Union, Tuple
from Utils.Utils     import parse_date, parse_time
import re
import traceback

class ZKServices:
    def __init__(self):
        self.zk = ZK(ZKTECA_CONFIG['host'],ZKTECA_CONFIG['port'])
    
    # obteniendo huella
    def obtener_huella(self, id_empleado):
        try:
            conexion = self.zk.connect()
            listHuella = conexion.get_templates()
            huella = list(filter(lambda f: f.uid == id_empleado, listHuella)) or None
            conexion.disconnect()
            return {'success':True, 'huella': huella[0] if huella else huella}
        except Exception as e:
            return {'success':False, 'message':'Ocurrio un error al obtener la huella'}

    #registrar empleado con huella
    def registrar_empleado_con_huella(self, id_empleado:int, nombre:str, cedula:str):
        try:
            conn = self.zk.connect()
            conn.enable_device()

            conn.set_user(uid = id_empleado, name = f'{nombre}-{cedula}')
            time.sleep(1)

            conn.enroll_user(uid=id_empleado, temp_id=9)

            start_time = time.time()
            while (time.time() - start_time) < 30:
                templates = conn.get_templates()
                huella    = list(filter(lambda t: t.uid == id_empleado, templates)) or None
                if huella: 
                    conn.test_voice(0)
                    return {'success':True,'message':'Se registro con exito el empleado.','huella_id_ZK':huella[0].uid}
                time.sleep(0.5)

            return {'success':True,'message':'Se registro el empleado pero sin huella.','huella_id_ZK':None}
        except Exception as e:
            logger.error(f'{e}')
            return {'success':False, 'message':f'Ocurrio un error al registrar el empleado.'}
    
    def obtener_asistencias(self, id_empleado: Optional[int]    = None, 
                        fecha: Optional[Union[date, str]]       = None,
                        rango_fechas: Optional[Union[Tuple[date, date], List[str]]] = None):
        try:
            if fecha:
                if isinstance(fecha, str):
                    fecha = parse_date(fecha)
            if rango_fechas:  
                if isinstance(rango_fechas, list):
                    if len(rango_fechas) != 2:
                        raise ValueError("El rango de fechas debe contener exactamente 2 elementos")
                    rango_fechas = (parse_date(rango_fechas[0]), parse_date(rango_fechas[1]))
                
                if rango_fechas[0] > rango_fechas[1]:
                    return {'success':False,'message':'La primera fecha del filtro debe ser menor o igual a la ultima fecha.'}

            conn        = self.zk.connect() 
            
            conn.disable_device()
            
            asistencias = conn.get_attendance()
            users       = conn.get_users()
            filtered    = []
            for asist in asistencias:
                asist_datetime = asist.timestamp
                
                # Filtro por ID de empleado
                if id_empleado and str(asist.user_id) != str(id_empleado):
                    continue
                # Filtro por fecha específica
                if fecha and asist_datetime.date() != fecha:
                    continue
                    
                # Filtro por rango de fechas
                if rango_fechas:
                    fecha_inicio, fecha_fin = rango_fechas
                    if not (fecha_inicio <= asist_datetime.date() <= fecha_fin):
                        continue
                # envia tanto el empleado al que le pertenece la asistencia como la misma asistencias
                empleado    = list(filter(lambda e: str(e.uid) ==  str(asist.user_id),users)) or None
                filtered.append((empleado,asist))
                
            conn.enable_device()
            conn.disconnect()
            return {'success':True, 'message':'Se obtuvieron las asistencias.','asistencias':filtered}
        except Exception as e:
            logger.error(f'{e}')
            return {'success':False, 'message':'Ocurrio un erro al obtener la asistencias'}
    
    def actualizar_empleado(self, id_em: int, nombre: str, cedula: str):
        try:
            conn = self.zk.connect()
            conn.enable_device()

            # Actualizar los datos del empleado
            conn.set_user(uid = id_em, name = f'{nombre}-{cedula}')
            time.sleep(1)

            # Aquí decidimos si también actualizamos la huella, si es necesario
            conn.enroll_user(uid=id_em, temp_id=9)

            start_time = time.time()
            while (time.time() - start_time) < 30:
                templates = conn.get_templates()
                huella = list(filter(lambda t: t.uid == id_em, templates)) or None

                if huella:
                    conn.test_voice(0)
                    conn.disconnect()
                    return {'success': True, 'message': 'Empleado actualizado con éxito.', 'huella_id_ZK': huella[0].uid}
                time.sleep(0.5)

            conn.disconnect()
            return {'success': True, 'message': 'Empleado actualizado pero sin huella.', 'huella_id_ZK': None}
        except Exception as e:
            logger.error(f'{e}')
            return {'success': False, 'message': 'Ocurrió un error al actualizar el empleado.'}

    def verificar_puntualidad(self, id_empleado: int):
        hoy = date.today()
        print(f"🔍 Buscando asistencias para {id_empleado} el día {hoy}")

        resultado = self.obtener_asistencias(id_empleado=id_empleado, fecha=hoy)
        print(f"📋 Resultado de obtener_asistencias: {resultado}")

        if not resultado["success"]:
            return {'success': False, 'message': resultado["message"]}

        asistencias = resultado.get("asistencias", [])
        if not asistencias:
            return {'success': False, 'message': "No hay asistencia registrada para hoy."}

        primera_asistencia = min(asistencias, key=lambda x: x.timestamp)
        hora_asistencia = primera_asistencia.timestamp.time()
        hora_limite = dt_time(14, 30)

        if hora_asistencia <= hora_limite:
            return {'success': True, 'message': f"✅ Llegaste a tiempo: {hora_asistencia}"}
        else:
            return {'success': True, 'message': f"⚠ Llegaste tarde: {hora_asistencia}"}