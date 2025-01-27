from PySide6.QtWidgets import QGraphicsDropShadowEffect, QLabel,QPushButton
from PySide6.QtGui import QPixmap, QPainter,QIcon
from PySide6.QtSvg import QSvgRenderer
from PySide6.QtCore import QSize, Qt
import os
import inspect

def Sombrear(QObjeto,shadow:int=0,xOffset:int=0,yOffset:int=0, color:str=None):
    """
    Aplica un estilo de sombra a un objeto Qt.
    
    :param shadow: Valor que indica la intencidad del blur.
    :param xOffset: Desplazamiento de la sombra en el eje x.
    :param yOffset: Desplazamiento de la sombra en el eje y.
    :return: No se retorna ningun dato.
    """
    sombra = QGraphicsDropShadowEffect(QObjeto)
    sombra.setBlurRadius(shadow)
    sombra.setXOffset(xOffset)
    sombra.setYOffset(yOffset)
    if color:
        sombra.setColor(color)
    QObjeto.setGraphicsEffect(sombra)
     
def cargar_Icono(QObjeto,archivoImg:str="",Size:QSize=None):
    try:
        ruta_relativa = os.getcwd()
        ruta = os.path.join(ruta_relativa,'src','UI','iconos',archivoImg)

        if not os.path.exists(ruta):
            raise ValueError(f'La ruta \'{ruta}\' no existe')
        
        if os.path.splitext(ruta)[1] != '.png':
            raise ValueError(f'La extencion del archivo en la ruta \'{ruta}\' no es validad, esta debe ser \'.png\'')
        
        pixmap = QPixmap(ruta) 

        # Qt.SmoothTransformation:
        # Mejora la calidad del escalado mediante interpolación suave.
        # Evita bordes pixelados o borrosos en imágenes escaladas.
        # Aspect Ratio:
        # Utilizamos Qt.KeepAspectRatio para mantener la proporción de la imagen al escalarla.

        if Size:
            pixmap = pixmap.scaled(Size, Qt.KeepAspectRatio, Qt.SmoothTransformation) 
        else:
            pixmap = pixmap.scaled(Size if Size else QSize(QObjeto.size().height(), QObjeto.size().height()),  Qt.KeepAspectRatio, Qt.SmoothTransformation) 
        QObjeto.setPixmap(pixmap)
    except Exception as e:
        print(f'Error: {e}')
    
def cargar_icono_svg(QObjeto, carpeta:str="iconos",archivoSVG:str="", Size:QSize=None):
    # Obtener el directorio del archivo que llama a esta función
    # tipo = type(QObjeto)
    # print(f"\n\ntipo: {tipo} \n\n")
    
    caller_frame = inspect.stack()[1]
    caller_file = caller_frame.filename
    current_dir = os.path.dirname(caller_file)
    
    # Crear la ruta completa del archivo SVG
    path_icono = os.path.join(current_dir, carpeta, archivoSVG)
    
    # Crear el renderer y el QPixmap
    svg_renderer = QSvgRenderer(path_icono)
    pixmap = QPixmap(Size if Size else QSize(QObjeto.size().height(), QObjeto.size().height()))
    pixmap.fill(Qt.transparent)
    
    painter = QPainter(pixmap)
    svg_renderer.render(painter)
    painter.end()
    
    if isinstance(QObjeto, QLabel):
        QObjeto.setPixmap(pixmap)
    elif isinstance(QObjeto, QPushButton):
        icon = QIcon(pixmap)
        QObjeto.setIcon(icon)
        QObjeto.setIconSize(Size if Size else QSize(QObjeto.size().height(), QObjeto.size().height()))
    else:
        print("QObjeto no es compatible con QLabel ni QPushButton")

def cargar_estilos(tema:str = 'default', archivoCSS:str='login.css', QObjeto = None): 
    ruta_relativa = os.getcwd()
    ruta = os.path.join(ruta_relativa,'src','UI','css',tema,archivoCSS)
    try:
        with open(ruta, "r") as file:
            style = file.read()
        if QObjeto:
            QObjeto.setStyleSheet(style)
        else:
            return style  
    except FileNotFoundError:
        print(f"Error: El archivo {ruta} no se encontró.")
        return None
    except Exception as e:
        print(f"Se produjo un error al leer el archivo: {e}")
        return None

def cargar_icono(Qpushbutton:QPushButton,icono:str,Size:QSize = None):
    try:
        ruta_relativa = os.getcwd()
        ruta = os.path.join(ruta_relativa, 'src', 'UI', 'iconos', icono)

        if not os.path.exists(ruta):
            raise ValueError(f'La ruta \'{ruta}\' no existe')
        
        if os.path.splitext(ruta)[1] != '.png':
            raise ValueError(f'La extencion del archivo en la ruta \'{ruta}\' no es validad, esta debe ser \'.png\'')
        
        icono_q = QIcon(ruta)
        Qpushbutton.setIcon(icono_q)
        if Size is not None:
            Qpushbutton.setIconSize(Size)
        else:
            altura = Qpushbutton.size().height()-30
            Qpushbutton.setIconSize(QSize(altura, altura))
    except Exception as e:
        print(f'Error: {e}')
