from PySide6.QtWidgets import *
from PySide6.QtCore import *



class TarjetaOpcion(QFrame):
    def __init__(self, opcionText="", opcionDesc="", icono =None,parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
                            QFrame{
                                background-color:#FFFFFF;
                                border-radius:10px;
                            }
                            QFrame::hover{
                               background-color:#DDDDDD;
                            }""")
        self.setMaximumSize(QSize(300,125))
        
        #icono
        self.lblIcono = QLabel()
        self.lblIcono.setText("Icono")
        self.lblIcono.setStyleSheet("color:#000000;background-color:transparent;")
        
        #nombre de la opcion
        self.lblOpcion = QLabel()
        self.lblOpcion.setStyleSheet("font: 700 14pt \"Segoe UI\";color:#000000;background-color:transparent;")
        self.lblOpcion.setWordWrap(True)
        self.lblOpcion.setText(opcionText)
        
        #descripcion de la opcion
        self.lblDescrip = QLabel();
        self.lblDescrip.setStyleSheet("font: 700 10pt \"Segoe UI\";color:#000000;background-color:transparent;")
        self.lblDescrip.setWordWrap(True)
        self.lblDescrip.setText(opcionDesc)
        
        #configura acomoda la tarjeta
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
        self.layoutFrame.addWidget(self.lblIcono,30)
        self.layoutFrame.addLayout(self.layoutText,70)
         
        self.setLayout(self.layoutFrame)
        self.configurar_sombra()
    
    def configurar_sombra(self):
        self.sombra = QGraphicsDropShadowEffect(self)
        self.sombra.setBlurRadius(20)
        self.sombra.setXOffset(0)
        self.sombra.setYOffset(0)
        self.setGraphicsEffect(self.sombra)
        
        
            