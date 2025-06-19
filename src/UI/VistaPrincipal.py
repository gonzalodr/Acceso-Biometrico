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
from UI.AdministrarUsuario.adminUsuario import *
from models.usuario import *
import sys


class vistaPrincipal(QWidget):
    listaOpciones = []  # numero Index en el stack, el nombre o texto, icono
    usuario: Usuario = None

    def __init__(
        self,
        usuario: Usuario,
        perfil:Perfil,
        permisos:Permiso_Perfil,
        parent=None,
    ):
        super().__init__(parent)
        
        self.usuario    = usuario
        self.permisos   = permisos
        self.perfil     = perfil
        
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

        if self.PermisoAModulo("Administrar horario"):
            getpermiso = next(filter(lambda per: per.tabla == ACCESO_TABLE["Administrar horario"], self.permisos),None)
            adminHorario = AdminHorario(parent = self, permiso = getpermiso)
            adminHorario.cerrar_adminH.connect(self._salir_crud)
            index = self.stackVistas.addWidget(adminHorario)
            self.listaOpciones.append((index, "Administrar Horarios", "weekly.png"))

        if self.PermisoAModulo("Administrar empleados"):
            getpermiso = next(filter(lambda per: per.tabla == ACCESO_TABLE["Administrar empleados"], self.permisos),None)
            adminempleado = AdminEmpleado(parent=self,permiso = getpermiso)
            adminempleado.signalCerrar.connect(self._salir_crud)
            index = self.stackVistas.addWidget(adminempleado)
            self.listaOpciones.append((index, "Admin. Empleados", "employees.png"))

<<<<<<< HEAD
        if self.PermisoAModulo("Administrar usuarios"):
            getpermiso = next(filter(lambda per: per.tabla == ACCESO_TABLE["Administrar usuarios"], self.permisos),None)
            adminUsuario = AdminUsuario(parent=self, permiso = getpermiso)
            adminUsuario.cerrar_adminU.connect(self._salir_crud)
            index = self.stackVistas.addWidget(adminUsuario)
            self.listaOpciones.append((index, "Administrar Usuarios", "management.png"))
=======
        if True:
           adminUsuario = AdminUsuario(parent=self)
           adminUsuario.cerrar_adminU.connect(self._salir_crud)
           index = self.stackVistas.addWidget(adminUsuario)
           self.listaOpciones.append((index, "Administrar Usuarios", "management.png"))
>>>>>>> parent of 543debc (Merge branch 'main' into Gonzalo)

        if self.PermisoAModulo("Administrar departamentos"):
            getpermiso = next(filter(lambda per: per.tabla == ACCESO_TABLE["Administrar departamentos"], self.permisos),None)  
            AdminDepart = AdminDepartament(parent=self, permiso = getpermiso)
            AdminDepart.cerrar_adminD.connect(self._salir_crud)
            index = self.stackVistas.addWidget(AdminDepart)
            self.listaOpciones.append((index, "Admin. Departamento", "company-department.png"))

        if self.PermisoAModulo("Administrar justificaciones"):
            getpermiso = next(filter(lambda per: per.tabla == ACCESO_TABLE["Administrar justificaciones"], self.permisos),None)
            adminJusficacion = AdminJustificacion(permiso=getpermiso)
            adminJusficacion.cerrar_adminJ.connect(self._salir_crud)
            index = self.stackVistas.addWidget(adminJusficacion)
<<<<<<< HEAD
            self.listaOpciones.append((index, "Admin.Justificacion", "division.png"))

        if self.PermisoAModulo("Administrar permisos empleado"):
            getpermiso = next(filter(lambda per: per.tabla == ACCESO_TABLE["Administrar permisos empleado"], self.permisos),None) 
            adminSoliPermiso = AdminSoliPermiso(permiso= getpermiso)
            adminSoliPermiso.cerrar_admin_soli_permiso.connect(self._salir_crud)
            index = self.stackVistas.addWidget(adminSoliPermiso)
            self.listaOpciones.append((index, "Admin Solicitud Permisos", "management.png"))
=======
            self.listaOpciones.append((index,"Admin.Justificacion",'division.png'))
>>>>>>> parent of 543debc (Merge branch 'main' into Gonzalo)

        # if True:
        #     adminrol = AdminRol()
        #     adminrol.cerrar_adminR.connect(self._salir_crud)
        #     index = self.stackVistas.addWidget(adminrol)
        #     self.listaOpciones.append((index,"Administrar rol",'workforce.png'))

        if self.PermisoAModulo("Administrar perfiles"):
            getpermiso = next(filter(lambda per: per.tabla ==ACCESO_TABLE["Administrar perfiles"], self.permisos),None)
            
            adminpermisosperfil = AdminPermisosPerfil(permiso=getpermiso)
            adminpermisosperfil.cerrar_adminP.connect(self._salir_crud)
            index = self.stackVistas.addWidget(adminpermisosperfil)
<<<<<<< HEAD
            self.listaOpciones.append( (index, "Perfiles de usuario", "access-control-list.png"))
        
        if self.PermisoAModulo("Administrar reportes"):
            getpermiso = next(filter(lambda per: per.tabla == ACCESO_TABLE["Administrar reportes"], self.permisos),None)
            adminreporte = AdminReporte(permiso=getpermiso)
=======
            self.listaOpciones.append((index,"Perfiles de usuario",'access-control-list.png'))
            
                 
        if True:
            adminreporte = AdminReporte()
>>>>>>> parent of 543debc (Merge branch 'main' into Gonzalo)
            adminreporte.signalCerrar.connect(self._salir_crud)
            index = self.stackVistas.addWidget(adminreporte)
            self.listaOpciones.append((index,"Admin. reportes",'online-survey.png'))
                         
        if self.PermisoAModulo("Administrar reportes"):
            getpermiso = next(filter(lambda per: per.tabla ==ACCESO_TABLE["Administrar reportes"], self.permisos),None)
            adminasistencia = AdminAsistencia(permiso= getpermiso)
            adminasistencia.cerrar_adminA.connect(self._salir_crud)
            index = self.stackVistas.addWidget(adminasistencia)
            self.listaOpciones.append((index,"Admin. Asistencia",'access-control-list.png'))

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
    
    def PermisoAModulo(self,tipoAdministracion):
        for modulo, tabla, *_ in MODULOS_ACCESO:
            if modulo == tipoAdministracion:
                for permiso in self.permisos:
                    if permiso.tabla == tabla:
                        return True
                return False 

        return False
            
        
        
        
    def _salir_crud(self):
        self.sidebar.deseleccionar()
        self.stackVistas.setCurrentIndex(0)

    def seleccion_sidebar(self, index):
        self.stackVistas.setCurrentIndex(index)
