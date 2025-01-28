CREATE DATABASE  IF NOT EXISTS `cancer_atlas` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `cancer_atlas`;
-- MySQL dump 10.13  Distrib 8.0.40, for Win64 (x86_64)
--
-- Host: localhost    Database: cancer_atlas
-- ------------------------------------------------------
-- Server version	9.1.0

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `states`
--

DROP TABLE IF EXISTS `states`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `states` (
  `id` tinyint unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `abbreviation` varchar(2) NOT NULL,
  `latitude` decimal(10,7) NOT NULL,
  `longitude` decimal(10,7) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=52 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `states`
--

LOCK TABLES `states` WRITE;
/*!40000 ALTER TABLE `states` DISABLE KEYS */;
INSERT INTO `states` VALUES (1,'alabama','AL',32.3182310,-86.9022980),(2,'alaska','AK',63.5887530,-154.4930620),(3,'arizona','AZ',34.0489280,-111.0937310),(4,'arkansas','AR',35.2010500,-91.8318330),(5,'california','CA',36.7782610,-119.4179320),(6,'colorado','CO',39.5500510,-105.7820670),(7,'connecticut','CT',41.6032210,-73.0877490),(8,'delaware','DE',38.9108320,-75.5276700),(9,'district of columbia','DC',38.9059850,-77.0334180),(10,'florida','FL',27.6648270,-81.5157540),(11,'georgia','GA',32.1574350,-82.9071230),(12,'hawaii','HI',19.8986820,-155.6658570),(13,'idaho','ID',44.0682020,-114.7420410),(14,'illinois','IL',40.6331250,-89.3985280),(15,'indiana','IN',40.5512170,-85.6023640),(16,'iowa','IA',41.8780030,-93.0977020),(17,'kansas','KS',39.0119020,-98.4842460),(18,'kentucky','KY',37.8393330,-84.2700180),(19,'louisiana','LA',31.2448230,-92.1450240),(20,'maine','ME',45.2537830,-69.4454690),(21,'maryland','MD',39.0457550,-76.6412710),(22,'massachusetts','MA',42.4072110,-71.3824370),(23,'michigan','MI',44.3148440,-85.6023640),(24,'minnesota','MN',46.7295530,-94.6859000),(25,'mississippi','MS',32.3546680,-89.3985280),(26,'missouri','MO',37.9642530,-91.8318330),(27,'montana','MT',46.8796820,-110.3625660),(28,'nebraska','NE',41.4925370,-99.9018130),(29,'nevada','NV',38.8026100,-116.4193890),(30,'new hampshire','NH',43.1938520,-71.5723950),(31,'new jersey','NJ',40.0583240,-74.4056610),(32,'new mexico','NM',34.9727300,-105.0323630),(33,'new york','NY',43.2994280,-74.2179330),(34,'north carolina','NC',35.7595730,-79.0193000),(35,'north dakota','ND',47.5514930,-101.0020120),(36,'ohio','OH',40.4172870,-82.9071230),(37,'oklahoma','OK',35.0077520,-97.0928770),(38,'oregon','OR',43.8041330,-120.5542010),(39,'pennsylvania','PA',41.2033220,-77.1945250),(40,'rhode island','RI',41.5800950,-71.4774290),(41,'south carolina','SC',33.8360810,-81.1637250),(42,'south dakota','SD',43.9695150,-99.9018130),(43,'tennessee','TN',35.5174910,-86.5804470),(44,'texas','TX',31.9685990,-99.9018130),(45,'utah','UT',39.3209800,-111.0937310),(46,'vermont','VT',44.5588030,-72.5778410),(47,'virginia','VA',37.4315730,-78.6568940),(48,'washington','WA',47.7510740,-120.7401390),(49,'west virginia','WV',38.5976260,-80.4549030),(50,'wisconsin','WI',43.7844400,-88.7878680),(51,'wyoming','WY',43.0759680,-107.2902840);
/*!40000 ALTER TABLE `states` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-01-27 15:08:06
