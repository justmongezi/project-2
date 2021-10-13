-- --------------------------------------------------------
-- Host:                         localhost
-- Server version:               10.4.19-MariaDB - mariadb.org binary distribution
-- Server OS:                    Win32
-- HeidiSQL Version:             11.2.0.6213
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- Dumping database structure for car_wash_db
CREATE DATABASE IF NOT EXISTS `car_wash_db` /*!40100 DEFAULT CHARACTER SET utf8 */;
USE `car_wash_db`;

-- Dumping structure for table car_wash_db.administrator
CREATE TABLE IF NOT EXISTS `administrator` (
  `adNo` varchar(10) NOT NULL,
  `adName` varchar(255) NOT NULL,
  `adDOB` date DEFAULT NULL,
  `adSystemPrivilege` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`adNo`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Dumping data for table car_wash_db.administrator: ~0 rows (approximately)
/*!40000 ALTER TABLE `administrator` DISABLE KEYS */;
/*!40000 ALTER TABLE `administrator` ENABLE KEYS */;

-- Dumping structure for table car_wash_db.appointment
CREATE TABLE IF NOT EXISTS `appointment` (
  `aNo` varchar(4) NOT NULL,
  `cID` varchar(5) DEFAULT NULL,
  `aDate` date DEFAULT NULL,
  `aTime` time DEFAULT NULL,
  PRIMARY KEY (`aNo`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Dumping data for table car_wash_db.appointment: ~0 rows (approximately)
/*!40000 ALTER TABLE `appointment` DISABLE KEYS */;
INSERT INTO `appointment` (`aNo`, `cID`, `aDate`, `aTime`) VALUES
	('1', '1', '2021-06-09', '08:05:00');
/*!40000 ALTER TABLE `appointment` ENABLE KEYS */;

-- Dumping structure for table car_wash_db.customer
CREATE TABLE IF NOT EXISTS `customer` (
  `cID` int(11) NOT NULL AUTO_INCREMENT,
  `cName` varchar(50) NOT NULL,
  `cUsername` varchar(50) NOT NULL,
  `cPassword` varchar(255) NOT NULL,
  `email` varchar(100) NOT NULL,
  PRIMARY KEY (`cID`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8;

-- Dumping data for table car_wash_db.customer: ~14 rows (approximately)
/*!40000 ALTER TABLE `customer` DISABLE KEYS */;
INSERT INTO `customer` (`cID`, `cName`, `cUsername`, `cPassword`, `email`) VALUES
	(1, 'Mongezi Masango', 'mongezi', 'system', 'momasango1@gmail.com'),
	(2, 'Mongezi Shaun', 'justmongezi1', 'system1', 'masangomsm@gmail.com'),
	(5, 'Thembisile', 'thembi', 'password123', 'khombimdhluli16@gmail.com'),
	(6, 'Andre', 'andre', 'ad123', 'aristotile.bulsie@gmail.com'),
	(7, 'Karen', 'kdog21', 'poplappie', 'karen@gmail.com'),
	(8, 'Michael', 'bigmike', 'soros', 'Michael@gmail.com'),
	(9, 'Jordan', 'jordanriver', 'Tellus', 'jordan@gmail.com'),
	(10, 'Megan', 'megzintheair', 'adidasho21', 'jmegan@gmail.com'),
	(11, 'George', 'gman', 'sistersnapped', 'george@gmail.com'),
	(12, 'Hulisani', 'whosid', 'owner123+', 'hman@gmail.com'),
	(13, 'Joe', 'joetheone', 'favechild', 'momasango2@gmail.com'),
	(14, 'Jonah', 'jdog333', 'System123', 'jdoge@gmail.com'),
	(15, 'Sarah', 'hillsarah', 'LadyGagafave', 'sarahhill@gmail.com'),
	(16, 'Stephenie Germanotta', 'ladygaga', 'ladygaga', 'ladygaga@icloud.com'),
	(17, 'Shaun', 'shaun123', 'yeehee', '123shaun@gmail.com'),
	(20, 'Shane Grey', 'shanegrey123', 'Regina', 'realshxnegrxy@gmail.com');
/*!40000 ALTER TABLE `customer` ENABLE KEYS */;

-- Dumping structure for table car_wash_db.service
CREATE TABLE IF NOT EXISTS `service` (
  `sID` int(11) NOT NULL AUTO_INCREMENT,
  `sName` varchar(255) DEFAULT NULL,
  `sDesc` text DEFAULT NULL,
  `sPrice` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`sID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Dumping data for table car_wash_db.service: ~0 rows (approximately)
/*!40000 ALTER TABLE `service` DISABLE KEYS */;
/*!40000 ALTER TABLE `service` ENABLE KEYS */;

-- Dumping structure for table car_wash_db.vehicle
CREATE TABLE IF NOT EXISTS `vehicle` (
  `vID` int(11) NOT NULL AUTO_INCREMENT,
  `vMake` varchar(50) NOT NULL,
  `custID` varchar(50) NOT NULL,
  `servID` varchar(255) NOT NULL,
  `vReg` varchar(8) DEFAULT NULL,
  PRIMARY KEY (`vID`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

-- Dumping data for table car_wash_db.vehicle: ~0 rows (approximately)
/*!40000 ALTER TABLE `vehicle` DISABLE KEYS */;
INSERT INTO `vehicle` (`vID`, `vMake`, `custID`, `servID`, `vReg`) VALUES
	(1, 'Toyota Corolla', '1', '1', NULL);
/*!40000 ALTER TABLE `vehicle` ENABLE KEYS */;

-- Dumping structure for table car_wash_db.vehicle_service
CREATE TABLE IF NOT EXISTS `vehicle_service` (
  `vID` int(11) NOT NULL,
  `sID` int(11) NOT NULL,
  KEY `fk_vehicle_service` (`vID`),
  KEY `fk_vehicle_service_2` (`sID`),
  CONSTRAINT `fk_vehicle_service` FOREIGN KEY (`vID`) REFERENCES `vehicle` (`vID`),
  CONSTRAINT `fk_vehicle_service_2` FOREIGN KEY (`sID`) REFERENCES `service` (`sID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Dumping data for table car_wash_db.vehicle_service: ~0 rows (approximately)
/*!40000 ALTER TABLE `vehicle_service` DISABLE KEYS */;
/*!40000 ALTER TABLE `vehicle_service` ENABLE KEYS */;

/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
