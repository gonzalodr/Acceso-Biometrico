from PySide6.QtWidgets import QGraphicsDropShadowEffect, QLabel,QPushButton
from PySide6.QtGui import QPixmap, QPainter,QIcon
from PySide6.QtSvg import QSvgRenderer
from PySide6.QtCore import QSize, Qt
import os
import inspect

def Sombrear(QObjeto,shadow:int=0,xOffset:int=0,yOffset:int=0, color:str=None):
    """
    Aplica un estilo de sombra a un objeto Q.
    
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
    
def add_Style(carpeta:str="css",archivoQSS:str="login.css",QObjeto = None):
    """
    Aplica un estilo a un objeto Q o devuelve el estilo como un string.
    
    :param carpeta: Nombre de la carpeta donde se encuentra el archivo QSS.
    :param archivoQSS: Nombre del archivo QSS a cargar.
    :param QObjeto: El objeto Q al que se le aplicará el estilo (opcional).
    :return: El estilo en forma de string si no se pasa QObjeto, None si se aplica el estilo.
    """
    # Obtener la ruta del archivo donde se llamó a este método
    caller_frame = inspect.stack()[1]
    caller_file = caller_frame.filename
    current_dir = os.path.dirname(caller_file)
    path_qss = os.path.join(current_dir, carpeta, archivoQSS)
    try:
        with open(path_qss, "r") as file:
            style = file.read()
        if QObjeto:
            QObjeto.setStyleSheet(style)
        else:
            return style  
    except FileNotFoundError:
        print(f"Error: El archivo {path_qss} no se encontró.")
        return None
    except Exception as e:
        print(f"Se produjo un error al leer el archivo: {e}")
        return None
    
def cargar_Icono(QObjeto,carpeta:str="iconos",archivoImg:str="",Size:QSize=None):
    """
    Carga un icono desde un archivo y lo establece en un objeto QPixmap.

    Args:
        QObjet (QLabel): Un objeto QLabel (o similar) donde se mostrará el icono.
        carpeta (str): Nombre de la carpeta donde se encuentra el archivo de imagen. 
                       Por defecto es "iconos".
        archivoImg (str): Nombre del archivo de imagen que se desea cargar. 
                          Debe incluir la extensión (ejemplo: 'User.png').
        Size (QSize): Tamaño al que se escalará el icono. 
                       Por defecto es QSize(30, 30). Si se proporciona un tamaño válido, 
                       se usará ese tamaño; de lo contrario, se usará el tamaño del QObjet.

    Este método realiza las siguientes acciones:
    1. Obtiene el directorio actual del archivo que se está ejecutando.
    2. Construye la ruta completa hacia el archivo de imagen especificado en 'carpeta' y 'archivoImg'.
    3. Carga la imagen como un objeto QPixmap.
    4. Escala el QPixmap al tamaño especificado por 'Size' o al tamaño del objeto QObjet si 'Size' no es válido.
    5. Establece el QPixmap escalado en QObjet, para que el icono se muestre adecuadamente.

    Asegúrate de que la imagen especificada esté ubicada en la carpeta correcta 
    para que la función funcione correctamente.
    """
    caller_frame = inspect.stack()[1]
    caller_file = caller_frame.filename
    current_dir = os.path.dirname(caller_file)#os.path.dirname(__file__)
    path_icono = os.path.join(current_dir, carpeta, archivoImg)
    pixmap = QPixmap(path_icono) 
    if Size:
        pixmap = pixmap.scaled(Size) 
    else:
        pixmap = pixmap.scaled(QObjeto.size()) 
    QObjeto.setPixmap(pixmap)
       
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

        
      