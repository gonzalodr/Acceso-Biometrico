DATABASE_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "accesobiometrico",
}

##
# declaracion de los nombres de las tablas
##
# Tabla persona y sus campos
TBPERSONA = "persona"
TBPERSONA_ID = "Id"
TBPERSONA_FOTO = "Foto"
TBPERSONA_NOMBRE = "Nombre"
TBPERSONA_APELLIDOS = "Apellidos"
TBPERSONA_APELLIDO2 = "Apellido2"
TBPERSONA_NACIMIENTO = "Fecha_Nacimiento"
TBPERSONA_CEDULA = "Cedula"
TBPERSONA_ESTADO_CIVIL = "Estado_Civil"
TBPERSONA_CORREO = "Correo"
TBPERSONA_DIRECCION = "Direccion"

# Tabla departamento  y sus campos
TBDEPARTAMENTO = "departamento"
TBDEPARTAMENTO_ID = "Id"
TBDEPARTAMENTO_NOMBRE = "Nombre"
TBDEPARTAMENTO_DESCRIPCION = "Descripcion"

# Tabla de usuarios y sus campos
TBUSUARIO_ID = "Id"
TBUSUARIO_ID_PERSONA = "id_persona"
TBUSUARIO_USUARIO = "Usuario"
TBUSUARIO_CONTRASENA = "contrasena"

# Tabla rol y sus campos
TBROL = "rol"
TBROL_ID = "Id"
TBROL_NOMBRE = "Nombre"
TBROL_DESCRIPCION = "Descripcion"

##
#   Tabla usuario y sus campos
#
TBUSUARIO = "usuario"
TBUSUARIOIDPERSONA = "Id_Persona"
TBUSUARIOUSUARIO = "Usuario"
TBUSUARIOCONTRASENA = "Contrasena"

##
#    Tabla de permisos de rol
#


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

# Tabla Rol_Horario
TBROLHORARIO = "rol_horario"
TBROLHORARIO_ID = "Id"
TBROLHORARIO_ID_ROL = "Id_Rol"
TBROLHORARIO_ID_HORARIO = "Id_Horario"
