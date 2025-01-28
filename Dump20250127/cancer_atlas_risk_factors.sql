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
-- Table structure for table `risk_factors`
--

DROP TABLE IF EXISTS `risk_factors`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `risk_factors` (
  `state_id` tinyint unsigned NOT NULL,
  `inactivity_rate` decimal(5,2) unsigned NOT NULL,
  `cigarette_use_rate` decimal(5,2) unsigned NOT NULL,
  PRIMARY KEY (`state_id`),
  UNIQUE KEY `state_id_UNIQUE` (`state_id`),
  CONSTRAINT `fk_risk_factors_states` FOREIGN KEY (`state_id`) REFERENCES `states` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `risk_factors`
--

LOCK TABLES `risk_factors` WRITE;
/*!40000 ALTER TABLE `risk_factors` DISABLE KEYS */;
INSERT INTO `risk_factors` VALUES (1,30.70,20.20),(2,20.80,17.40),(3,23.30,14.90),(4,31.10,20.20),(5,21.20,10.00),(6,17.70,13.50),(7,22.60,12.10),(8,27.20,15.90),(9,20.20,12.70),(10,27.30,14.80),(11,27.40,16.30),(12,21.70,12.30),(13,22.20,15.30),(14,24.90,14.50),(15,28.50,19.20),(16,24.50,16.40),(17,24.80,16.20),(18,32.50,23.60),(19,30.80,21.90),(20,24.80,17.60),(21,23.20,12.70),(22,23.30,12.00),(23,24.30,18.70),(24,21.00,14.60),(25,33.20,20.40),(26,27.80,19.60),(27,21.50,16.60),(28,24.30,14.70),(29,26.00,15.70),(30,21.50,15.90),(31,25.40,16.25),(32,23.70,16.00),(33,25.90,12.70),(34,24.60,18.50),(35,25.60,17.00),(36,26.90,20.80),(37,30.50,18.90),(38,20.70,14.50),(39,24.70,17.30),(40,25.30,13.30),(41,27.60,17.50),(42,25.30,18.30),(43,28.90,19.90),(44,27.50,14.70),(45,18.20,7.90),(46,19.60,15.10),(47,23.40,14.00),(48,18.40,12.60),(49,30.10,23.80),(50,21.90,15.40),(51,23.60,18.40);
/*!40000 ALTER TABLE `risk_factors` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-01-27 15:08:02
