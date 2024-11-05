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
TBPERSONA_APELLIDO1 = "Apellido1"
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

# Tabla horario y sus campos
TBHORARIO = "horario"
TBHORARIO_ID = "Id"
TBHORARIO_DIAS_SEMANALES = "Dias_Semanales"
TBHORARIO_TIPO_JORNADA = "Tipo_Jornada"
TBHORARIO_HORA_INICIO = "Hora_Inicio"
TBHORARIO_HORA_FIN = "Hora_Fin"
TBHORARIO_DESCRIPCION = "Descripcion"
