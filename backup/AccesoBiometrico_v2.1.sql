/*
    El nombre de la base de datos debe ser `accesobiometrico`
*/

CREATE TABLE `Asistencia`
(
 `Id`                int NOT NULL AUTO_INCREMENT,
 `Id_Empleado`       int NOT NULL,
 `Fecha`             date NOT NULL,
 `Estado_Asistencia` varchar(45) NOT NULL,
 PRIMARY KEY (`Id`)
);

CREATE TABLE `Departamento`
(
 `Id`          int NOT NULL AUTO_INCREMENT,
 `Nombre`      varchar(50) NOT NULL,
 `Descripcion` varchar(100),
 PRIMARY KEY (`Id`)
);

CREATE TABLE `Detalle_Asistencia`
(
 `Id`               int NOT NULL AUTO_INCREMENT,
 `Id_Asistencia`    int NOT NULL,
 `Hora_Entrada`     time NOT NULL,
 `Hora_Salida`      time NOT NULL,
 `Horas_Trabajadas` decimal(5,2) NOT NULL,
 PRIMARY KEY (`Id`)
);

CREATE TABLE `Empleado`
(
 `Id`              int NOT NULL AUTO_INCREMENT,
 `Id_Persona`      int NOT NULL,
 `Id_Departamento` int,
 `Id_Horario`      int,
 PRIMARY KEY (`Id`)
);

CREATE TABLE `Empleado_Rol`
(
 `Id`          int NOT NULL AUTO_INCREMENT,
 `Id_Empleado` int NOT NULL,
 `Id_Rol`      int NOT NULL,
 PRIMARY KEY (`Id`)
);

CREATE TABLE `Horario`
(
 `Id`           int NOT NULL AUTO_INCREMENT,
 `Dia_Semanal`  varchar(20) NOT NULL,
 `Tipo_Jornada` varchar(30) NOT NULL,
 `Hora_Inicio`  time NOT NULL,
 `Hora_Fin`     time NOT NULL,
 `Descripcion`  varchar(100),
 PRIMARY KEY (`Id`)
);

CREATE TABLE `Huella`
(
 `Id`          int NOT NULL AUTO_INCREMENT,
 `Id_Empleado` int NOT NULL,
 `Huella`      varbinary(255) NOT NULL,
 PRIMARY KEY (`Id`)
);

CREATE TABLE `Justificacion`
(
 `Id`            int NOT NULL AUTO_INCREMENT,
 `Id_Empleado`   int NOT NULL,
 `Id_Asistencia` int NOT NULL,
 `Fecha`         date NOT NULL,
 `Motivo`        varchar(100) NOT NULL,
 `Descripcion`   text,
 PRIMARY KEY (`Id`)
);

CREATE TABLE `Mantenimiento`
(
 `Id`               int NOT NULL AUTO_INCREMENT,
 `Id_usuario`       int NOT NULL,
 `Fecha`            date NOT NULL,
 `Accion_Realizada` varchar(50) NOT NULL,
 `Descripcion`      text,
 PRIMARY KEY (`Id`)
);

CREATE TABLE `Permiso_Rol`
(
 `Id`           int NOT NULL AUTO_INCREMENT,
 `Id_rol`       int NOT NULL ,
 `nombre_tabla` varchar(45) NOT NULL ,
 `Ver`          boolean NOT NULL ,
 `Insertar`     boolean NOT NULL ,
 `Editar`       boolean NOT NULL ,
 `Eliminar`     boolean NOT NULL ,

 PRIMARY KEY (`Id`)
);

CREATE TABLE `Persona`
(
 `Id`               int NOT NULL AUTO_INCREMENT,
 `Foto`             mediumblob NULL,
 `Nombre`           varchar(50) NOT NULL,
 `Apellido1`        varchar(50) NOT NULL,
 `Apellido2`        varchar(50) NOT NULL,
 `Fecha_Nacimiento` date NOT NULL,
 `Cedula`           varchar(20) NOT NULL UNIQUE,
 `Estado_Civil`     varchar(20) NOT NULL,
 `Correo`           varchar(255) NOT NULL UNIQUE,
 `Direccion`        varchar(50) NOT NULL,
 PRIMARY KEY (`Id`)
);

CREATE TABLE `Reporte`
(
 `Id`               int NOT NULL AUTO_INCREMENT,
 `Id_Empleado`      int,
 `Fecha_Generacion` date,
 `Tipo_Reporte`     varchar(50),
 `Contenido`        text,
 PRIMARY KEY (`Id`)
);

CREATE TABLE `Rol`
(
 `Id`          int NOT NULL AUTO_INCREMENT,
 `Nombre`      varchar(50) NOT NULL,
 `Descripcion` varchar(100),
 PRIMARY KEY (`Id`)
);

CREATE TABLE `Solicitud_Permiso`
(
 `Id`           int NOT NULL AUTO_INCREMENT,
 `Id_Empleado`  int NOT NULL,
 `Tipo`         varchar(50) NOT NULL,
 `Fecha_Inicio` date NOT NULL,
 `Fecha_Fin`    date NOT NULL,
 `Descripcion`  text NOT NULL,
 `Estado`       varchar(20) NOT NULL,
 PRIMARY KEY (`Id`)
);

CREATE TABLE `Telefono`
(
 `Id`            int NOT NULL AUTO_INCREMENT,
 `Id_Persona`    int NOT NULL,
 `Numero`        varchar(15) NOT NULL,
 `Tipo_Contacto` varchar(45) NOT NULL,
 PRIMARY KEY (`Id`)
);

CREATE TABLE `Usuario`
(
 `Id`         int NOT NULL AUTO_INCREMENT,
 `Id_Persona` int NOT NULL,
 `Usuario`    varchar(50) NOT NULL UNIQUE,
 `Contrasena` varchar(100) NOT NULL,
 PRIMARY KEY (`Id`)
);

CREATE TABLE `Usuario_Rol`
(
 `Id`         int NOT NULL AUTO_INCREMENT,
 `Id_Usuario` int NOT NULL,
 `Id_Rol`     int NOT NULL,
 PRIMARY KEY (`Id`)
);

-- Crear las restricciones FOREIGN KEY después de crear todas las tablas
ALTER TABLE `Asistencia` 
ADD CONSTRAINT `FK_Asistencia_Empleado` FOREIGN KEY (`Id_Empleado`) REFERENCES `Empleado` (`Id`);

ALTER TABLE `Detalle_Asistencia` 
ADD CONSTRAINT `FK_Detalle_Asistencia_Asistencia` FOREIGN KEY (`Id_Asistencia`) REFERENCES `Asistencia` (`Id`);

ALTER TABLE `Empleado` 
ADD CONSTRAINT `FK_Empleado_Departamento` FOREIGN KEY (`Id_Departamento`) REFERENCES `Departamento` (`Id`);

ALTER TABLE `Empleado` 
ADD CONSTRAINT `FK_Empleado_Horario` FOREIGN KEY (`Id_Horario`) REFERENCES `Horario` (`Id`);

ALTER TABLE `Empleado` 
ADD CONSTRAINT `FK_Empleado_Persona` FOREIGN KEY (`Id_Persona`) REFERENCES `Persona` (`Id`);

ALTER TABLE `Empleado_Rol` 
ADD CONSTRAINT `FK_Empleado_Rol_Empleado` FOREIGN KEY (`Id_Empleado`) REFERENCES `Empleado` (`Id`);

ALTER TABLE `Empleado_Rol` 
ADD CONSTRAINT `FK_Empleado_Rol_Rol` FOREIGN KEY (`Id_Rol`) REFERENCES `Rol` (`Id`);

ALTER TABLE `Huella` 
ADD CONSTRAINT `FK_Huella_Empleado` FOREIGN KEY (`Id_Empleado`) REFERENCES `Empleado` (`Id`);

ALTER TABLE `Justificacion` 
ADD CONSTRAINT `FK_Justificacion_Empleado` FOREIGN KEY (`Id_Empleado`) REFERENCES `Empleado` (`Id`);

ALTER TABLE `Justificacion` 
ADD CONSTRAINT `FK_Justificacion_Asistencia` FOREIGN KEY (`Id_Asistencia`) REFERENCES `Asistencia` (`Id`);

ALTER TABLE `Mantenimiento` 
ADD CONSTRAINT `FK_Mantenimiento_Usuario` FOREIGN KEY (`Id_usuario`) REFERENCES `Usuario` (`Id`);

ALTER TABLE `Permiso_Rol` 
ADD CONSTRAINT `FK_Permiso_Rol_Rol` FOREIGN KEY (`Id_rol`) REFERENCES `Rol` (`Id`);

ALTER TABLE `Reporte` 
ADD CONSTRAINT `FK_Reporte_Empleado` FOREIGN KEY (`Id_Empleado`) REFERENCES `Empleado` (`Id`);

ALTER TABLE `Solicitud_Permiso` 
ADD CONSTRAINT `FK_Solicitud_Permiso_Empleado` FOREIGN KEY (`Id_Empleado`) REFERENCES `Empleado` (`Id`);

ALTER TABLE `Telefono` 
ADD CONSTRAINT `FK_Telefono_Persona` FOREIGN KEY (`Id_Persona`) REFERENCES `Persona` (`Id`);

ALTER TABLE `Usuario` 
ADD CONSTRAINT `FK_Usuario_Persona` FOREIGN KEY (`Id_Persona`) REFERENCES `Persona` (`Id`);

ALTER TABLE `Usuario_Rol` 
ADD CONSTRAINT `FK_Usuario_Rol_Usuario` FOREIGN KEY (`Id_Usuario`) REFERENCES `Usuario` (`Id`);

ALTER TABLE `Usuario_Rol` 
ADD CONSTRAINT `FK_Usuario_Rol_Rol` FOREIGN KEY (`Id_Rol`) REFERENCES `Rol` (`Id`);
