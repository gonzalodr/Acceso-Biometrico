import logging
import os
from logging.handlers import RotatingFileHandler

# Asegurando que la carpeta de logs exista
log_directory = 'src/loggers'
if not os.path.exists(log_directory):
    os.makedirs(log_directory)

# Creando el logger
logger = logging.getLogger(__name__)

# Creando el manejador de archivos logs
# máximo de tamaño por archivo 10 MB
# tiempo máximo de existencia de archivos 
# solo los 5 últimos 
file_handler = RotatingFileHandler(os.path.join(log_directory, 'Debugg.log'), maxBytes=2*1024*1024, backupCount=5)

# Estableciendo un formato de escritura
formato = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s - %(filename)s:%(lineno)d')
file_handler.setFormatter(formato)

# Añadiendo los manejadores al logger
logger.addHandler(file_handler)

# Exportando nada más el logger
__all__ = ['logger']