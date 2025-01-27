import logging
import os
from logging.handlers import RotatingFileHandler

# Crear el directorio loggers si no existe
log_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'loggers')
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

# Creando el logger
logger = logging.getLogger(__name__)

# Creando el manejador de archivos logs
# Máximo de tamaño por archivo: 2 MB, se mantienen los 5 archivos más recientes
log_file = os.path.join(log_dir, 'Debugg.log')
file_handler = RotatingFileHandler(log_file, maxBytes=2*1024*1024, backupCount=5)

# Estableciendo un formato de escritura
formato = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formato)

# Añadiendo los manejadores al logger
logger.addHandler(file_handler)

# Establecer el nivel de registro (opcional, dependiendo de tus necesidades)
logger.setLevel(logging.DEBUG)