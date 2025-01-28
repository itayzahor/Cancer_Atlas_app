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
-- Table structure for table `environmental`
--

DROP TABLE IF EXISTS `environmental`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `environmental` (
  `state_id` tinyint unsigned NOT NULL,
  `air_quality_index` decimal(5,2) unsigned NOT NULL,
  `co2_emissions` decimal(5,2) unsigned NOT NULL,
  PRIMARY KEY (`state_id`),
  CONSTRAINT `fk_environmental_states` FOREIGN KEY (`state_id`) REFERENCES `states` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `environmental`
--

LOCK TABLES `environmental` WRITE;
/*!40000 ALTER TABLE `environmental` DISABLE KEYS */;
INSERT INTO `environmental` VALUES (1,39.07,21.50),(2,22.75,56.30),(3,43.69,11.10),(4,43.73,20.70),(5,43.73,8.40),(6,40.19,15.20),(7,39.63,10.30),(8,43.00,12.40),(9,45.00,3.90),(10,43.21,10.40),(11,43.48,11.40),(12,26.00,12.60),(13,26.11,10.70),(14,43.52,14.60),(15,42.33,23.90),(16,43.14,22.30),(17,36.73,21.20),(18,41.42,24.30),(19,43.23,41.80),(20,35.36,10.80),(21,41.31,8.20),(22,38.69,8.50),(23,39.85,15.30),(24,34.62,14.80),(25,43.00,22.10),(26,41.14,18.30),(27,24.04,26.30),(28,33.00,24.40),(29,38.44,12.70),(30,38.29,9.90),(31,40.00,10.00),(32,32.69,22.00),(33,37.27,8.40),(34,39.63,10.90),(35,39.56,73.20),(36,43.22,16.70),(37,45.24,21.70),(38,27.52,8.90),(39,39.63,16.50),(40,37.33,9.30),(41,43.69,12.70),(42,31.50,17.20),(43,40.78,12.90),(44,43.00,22.10),(45,41.53,17.80),(46,30.75,8.50),(47,36.70,11.10),(48,25.39,9.60),(49,39.85,44.60),(50,39.00,15.40),(51,34.95,96.60);
/*!40000 ALTER TABLE `environmental` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-01-27 15:08:13
