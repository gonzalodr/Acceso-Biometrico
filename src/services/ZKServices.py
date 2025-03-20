from settings.config import ZKTECA_CONFIG
from settings.logger import logger
from zk              import ZK

class ZKServices:
    def __init__(self):
        self.zk = ZK(ZKTECA_CONFIG['host'],ZKTECA_CONFIG['port'])

    def capture_fingerprint(self,conn):
        """Función para capturar y obtener la huella dactilar."""
        print('Por favor, coloca tu dedo en el lector...')
        
        # Espera a que se capture la huella
        while True:
            try:
                fingerprint = conn.capture_finger()
                print('Huella capturada con éxito.')
                return fingerprint  # Devuelve la huella capturada
            except Exception as e:
                print(f'Error al capturar la huella: {e}')
                time.sleep(1)  # Espera un segundo antes de volver a intentar

    def crear_usuario(self,id:int, nombre:str):
        try:
            conn = self.zk.connect()
            conn.set_user(id,nombre)
            conn.disconnect()
        except Exception as e:
            logger.error(f'{e}')
        
