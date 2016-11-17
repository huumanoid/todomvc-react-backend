CREATE DATABASE IF NOT EXISTS`_ru_hmnid_testdb`;

-- CREATE USER IF NOT EXISTS `_ru_hmnid_tstusr`;
GRANT ALL ON `_ru_hmnid_testdb`.* TO '_ru_hmnid_tstusr'@'localhost' IDENTIFIED BY 'password';

USE `_ru_hmnid_testdb`;
CREATE TABLE IF NOT EXISTS `list`(
        id INTEGER KEY AUTO_INCREMENT,
        title VARCHAR(256) NOT NULL,
        completed BOOLEAN NOT NULL DEFAULT 0
    );
