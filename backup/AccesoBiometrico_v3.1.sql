CREATE TABLE `Asistencia`
(
        `Id`                int PRIMARY KEY NOT NULL AUTO_INCREMENT ,
        `Id_Empleado`       int NOT NULL ,
        `Fecha`             date NOT NULL ,
        `Estado_Asistencia` varchar(45) NOT NULL
);

CREATE TABLE `Departamento`
(
        `Id`          int PRIMARY KEY NOT NULL AUTO_INCREMENT ,
        `Nombre`      varchar(50) UNIQUE NOT NULL ,
        `Descripcion` varchar(100) NULL
);

CREATE TABLE `Detalle_Asistencia`
(
        `Id`               int PRIMARY KEY NOT NULL AUTO_INCREMENT ,
        `Id_Asistencia`    int NOT NULL ,
        `Hora_Entrada`     time NOT NULL ,
        `Hora_Salida`      time NOT NULL ,
        `Horas_Trabajadas` decimal(5,2) NULL
);

CREATE TABLE `Empleado`
(
        `Id`              int PRIMARY KEY NOT NULL AUTO_INCREMENT ,
        `Id_Persona`      int NOT NULL ,
        `Id_Departamento` int NULL
);

CREATE TABLE `Empleado_Rol`
(
        `Id`          int PRIMARY KEY NOT NULL AUTO_INCREMENT ,
        `Id_Empleado` int NOT NULL ,
        `Id_Rol`      int NOT NULL
);


CREATE TABLE `Horario`
(
        `Id`             int PRIMARY KEY NOT NULL AUTO_INCREMENT ,
        `Nombre_Horario`  varchar(20) NOT NULL,
        `Dia_Semanal`    varchar(20) NOT NULL ,
        `Tipo_Jornada`   varchar(30) NOT NULL ,
        `Hora_Inicio`    time NOT NULL ,
        `Hora_Fin`       time NOT NULL ,
        `Descripcion`    varchar(100) NULL
);


CREATE TABLE `Huella`
(
        `Id`          int PRIMARY KEY NOT NULL AUTO_INCREMENT ,
        `Id_Empleado` int UNIQUE NOT NULL ,
        `Huella`      varbinary(255) NOT NULL
);

CREATE TABLE `Justificacion`
(
        `Id`            int PRIMARY KEY NOT NULL AUTO_INCREMENT ,
        `Id_Empleado`   int NOT NULL ,
        `Id_Asistencia` int NOT NULL ,
        `Fecha`         date NOT NULL ,
        `Motivo`        varchar(100) NOT NULL ,
        `Descripcion`   text NULL
);

CREATE TABLE `Mantenimiento`
(
        `Id`               int PRIMARY KEY NOT NULL AUTO_INCREMENT ,
        `Id_usuario`       int NOT NULL ,
        `Fecha`            date NOT NULL ,
        `Accion_Realizada` varchar(50) NOT NULL ,
        `Descripcion`      text NULL
);

CREATE TABLE `Perfil`
(
        `Id`          int PRIMARY KEY NOT NULL AUTO_INCREMENT,
        `Nombre`      varchar(50) UNIQUE NOT NULL ,
        `Descripcion` varchar(100) NULL 
);


CREATE TABLE `Permiso_Perfil`
(
        `Id`           int PRIMARY KEY NOT NULL AUTO_INCREMENT ,
        `Id_Perfil`    int NOT NULL ,
        `nombre_tabla` varchar(45) NOT NULL ,
        `Ver`          boolean NOT NULL ,
        `Insertar`     boolean NOT NULL ,
        `Editar`       boolean NOT NULL ,
        `Eliminar`     boolean NOT NULL
);

CREATE TABLE `Persona`
(
        `Id`               int PRIMARY KEY NOT NULL AUTO_INCREMENT ,
        `Foto`             blob NULL ,
        `Nombre`           varchar(50) NOT NULL ,
        `Apellidos`        varchar(50) NOT NULL ,
        `Fecha_Nacimiento` date NOT NULL ,
        `Cedula`           varchar(20) UNIQUE NOT NULL ,
        `Estado_Civil`     varchar(20) NOT NULL ,
        `Correo`           varchar(255) UNIQUE NOT NULL ,
        `Direccion`        varchar(50) NOT NULL
);


CREATE TABLE `Reporte`
(
        `Id`               int PRIMARY KEY NOT NULL AUTO_INCREMENT ,
        `Id_Empleado`      int NULL ,
        `Fecha_Generacion` datetime NULL ,
        `Tipo_Reporte`     varchar(50) NULL ,
        `Contenido`        text NULL
);

CREATE TABLE `Rol`
(
        `Id`          int PRIMARY KEY NOT NULL AUTO_INCREMENT ,
        `Nombre`      varchar(50) UNIQUE NOT NULL ,
        `Descripcion` varchar(100) NULL
);


CREATE TABLE `Rol_Horario`
(
        `Id`     int PRIMARY KEY NOT NULL AUTO_INCREMENT ,
        `Id_Rol` int NOT NULL ,
        `Id_Horario` int NOT NULL 
);

CREATE TABLE `Solicitud_Permiso`
(
        `Id`           int PRIMARY KEY NOT NULL AUTO_INCREMENT ,
        `Id_Empleado`  int NOT NULL ,
        `Tipo`         varchar(50) NOT NULL ,
        `Fecha_Inicio` date NOT NULL ,
        `Fecha_Fin`    date NOT NULL ,
        `Descripcion`  text NOT NULL ,
        `Estado`       varchar(20) NOT NULL 
);

CREATE TABLE `Telefono`
(
        `Id`            int PRIMARY KEY NOT NULL AUTO_INCREMENT ,
        `Id_Persona`    int NOT NULL ,
        `Numero`        varchar(15) UNIQUE NOT NULL ,
        `Tipo_Contacto` varchar(45) NOT NULL 
);

CREATE TABLE `Usuario`
(
        `Id`         int PRIMARY KEY NOT NULL AUTO_INCREMENT,
        `Id_Persona` int NOT NULL ,
        `Usuario`    varchar(50) UNIQUE NOT NULL ,
        `Contrasena` varchar(100) NOT NULL 
);

CREATE TABLE `Usuario_Perfil`
(
        `Id`         int PRIMARY KEY NOT NULL AUTO_INCREMENT ,
        `Id_Perfil`  int NOT NULL ,
        `Id_Usuario` int NOT NULL 
);



-- Now define the foreign key constraints:

ALTER TABLE `Asistencia`
ADD CONSTRAINT `FK_Asistencia_Empleado` FOREIGN KEY (`Id_Empleado`) REFERENCES `Empleado` (`Id`);

ALTER TABLE `Detalle_Asistencia`
ADD CONSTRAINT `FK_Detalle_Asistencia_Asistencia` FOREIGN KEY (`Id_Asistencia`) REFERENCES `Asistencia` (`Id`);

ALTER TABLE `Empleado`
ADD CONSTRAINT `FK_Empleado_Departamento` FOREIGN KEY (`Id_Departamento`) REFERENCES `Departamento` (`Id`),
ADD CONSTRAINT `FK_Empleado_Persona` FOREIGN KEY (`Id_Persona`) REFERENCES `Persona` (`Id`);

ALTER TABLE `Empleado_Rol`
ADD CONSTRAINT `FK_Empleado_Rol_Empleado` FOREIGN KEY (`Id_Empleado`) REFERENCES `Empleado` (`Id`),
ADD CONSTRAINT `FK_Empleado_Rol_Rol` FOREIGN KEY (`Id_Rol`) REFERENCES `Rol` (`Id`);


ALTER TABLE `Huella`
ADD CONSTRAINT `FK_Huella_Empleado` FOREIGN KEY (`Id_Empleado`) REFERENCES `Empleado` (`Id`);

ALTER TABLE `Justificacion`
ADD CONSTRAINT `FK_Justificacion_Asistencia` FOREIGN KEY (`Id_Asistencia`) REFERENCES `Asistencia` (`Id`),
ADD CONSTRAINT `FK_Justificacion_Empleado` FOREIGN KEY (`Id_Empleado`) REFERENCES `Empleado` (`Id`);

ALTER TABLE `Mantenimiento`
ADD CONSTRAINT `FK_Mantenimiento_Usuario` FOREIGN KEY (`Id_usuario`) REFERENCES `Usuario` (`Id`);

ALTER TABLE `Permiso_Perfil`
ADD CONSTRAINT `FK_Permiso_Perfil_Perfil` FOREIGN KEY (`Id_Perfil`) REFERENCES `Perfil` (`Id`);

ALTER TABLE `Reporte`
ADD CONSTRAINT `FK_Reporte_Empleado` FOREIGN KEY (`Id_Empleado`) REFERENCES `Empleado` (`Id`);

ALTER TABLE `Rol_Horario`
ADD CONSTRAINT `FK_Rol_Horario_Rol` FOREIGN KEY (`Id_Rol`) REFERENCES `Rol` (`Id`),
ADD CONSTRAINT `FK_Rol_Horario_Horario` FOREIGN KEY (`Id_Horario`) REFERENCES `Horario` (`Id`);

ALTER TABLE `Solicitud_Permiso`
ADD CONSTRAINT `FK_Solicitud_Permiso_Empleado` FOREIGN KEY (`Id_Empleado`) REFERENCES `Empleado` (`Id`);

ALTER TABLE `Telefono`
ADD CONSTRAINT `FK_Telefono_Persona` FOREIGN KEY (`Id_Persona`) REFERENCES `Persona` (`Id`);

ALTER TABLE `Usuario`
ADD CONSTRAINT `FK_Usuario_Persona` FOREIGN KEY (`Id_Persona`) REFERENCES `Persona` (`Id`);

ALTER TABLE `Usuario_Perfil`
ADD CONSTRAINT `FK_Usuario_Perfil_Perfil` FOREIGN KEY (`Id_Perfil`) REFERENCES `Perfil` (`Id`),
ADD CONSTRAINT `FK_Usuario_Perfil_Usuario` FOREIGN KEY (`Id_Usuario`) REFERENCES `Usuario` (`Id`);

-- Insertando en la tabla Persona
-- Iniciando una transacción
START TRANSACTION;

-- Insertando en la tabla Persona
INSERT INTO `Persona` (Nombre, Apellidos, Fecha_Nacimiento, Cedula, Estado_Civil, Correo, Direccion)
VALUES ('admin', 'admin', '2000-01-01', '0000000000', 'vacio', 'admin@admin.admin', 'direccion admin');

-- Obteniendo el ID de la persona recién insertada
SET @IdPersona = LAST_INSERT_ID();

-- Insertando en la tabla Empleado usando el ID de la persona insertada
INSERT INTO Empleado (Id_Persona) VALUES (@IdPersona);

-- Insertando en la tabla Usuario usando el ID de la persona insertada
INSERT INTO `Usuario` (Id_Persona, Usuario, Contrasena)
VALUES (@IdPersona, 'admin', '$2a$12$38OuH8cvPIAxyqLqm240f.8TVh8o8eReC.UCWS2HJYBaqsmPlFNCC');

-- Confirmando la transacción
COMMIT;

-- Contrasena 12345678