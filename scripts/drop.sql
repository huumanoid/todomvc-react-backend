CREATE DATABASE IF NOT EXISTS `_ru_hmnid_testtmpdb`;
GRANT ALL ON `_ru_hmnid_testtmpdb`.* TO '_ru_hmnid_tstusr'@'localhost';
DROP USER '_ru_hmnid_tstusr'@'localhost';
DROP DATABASE `_ru_hmnid_testtmpdb`;
USE `_ru_hmnid_testdb`;
DROP TABLE IF EXISTS `list`;
DROP DATABASE IF EXISTS `_ru_hmnid_testdb`;
