import time
from settings.config import ZKTECA_CONFIG
from settings.logger import logger
from zk import ZK, user, Finger
from typing import Optional, List, Union, Dict, Tuple


class ZKServices:
    def __init__(self):
        self.zk = ZK(ZKTECA_CONFIG["host"], ZKTECA_CONFIG["port"])

    def capture_fingerprint(self, conn):
        """Función para capturar y obtener la huella dactilar."""
        print("Por favor, coloca tu dedo en el lector...")

        # Espera a que se capture la huella
        while True:
            try:
                fingerprint = conn.capture_finger()
                print("Huella capturada con éxito.")
                return fingerprint  # Devuelve la huella capturada
            except Exception as e:
                print(f"Error al capturar la huella: {e}")
                time.sleep(1)  # Espera un segundo antes de volver a intentar

    def crear_usuario(self, id: int, nombre: str):
        try:
            conn = self.zk.connect()
            conn.set_user(id, nombre)
            conn.disconnect()
        except Exception as e:
            logger.error(f"{e}")

    # registra
    def registrar_Empleado(self, id_empleado, nombre, cedula):
        try:
            conexion = self.zk.connect()
            conexion.set_user(id_empleado, f"{nombre} {cedula}")
            listaUser = conexion.get_users()
            user = list(filter(lambda u: u.uid == id_empleado, listaUser))
            conexion.disconnect()
            return user
        except Exception as e:
            return f"Error {e}"

    # obteniendo huella
    def obtener_huella(self, id_empleado):
        try:
            conexion = self.zk.connect()
            listFingers = conexion.get_templates()
            finger = list(filter(lambda f: f.uid == id_empleado, listFingers)) or None
            conexion.disconnect()
            return finger
        except Exception as e:
            return f"Error{e}"

    def mostrar_ventana_huella(self, id_empleado):

        try:
            conn = self.zk.connect()
            conn.enable_device()

            exito = conn.enroll_user(user_id=id_empleado, temp_id=1)

            start_time = time.time()
            while (time.time() - start_time) < 30:
                templates = conn.get_templates()
                huella = (
                    list(filter(lambda t: t.uid == str(id_empleado), templates)) or None
                )
                print(huella)
                if huella:
                    print("Huella recuperada..")
                    print(f"id huella {huella.uid}")
                    return "Huella compleatada"
                    break
                else:
                    print("No hay huella")
                time.sleep(1)

            conn.disconnect()
            return None  # Timeout
        except Exception as e:
            print(f"Error del dispositivo: {e}")
            return False

    def registrar_empleado_con_huella(self, id_em: int, nombre: str, cedula: str):
        try:
            conn = self.zk.connect()
            conn.enable_device()

            conn.set_user(uid=id_em, name=f"{nombre}-{cedula}")
            time.sleep(1)
            print("Ingrese la huella digital..")

            print("-------------------------------------")

            exito = conn.enroll_user(uid=id_em, temp_id=9)

            print("valor de exito")
            print(exito)

            start_time = time.time()
            while (time.time() - start_time) < 30:
                templates = conn.get_templates()
                huella = list(filter(lambda t: t.uid == id_em, templates)) or None
                print(huella)
                if huella:
                    print("Huella recuperada..")
                    print(f"id huella {huella.uid}")
                    return "Huella compleatada"
                    break
                else:
                    print("No hay huella")
                time.sleep(1)

            print("-------------------------------------")
            return "No se completo la tarea"
        except Exception as e:
            return f"{e}"

    def obtener_huellas_usuario(self, user_id: int) -> List[Finger]:

        # Obtiene todas las huellas registradas para un usuario.
        try:
            if not self.connect():
                return []

            templates = self.conn.get_templates()
            return [t for t in templates if t.uid == user_id]

        except Exception as e:
            logger.error(f"Error al obtener huellas: {e}")
            return []
        finally:
            self.disconnect()

    def verificar_usuario(self, user_id: int) -> Tuple[bool, bool]:
        """
        Verifica si un usuario existe y si tiene huellas registradas.

        """
        try:
            if not self.connect():
                return (False, False)

            # Obtener todos los usuarios
            usuarios = self.conn.get_users()
            if not usuarios:  # Si la lista está vacía
                return (False, False)

            # Verificar si el usuario existe
            usuario_existe = any(u.uid == user_id for u in usuarios)

            # Verificar huellas solo si el usuario existe
            tiene_huellas = False
            if usuario_existe:
                huellas = self.obtener_huellas_usuario(user_id)
                tiene_huellas = len(huellas) > 0

            return (usuario_existe, tiene_huellas)

        except Exception as e:
            logger.error(f"Error al verificar usuario: {e}")
            return (False, False)
        finally:
            self.disconnect()
