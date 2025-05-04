DATABASE_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "accesobiometrico",
}

ZKTECA_CONFIG = {"host": "192.168.1.201", "port": 4370}

# array accesos para los usuarios
ACCESO_TABLE = {
    "administrar personas": "persona",
    "administrar departamentos": "departamentos",
    "administrar rol": "rol",
    "administrar perfil": "permiso_perfil",
    "administrar justificacion": "justificaciones",
}

MODULOS_ACCESO = [
    ("Administrar empleados", "empleado"),
    ("Administrar usuarios", "usuario"),
    ("Administrar asistencias", "asistencia"),
    ("Administrar justificaciones", "justificacion"),
    ("Administrar reportes", "reporte"),
    ("Administrar departamentos", "departamento"),
    ("Administrar roles", "rol"),
    ("Administrar perfiles", "perfil", "perfil"),
]

##
# declaracion de los nombres de las tablas
##

# Tabla de asistencia y sus campos
TBASISTENCIA = "asistencia"
TBASISTENCIA_ID = "Id"
TBASISTENCIA_ID_EMPLEADO = "Id_Empleado"
TBASISTENCIA_FECHA = "Fecha"
TBASISTENCIA_ESTADO_ASISTENCIA = "Estado_Asistencia"


# Tabla departamento  y sus campos
TBDEPARTAMENTO = "departamento"
TBDEPARTAMENTO_ID = "Id"
TBDEPARTAMENTO_NOMBRE = "Nombre"
TBDEPARTAMENTO_DESCRIPCION = "Descripcion"


# Tabla de permisos de rol
TBPERMISOROL = "permiso_rol"
TBPERMISOROL_ID = "Id"
TBPERMISOROL_ROL_ID = "Id_rol"
TBPERMISOROL_TABLA = "nombre_tabla"
TBPERMISOROL_VER = "Ver"
TBPERMISOROL_INSERTAR = "Insertar"
TBPERMISOROL_EDITAR = "Editar"
TBPERMISOROL_ELIMINAR = "Eliminar"

# Tabla horario y sus campos
TBHORARIO = "horario"
TBHORARIO_ID = "Id"
TBHORARIO_NOMBRE_HORARIO = "Nombre_Horario"
TBHORARIO_DIAS_SEMANALES = "Dia_Semanal"
TBHORARIO_TIPO_JORNADA = "Tipo_Jornada"
TBHORARIO_HORA_INICIO = "Hora_Inicio"
TBHORARIO_HORA_FIN = "Hora_Fin"
TBHORARIO_DESCRIPCION = "Descripcion"

# PERMISO PERFIL
TBPERMISOPERFIL = "permiso_perfil"
TBPERMISOPERFIL_ID = "Id"
TBPERMISOPERFIL_PERFIL_ID = "Id_Perfil"
TBPERMISOPERFIL_TABLA = "nombre_tabla"
TBPERMISOPERFIL_VER = "Ver"
TBPERMISOPERFIL_INSERTAR = "Insertar"
TBPERMISOPERFIL_EDITAR = "Editar"
TBPERMISOPERFIL_ELIMINAR = "Eliminar"

# PERFIL
TBPERFIL = "perfil"
TBPERFIL_ID = "Id"
TBPERFIL_NOMBRE = "Nombre"
TBPERFIL_DESCRIPCION = "Descripcion"

# REPORTE
TBREPORTE = "reporte"
TBREPORTE_ID = "Id"
TBREPORTE_ID_EMPLEADO = "Id_Empleado"
TBREPORTE_FECHA_GENERACION = "Fecha_Generacion"
TBREPORTE_TIPO_REPORTE = "Tipo_Reporte"
TBREPORTE_CONTENIDO = "Contenido"
# Tabla Rol_Horario
TBROLHORARIO = "rol_horario"
TBROLHORARIO_ID = "Id"
TBROLHORARIO_ID_ROL = "Id_Rol"
TBROLHORARIO_ID_HORARIO = "Id_Horario"

TBASISTENCIA = "asistencia"
TBASISTENCIA_ID = "Id"
TBASISTENCIA_ID_EMPLEADO = "Id_Empleado"
TBASISTENCIA_FECHA = "Fecha"
TBASISTENCIA_ESTADO_ASISTENCIA = "Estado_Asistencia"

# PERFIL
TBPERFIL = "perfil"
TBPERFIL_ID = "Id"
TBPERFIL_NOMBRE = "Nombre"
TBPERFIL_DESCRIPCION = "Descripcion"

# Tabla justificacion y sus campos
TBJUSTIFICACION = "justificacion"
TBJUSTIFICACION_ID = "Id"
TBJUSTIFICACION_ID_EMPLEADO = "Id_Empleado"
TBJUSTIFICACION_ID_ASISTENCIA = "Id_Asistencia"
TBJUSTIFICACION_FECHA = "Fecha"
TBJUSTIFICACION_MOTIVO = "Motivo"
TBJUSTIFICACION_DESCRIPCION = "Descripcion"


# Variables del archivo "Tablas"

##Tabla empleado
TBEMPLEADO = "empleado"
TBEMPLEADO_ID = "Id"
TBEMPLEADO_PERSONA = "Id_Persona"
TBEMPLEADO_DEPARTAMENTO = "Id_Departamento"

# Tabla persona
TBPERSONA = "persona"
TBPERSONA_ID = "Id"
TBPERSONA_FOTO = "Foto"
TBPERSONA_NOMBRE = "Nombre"
TBPERSONA_APELLIDOS = "Apellidos"
TBPERSONA_NACIMIENTO = "Fecha_Nacimiento"
TBPERSONA_CEDULA = "Cedula"
TBPERSONA_ESTADO_CIVIL = "Estado_Civil"
TBPERSONA_CORREO = "Correo"
TBPERSONA_DIRECCION = "Direccion"

# Tabla Empleado y rol relación
TBROLEMPLEADO = "empleado_rol"
TBROLEMPLEADO_ID = "Id"
TBROLEMPLEADO_ID_EMPLEADO = "Id_Empleado"
TBROLEMPLEADO_ID_ROL = "Id_Rol"

# Tabla Usuario
TBUSUARIO = "usuario"
TBUSUARIO_ID = "Id"
TBUSUARIO_ID_PERSONA = "Id_Persona"
TBUSUARIO_USUARIO = "Usuario"
TBUSUARIO_CONTRASENA = "Contrasena"

# Tabla Usuario perfil
TBUSUARIOPERFIL = "usuario_perfil"
TBUSUARIOPERFIL_ID = "Id"
TBUSUARIOPERFIL_ID_USER = "Id_Usuario"
TBUSUARIOPERFIL_ID_PERF = "Id_Perfil"

# PERMISO PERFIL
TBPERMISOPERFIL = "permiso_perfil"
TBPERMISOPERFIL_ID = "Id"
TBPERMISOPERFIL_PERFIL_ID = "Id_Perfil"
TBPERMISOPERFIL_TABLA = "nombre_tabla"
TBPERMISOPERFIL_VER = "Ver"
TBPERMISOPERFIL_INSERTAR = "Insertar"
TBPERMISOPERFIL_EDITAR = "Editar"
TBPERMISOPERFIL_ELIMINAR = "Eliminar"

# Tabla rol
TBROL = "rol"
TBROL_ID = "Id"
TBROL_NOMBRE = "Nombre"
TBROL_DESCRIPCION = "Descripcion"

# Tabla teléfono
TBTELEFONO = "telefono"
TBTELEFONO_ID = "Id"
TBTELEFONO_ID_PERSONA = "Id_Persona"
TBTELEFONO_NUMERO = "Numero"
TBTELEFONO_TIPO_CONTACTO = "Tipo_Contacto"

# PERMISO PERFIL
TBPERMISOPERFIL = "permiso_perfil"
TBPERMISOPERFIL_ID = "Id"
TBPERMISOPERFIL_PERFIL_ID = "Id_Perfil"
TBPERMISOPERFIL_TABLA = "nombre_tabla"
TBPERMISOPERFIL_VER = "Ver"
TBPERMISOPERFIL_INSERTAR = "Insertar"
TBPERMISOPERFIL_EDITAR = "Editar"
TBPERMISOPERFIL_ELIMINAR = "Eliminar"

# Tabla justificación
TBJUSTIFICACION = "justificacion"
TBJUSTIFICACION_ID = "Id"
TBJUSTIFICACION_ID_EMPLEADO = "Id_Empleado"
TBJUSTIFICACION_ID_ASISTENCIA = "Id_Asistencia"
TBJUSTIFICACION_FECHA = "Fecha"
TBJUSTIFICACION_MOTIVO = "Motivo"
TBJUSTIFICACION_DESCRIPCION = "Descripcion"
TBJUSTIFICACION_TIPO = "Tipo"

# Tabla de Solicitud de Permisos
TBSOLICITUD_PERMISO = "Solicitud_Permiso"
TBSOLICITUD_PERMISO_ID = "Id"
TBSOLICITUD_PERMISO_ID_EMPLEADO = "Id_Empleado"
TBSOLICITUD_PERMISO_TIPO = "Tipo"
TBSOLICITUD_PERMISO_FECHA_INICIO = "Fecha_Inicio"
TBSOLICITUD_PERMISO_FECHA_FIN = "Fecha_Fin"
TBSOLICITUD_PERMISO_DESCRIPCION = "Descripcion"
TBSOLICITUD_PERMISO_ESTADO = "Estado"
