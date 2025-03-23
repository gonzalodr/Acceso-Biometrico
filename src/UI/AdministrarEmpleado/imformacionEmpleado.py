import sys
from PySide6.QtWidgets import *
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap

from services.empleadoServices import EmpleadoServices
from models.persona import Persona
from models.usuario import Usuario

from UI.DialogoEmergente import DialogoEmergente
from Utils.Utils import *

class informacionEmpleado(QDialog):
    def __init__(self,id_empleado:int,parent = None):
        super().__init__(parent)
        self.setWindowTitle("Informacion del empleado")
        self.setMinimumSize(700, 675)
        
        main_layout = QVBoxLayout()
        lbltitulo = QLabel('Informacion del empleado')
        lbltitulo.setObjectName('lbltitulo')
        lbltitulo.setAlignment(Qt.AlignCenter)
        lbltitulo.setMinimumHeight(40)
        main_layout.addWidget(lbltitulo)
        
        cargar_estilos('claro','informacionEm.css',self)
        
        # Contenedor principal con scroll
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        
        scroll_widget = QWidget()
        content_layout = QVBoxLayout(scroll_widget)
        
        # Sección de Datos Personales
        self.personal_group = QGroupBox("Datos Personales")
        personal_layout = QHBoxLayout()
        
        # Foto del empleado
        self.foto = QLabel()
        self.foto.setAlignment(Qt.AlignCenter)
        self.foto.setObjectName('foto')
        self.foto.setFixedSize(150, 150)

        personal_layout.addWidget(self.foto)
        
        # Campos de datos personales
        self.form_layout = QFormLayout()
        self.form_layout.setSpacing(10)
        
        self.nombre     = QLineEdit()
        self.apellidos  = QLineEdit()
        self.cedula     = QLineEdit()
        self.nacimiento = QLineEdit()
        self.correo     = QLineEdit()
        self.estadoCivil= QLineEdit()
        self.direccion  = QLineEdit()
        
        for field in [self.nombre, self.apellidos, self.cedula, self.nacimiento, self.correo, self.estadoCivil, self.direccion]:
            field.setReadOnly(True)
            field.setMinimumHeight(25)
        
        self.form_layout.addRow(QLabel("Nombre:"), self.nombre)
        self.form_layout.addRow(QLabel("Apellidos:"), self.apellidos)
        self.form_layout.addRow(QLabel("Cédula:"), self.cedula)
        self.form_layout.addRow(QLabel("Nacimiento:"), self.nacimiento)
        self.form_layout.addRow(QLabel("Correo:"), self.correo)
        self.form_layout.addRow(QLabel("Estado Civil:"), self.estadoCivil)
        self.form_layout.addRow(QLabel("Dirección:"), self.direccion)
        
        form_widget = QWidget()
        form_widget.setLayout(self.form_layout)
        personal_layout.addWidget(form_widget)
        self.personal_group.setLayout(personal_layout)
        
        # Sección de Teléfonos
        self.phone_group = QGroupBox("Teléfonos")
        self.phone_layout = QVBoxLayout()
        phone_widget = QWidget()
        phone_widget.setLayout(self.phone_layout)
        self.phone_group.setLayout(QVBoxLayout())
        self.phone_group.layout().addWidget(phone_widget)
        
        # Sección de Rol y Departamento
        self.role_group = QGroupBox("Rol y Departamento")
        self.role_layout = QFormLayout()
        self.role_group.setLayout(self.role_layout)
        
        # Sección de Usuario
        self.user_group = QGroupBox("Cuenta de Usuario")
        self.user_layout = QFormLayout()
        self.user_group.setLayout(self.user_layout)
        
        # Agregar secciones al layout del widget con scroll
        content_layout.addWidget(self.personal_group)
        content_layout.addWidget(self.phone_group)
        content_layout.addWidget(self.role_group)
        content_layout.addWidget(self.user_group)
        content_layout.addStretch()
        
        scroll_area.setWidget(scroll_widget)
        main_layout.addWidget(scroll_area)
        
        # Botón de cierre
        btn_close = QPushButton("Cerrar")
        btn_close.setFixedSize(100,30)
        btn_close.clicked.connect(self.cerrar)

        main_layout.addWidget(btn_close, alignment=Qt.AlignRight)
        
        self.setLayout(main_layout)
        self.cargarInformacionEmpleado(id_empleado)
    
    def cerrar(self):
        self.reject()

    def cargarInformacionEmpleado(self,id_empleado:int):
        result = EmpleadoServices().obtener_empleado_por_id(id_empleado)
        if not result['success']:
            dial = DialogoEmergente('','Ocurrio un error al precargar los datos de los empleados.\nError: '+result['message'],'Error',True,False)
            dial.exec()
            self.reject()

        datos   = result.get('empleado')
        persona:Persona = datos.get('persona')  #objeto Persona
        usuario:Usuario = datos.get('usuario')  #objeto Usuario
        dictPerfil = datos.get('pefilUsuario')  #diccionario
        dictRolEmp = datos.get('rolEmpleado')   #diccionario
        departamen = datos.get('departamento')  #int
        listaTelef = datos.get('listaTelefonos')#telefonos del usuario

        # Cargar la foto si está disponible
        if persona.foto:
            pixmap = QPixmap()
            pixmap.loadFromData(persona.foto)
            self.foto.setPixmap(pixmap.scaled(150, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        else:
            cargar_Icono(self.foto,'userPerson.png')
        
        # Cargar datos personales
        self.nombre.setText(persona.nombre)
        self.apellidos.setText(persona.apellidos)
        self.cedula.setText(persona.cedula)
        self.nacimiento.setText(format_Fecha(str(persona.fecha_nacimiento)))
        self.correo.setText(persona.correo)
        self.estadoCivil.setText(persona.estado_civil)
        self.direccion.setText(persona.direccion)

        # Cargar telefonos
        if listaTelef:
            for telefono in listaTelef:
                phone_layout = QHBoxLayout()
                
                phone_input = QLineEdit(telefono.numero)
                phone_input.setReadOnly(True)
                
                type_input = QLineEdit(telefono.tipo)
                type_input.setReadOnly(True)
                
                phone_layout.addWidget(QLabel("Número:"))
                phone_layout.addWidget(phone_input)
                phone_layout.addWidget(QLabel("Tipo:"))
                phone_layout.addWidget(type_input)
                
                self.phone_layout.addLayout(phone_layout)
        else:
            self.phone_group.hide()

        #Cargar el rol y el departamento
        if dictRolEmp or departamen:
            self.dept_input = QLineEdit(str(departamen))

            id_rol = dictRolEmp.get('id_rol') if isinstance(dictRolEmp,dict) else 'Sin Rol asignado asignado'
            self.role_input = QLineEdit(str(id_rol))
            
            self.role_input.setReadOnly(True)
            self.dept_input.setReadOnly(True)
            
            self.role_layout.addRow(QLabel("Departamento:"), self.dept_input)
            self.role_layout.addRow(QLabel("Rol:"), self.role_input)
            self.role_group.setLayout(self.role_layout)
        else:
            self.role_group.hide()

        # cargar usuario
        if usuario:
            self.username_input = QLineEdit(usuario.usuario)

            id_perfil = dictPerfil.get('id_perfil') if isinstance(dictPerfil, dict) else 'Sin perfil asignado'
            self.profile_input = QLineEdit(str(id_perfil))
            
            self.username_input.setReadOnly(True)
            self.profile_input.setReadOnly(True)
            
            self.user_layout.addRow(QLabel("Usuario:"), self.username_input)
            self.user_layout.addRow(QLabel("Perfil:"), self.profile_input)
            self.user_group.setLayout(self.user_layout)
        else:
            self.user_group.hide()