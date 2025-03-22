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
        self.setWindowTitle("Sistema de Gestión de Empleados")
        self.setMinimumSize(700, 700)

        main_layout = QVBoxLayout()
        # Sección de Datos Personales con Scroll
        self.personal_group = QGroupBox("Datos Personales")
        personal_layout = QHBoxLayout()  # Cambiamos a QHBoxLayout
        
        # Foto del empleado (lado izquierdo)
        self.foto = QLabel()
        self.foto.setAlignment(Qt.AlignCenter)
        self.foto.setFixedSize(150, 150)  # Tamaño fijo para la foto
        self.foto.setStyleSheet("border: 2px solid #ccc; border-radius: 75px;")
        personal_layout.addWidget(self.foto)
        
        # Campos de datos personales (lado derecho)
        self.form_layout = QFormLayout()
        self.form_layout.setSpacing(10)
        
        self.nombre     = QLineEdit()
        self.apellidos  = QLineEdit()
        self.cedula     = QLineEdit()
        self.nacimiento = QLineEdit()
        self.correo     = QLineEdit()
        self.estadoCivil= QLineEdit()
        self.direccion  = QLineEdit()
        
        # Establecer los campos como solo lectura
        for field in [self.nombre, self.apellidos, self.cedula, self.nacimiento, self.correo, self.estadoCivil, self.direccion]:
            field.setReadOnly(True)
            field.setMinimumHeight(30)
        
        # Agregar los campos al form_layout en el mismo orden que se crearon
        self.form_layout.addRow(QLabel("Nombre:")    , self.nombre)
        self.form_layout.addRow(QLabel("Apellidos:") , self.apellidos)
        self.form_layout.addRow(QLabel("Cédula:")    , self.cedula)
        self.form_layout.addRow(QLabel("Nacimiento:"), self.nacimiento)
        self.form_layout.addRow(QLabel("Correo:")    , self.correo)
        self.form_layout.addRow(QLabel("Estado Civil:"), self.estadoCivil)
        self.form_layout.addRow(QLabel("Dirección:") , self.direccion)
        
        # Widget contenedor para el formulario
        form_widget = QWidget()
        form_widget.setLayout(self.form_layout)
        
        # Scroll Area para el formulario
        scroll_area_personal = QScrollArea()
        scroll_area_personal.setWidgetResizable(True)
        scroll_area_personal.setWidget(form_widget)
        personal_layout.addWidget(scroll_area_personal)
        self.personal_group.setLayout(personal_layout)
        
        # Sección de Teléfonos con Scroll
        self.phone_group = QGroupBox("Teléfonos")
        self.phone_layout = QVBoxLayout()
        
        # Widget contenedor para los teléfonos
        phone_widget = QWidget()
        phone_widget.setLayout(self.phone_layout)
        
        # Scroll Area para los teléfonos
        scroll_area_phones = QScrollArea()
        scroll_area_phones.setWidgetResizable(True)
        scroll_area_phones.setWidget(phone_widget)
        
        self.phone_group.setLayout(QVBoxLayout())
        self.phone_group.layout().addWidget(scroll_area_phones)
        
        # Sección de Rol y Departamento
        self.role_group = QGroupBox("Rol y Departamento")
        self.role_layout = QFormLayout()
        
        # Sección de Usuario
        self.user_group = QGroupBox("Cuenta de Usuario")
        self.user_layout = QFormLayout()
        
        # Agregar secciones al layout principal
        main_layout.addWidget(self.personal_group)
        main_layout.addWidget(self.phone_group)
        main_layout.addWidget(self.role_group)
        main_layout.addWidget(self.user_group)
        
        # Botón de cierre
        btn_close = QPushButton("Cerrar")
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
            self.role_input = QLineEdit()
            if dictRolEmp:
                id_rol = dictRolEmp.get('id_rol')
                self.role_input.setText(str(id_rol))
            
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

            id_perfil = dictPerfil.get('id_perfil') if isinstance(dictPerfil, dict) else None
            self.profile_input = QLineEdit(str(id_perfil))
            
            self.username_input.setReadOnly(True)
            self.profile_input.setReadOnly(True)
            
            self.user_layout.addRow(QLabel("Usuario:"), self.username_input)
            self.user_layout.addRow(QLabel("Perfil:"), self.profile_input)
            self.user_group.setLayout(self.user_layout)
        else:
            self.user_group.hide()