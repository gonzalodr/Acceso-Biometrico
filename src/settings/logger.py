import logging
import os
from logging.handlers import RotatingFileHandler



# Verificar y crear la carpeta loggers si no existe
log_dir = os.path.join('src','loggers')
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

# Creando el logger
logger = logging.getLogger(__name__)

#creando el manejador de archivos logs
#máximo de tamaño por archivo 10 mb, 
# tiempo máximo de existencia de archivos 
# completos solo los 5 últimos 
file_handler = RotatingFileHandler(os.path.join(log_dir,'Debugg.log'), maxBytes=2*1024*1024, backupCount=5)

# Estableciendo un formato de escritura
formato = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s - %(filename)s:%(lineno)d')
file_handler.setFormatter(formato)

# añadiendo los manejadores al logger
logger.addHandler(file_handler)

#exportando nada mas el logger
__all__ = ['logger']
