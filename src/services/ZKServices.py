from settings.config import ZKTECA_CONFIG
from settings.logger import logger
from zk              import ZK

class ZKServices:
    def __init__(self):
        self.zk = ZK(ZKTECA_CONFIG['host'],ZKTECA_CONFIG['port'])

    def crear_usuario(self,id:int, nombre:str):
        try:
            conn = self.zk.connect()
            conn.set_user(id,nombre)
            conn.disconnect()
        except Exception as e:
            logger.error(f'{e}')
        
