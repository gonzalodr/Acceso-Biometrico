import logging
import os
from logging.handlers import RotatingFileHandler

# Crear el directorio loggers si no existe
log_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'loggers')
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

# Creando el logger
logger = logging.getLogger(__name__)

#creando el manejador de archivos logs
#maximo de tamano por archivo 10 mb, 
# tiempo maximo de existecia de archivos 
# completos solo los 5 ultimos 
file_handler = RotatingFileHandler('src/loggers/Debugg.log', maxBytes=2*1024*1024, backupCount=5)

# Estableciendo un formato de escritura
formato = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s - %(filename)s:%(lineno)d')
file_handler.setFormatter(formato)

# anadiendo los manejadores al logger
logger.addHandler(file_handler)

#exportando nada mas el logger
__all__ = ['logger']
