# from PySide6.QtWidgets import QGraphicsDropShadowEffect, QLabel,QPushButton
# from PySide6.QtGui import QPixmap, QPainter,QIcon
# from PySide6.QtSvg import QSvgRenderer
# from PySide6.QtCore import QSize, Qt
# from datetime import date, time, datetime
# import re
# import os
# import inspect
# import socket

# def Sombrear(QObjeto,shadow:int=0,xOffset:int=0,yOffset:int=0, color:str=None):
#     sombra = QGraphicsDropShadowEffect(QObjeto)
#     sombra.setBlurRadius(shadow)
#     sombra.setXOffset(xOffset)
#     sombra.setYOffset(yOffset)
#     if color:
#         sombra.setColor(color)
#     QObjeto.setGraphicsEffect(sombra)
     
# def cargar_Icono(QObjeto,archivoImg:str="",Size:QSize=None):
#     try:
#         ruta_relativa = os.getcwd()
#         ruta = os.path.join(ruta_relativa,'src','UI','iconos',archivoImg)

#         if not os.path.exists(ruta):
#             raise ValueError(f'La ruta \'{ruta}\' no existe')
        
#         if os.path.splitext(ruta)[1] != '.png':
#             raise ValueError(f'La extencion del archivo en la ruta \'{ruta}\' no es validad, esta debe ser \'.png\'')
        
#         pixmap = QPixmap(ruta) 

#         # Qt.SmoothTransformation:
#         # Mejora la calidad del escalado mediante interpolación suave.
#         # Evita bordes pixelados o borrosos en imágenes escaladas.
#         # Aspect Ratio:
#         # Utilizamos Qt.KeepAspectRatio para mantener la proporción de la imagen al escalarla.

#         if Size:
#             pixmap = pixmap.scaled(Size, Qt.KeepAspectRatio, Qt.SmoothTransformation) 
#         else:
#             pixmap = pixmap.scaled(Size if Size else QSize(QObjeto.size().height(), QObjeto.size().height()),  Qt.KeepAspectRatio, Qt.SmoothTransformation) 
#         QObjeto.setPixmap(pixmap)
#     except Exception as e:
#         print(f'Error: {e}')
    
# def cargar_icono_svg(QObjeto, carpeta:str="iconos",archivoSVG:str="", Size:QSize=None):
#     # Obtener el directorio del archivo que llama a esta función
#     # tipo = type(QObjeto)
#     # print(f"\n\ntipo: {tipo} \n\n")
    
#     caller_frame = inspect.stack()[1]
#     caller_file = caller_frame.filename
#     current_dir = os.path.dirname(caller_file)
    
#     # Crear la ruta completa del archivo SVG
#     path_icono = os.path.join(current_dir, carpeta, archivoSVG)
    
#     # Crear el renderer y el QPixmap
#     svg_renderer = QSvgRenderer(path_icono)
#     pixmap = QPixmap(Size if Size else QSize(QObjeto.size().height(), QObjeto.size().height()))
#     pixmap.fill(Qt.transparent)
    
#     painter = QPainter(pixmap)
#     svg_renderer.render(painter)
#     painter.end()
    
#     if isinstance(QObjeto, QLabel):
#         QObjeto.setPixmap(pixmap)
#     elif isinstance(QObjeto, QPushButton):
#         icon = QIcon(pixmap)
#         QObjeto.setIcon(icon)
#         QObjeto.setIconSize(Size if Size else QSize(QObjeto.size().height(), QObjeto.size().height()))
#     else:
#         print("QObjeto no es compatible con QLabel ni QPushButton")

# def cargar_estilos(tema:str = 'default', archivoCSS:str='login.css', QObjeto = None): 
#     ruta_relativa = os.getcwd()
#     ruta = os.path.join(ruta_relativa,'src','UI','css',tema,archivoCSS)
#     try:
#         with open(ruta, "r") as file:
#             style = file.read()
#         if QObjeto:
#             QObjeto.setStyleSheet(style)
#         else:
#             return style  
#     except FileNotFoundError:
#         print(f"Error: El archivo {ruta} no se encontró.")
#         return None
#     except Exception as e:
#         print(f"Se produjo un error al leer el archivo: {e}")
#         return None

# def cargar_icono(Qpushbutton:QPushButton,icono:str,Size:QSize = None):
#     try:
#         ruta_relativa = os.getcwd()
#         ruta = os.path.join(ruta_relativa, 'src', 'UI', 'iconos', icono)

#         if not os.path.exists(ruta):
#             raise ValueError(f'La ruta \'{ruta}\' no existe')
        
#         if os.path.splitext(ruta)[1] != '.png':
#             raise ValueError(f'La extencion del archivo en la ruta \'{ruta}\' no es validad, esta debe ser \'.png\'')
        
#         icono_q = QIcon(ruta)
#         Qpushbutton.setIcon(icono_q)
#         if Size is not None:
#             Qpushbutton.setIconSize(Size)
#         else:
#             altura = Qpushbutton.size().height()-30
#             Qpushbutton.setIconSize(QSize(altura, altura))
#     except Exception as e:
#         print(f'Error: {e}')

# def format_Fecha(fecha):
#     fecha = str(fecha)
#     partes = fecha.split(' ')
#     fecha_parte = partes[0]
#     hora_parte = partes[1] if len(partes) > 1 else None
    
#     # Procesar la parte de la fecha
#     año, mes, dia = fecha_parte.split("-")
#     meses = {
#         '01': 'enero',
#         '02': 'febrero',
#         '03': 'marzo',
#         '04': 'abril',
#         '05': 'mayo',
#         '06': 'junio',
#         '07': 'julio',
#         '08': 'agosto',
#         '09': 'septiembre',
#         '10': 'octubre',
#         '11': 'noviembre',
#         '12': 'diciembre'
#     }
#     mes_nombre = meses[mes]
    
#     if hora_parte:
#         hh, mn, sec = hora_parte.split(':')
#     else:
#         hh, mn, sec = '00', '00', '00'
    
#     resultado = f"{int(dia)} de {mes_nombre} del {año}"
#     if hora_parte:
#         resultado += f", {hh}:{mn}:{sec}"
    
#     return resultado

# def parse_date(date_str: str) -> date:
#     """Convierte string 'dd-mm-yyyy' a objeto date"""
#     try:
#         day, month, year = map(int, date_str.split('-'))
#         return date(year, month, day)
#     except (ValueError, AttributeError) as e:
#         raise ValueError(f"Formato de fecha inválido: {date_str}. Use 'dd-mm-yyyy'") from e

# def parse_time(time_str: str) -> time:
#     """Convierte string 'HH:MM' a objeto time"""
#     try:
#         hours, minutes = map(int, time_str.split(':'))
#         return time(hours, minutes)
#     except (ValueError, AttributeError) as e:
#         raise ValueError(f"Formato de hora inválido: {time_str}. Use 'HH:MM'") from e
    
    


# def is_device_reachable(ip: str, port: int, timeout: float = 3.0) -> bool:
#     try:
#         with socket.create_connection((ip, port), timeout=timeout):
#             return True
#     except (socket.timeout, socket.error):
#         return False 

from PySide6.QtWidgets import QGraphicsDropShadowEffect, QLabel, QPushButton
from PySide6.QtGui import QPixmap, QPainter, QIcon
from PySide6.QtSvg import QSvgRenderer
from PySide6.QtCore import QSize, Qt
from datetime import date, time, datetime
import re
import os
import sys
import inspect
import socket

# --- Función centralizada para manejar rutas de recursos ---
def resource_path(relative_path):
    """
    Obtiene la ruta absoluta a un recurso, funciona tanto en desarrollo
    como cuando se empaqueta con PyInstaller.

    Args:
        relative_path (str): La ruta relativa del recurso *dentro de la estructura
                             que PyInstaller empaqueta*. Por ejemplo, si empaquetas
                             'src/ui/iconos' como 'src/ui/iconos', entonces
                             'src/ui/iconos/mi_icono.png' sería la relative_path.
    """
    try:
        # PyInstaller crea una carpeta temporal y la añade a _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        # Si no está empaquetado, estamos en el entorno de desarrollo.
        # Asumimos que el script principal (main.py) se ejecuta desde la raíz del proyecto.
        # Por lo tanto, la base para los recursos es la raíz del proyecto.
        # Si este archivo 'utils.py' se llama desde 'main.py' en 'src/',
        # entonces os.path.abspath(".") es 'Acceso-Biometrico/'
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, relative_path)

def Sombrear(QObjeto, shadow: int = 0, xOffset: int = 0, yOffset: int = 0, color: str = None):
    sombra = QGraphicsDropShadowEffect(QObjeto)
    sombra.setBlurRadius(shadow)
    sombra.setXOffset(xOffset)
    sombra.setYOffset(yOffset)
    if color:
        sombra.setColor(color)
    QObjeto.setGraphicsEffect(sombra)
      
def cargar_Icono(QObjeto, archivoImg: str = "", Size: QSize = None):
    try:
        # Usamos resource_path para obtener la ruta correcta
        # La ruta relativa dentro del ejecutable es 'src/ui/iconos/archivoImg'
        ruta = resource_path(os.path.join('src', 'ui', 'iconos', archivoImg))

        if not os.path.exists(ruta):
            raise ValueError(f'La ruta \'{ruta}\' no existe')
        
        if os.path.splitext(ruta)[1].lower() != '.png': # Convertir a minúsculas para comparación robusta
            raise ValueError(f'La extensión del archivo en la ruta \'{ruta}\' no es válida, esta debe ser \'.png\'')
        
        pixmap = QPixmap(ruta) 

        if Size:
            pixmap = pixmap.scaled(Size, Qt.KeepAspectRatio, Qt.SmoothTransformation) 
        else:
            # Asegúrate de que QObjeto.size() tenga un valor válido
            target_size = QObjeto.size() if QObjeto.size().isValid() else QSize(64, 64) # Valor por defecto si no es válido
            pixmap = pixmap.scaled(target_size, Qt.KeepAspectRatio, Qt.SmoothTransformation) 
        QObjeto.setPixmap(pixmap)
    except Exception as e:
        print(f'Error al cargar icono PNG: {e}')
    
def cargar_icono_svg(QObjeto, archivoSVG: str = "", Size: QSize = None):
    try:
        # Usamos resource_path para obtener la ruta correcta
        # La ruta relativa dentro del ejecutable es 'src/ui/iconos/archivoSVG'
        path_icono = resource_path(os.path.join('src', 'ui', 'iconos', archivoSVG))
        
        if not os.path.exists(path_icono):
            raise ValueError(f'La ruta SVG \'{path_icono}\' no existe')

        if os.path.splitext(path_icono)[1].lower() != '.svg':
            raise ValueError(f'La extensión del archivo en la ruta \'{path_icono}\' no es válida, esta debe ser \'.svg\'')

        # Crear el renderer y el QPixmap
        svg_renderer = QSvgRenderer(path_icono)
        
        # Asegúrate de que QObjeto.size() tenga un valor válido
        target_size = Size if Size else (QObjeto.size() if QObjeto.size().isValid() else QSize(64, 64))
        
        pixmap = QPixmap(target_size)
        pixmap.fill(Qt.transparent)
        
        painter = QPainter(pixmap)
        svg_renderer.render(painter)
        painter.end()
        
        if isinstance(QObjeto, QLabel):
            QObjeto.setPixmap(pixmap)
        elif isinstance(QObjeto, QPushButton):
            icon = QIcon(pixmap)
            QObjeto.setIcon(icon)
            QObjeto.setIconSize(target_size)
        else:
            print("QObjeto no es compatible con QLabel ni QPushButton para cargar SVG.")
    except Exception as e:
        print(f'Error al cargar icono SVG: {e}')

def cargar_estilos(tema: str = 'claro', archivoCSS: str = 'main_window.css', QObjeto = None): 
    try:
        # Usamos resource_path para obtener la ruta correcta
        # La ruta relativa dentro del ejecutable es 'src/ui/css/tema/archivoCSS'
        ruta = resource_path(os.path.join('src', 'ui', 'css', tema, archivoCSS))
        
        with open(ruta, "r", encoding="utf-8") as file: # Añadir encoding para evitar errores
            style = file.read()
        if QObjeto:
            QObjeto.setStyleSheet(style)
        else:
            return style 
    except FileNotFoundError:
        print(f"Error: El archivo CSS {ruta} no se encontró.")
        return None
    except Exception as e:
        print(f"Se produjo un error al leer el archivo CSS: {e}")
        return None

def cargar_icono(Qpushbutton: QPushButton, icono: str, Size: QSize = None):
    try:
        # Usamos resource_path para obtener la ruta correcta
        # La ruta relativa dentro del ejecutable es 'src/ui/iconos/icono'
        ruta = resource_path(os.path.join('src', 'ui', 'iconos', icono))

        if not os.path.exists(ruta):
            raise ValueError(f'La ruta \'{ruta}\' no existe')
        
        if os.path.splitext(ruta)[1].lower() != '.png':
            raise ValueError(f'La extensión del archivo en la ruta \'{ruta}\' no es válida, esta debe ser \'.png\'')
        
        icono_q = QIcon(ruta)
        Qpushbutton.setIcon(icono_q)
        if Size is not None:
            Qpushbutton.setIconSize(Size)
        else:
            # Asegúrate de que Qpushbutton.size() tenga un valor válido
            altura = Qpushbutton.size().height() - 30 if Qpushbutton.size().isValid() else 34 # Valor por defecto
            Qpushbutton.setIconSize(QSize(altura, altura))
    except Exception as e:
        print(f'Error al cargar icono en QPushButton: {e}')

def format_Fecha(fecha):
    fecha = str(fecha)
    partes = fecha.split(' ')
    fecha_parte = partes[0]
    hora_parte = partes[1] if len(partes) > 1 else None
    
    # Procesar la parte de la fecha
    año, mes, dia = fecha_parte.split("-")
    meses = {
        '01': 'enero', '02': 'febrero', '03': 'marzo', '04': 'abril',
        '05': 'mayo', '06': 'junio', '07': 'julio', '08': 'agosto',
        '09': 'septiembre', '10': 'octubre', '11': 'noviembre', '12': 'diciembre'
    }
    mes_nombre = meses[mes]
    
    if hora_parte:
        hh, mn, sec = hora_parte.split(':')
    else:
        hh, mn, sec = '00', '00', '00'
    
    resultado = f"{int(dia)} de {mes_nombre} del {año}"
    if hora_parte:
        resultado += f", {hh}:{mn}:{sec}"
    
    return resultado

def parse_date(date_str: str) -> date:
    """Convierte string 'dd-mm-yyyy' a objeto date"""
    try:
        day, month, year = map(int, date_str.split('-'))
        return date(year, month, day)
    except (ValueError, AttributeError) as e:
        raise ValueError(f"Formato de fecha inválido: {date_str}. Use 'dd-mm-yyyy'") from e

def parse_time(time_str: str) -> time:
    """Convierte string 'HH:MM' a objeto time"""
    try:
        hours, minutes = map(int, time_str.split(':'))
        return time(hours, minutes)
    except (ValueError, AttributeError) as e:
        raise ValueError(f"Formato de hora inválido: {time_str}. Use 'HH:MM'") from e
    
def is_device_reachable(ip: str, port: int, timeout: float = 3.0) -> bool:
    try:
        with socket.create_connection((ip, port), timeout=timeout):
            return True
    except (socket.timeout, socket.error):
        return False
