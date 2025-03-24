from PySide6.QtWidgets import *
from PySide6.QtCore import *
from Utils.Utils import *
from UI.slideBar import *
from UI.AdministrarHorario.adminHorario import *
from UI.AdministrarJustificacion.adminJustificacion import *
from UI.AdministraPersona.adminPersona import *
from UI.AdministraDepartamento.adminDepartamento import *  # Importa la clase AdminDepartamento
from UI.AdministrarRol.adminRol import *
from UI.AdministrarReporte.AdminReporte import *
from UI.AdministrarPermisosRol.AdminPermisosRol import *
from UI.AdministrarPermisosPerfil.AdminPermisosPerfil import *
from UI.AdministrarEmpleado.administrarEmpleado import *
from UI.AdministrarAsistencia.AdminAsistencia import *
from models.usuario import *
import sys


class vistaPrincipal(QWidget):
    listaOpciones = []  # numero Index en el stack, el nombre o texto, icono
    usuario: Usuario = None

    def __init__(
        self,
        usuario: Usuario,
        parent=None,
    ):
        super().__init__(parent)
        self.usuario = usuario
        self.setObjectName("vistaPrincipal")

        cargar_estilos("claro", "ventanaPrincipal.css", self)

        frame = QFrame()
        frame.setObjectName("frameFondoPrincipal")
        frame.setContentsMargins(0, 0, 0, 0)

        """
        layoutFrame: Acomoda tanto la seccion de encabezado como la de cuerpo 
        """
        layoutFrame = QVBoxLayout()
        layoutFrame.setContentsMargins(10, 10, 10, 10)
        layoutFrame.setSpacing(10)

        """
        frameEncabezado: le da color al encabezado de la ventana
        """
        frameEncabezado = QFrame()
        frameEncabezado.setObjectName("frameEnca")
        frameEncabezado.setContentsMargins(0, 0, 0, 0)
        Sombrear(frameEncabezado, 30, 0, 5)

        """
        layoutEncabezado: Acomoda todos los elementos que se mostraran en el encabezado
        """
        layoutEncabezado = QHBoxLayout()
        layoutEncabezado.setSpacing(0)
        layoutEncabezado.setContentsMargins(20, 5, 20, 5)

        """
            btnAbrir_SideBar: Este boton nos permitirar abrir y cerrar nuestro sidebar de la ventana
        """
        self.btnAbrir_SideBar = QPushButton(text="")
        self.btnAbrir_SideBar.setCursor(Qt.PointingHandCursor)
        self.btnAbrir_SideBar.setMaximumSize(QSize(45, 45))
        cargar_icono_svg(
            QObjeto=self.btnAbrir_SideBar,
            archivoSVG="arrow-bar-right.svg",
            Size=QSize(
                self.btnAbrir_SideBar.size().width() - 15,
                self.btnAbrir_SideBar.size().height() - 15,
            ),
        )
        Sombrear(self.btnAbrir_SideBar, 20, 0, 5)

        """
            lblEncabezado: Mostrara el nombre de nuestra ventana.
        """
        self.lblEncabezado = QLabel(text=f"Bienvenido/a {usuario.usuario}.")
        self.lblEncabezado.setAlignment(Qt.AlignCenter)
        self.lblEncabezado.setMaximumHeight(30)

        """
            lblIconUser: Mostrara la foto de nuestro usuario
        """
        self.lblIconoUser = QLabel(text="User")
        self.lblIconoUser.setObjectName("iconoUser")
        self.lblIconoUser.setMaximumSize(QSize(50, 50))
        self.lblIconoUser.setMinimumSize(QSize(50, 50))
        cargar_Icono(self.lblIconoUser, archivoImg="user.png")
        Sombrear(self.lblIconoUser, 30, 0, 5)

        """
            Acomodamos los elementos de nuestra ventana
        """
        layoutEncabezado.addWidget(self.btnAbrir_SideBar, 1)
        layoutEncabezado.addStretch(4)
        layoutEncabezado.addWidget(self.lblEncabezado, 2)
        layoutEncabezado.addStretch(4)
        layoutEncabezado.addWidget(self.lblIconoUser, 1)
        """Agregamos nuestro layout del encabezado a nuestro frame"""
        frameEncabezado.setLayout(layoutEncabezado)

        layoutFrame.addWidget(frameEncabezado, 1)

        """Este layoout es para acomodar los elementos del cuerpo de la ventana"""
        layoutCuerpo = QHBoxLayout()
        layoutCuerpo.setSpacing(20)
        layoutCuerpo.setContentsMargins(1, 10, 1, 10)

        self.stackVistas = QStackedWidget()
        self._llenar_stack_vista()

        self.sidebar = SlideBar(listaOpciones=self.listaOpciones)
        cargar_Icono(self.sidebar.lblUsuario, archivoImg="user.png")
        # self.cargar_imagen_usuario(self.sidebar.lblUsuario)
        self.btnAbrir_SideBar.clicked.connect(
            lambda click, btn=self.btnAbrir_SideBar: self.sidebar.accion_anim(
                btnSidebar=btn
            )
        )

        """Recibimos una señal la cual nos servira para detectar los btn del sidebar"""
        self.sidebar.index_opcion_selecionada.connect(self.seleccion_sidebar)

        layoutCuerpo.addWidget(self.sidebar, 1)
        layoutCuerpo.addWidget(self.stackVistas, 3)

        """Agregando sidebar"""
        layoutFrame.addLayout(layoutCuerpo, 9)

        """Acomodando todo en la ventana"""
        frame.setLayout(layoutFrame)
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(frame)
        self.setLayout(layout)

    def _llenar_stack_vista(self):
        self.stackVistas.addWidget(self._widget_presentacion())

        """
        al agregar a la lista se asigna el index, el titulo, y el png para el icono.
        """

        # if True:
        #     adminpersona = AdminPersona(parent=self)
        #     adminpersona.cerrar_adminP.connect(self._salir_crud)
        #     index = self.stackVistas.addWidget(adminpersona)
        #     self.listaOpciones.append((index, "Administrar Persona",'employees.png'))

        if True:
            adminHorario = AdminHorario(parent=self)
            adminHorario.cerrar_adminH.connect(self._salir_crud)
            index = self.stackVistas.addWidget(adminHorario)
            self.listaOpciones.append((index, "Administrar Horarios", "weekly.png"))

        if True:
            adminempleado = AdminEmpleado(parent=self)
            adminempleado.signalCerrar.connect(self._salir_crud)
            index = self.stackVistas.addWidget(adminempleado)
            self.listaOpciones.append((index, "Admin. Empleados", "employees.png"))

        if True:
            AdminDepart = AdminDepartament(parent=self)
            AdminDepart.cerrar_adminD.connect(self._salir_crud)
            index = self.stackVistas.addWidget(AdminDepart)
            self.listaOpciones.append(
                (index, "Admin. Departamento", "company-department.png")
            )

        if True:
            adminJusficacion = AdminJustificacion()
            adminJusficacion.cerrar_adminJ.connect(self._salir_crud)
            index = self.stackVistas.addWidget(adminJusficacion)
            self.listaOpciones.append((index,"Admin.Justificacion",'division.png'))

        # if True:
        #     adminrol = AdminRol()
        #     adminrol.cerrar_adminR.connect(self._salir_crud)
        #     index = self.stackVistas.addWidget(adminrol)
        #     self.listaOpciones.append((index,"Administrar rol",'workforce.png'))

        # if True:
        #     adminpermisos = AdminPermisosRol()
        #     adminpermisos.cerrar_adminP.connect(self._salir_crud)
        #     index = self.stackVistas.addWidget(adminpermisos)
        #     self.listaOpciones.append((index,"Admin. permisos rol",'access-control-list.png'))

        if True:
            adminpermisosperfil = AdminPermisosPerfil()
            adminpermisosperfil.cerrar_adminP.connect(self._salir_crud)
            index = self.stackVistas.addWidget(adminpermisosperfil)
            self.listaOpciones.append((index,"Admin. permisos perfil",'access-control-list.png'))
            
                 
        if True:
            adminreporte = AdminReporte()
            adminreporte.cerrar_adminR.connect(self._salir_crud)
            index = self.stackVistas.addWidget(adminreporte)
            self.listaOpciones.append((index,"Admin. reportes",'access-control-list.png'))
            
                     
        if True:
            adminasistencia = AdminAsistencia()
            adminasistencia.cerrar_adminA.connect(self._salir_crud)
            index = self.stackVistas.addWidget(adminasistencia)
            self.listaOpciones.append((index,"Admin. Asistencia",'access-control-list.png'))
            
            
        
            self.listaOpciones.append(
                (index, "Admin. permisos perfil", "access-control-list.png")
            )

        self.stackVistas.setCurrentIndex(0)

    def _widget_presentacion(self):
        widgetP = QWidget()
        widgetP.setObjectName("widgetDefault")
        frame = QFrame()
        layout = QVBoxLayout()
        layout.addWidget(frame)
        lblPresentacion = QLabel(text="Acceso Biometrico")
        lblPresentacion.setAlignment(Qt.AlignCenter)
        Sombrear(lblPresentacion, 20, 0, 0)
        layoutP = QVBoxLayout()
        layoutP.setContentsMargins(0, 0, 0, 0)
        layoutP.addWidget(lblPresentacion)
        frame.setLayout(layoutP)
        widgetP.setLayout(layout)
        Sombrear(widgetP, 50, 0, 0)
        return widgetP

    def _salir_crud(self):
        self.sidebar.deseleccionar()
        self.stackVistas.setCurrentIndex(0)

    def seleccion_sidebar(self, index):
        self.stackVistas.setCurrentIndex(index)
