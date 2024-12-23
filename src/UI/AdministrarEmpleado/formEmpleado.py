from PySide6.QtWidgets import *
from PySide6.QtCore import *
# from Utils.Utils import *
# from UI.DialogoEmergente import *
import sys

class formEmpleado(QDialog):
    idEmpleado = None
    fotografia = None
    def __init__(self, parent = None, titulo = 'Registrar empleado', id_empleado = None):
        super().__init__(parent)
        self.setObjectName('form')
        self.setMinimumSize(QSize(700,650))
        # self.setWindowFlags(Qt.FramelessWindowHint)
        # cargar_estilos('claro','form.css',self)
        '''
        JERARQUIA DE WIDGETS Y OBJETOS QT

        *layoutPrin:QLayout
            *frame:QFrame
            *layoutFrame:QVBoxLayout
                *layoutContent:QHBoxLayout
                    *layoutIzq:QVBoxLayout
                        *tituloIzq:QLabel
                        *layoutFoto:QVBoxLayout
                            *foto:QLable
                            *btnFoto:QPushButton
                        *layout:QVBoxLayout
                            *lblNombre:QLabel
                            *inNombre:QLineEdit
                            *errNombre:QLabel
                        *layout:QVBoxLayout
                            *lblApellidos:QLabel
                            *inApellidos:QLineEdit
                            *errApellidos:QLabel
                        *layout:QVBoxLayout
                            *lblCedula:QLabel
                            *inCedula:QLineEdit
                            *errCedula:QLabel
                        *layout:QVBoxLayout
                            *lblCorreo:QLabel
                            *inCorreo:QLineEdit
                            *errCorreo:QLabel
                        *layout:QVBoxLayout
                            *lblNacimiento:QLabel
                            *inNacimiento:QDateEdit
                            *errNacimiento:QLabel
                        *layout:QVBoxLayout
                            *lblEstCivil:QLabel
                            *inEstCivil:QComboBox
                            *errEstCivil:QLabel
                        *layout:QVBoxLayout
                            *lblDireccion:QLabel
                            *inDireccion:QTextEdit
                            *errDireccion:QLabel
                    *layoutCent:QVBoxLayout
                        *tituloCent:QLabel
                        *layout:QVBoxLayout
                            *lblDepa:QLabel
                            *inDepa:QComboBox
                            *errDepa:QLabel
                        *layout:QVBoxLayout
                            *lblRol:QLabel
                            *inRol:QComboBox
                            *errRol:QLabel
                    *layoutDer:QVBoxLayout
                        *tituloDer:QLabel
                        *layout:QHBoxLayout
                            *lblCrearUser:QLabel
                            *btnCrear:QPushButton
                            *btnElim:QPushButton
                        *layoutListU:QVBoxLayout
                            *layoutUser:QVBoxLayou
                                *layout:QVBoxLayout
                                    *lblUser:QLabel
                                    *inUser:QComboBox
                                    *errUser:QLabel
                                *layout:QVBoxLayout
                                    *lblPass:QLabel
                                    *inPass:QComboBox
                                    *errPass:QLabel
                                *layoutPerfil
                                    *lblPerfil:QLabel
                                    *inPerfil:QComboBox
                                    *errPerfil:QLabel
            button_box:QDialogButtonBox

        '''
        layoutPrin =QVBoxLayout()
        frame = QFrame()
        frame.setObjectName('formFrame')
        #asignando el frame al layout principal
        layoutPrin.addWidget(frame)

        ## layoutFrame
        layoutFrame = QVBoxLayout()

        ## layoutContent
        self.layoutContent = QHBoxLayout()
        
        self._llenar_layoutConten()

        layoutFrame.addLayout(self.layoutContent)
        frame.setLayout(layoutFrame)
        self.setLayout(layoutPrin)


    '''
    LLenado de layoutContent
    '''
    def _llenar_layoutConten(self):
        #creando widgets para el scrol
        self.widgetIzq = QWidget()
        self.widgetCent = QWidget()
        self.widgetDer = QWidget()

        #creando los layouts
        self.layoutIzq = QVBoxLayout()
        self.layoutCent = QVBoxLayout()
        self.layoutDer = QVBoxLayout()

        #creando scrolls
        scroll_areaIzq = QScrollArea()
        scroll_areaIzq.setWidgetResizable(True)
        scroll_areaCent= QScrollArea()
        scroll_areaCent.setWidgetResizable(True)
        scroll_areaDer = QScrollArea()
        scroll_areaDer.setWidgetResizable(True)


        self._llenar_layoutIzq()
        self._llenar_layoutCent()
        self._llenar_layoutDer()
        
        # self.layoutContent.addLayout(self.layoutIzq)
        # self.layoutContent.addLayout(self.layoutCent)
        # self.layoutContent.addLayout(self.layoutDer)

        ###############################
        # Crear los scroll areas
        self.scrollIzq = QScrollArea()
        self.scrollCent = QScrollArea()
        self.scrollDer = QScrollArea()

        # Configurar las scroll areas
        self.scrollIzq.setWidgetResizable(True)
        self.scrollCent.setWidgetResizable(True)
        self.scrollDer.setWidgetResizable(True)

        # Crear widgets contenedores para cada scroll area
        widgetIzq = QWidget()
        widgetCent = QWidget()
        widgetDer = QWidget()

        # Asignar layouts a los widgets contenedores
        widgetIzq.setLayout(self.layoutIzq)
        widgetCent.setLayout(self.layoutCent)
        widgetDer.setLayout(self.layoutDer)

        # Asignar los widgets a las scroll areas
        self.scrollIzq.setWidget(widgetIzq)
        self.scrollCent.setWidget(widgetCent)
        self.scrollDer.setWidget(widgetDer)

        # Agregar las scroll areas al layout principal
        self.layoutContent.addWidget(self.scrollIzq)
        self.layoutContent.addWidget(self.scrollCent)
        self.layoutContent.addWidget(self.scrollDer)


        pass

    '''
    Llenado de layoutIzq
    '''
    def _llenar_layoutIzq(self):
        tituloIzq = QLabel('Datos Personales')

        self.layoutFoto = QVBoxLayout()
        self._llenar_LayoutFoto()
        #Creando Label, Input y label de error
        #Nombre
        self.lblNombre = QLabel('Nombre')
        self.inNombre = QLineEdit()
        self.errNombre = QLabel('Error nombre')
        #Apellidos
        self.lblApellidos = QLabel('Apellidos')
        self.inApellidos = QLineEdit()
        self.errApellidos = QLabel('Error apellidos')
        #Cedula
        self.lblCedula = QLabel('Cedula')
        self.inCedula = QLineEdit()
        self.errCedula = QLabel('Error cedula')
        #Fecha de nacimiento
        self.lblNacimiento = QLabel('Nacimiento')
        self.inNacimiento = QDateEdit()
        self.errNacimiento = QLabel('Error nacimiento')
        #Correo
        self.lblCorreo = QLabel('Correo')
        self.inCorreo = QLineEdit()
        self.errCorreo = QLabel('Error correo')
        #Estado civil
        self.lblEstCivil = QLabel('Estado civil')
        self.inEstCivil = QComboBox()
        self.errEstCivil = QLabel('Error estado civil')
        #Direccion
        self.lblDireccion = QLabel('Direccion')
        self.inDireccion = QTextEdit()
        self.errDireccion = QLabel('Error Direccion')
        
        #asignando al layoutIzq
        self.layoutIzq.addWidget(tituloIzq)
        self.layoutIzq.addLayout(self.layoutFoto)
        self.layoutIzq.addLayout(self._contenedor(self.lblNombre,self.inNombre,self.errNombre))
        self.layoutIzq.addLayout(self._contenedor(self.lblApellidos,self.inApellidos,self.errApellidos))
        self.layoutIzq.addLayout(self._contenedor(self.lblCedula,self.inCedula,self.errCedula))
        self.layoutIzq.addLayout(self._contenedor(self.lblNacimiento,self.inNacimiento,self.errNacimiento))
        self.layoutIzq.addLayout(self._contenedor(self.lblCorreo,self.inCorreo,self.errCorreo))
        self.layoutIzq.addLayout(self._contenedor(self.lblEstCivil,self.inEstCivil,self.errEstCivil))
        self.layoutIzq.addLayout(self._contenedor(self.lblDireccion,self.inDireccion,self.errDireccion))

        pass

    '''
    Llenado de layoutCent
    '''
    def _llenar_layoutCent(self):
        tituloCent = QLabel('Departamento y Rol')
        #Departamento
        self.lblDep = QLabel('Departamento')
        self.inDep = QComboBox()
        self.errDep = QLabel('Error Departamento')
        #Departamento
        self.lblRol = QLabel('Rol')
        self.inRol = QComboBox()
        self.errRol = QLabel('Error Rol')

        self.layoutCent.addWidget(tituloCent)
        self.layoutCent.addLayout(self._contenedor(self.lblDep,self.inDep,self.errDep))
        self.layoutCent.addLayout(self._contenedor(self.lblRol,self.inRol,self.errRol))
        self.layoutCent.setAlignment(Qt.AlignTop) ##Alinea los widgets arriba

        pass
    '''
    Llenado de layoutDer
    '''
    def _llenar_layoutDer(self):
        tituloDer = QLabel('Usuarios')

        pass
    '''
    Llenado de layoutFoto
    '''
    def _llenar_LayoutFoto(self):
        self.foto = QLabel('foto')
        self.btnFoto = QPushButton()
        self.layoutFoto.addWidget(self.foto)
        self.layoutFoto.addWidget(self.btnFoto)
        pass
    '''
    Contenedor independiente para cada input
    '''
    def _contenedor(self,label:QLabel,input,label_error:QLabel)->QVBoxLayout:
        layout = QVBoxLayout()
        layout.setContentsMargins(0,0,0,0)
        layout.setSpacing(5)
        
        label_error.setObjectName("lblerror")
        label_error.setMaximumHeight(25)
        label_error.setMinimumHeight(25)
        label_error.setWordWrap(True)
        
        layout.addWidget(label)
        layout.addWidget(input)
        layout.addWidget(label_error)
        return layout

if __name__ == '__main__':
    app = QApplication(sys.argv)
    dialogo = formEmpleado()
    dialogo.show()
    sys.exit(app.exec_())