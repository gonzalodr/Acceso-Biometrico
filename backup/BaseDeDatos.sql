CREATE TABLE Persona (
  Id INT PRIMARY KEY,
  Nombre VARCHAR(50),
  Apellido VARCHAR(50),
  Cedula VARCHAR(20) UNIQUE,
  Estado_Civil VARCHAR(20)
);

CREATE TABLE Tipo_Contacto (
  Id INT PRIMARY KEY,
  Tipo VARCHAR(20),
  Categoria VARCHAR(10)
);

CREATE TABLE Telefono (
  Id INT PRIMARY KEY,
  Numero VARCHAR(15),
  Id_Tipo_Contacto INT,
  Id_Persona INT,
  FOREIGN KEY (Id_Tipo_Contacto) REFERENCES Tipo_Contacto(Id),
  FOREIGN KEY (Id_Persona) REFERENCES Persona(Id)
);

CREATE TABLE Correo (
  Id INT PRIMARY KEY,
  Direccion VARCHAR(100),
  Id_Tipo_Contacto INT,
  Id_Persona INT,
  FOREIGN KEY (Id_Tipo_Contacto) REFERENCES Tipo_Contacto(Id),
  FOREIGN KEY (Id_Persona) REFERENCES Persona(Id)
);

CREATE TABLE Empleado (
  Id INT PRIMARY KEY,
  Id_Persona INT,
  Id_Departamento INT,
  Id_Horario INT,
  FOREIGN KEY (Id_Persona) REFERENCES Persona(Id),
  FOREIGN KEY (Id_Departamento) REFERENCES Departamento(Id),
  FOREIGN KEY (Id_Horario) REFERENCES Horario(Id)
);

CREATE TABLE Huella (
  Id INT PRIMARY KEY,
  Datos BLOB,
  Id_Empleado INT,
  FOREIGN KEY (Id_Empleado) REFERENCES Empleado(Id)
);

CREATE TABLE Empleado_Rol (
  Id INT PRIMARY KEY,
  Id_Empleado INT,
  Id_Rol INT,
  FOREIGN KEY (Id_Empleado) REFERENCES Empleado(Id),
  FOREIGN KEY (Id_Rol) REFERENCES Rol(Id)
);

CREATE TABLE Asistencia (
  Id INT PRIMARY KEY,
  Fecha DATE,
  Id_Empleado INT,
  FOREIGN KEY (Id_Empleado) REFERENCES Empleado(Id)
);

CREATE TABLE Detalle_Asistencia (
  Id INT PRIMARY KEY,
  Hora_Entrada TIME,
  Hora_Salida TIME,
  Horas_Trabajadas DECIMAL(5,2),
  Id_Asistencia INT,
  FOREIGN KEY (Id_Asistencia) REFERENCES Asistencia(Id)
);

CREATE TABLE Administrador (
  Id INT PRIMARY KEY,
  Usuario VARCHAR(50),
  Contrasena VARCHAR(100),
  Id_Persona INT,
  FOREIGN KEY (Id_Persona) REFERENCES Persona(Id)
);

CREATE TABLE Reporte (
  Id INT PRIMARY KEY,
  Fecha_Generacion DATE,
  Tipo_Reporte VARCHAR(50),
  Contenido TEXT,
  Id_Empleado INT,
  FOREIGN KEY (Id_Empleado) REFERENCES Empleado(Id)
);

CREATE TABLE Justificacion (
  Id INT PRIMARY KEY,
  Fecha DATE,
  Motivo VARCHAR(100),
  Descripcion TEXT,
  Id_Empleado INT,
  FOREIGN KEY (Id_Empleado) REFERENCES Empleado(Id)
);

CREATE TABLE Departamento (
  Id INT PRIMARY KEY,
  Nombre VARCHAR(50),
  Descripcion VARCHAR(100)
);

CREATE TABLE Rol (
  Id INT PRIMARY KEY,
  Nombre VARCHAR(50),
  Descripcion VARCHAR(100)
);

CREATE TABLE Horario (
  Id INT PRIMARY KEY,
  Descripcion VARCHAR(100),
  Hora_Inicio TIME,
  Hora_Fin TIME
);

CREATE TABLE Permiso (
  Id INT PRIMARY KEY,
  Tipo VARCHAR(50),
  Fecha_Inicio DATE,
  Fecha_Fin DATE,
  Descripcion TEXT,
  Estado VARCHAR(20),
  Id_Empleado INT,
  FOREIGN KEY (Id_Empleado) REFERENCES Empleado(Id)
);

CREATE TABLE Mantenimiento (
  Id INT PRIMARY KEY,
  Fecha DATE,
  Accion_Realizada VARCHAR(50),
  Descripcion TEXT,
  Id_Administrador INT,
  FOREIGN KEY (Id_Administrador) REFERENCES Administrador(Id)
);
