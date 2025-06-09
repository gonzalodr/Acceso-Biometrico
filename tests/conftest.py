# tests/conftest.py

import sys
import os

# Calculamos la ruta absoluta de la carpeta raíz del proyecto (dos niveles arriba de este archivo)
proyecto_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# Construimos la ruta completa a la carpeta `src` dentro de la raíz
ruta_src = os.path.join(proyecto_root, 'src')

# Insertamos `src/` al comienzo de sys.path para poder hacer `import src.<algo>`
if ruta_src not in sys.path:
    sys.path.insert(0, ruta_src)