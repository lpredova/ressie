SET @OLD_UNIQUE_CHECKS = @@UNIQUE_CHECKS, UNIQUE_CHECKS = 0;
SET @OLD_FOREIGN_KEY_CHECKS = @@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS = 0;
SET @OLD_SQL_MODE = @@SQL_MODE, SQL_MODE = 'TRADITIONAL,ALLOW_INVALID_DATES';

CREATE DATABASE ressie;

CREATE USER 'ressie'@'localhost'
  IDENTIFIED BY '123456';
GRANT ALL PRIVILEGES ON *.* TO 'ressie'@'localhost'
WITH GRANT OPTION;

CREATE USER 'ressie'@'%'
  IDENTIFIED BY '123456';
GRANT ALL PRIVILEGES ON *.* TO 'ressie'@'%'
WITH GRANT OPTION;


-- -----------------------------------------------------
-- Schema ressie
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `ressie`
  DEFAULT CHARACTER SET utf8
  COLLATE utf8_general_ci;
USE `ressie`;

-- -----------------------------------------------------
-- Table `ressie`.`incident`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `ressie`.`incident` (
  `id`        INT          NOT NULL AUTO_INCREMENT,
  `payload`   TEXT         NULL,
  `message`   VARCHAR(255) NULL,
  `type`      VARCHAR(255) NULL,
  `createdAt` INT          NOT NULL,
  PRIMARY KEY (`id`)
)
  ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table `ressie`.`request_counts`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `ressie`.`request_counts` (
  `id`        INT NOT NULL AUTO_INCREMENT,
  `count`     INT NOT NULL,
  `createdAt` INT NOT NULL,
  PRIMARY KEY (`id`)
)
  ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table `ressie`.`request_length`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `ressie`.`request_length` (
  `id`        INT NOT NULL AUTO_INCREMENT,
  `length`    INT NOT NULL,
  `createdAt` INT NOT NULL,
  PRIMARY KEY (`id`)
)
  ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table `ressie`.`response_times`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `ressie`.`response_times` (
  `id`        INT NOT NULL AUTO_INCREMENT,
  `time`    INT NOT NULL,
  `createdAt` INT NOT NULL,
  PRIMARY KEY (`id`)
)
  ENGINE = InnoDB;

SET SQL_MODE = @OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS = @OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS = @OLD_UNIQUE_CHECKS;
