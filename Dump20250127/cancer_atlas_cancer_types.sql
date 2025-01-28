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
-- Table structure for table `cancer_types`
--

DROP TABLE IF EXISTS `cancer_types`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cancer_types` (
  `id` tinyint unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=27 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cancer_types`
--

LOCK TABLES `cancer_types` WRITE;
/*!40000 ALTER TABLE `cancer_types` DISABLE KEYS */;
INSERT INTO `cancer_types` VALUES (1,'Brain and Other Nervous System'),(2,'Cervix'),(3,'Colon and Rectum'),(4,'Corpus and Uterus, NOS'),(5,'Esophagus'),(6,'Female Breast'),(7,'Female Breast, <i>in situ</i>'),(8,'Hodgkin Lymphoma'),(9,'Kaposi Sarcoma'),(10,'Kidney and Renal Pelvis'),(11,'Larynx'),(12,'Leukemias'),(13,'Liver and Intrahepatic Bile Duct'),(14,'Lung and Bronchus'),(15,'Melanomas of the Skin'),(16,'Mesothelioma'),(17,'Myeloma'),(18,'Non-Hodgkin Lymphoma'),(19,'Oral Cavity and Pharynx'),(20,'Ovary'),(21,'Pancreas'),(22,'Stomach'),(23,'Thyroid'),(24,'Urinary Bladder'),(25,'Prostate'),(26,'Testis');
/*!40000 ALTER TABLE `cancer_types` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-01-27 15:07:59
