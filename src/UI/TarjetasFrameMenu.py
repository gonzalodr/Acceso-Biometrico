from PySide6.QtWidgets import *
from PySide6.QtCore import *



class TarjetaOpcion(QFrame):
    def __init__(self, opcionText="", opcionDesc="", icono =None,parent=None):
        self.setStyleSheet("background-color:#000000;")
        self.setMaximumSize(QSize(100,70))
        
        #icono
        self.lblIcono = QLabel()
        self.lblIcono.setText("I")
        self.lblIcono.setStyleSheet("color:#FFFFFF;")
        
        #nombre de la opcion
        self.lblOpcion = QLabel()
        self.lblOpcion.setStyleSheet("font: 700 12pt \"Segoe UI\";color:#FFFFFF;")
        self.lblOpcion.setWordWrap(True)
        self.lblOpcion.setText(opcionText)
        
        #descripcion de la opcion
        self.lblDescrip = QLabel();
        self.lblDescrip.setStyleSheet("font: 700 8pt \"Segoe UI\";color:#FFFFFF;")
        self.lblDescrip.wordWrap(True)
        self.lblDescrip.setText(opcionDesc)
        
        self.configurarFrame()
        
    def configurarFrame(self):
        self.layoutFrame = QHBoxLayout()
        self.layoutFrame.setSpacing(3)
        self.layoutFrame.setContentsMargins(2,2,2,2)
        
        ##layouts para los textos
        self.layoutText = QVBoxLayout()
        self.layoutText.setSpacing(3)
        self.layoutText.setContentsMargins(0,0,0,0)
        # agrega los textos al layout de los textos
        self.layoutText.addWidget(self.lblOpcion,25)
        self.layoutText.addWidget(self.lblDescrip,75)
        # agrega tanto el icono como el layout de los textos como el icono
        self.layoutFrame.addWidget(self.lblIcono,25)
        self.layoutFrame.addLayout(self.layoutText,72)
         
        self.setLayout(self.layoutFrame)
        
        
            