-- MySQL dump 10.13  Distrib 8.0.38, for Win64 (x86_64)
--
-- Host: localhost    Database: alumni_portal
-- ------------------------------------------------------
-- Server version	9.0.0

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
-- Table structure for table `account_alumni`
--

DROP TABLE IF EXISTS `account_alumni`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `account_alumni` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `website` varchar(200) NOT NULL,
  `linked_in` varchar(200) NOT NULL,
  `twitter_handle` varchar(225) NOT NULL,
  `address` longtext NOT NULL,
  `postal_code` varchar(10) NOT NULL,
  `registered_on` date DEFAULT NULL,
  `location_id` bigint DEFAULT NULL,
  `member_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `account_alumni_location_id_97ed667f_fk_account_location_id` (`location_id`),
  KEY `account_alumni_member_id_7af35b7d_fk_account_member_id` (`member_id`),
  CONSTRAINT `account_alumni_location_id_97ed667f_fk_account_location_id` FOREIGN KEY (`location_id`) REFERENCES `account_location` (`id`),
  CONSTRAINT `account_alumni_member_id_7af35b7d_fk_account_member_id` FOREIGN KEY (`member_id`) REFERENCES `account_member` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `account_alumni`
--

LOCK TABLES `account_alumni` WRITE;
/*!40000 ALTER TABLE `account_alumni` DISABLE KEYS */;
INSERT INTO `account_alumni` VALUES (2,'http://example.com','http://linkedin.com/in/example','@example','123 Example St, Example City','12345','2024-10-07',1,9),(3,'http://industry2.com','','','','',NULL,NULL,29);
/*!40000 ALTER TABLE `account_alumni` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `account_batch`
--

DROP TABLE IF EXISTS `account_batch`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `account_batch` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `title` varchar(55) NOT NULL,
  `start_year` int NOT NULL,
  `end_year` int NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `account_batch`
--

LOCK TABLES `account_batch` WRITE;
/*!40000 ALTER TABLE `account_batch` DISABLE KEYS */;
INSERT INTO `account_batch` VALUES (1,'batch 1',2020,2024),(2,'batch 2',2023,2026);
/*!40000 ALTER TABLE `account_batch` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `account_country`
--

DROP TABLE IF EXISTS `account_country`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `account_country` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `country_name` varchar(50) NOT NULL,
  `country_code` varchar(10) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `account_country`
--

LOCK TABLES `account_country` WRITE;
/*!40000 ALTER TABLE `account_country` DISABLE KEYS */;
INSERT INTO `account_country` VALUES (1,'India','91');
/*!40000 ALTER TABLE `account_country` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `account_course`
--

DROP TABLE IF EXISTS `account_course`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `account_course` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `title` varchar(255) NOT NULL,
  `graduate` varchar(55) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `department_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `account_course_department_id_b852fca9_fk_account_department_id` (`department_id`),
  CONSTRAINT `account_course_department_id_b852fca9_fk_account_department_id` FOREIGN KEY (`department_id`) REFERENCES `account_department` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `account_course`
--

LOCK TABLES `account_course` WRITE;
/*!40000 ALTER TABLE `account_course` DISABLE KEYS */;
INSERT INTO `account_course` VALUES (1,'course 1','UG',1,1),(2,'course 2','UG',1,2);
/*!40000 ALTER TABLE `account_course` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `account_department`
--

DROP TABLE IF EXISTS `account_department`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `account_department` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `short_name` varchar(55) NOT NULL,
  `full_name` varchar(255) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `account_department`
--

LOCK TABLES `account_department` WRITE;
/*!40000 ALTER TABLE `account_department` DISABLE KEYS */;
INSERT INTO `account_department` VALUES (1,'CSE','Computer Science and Engineering',1),(2,'IT','information Technology',1);
/*!40000 ALTER TABLE `account_department` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `account_industry`
--

DROP TABLE IF EXISTS `account_industry`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `account_industry` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `title` varchar(255) NOT NULL,
  `description` varchar(255) NOT NULL,
  `website` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `account_industry`
--

LOCK TABLES `account_industry` WRITE;
/*!40000 ALTER TABLE `account_industry` DISABLE KEYS */;
INSERT INTO `account_industry` VALUES (1,'Industry 1','industry','http://industry.com');
/*!40000 ALTER TABLE `account_industry` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `account_industry_type`
--

DROP TABLE IF EXISTS `account_industry_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `account_industry_type` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `type_name` varchar(255) NOT NULL,
  `description` longtext NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `account_industry_type`
--

LOCK TABLES `account_industry_type` WRITE;
/*!40000 ALTER TABLE `account_industry_type` DISABLE KEYS */;
INSERT INTO `account_industry_type` VALUES (1,'Education and training','Education and training');
/*!40000 ALTER TABLE `account_industry_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `account_institution`
--

DROP TABLE IF EXISTS `account_institution`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `account_institution` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `title` varchar(255) NOT NULL,
  `description` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `account_institution`
--

LOCK TABLES `account_institution` WRITE;
/*!40000 ALTER TABLE `account_institution` DISABLE KEYS */;
INSERT INTO `account_institution` VALUES (1,'Karpagam Insitute of Technology','');
/*!40000 ALTER TABLE `account_institution` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `account_location`
--

DROP TABLE IF EXISTS `account_location`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `account_location` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `location` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `account_location`
--

LOCK TABLES `account_location` WRITE;
/*!40000 ALTER TABLE `account_location` DISABLE KEYS */;
INSERT INTO `account_location` VALUES (1,'Coimbatore');
/*!40000 ALTER TABLE `account_location` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `account_member`
--

DROP TABLE IF EXISTS `account_member`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `account_member` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `gender` varchar(10) NOT NULL,
  `dob` date DEFAULT NULL,
  `blood_group` varchar(11) DEFAULT NULL,
  `profile_picture` varchar(100) DEFAULT NULL,
  `about_me` longtext,
  `mobile_no` varchar(25) DEFAULT NULL,
  `email` varchar(254) NOT NULL,
  `batch_id` bigint DEFAULT NULL,
  `course_id` bigint DEFAULT NULL,
  `user_id` int DEFAULT NULL,
  `salutation_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  KEY `account_member_salutation_id_2ac8785f_fk_account_salutation_id` (`salutation_id`),
  KEY `account_member_batch_id_9439c83c_fk_account_batch_id` (`batch_id`),
  KEY `account_member_course_id_976cf24f_fk_account_course_id` (`course_id`),
  CONSTRAINT `account_member_batch_id_9439c83c_fk_account_batch_id` FOREIGN KEY (`batch_id`) REFERENCES `account_batch` (`id`),
  CONSTRAINT `account_member_course_id_976cf24f_fk_account_course_id` FOREIGN KEY (`course_id`) REFERENCES `account_course` (`id`),
  CONSTRAINT `account_member_salutation_id_2ac8785f_fk_account_salutation_id` FOREIGN KEY (`salutation_id`) REFERENCES `account_salutation` (`id`),
  CONSTRAINT `account_member_user_id_86266795_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=51 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `account_member`
--

LOCK TABLES `account_member` WRITE;
/*!40000 ALTER TABLE `account_member` DISABLE KEYS */;
INSERT INTO `account_member` VALUES (7,'M','1985-05-12','A_POSITIVE','profile_pictures/3135715.png','','1234567890','21ita62@karpagamtech.ac.in',1,1,24,1),(9,'M','1990-01-01','O_POSITIVE','profile_pictures/111.jpg',NULL,'1234567890','sakthikumar@gmail.com',1,1,25,1),(10,'M','1990-01-01','O_POSITIVE','',NULL,'1234567890','prveen@gmail.com',1,1,34,1),(29,'M','1985-05-12','A_POSITIVE','','','1234567890','20csa24@karpagamtech.ac.in',1,1,2,1),(30,'F','1990-08-20','B_NEGATIVE','(optional)',NULL,'987654321','vikashvip780@gmail.com',NULL,NULL,NULL,2),(35,'M','1985-05-12','A_POSITIVE','(optional)',NULL,'1234567890','mitun@gmail.com',1,1,49,1),(36,'F','1990-08-20','B_NEGATIVE','(optional)',NULL,'987654321','mitung12@gmail.com',NULL,NULL,50,2),(37,'M','1985-05-12','A_POSITIVE','(optional)',NULL,'1234567890','sam@gmail.com',1,1,51,1),(38,'M','1985-05-12','A_POSITIVE','(optional)',NULL,'1234567890','naveen@gmail.com',1,1,54,1),(39,'M','1985-05-12','A_POSITIVE','(optional)',NULL,'1234567890','surya@gmail.com',1,1,55,1),(40,'M','1985-05-12','A_POSITIVE','(optional)',NULL,'1234567890','afsal@gmail.com',1,1,NULL,1),(41,'F','1990-08-20','B_NEGATIVE','(optional)',NULL,'987654321','arun@gmail.com',NULL,NULL,NULL,2),(45,'M','1990-01-01','O_POSITIVE','',NULL,'1234567890','yalan@gmail.com',1,1,NULL,1),(46,'M','1990-01-01','O_POSITIVE','',NULL,'1234567890','samar@gmail.com',1,1,69,1),(49,'M','1985-05-12','A_POSITIVE','',NULL,'1234567890','afsal234@gmail.com',NULL,1,NULL,1),(50,'F','1990-08-20','B_NEGATIVE','',NULL,'987654321','arun234@gmail.com',NULL,NULL,NULL,2);
/*!40000 ALTER TABLE `account_member` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `account_member_education`
--

DROP TABLE IF EXISTS `account_member_education`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `account_member_education` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `degree` varchar(255) NOT NULL,
  `start_year` int NOT NULL,
  `end_year` int DEFAULT NULL,
  `is_currently_pursuing` tinyint(1) NOT NULL,
  `institute_id` bigint NOT NULL,
  `location_id` bigint DEFAULT NULL,
  `member_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `account_member_educa_institute_id_275495d7_fk_account_i` (`institute_id`),
  KEY `account_member_educa_location_id_41f7ae0c_fk_account_l` (`location_id`),
  KEY `account_member_education_member_id_a968d688_fk_account_member_id` (`member_id`),
  CONSTRAINT `account_member_educa_institute_id_275495d7_fk_account_i` FOREIGN KEY (`institute_id`) REFERENCES `account_institution` (`id`),
  CONSTRAINT `account_member_educa_location_id_41f7ae0c_fk_account_l` FOREIGN KEY (`location_id`) REFERENCES `account_location` (`id`),
  CONSTRAINT `account_member_education_member_id_a968d688_fk_account_member_id` FOREIGN KEY (`member_id`) REFERENCES `account_member` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `account_member_education`
--

LOCK TABLES `account_member_education` WRITE;
/*!40000 ALTER TABLE `account_member_education` DISABLE KEYS */;
INSERT INTO `account_member_education` VALUES (1,'Bachelor of Science',2020,2024,1,1,1,9),(2,'IT',2024,2028,1,1,1,9),(3,'Information Technology',2024,NULL,1,1,1,10),(4,'CSE',2024,0,1,1,1,10);
/*!40000 ALTER TABLE `account_member_education` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `account_member_experience`
--

DROP TABLE IF EXISTS `account_member_experience`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `account_member_experience` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `start_date` date NOT NULL,
  `end_date` date DEFAULT NULL,
  `is_currently_working` tinyint(1) NOT NULL,
  `industry_id` bigint NOT NULL,
  `location_id` bigint NOT NULL,
  `member_id` bigint NOT NULL,
  `role_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `account_member_exper_industry_id_28dd0035_fk_account_i` (`industry_id`),
  KEY `account_member_exper_location_id_545ffe50_fk_account_l` (`location_id`),
  KEY `account_member_exper_member_id_9d1aea16_fk_account_m` (`member_id`),
  KEY `account_member_experience_role_id_1e1c64e8_fk_account_role_id` (`role_id`),
  CONSTRAINT `account_member_exper_industry_id_28dd0035_fk_account_i` FOREIGN KEY (`industry_id`) REFERENCES `account_industry` (`id`),
  CONSTRAINT `account_member_exper_location_id_545ffe50_fk_account_l` FOREIGN KEY (`location_id`) REFERENCES `account_location` (`id`),
  CONSTRAINT `account_member_exper_member_id_9d1aea16_fk_account_m` FOREIGN KEY (`member_id`) REFERENCES `account_member` (`id`),
  CONSTRAINT `account_member_experience_role_id_1e1c64e8_fk_account_role_id` FOREIGN KEY (`role_id`) REFERENCES `account_role` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `account_member_experience`
--

LOCK TABLES `account_member_experience` WRITE;
/*!40000 ALTER TABLE `account_member_experience` DISABLE KEYS */;
INSERT INTO `account_member_experience` VALUES (1,'2023-01-01',NULL,1,1,1,9,1),(2,'2022-01-01','2022-12-25',0,1,1,9,1);
/*!40000 ALTER TABLE `account_member_experience` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `account_member_skills`
--

DROP TABLE IF EXISTS `account_member_skills`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `account_member_skills` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `member_id` bigint NOT NULL,
  `skill_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `account_member_skills_member_id_bb99dfba_fk_account_member_id` (`member_id`),
  KEY `account_member_skills_skill_id_83f11e5e_fk_account_skill_id` (`skill_id`),
  CONSTRAINT `account_member_skills_member_id_bb99dfba_fk_account_member_id` FOREIGN KEY (`member_id`) REFERENCES `account_member` (`id`),
  CONSTRAINT `account_member_skills_skill_id_83f11e5e_fk_account_skill_id` FOREIGN KEY (`skill_id`) REFERENCES `account_skill` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `account_member_skills`
--

LOCK TABLES `account_member_skills` WRITE;
/*!40000 ALTER TABLE `account_member_skills` DISABLE KEYS */;
INSERT INTO `account_member_skills` VALUES (3,9,1),(4,9,2);
/*!40000 ALTER TABLE `account_member_skills` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `account_role`
--

DROP TABLE IF EXISTS `account_role`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `account_role` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `role` varchar(255) NOT NULL,
  `description` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `account_role`
--

LOCK TABLES `account_role` WRITE;
/*!40000 ALTER TABLE `account_role` DISABLE KEYS */;
INSERT INTO `account_role` VALUES (1,'Devoleper','Devoleper');
/*!40000 ALTER TABLE `account_role` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `account_salutation`
--

DROP TABLE IF EXISTS `account_salutation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `account_salutation` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `salutation` varchar(10) NOT NULL,
  `description` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `account_salutation`
--

LOCK TABLES `account_salutation` WRITE;
/*!40000 ALTER TABLE `account_salutation` DISABLE KEYS */;
INSERT INTO `account_salutation` VALUES (1,'Mr','mr'),(2,'Mrs','mrs'),(3,'Dr','docter');
/*!40000 ALTER TABLE `account_salutation` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `account_skill`
--

DROP TABLE IF EXISTS `account_skill`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `account_skill` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `skill` varchar(255) NOT NULL,
  `description` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `account_skill`
--

LOCK TABLES `account_skill` WRITE;
/*!40000 ALTER TABLE `account_skill` DISABLE KEYS */;
INSERT INTO `account_skill` VALUES (1,'Team work','Team work'),(2,'Python','A high-level programming language.'),(3,'skill 3','work'),(4,'Team','ok');
/*!40000 ALTER TABLE `account_skill` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `account_social_media`
--

DROP TABLE IF EXISTS `account_social_media`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `account_social_media` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `title` varchar(55) NOT NULL,
  `icon` varchar(100) NOT NULL,
  `url` varchar(255) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `account_social_media`
--

LOCK TABLES `account_social_media` WRITE;
/*!40000 ALTER TABLE `account_social_media` DISABLE KEYS */;
/*!40000 ALTER TABLE `account_social_media` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
INSERT INTO `auth_group` VALUES (5,'Administrator'),(1,'Alumni'),(4,'Alumni_Manager'),(3,'Faculty'),(2,'Student');
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=165 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add user',4,'add_user'),(14,'Can change user',4,'change_user'),(15,'Can delete user',4,'delete_user'),(16,'Can view user',4,'view_user'),(17,'Can add content type',5,'add_contenttype'),(18,'Can change content type',5,'change_contenttype'),(19,'Can delete content type',5,'delete_contenttype'),(20,'Can view content type',5,'view_contenttype'),(21,'Can add session',6,'add_session'),(22,'Can change session',6,'change_session'),(23,'Can delete session',6,'delete_session'),(24,'Can view session',6,'view_session'),(25,'Can add batch',7,'add_batch'),(26,'Can change batch',7,'change_batch'),(27,'Can delete batch',7,'delete_batch'),(28,'Can view batch',7,'view_batch'),(29,'Can add country',8,'add_country'),(30,'Can change country',8,'change_country'),(31,'Can delete country',8,'delete_country'),(32,'Can view country',8,'view_country'),(33,'Can add department',9,'add_department'),(34,'Can change department',9,'change_department'),(35,'Can delete department',9,'delete_department'),(36,'Can view department',9,'view_department'),(37,'Can add industry',10,'add_industry'),(38,'Can change industry',10,'change_industry'),(39,'Can delete industry',10,'delete_industry'),(40,'Can view industry',10,'view_industry'),(41,'Can add industry_ type',11,'add_industry_type'),(42,'Can change industry_ type',11,'change_industry_type'),(43,'Can delete industry_ type',11,'delete_industry_type'),(44,'Can view industry_ type',11,'view_industry_type'),(45,'Can add institution',12,'add_institution'),(46,'Can change institution',12,'change_institution'),(47,'Can delete institution',12,'delete_institution'),(48,'Can view institution',12,'view_institution'),(49,'Can add location',13,'add_location'),(50,'Can change location',13,'change_location'),(51,'Can delete location',13,'delete_location'),(52,'Can view location',13,'view_location'),(53,'Can add role',14,'add_role'),(54,'Can change role',14,'change_role'),(55,'Can delete role',14,'delete_role'),(56,'Can view role',14,'view_role'),(57,'Can add salutation',15,'add_salutation'),(58,'Can change salutation',15,'change_salutation'),(59,'Can delete salutation',15,'delete_salutation'),(60,'Can view salutation',15,'view_salutation'),(61,'Can add skill',16,'add_skill'),(62,'Can change skill',16,'change_skill'),(63,'Can delete skill',16,'delete_skill'),(64,'Can view skill',16,'view_skill'),(65,'Can add social_ media',17,'add_social_media'),(66,'Can change social_ media',17,'change_social_media'),(67,'Can delete social_ media',17,'delete_social_media'),(68,'Can view social_ media',17,'view_social_media'),(69,'Can add course',18,'add_course'),(70,'Can change course',18,'change_course'),(71,'Can delete course',18,'delete_course'),(72,'Can view course',18,'view_course'),(73,'Can add member',19,'add_member'),(74,'Can change member',19,'change_member'),(75,'Can delete member',19,'delete_member'),(76,'Can view member',19,'view_member'),(77,'Can add alumni',20,'add_alumni'),(78,'Can change alumni',20,'change_alumni'),(79,'Can delete alumni',20,'delete_alumni'),(80,'Can view alumni',20,'view_alumni'),(81,'Can add member_ education',21,'add_member_education'),(82,'Can change member_ education',21,'change_member_education'),(83,'Can delete member_ education',21,'delete_member_education'),(84,'Can view member_ education',21,'view_member_education'),(85,'Can add member_ experience',22,'add_member_experience'),(86,'Can change member_ experience',22,'change_member_experience'),(87,'Can delete member_ experience',22,'delete_member_experience'),(88,'Can view member_ experience',22,'view_member_experience'),(89,'Can add member_ skills',23,'add_member_skills'),(90,'Can change member_ skills',23,'change_member_skills'),(91,'Can delete member_ skills',23,'delete_member_skills'),(92,'Can view member_ skills',23,'view_member_skills'),(93,'Can add user group',24,'add_usergroup'),(94,'Can change user group',24,'change_usergroup'),(95,'Can delete user group',24,'delete_usergroup'),(96,'Can view user group',24,'view_usergroup'),(97,'Can add business directory',25,'add_businessdirectory'),(98,'Can change business directory',25,'change_businessdirectory'),(99,'Can delete business directory',25,'delete_businessdirectory'),(100,'Can view business directory',25,'view_businessdirectory'),(101,'Can add job comment',26,'add_jobcomment'),(102,'Can change job comment',26,'change_jobcomment'),(103,'Can delete job comment',26,'delete_jobcomment'),(104,'Can view job comment',26,'view_jobcomment'),(105,'Can add job post',27,'add_jobpost'),(106,'Can change job post',27,'change_jobpost'),(107,'Can delete job post',27,'delete_jobpost'),(108,'Can view job post',27,'view_jobpost'),(109,'Can add application',28,'add_application'),(110,'Can change application',28,'change_application'),(111,'Can delete application',28,'delete_application'),(112,'Can view application',28,'view_application'),(113,'Can add ticket',29,'add_ticket'),(114,'Can change ticket',29,'change_ticket'),(115,'Can delete ticket',29,'delete_ticket'),(116,'Can view ticket',29,'view_ticket'),(117,'Can add ticket assignment',30,'add_ticketassignment'),(118,'Can change ticket assignment',30,'change_ticketassignment'),(119,'Can delete ticket assignment',30,'delete_ticketassignment'),(120,'Can view ticket assignment',30,'view_ticketassignment'),(121,'Can add ticket reply',31,'add_ticketreply'),(122,'Can change ticket reply',31,'change_ticketreply'),(123,'Can delete ticket reply',31,'delete_ticketreply'),(124,'Can view ticket reply',31,'view_ticketreply'),(125,'Can add ticket category',32,'add_ticketcategory'),(126,'Can change ticket category',32,'change_ticketcategory'),(127,'Can delete ticket category',32,'delete_ticketcategory'),(128,'Can view ticket category',32,'view_ticketcategory'),(129,'Can add ticket status',33,'add_ticketstatus'),(130,'Can change ticket status',33,'change_ticketstatus'),(131,'Can delete ticket status',33,'delete_ticketstatus'),(132,'Can view ticket status',33,'view_ticketstatus'),(133,'Can add event like',34,'add_eventlike'),(134,'Can change event like',34,'change_eventlike'),(135,'Can delete event like',34,'delete_eventlike'),(136,'Can view event like',34,'view_eventlike'),(137,'Can add event category',35,'add_eventcategory'),(138,'Can change event category',35,'change_eventcategory'),(139,'Can delete event category',35,'delete_eventcategory'),(140,'Can view event category',35,'view_eventcategory'),(141,'Can add registration response',36,'add_registrationresponse'),(142,'Can change registration response',36,'change_registrationresponse'),(143,'Can delete registration response',36,'delete_registrationresponse'),(144,'Can view registration response',36,'view_registrationresponse'),(145,'Can add event comment',37,'add_eventcomment'),(146,'Can change event comment',37,'change_eventcomment'),(147,'Can delete event comment',37,'delete_eventcomment'),(148,'Can view event comment',37,'view_eventcomment'),(149,'Can add event registration',38,'add_eventregistration'),(150,'Can change event registration',38,'change_eventregistration'),(151,'Can delete event registration',38,'delete_eventregistration'),(152,'Can view event registration',38,'view_eventregistration'),(153,'Can add event',39,'add_event'),(154,'Can change event',39,'change_event'),(155,'Can delete event',39,'delete_event'),(156,'Can view event',39,'view_event'),(157,'Can add event question',40,'add_eventquestion'),(158,'Can change event question',40,'change_eventquestion'),(159,'Can delete event question',40,'delete_eventquestion'),(160,'Can view event question',40,'view_eventquestion'),(161,'Can add question',41,'add_question'),(162,'Can change question',41,'change_question'),(163,'Can delete question',41,'delete_question'),(164,'Can view question',41,'view_question');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=70 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES (1,'pbkdf2_sha256$870000$vwthDMJRrFRxMYgLPLKqDP$czMXTCdiJTHRYtYhYndRvrG+xg6+UGdSCRuPgSDz20c=','2024-10-24 12:11:47.332596',1,'admin','','','',1,1,'2024-09-25 12:04:13.000000'),(2,'pbkdf2_sha256$870000$wUEcg4R8ZIRDtbNxCbe2bd$JUwDvkZWO4GhxSy2vM/d4jtrSSV7QfQjW/VJw+c2Uuc=',NULL,0,'20csa24@karpagamtech.ac.in','Mitun','G','20csa24@karpagamtech.ac.in',0,1,'2024-09-26 04:26:59.000000'),(24,'pbkdf2_sha256$870000$tFPiEv0eNb7cPjxtjyAtq4$LJbP0fu7BfPsK+MEN7JDcIFk8g6OgCUaiD974DQdJ64=',NULL,0,'21ita62@karpagamtech.ac.in','vikash','R','21ita62@karpagamtech.ac.in',0,1,'2024-09-30 06:06:33.000000'),(25,'pbkdf2_sha256$870000$IVCuy6aoviEsgdigocOYDc$R7e4VvpQkZwO+6hNw1FQ6Gio7UzjWhgXO+ifiqnGqqA=',NULL,0,'sakthikumar@gmail.com','Sakthi','Kumar','sakthikumar@gmail.com',0,1,'2024-09-30 07:02:38.000000'),(34,'pbkdf2_sha256$870000$H8lz8tF4UIuLXXtVKgLWFa$g9URx+5EP5hhk8TB1JczSh1PMm+8xHf9LM8w4pW+0yU=',NULL,0,'prveen@gmail.com','Praveen','VG','prveen@gmail.com',0,1,'2024-10-03 06:44:31.000000'),(49,'pbkdf2_sha256$870000$BRqc6tpcILRk4d2wdv0WLv$uRR/kJYwIvAI+zvyoGJMpErmZ5P+EbDUxpsYSWu81tE=',NULL,0,'mitun@gmail.com','mithun','G','mitun@gmail.com',0,1,'2024-10-05 06:32:01.000000'),(50,'pbkdf2_sha256$870000$qgXhqhs9B6xhz4AZtAwdz8$nTTBOeyeSjmR0uXbfr31OgbM8iSeeAskHyVAi3DKjgg=',NULL,0,'mitung12@gmail.com','Mithran','G','mitung12@gmail.com',0,1,'2024-10-05 06:32:05.000000'),(51,'pbkdf2_sha256$870000$RiFerjbVGeBNpneYdBPd2O$U2GcD0Bw1/+5I6DLuGLHIgTQzLrrszyMoONn0wAPTa8=',NULL,0,'sam@gmail.com','Sam','C','sam@gmail.com',0,1,'2024-10-05 06:34:49.000000'),(54,'pbkdf2_sha256$870000$Qiz8J6aythI1HhgtdHPaCs$A/IysnMgcIRm8A9jJkBbdVflS9Rb41gtPM4QnkBGHs0=',NULL,0,'naveen@gmail.com','Naveen','A','naveen@gmail.com',0,1,'2024-10-05 06:34:55.000000'),(55,'pbkdf2_sha256$870000$7sM1lQYBsgDOGUQG4Zo0g1$6V9Nh/r3o3tsdbUZanfdlC53H9NobsCOB8GjQHuxgXU=',NULL,0,'surya@gmail.com','Surya','R','surya@gmail.com',0,1,'2024-10-05 06:35:00.000000'),(56,'pbkdf2_sha256$870000$7S2sVLHcoh0mBpYpHWpFI0$87q+j9M64OOJhkyIE+RpCil4RSri7K0SUyLfKENzXKM=',NULL,0,'tamil@gmail.com','','','tamil@gmail.com',0,1,'2024-10-08 06:37:51.050679'),(57,'pbkdf2_sha256$870000$1Nne6PQhZvXRccRf9c56D4$vmpEiLTSD/ir+3tdj/LHKorQqo7SnKgn9nWuPeJl1mo=',NULL,0,'yalan@gmail.com','','','yalan@gmail.com',0,1,'2024-10-08 06:46:02.958111'),(58,'pbkdf2_sha256$870000$1txL6F9fI2FYAUZ3XXj1yt$gvxmNApit5q7CRrvjdsP1uFIWdG+G9VB4dSm+Mwe5Z0=',NULL,0,'yan@gmail.com','','','yan@gmail.com',0,1,'2024-10-08 06:49:49.165938'),(69,'pbkdf2_sha256$870000$4sKSBfDyzGnwJxuj8iT0m2$8FQQD//Ycln3s9gmujeGNXrHcDY8QB2IKiHs6JGqZOo=',NULL,0,'samar@gmail.com','','','samar@gmail.com',0,1,'2024-10-08 07:06:11.513381');
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=40 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
INSERT INTO `auth_user_groups` VALUES (15,1,4),(39,2,3),(38,2,4),(13,24,1),(14,25,3),(22,34,1),(25,49,3),(26,50,3),(27,51,3),(28,54,3),(29,55,3),(30,56,3),(31,57,3),(32,58,3),(33,69,3);
/*!40000 ALTER TABLE `auth_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=154 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
INSERT INTO `django_admin_log` VALUES (1,'2024-09-26 04:27:00.776169','2','mitun',1,'[{\"added\": {}}]',4,1),(2,'2024-09-26 04:27:22.080790','2','mitun',2,'[{\"changed\": {\"fields\": [\"First name\", \"Last name\", \"Email address\"]}}]',4,1),(3,'2024-09-26 04:29:02.167677','1','Alumni',1,'[{\"added\": {}}]',3,1),(4,'2024-09-26 04:29:07.642072','2','Student',1,'[{\"added\": {}}]',3,1),(5,'2024-09-26 04:29:31.202919','3','Faculty',1,'[{\"added\": {}}]',3,1),(6,'2024-09-26 04:29:41.514956','4','Alumni Manager',1,'[{\"added\": {}}]',3,1),(7,'2024-09-26 04:29:55.604751','5','Administrator',1,'[{\"added\": {}}]',3,1),(8,'2024-09-27 06:32:00.356804','1','computer science',1,'[{\"added\": {}}]',7,1),(9,'2024-09-27 06:32:38.043558','1','India',1,'[{\"added\": {}}]',8,1),(10,'2024-09-27 06:33:22.099275','1','Computer Science and Engineering',1,'[{\"added\": {}}]',9,1),(11,'2024-09-27 06:36:35.717157','1','batch 1',2,'[{\"changed\": {\"fields\": [\"Title\"]}}]',7,1),(12,'2024-09-27 06:37:19.222776','1','course 1',1,'[{\"added\": {}}]',18,1),(13,'2024-09-27 06:37:56.280544','1','Education and training',1,'[{\"added\": {}}]',11,1),(14,'2024-09-27 06:38:24.947114','1','Karpagam Insitute of Technology',1,'[{\"added\": {}}]',12,1),(15,'2024-09-27 06:39:20.911223','1','Coimbatore',1,'[{\"added\": {}}]',13,1),(16,'2024-09-27 06:39:47.963848','1','Devoleper',1,'[{\"added\": {}}]',14,1),(17,'2024-09-27 06:40:01.896678','1','Mr',1,'[{\"added\": {}}]',15,1),(18,'2024-09-27 06:40:29.472575','2','Mrs',1,'[{\"added\": {}}]',15,1),(19,'2024-09-27 06:40:58.958715','1','Team work',1,'[{\"added\": {}}]',16,1),(20,'2024-09-27 07:20:41.049764','5','vimal',3,'',4,1),(21,'2024-09-27 07:20:50.551245','3','arun',3,'',4,1),(22,'2024-09-27 07:21:55.643256','6','vimal',3,'',4,1),(23,'2024-09-28 07:34:04.975322','10','20csa24@karpagamtech.ac.in',3,'',4,1),(24,'2024-09-28 07:34:04.975322','11','vikashvip780@gmail.com',3,'',4,1),(25,'2024-09-28 07:36:30.234432','12','20csa24@karpagamtech.ac.in',3,'',4,1),(26,'2024-09-28 07:36:30.234432','13','vikashvip780@gmail.com',3,'',4,1),(27,'2024-09-28 07:38:33.288046','14','20csa24@karpagamtech.ac.in',3,'',4,1),(28,'2024-09-28 07:38:33.288046','15','vikashvip780@gmail.com',3,'',4,1),(29,'2024-09-28 07:40:22.406011','18','20csa24@karpagamtech.ac.in',3,'',4,1),(30,'2024-09-28 07:40:22.406011','19','vikashvip780@gmail.com',3,'',4,1),(31,'2024-09-28 07:48:21.053570','9','arun',3,'',4,1),(32,'2024-09-28 07:48:21.053570','8','vimal',3,'',4,1),(33,'2024-09-30 05:47:56.336410','22','mitung@gmail.com',3,'',4,1),(34,'2024-10-01 09:50:49.178526','1','admin',2,'[{\"changed\": {\"fields\": [\"Groups\"]}}]',4,1),(35,'2024-10-01 12:16:04.801842','2','mitun',2,'[]',4,1),(36,'2024-10-03 04:36:10.574257','20','20csa24@karpagamtech.ac.in',3,'',4,1),(37,'2024-10-03 04:36:10.574257','21','vikashvip780@gmail.com',3,'',4,1),(38,'2024-10-03 06:10:13.718908','2','Mrs',2,'[]',15,1),(39,'2024-10-03 06:10:16.969889','1','Mr',2,'[]',15,1),(40,'2024-10-03 06:27:16.345177','26','20csa24@karpagamtech.ac.in',3,'',4,1),(41,'2024-10-03 06:27:16.345177','27','vikashvip780@gmail.com',3,'',4,1),(42,'2024-10-03 06:27:52.288057','30','20csa24@karpagamtech.ac.in',3,'',4,1),(43,'2024-10-03 06:27:52.288057','31','vikashvip780@gmail.com',3,'',4,1),(44,'2024-10-03 06:34:53.143873','23','mitung@gmail.com',3,'',4,1),(45,'2024-10-03 11:44:19.455250','32','20csa24@karpagamtech.ac.in',3,'',4,1),(46,'2024-10-03 11:44:19.455250','33','vikashvip780@gmail.com',3,'',4,1),(47,'2024-10-03 11:48:35.898456','14','vikashvip780@gmail.com',3,'',19,1),(48,'2024-10-03 11:48:35.898456','13','20csa24@karpagamtech.ac.in',3,'',19,1),(49,'2024-10-03 11:49:18.851512','16','vikashvip780@gmail.com',3,'',19,1),(50,'2024-10-03 11:49:18.851512','15','20csa24@karpagamtech.ac.in',3,'',19,1),(51,'2024-10-03 11:58:12.111408','18','vikashvip780@gmail.com',3,'',19,1),(52,'2024-10-03 11:58:12.111408','17','20csa24@karpagamtech.ac.in',3,'',19,1),(53,'2024-10-03 12:00:01.548011','20','vikashvip780@gmail.com',3,'',19,1),(54,'2024-10-03 12:00:01.548011','19','20csa24@karpagamtech.ac.in',3,'',19,1),(55,'2024-10-03 12:01:41.389981','22','vikashvip780@gmail.com',3,'',19,1),(56,'2024-10-03 12:01:41.389981','21','20csa24@karpagamtech.ac.in',3,'',19,1),(57,'2024-10-03 12:03:05.286540','24','vikashvip780@gmail.com',3,'',19,1),(58,'2024-10-03 12:03:05.286540','23','20csa24@karpagamtech.ac.in',3,'',19,1),(59,'2024-10-03 12:03:58.818942','25','20csa24@karpagamtech.ac.in',3,'',19,1),(60,'2024-10-03 12:05:00.069517','27','vikashvip780@gmail.com',3,'',19,1),(61,'2024-10-03 12:05:00.069517','26','20csa24@karpagamtech.ac.in',3,'',19,1),(62,'2024-10-03 12:08:06.836024','28','20csa24@karpagamtech.ac.in',3,'',19,1),(63,'2024-10-05 06:26:08.809328','34','mitun@gmail.com',3,'',19,1),(64,'2024-10-05 06:26:08.809328','33','mitun@gmail.com',3,'',19,1),(65,'2024-10-05 06:26:08.809328','32','mitun@gmail.com',3,'',19,1),(66,'2024-10-05 06:26:08.809328','31','mitung@gmail.com',3,'',19,1),(67,'2024-10-05 06:26:29.881068','41','mitun@gmail.com',3,'',4,1),(68,'2024-10-05 06:26:29.881068','37','mitung@gmail.com',3,'',4,1),(69,'2024-10-07 04:24:24.596241','1','Industry 1',1,'[{\"added\": {}}]',10,1),(70,'2024-10-07 08:02:01.289020','24','21ita62@karpagamtech.ac.in',2,'[{\"changed\": {\"fields\": [\"First name\", \"Last name\"]}}]',4,1),(71,'2024-10-07 08:02:30.937389','49','mitun@gmail.com',2,'[{\"changed\": {\"fields\": [\"First name\", \"Last name\"]}}]',4,1),(72,'2024-10-07 08:02:56.862224','50','mitung12@gmail.com',2,'[{\"changed\": {\"fields\": [\"First name\", \"Last name\"]}}]',4,1),(73,'2024-10-07 08:03:16.988434','54','naveen@gmail.com',2,'[{\"changed\": {\"fields\": [\"First name\", \"Last name\"]}}]',4,1),(74,'2024-10-07 08:03:59.255802','34','prveen@gmail.com',2,'[{\"changed\": {\"fields\": [\"First name\", \"Last name\"]}}]',4,1),(75,'2024-10-07 08:04:10.615731','25','sakthi@gmail.com',2,'[{\"changed\": {\"fields\": [\"First name\", \"Last name\"]}}]',4,1),(76,'2024-10-07 08:04:22.712643','51','sam@gmail.com',2,'[{\"changed\": {\"fields\": [\"First name\", \"Last name\"]}}]',4,1),(77,'2024-10-07 08:04:31.607589','55','surya@gmail.com',2,'[{\"changed\": {\"fields\": [\"First name\", \"Last name\"]}}]',4,1),(78,'2024-10-08 06:50:59.562101','44','yan@gmail.com',3,'',19,1),(79,'2024-10-08 06:50:59.562101','43','yalan@gmail.com',3,'',19,1),(80,'2024-10-08 06:50:59.562101','42','tamil@gmail.com',3,'',19,1),(81,'2024-10-08 07:43:49.965298','25','sakthikumar@gmail.com',2,'[{\"changed\": {\"fields\": [\"Username\"]}}]',4,1),(82,'2024-10-08 07:44:05.975655','25','sakthikumar@gmail.com',2,'[{\"changed\": {\"fields\": [\"Email address\"]}}]',4,1),(83,'2024-10-08 11:23:56.267811','2','title 1',2,'[{\"changed\": {\"fields\": [\"Contact link\", \"Post type\"]}}]',27,1),(84,'2024-10-08 11:24:41.134539','3','title 2',2,'[{\"changed\": {\"fields\": [\"Contact link\", \"Post type\"]}}]',27,1),(85,'2024-10-08 11:24:57.480725','4','title 3',2,'[{\"changed\": {\"fields\": [\"Contact link\", \"Post type\"]}}]',27,1),(86,'2024-10-08 11:59:17.388902','4','title 3',2,'[{\"changed\": {\"fields\": [\"Posted by\"]}}]',27,1),(87,'2024-10-09 06:04:34.327677','3','sakthikumar@gmail.com - Team work',1,'[{\"added\": {}}]',23,1),(88,'2024-10-09 06:04:39.574672','4','sakthikumar@gmail.com - Python',1,'[{\"added\": {}}]',23,1),(89,'2024-10-09 06:22:36.615765','5','title 3',1,'[{\"added\": {}}]',27,1),(90,'2024-10-09 06:22:52.380412','5','title 3',3,'',27,1),(91,'2024-10-10 07:27:12.051753','1','sakthikumar@gmail.com - Alumni',3,'',20,1),(92,'2024-10-15 04:48:06.658477','1','Submitted',1,'[{\"added\": {}}]',33,1),(93,'2024-10-15 04:48:15.089419','2','Closed',1,'[{\"added\": {}}]',33,1),(94,'2024-10-15 04:48:22.778622','3','Assigned',1,'[{\"added\": {}}]',33,1),(95,'2024-10-15 04:49:01.754101','1','cat 1',1,'[{\"added\": {}}]',32,1),(96,'2024-10-15 04:49:04.995011','2','cat 2',1,'[{\"added\": {}}]',32,1),(97,'2024-10-15 04:49:09.536044','3','cat 3',1,'[{\"added\": {}}]',32,1),(98,'2024-10-15 05:20:25.934088','2','20csa24@karpagamtech.ac.in',2,'[{\"changed\": {\"fields\": [\"Username\"]}}]',4,1),(99,'2024-10-15 05:22:42.413142','29','20csa24@karpagamtech.ac.in',2,'[{\"changed\": {\"fields\": [\"User\"]}}]',19,1),(100,'2024-10-15 05:23:33.858300','3','20csa24@karpagamtech.ac.in - Alumni',1,'[{\"added\": {}}]',20,1),(101,'2024-10-15 05:40:05.485571','2','Ticket #2 - sakthikumar@gmail.com',2,'[{\"changed\": {\"fields\": [\"Alumni\", \"Priority\"]}}]',29,1),(102,'2024-10-15 06:01:19.514139','2','20csa24@karpagamtech.ac.in',2,'[{\"changed\": {\"fields\": [\"Groups\"]}}]',4,1),(103,'2024-10-15 06:01:36.876015','1','Assignment for Ticket #1 to 20csa24@karpagamtech.ac.in',2,'[{\"changed\": {\"fields\": [\"Assigned to\"]}}]',30,1),(104,'2024-10-15 06:33:50.263664','1','Assignment for Ticket #1 to 20csa24@karpagamtech.ac.in',3,'',30,1),(105,'2024-10-15 06:56:11.999950','7','21ita62@karpagamtech.ac.in',2,'[{\"changed\": {\"fields\": [\"Profile picture\"]}}]',19,1),(106,'2024-10-15 07:03:15.843747','7','21ita62@karpagamtech.ac.in',2,'[{\"changed\": {\"fields\": [\"Profile picture\"]}}]',19,1),(107,'2024-10-15 09:11:11.265144','4','Assignment for Ticket #1 to sakthikumar@gmail.com',3,'',30,1),(108,'2024-10-15 09:11:11.266144','3','Assignment for Ticket #1 to sakthikumar@gmail.com',3,'',30,1),(109,'2024-10-15 09:11:11.266144','2','Assignment for Ticket #1 to sakthikumar@gmail.com',3,'',30,1),(110,'2024-10-15 09:12:11.862044','5','Assignment for Ticket #1 to 20csa24@karpagamtech.ac.in',2,'[{\"changed\": {\"fields\": [\"Assigned to\"]}}]',30,1),(111,'2024-10-15 11:46:24.597143','2','Ticket #2 - 20csa24@karpagamtech.ac.in',2,'[{\"changed\": {\"fields\": [\"Alumni\", \"Status\"]}}]',29,1),(112,'2024-10-15 11:46:58.960570','6','Assignment for Ticket #2 to 20csa24@karpagamtech.ac.in',1,'[{\"added\": {}}]',30,1),(113,'2024-10-15 12:37:59.201164','48','arun234@gmail.com',3,'',19,1),(114,'2024-10-15 12:37:59.201164','47','afsal234@gmail.com',3,'',19,1),(115,'2024-10-16 06:44:49.234404','4','Alumni_Manager',2,'[{\"changed\": {\"fields\": [\"Name\"]}}]',3,1),(116,'2024-10-16 12:04:17.232670','29','20csa24@karpagamtech.ac.in',2,'[{\"changed\": {\"fields\": [\"Profile picture\"]}}]',19,1),(117,'2024-10-17 11:56:34.412038','3','skill 3',1,'[{\"added\": {}}]',16,1),(118,'2024-10-17 12:06:47.585456','3','title 3',3,'',27,1),(119,'2024-10-17 12:07:38.534276','4','Team',1,'[{\"added\": {}}]',16,1),(120,'2024-10-17 12:07:50.678817','4','title 3',2,'[]',27,1),(121,'2024-10-18 05:24:18.820813','6','title 4',1,'[{\"added\": {}}]',27,1),(122,'2024-10-18 05:56:13.843210','4','Open',1,'[{\"added\": {}}]',33,1),(123,'2024-10-18 05:56:18.297692','5','Replied',1,'[{\"added\": {}}]',33,1),(124,'2024-10-18 05:56:23.218248','6','On Hold',1,'[{\"added\": {}}]',33,1),(125,'2024-10-18 05:56:38.885556','3','Assigned',3,'',33,1),(126,'2024-10-18 05:56:38.885556','1','Submitted',3,'',33,1),(127,'2024-10-18 05:57:54.345204','7','A',1,'[{\"added\": {}}]',33,1),(128,'2024-10-18 05:58:00.235842','7','Assigned',2,'[{\"changed\": {\"fields\": [\"Status\"]}}]',33,1),(129,'2024-10-19 05:41:18.040189','5','Ticket #5 - sakthikumar@gmail.com',1,'[{\"added\": {}}]',29,1),(130,'2024-10-21 04:28:32.176313','1','Sample Event',2,'[{\"changed\": {\"fields\": [\"Event wallpaper\"]}}]',39,1),(131,'2024-10-21 09:00:27.098881','2','event 2',1,'[{\"added\": {}}]',39,1),(132,'2024-10-21 10:22:33.584386','1','are you ok',1,'[{\"added\": {}}]',40,1),(133,'2024-10-21 10:22:53.976595','2','are you ok with food',1,'[{\"added\": {}}]',40,1),(134,'2024-10-21 10:23:03.695670','1','20csa24@karpagamtech.ac.in registered for Sample Event but ok',1,'[{\"added\": {}}]',38,1),(135,'2024-10-22 11:31:42.575004','2','EventQuestion object (2)',2,'[{\"changed\": {\"fields\": [\"Question\"]}}]',40,1),(136,'2024-10-22 11:31:46.830527','1','EventQuestion object (1)',2,'[{\"changed\": {\"fields\": [\"Question\"]}}]',40,1),(137,'2024-10-22 11:33:52.032556','2','EventQuestion object (2)',3,'',40,1),(138,'2024-10-22 11:33:52.032556','1','EventQuestion object (1)',3,'',40,1),(139,'2024-10-22 11:37:07.937652','1','What is your favorite color?',2,'[{\"changed\": {\"fields\": [\"Help text\"]}}]',41,1),(140,'2024-10-22 11:39:39.489288','3','like me',1,'[{\"added\": {}}]',41,1),(141,'2024-10-22 11:40:02.116059','5','EventQuestion object (5)',2,'[{\"changed\": {\"fields\": [\"Event\"]}}]',40,1),(142,'2024-10-22 11:48:16.490764','3','event 3',1,'[{\"added\": {}}]',39,1),(143,'2024-10-24 10:12:13.763646','12','Assignment for Ticket #1 to surya@gmail.com',3,'',30,1),(144,'2024-10-24 10:12:13.763646','11','Assignment for Ticket #1 to naveen@gmail.com',3,'',30,1),(145,'2024-10-24 10:12:13.763646','10','Assignment for Ticket #1 to mitung12@gmail.com',3,'',30,1),(146,'2024-10-24 10:12:13.763646','9','Assignment for Ticket #1 to mitun@gmail.com',3,'',30,1),(147,'2024-10-24 10:12:13.763646','8','Assignment for Ticket #1 to sakthikumar@gmail.com',3,'',30,1),(148,'2024-10-24 10:14:37.618943','15','Assignment for Ticket #1 to surya@gmail.com',3,'',30,1),(149,'2024-10-24 10:14:37.619945','14','Assignment for Ticket #1 to mitun@gmail.com',3,'',30,1),(150,'2024-10-24 10:14:37.619945','13','Assignment for Ticket #1 to sakthikumar@gmail.com',3,'',30,1),(151,'2024-10-24 10:14:44.848237','5','Assignment for Ticket #1 to 20csa24@karpagamtech.ac.in',3,'',30,1),(152,'2024-10-24 12:11:59.969779','7','Assignment for Ticket #1 to sakthikumar@gmail.com',2,'[{\"changed\": {\"fields\": [\"Response\"]}}]',30,1),(153,'2024-10-24 12:12:04.684206','17','Assignment for Ticket #1 to surya@gmail.com',2,'[{\"changed\": {\"fields\": [\"Response\"]}}]',30,1);
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=42 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (20,'account','alumni'),(7,'account','batch'),(8,'account','country'),(18,'account','course'),(9,'account','department'),(10,'account','industry'),(11,'account','industry_type'),(12,'account','institution'),(13,'account','location'),(19,'account','member'),(21,'account','member_education'),(22,'account','member_experience'),(23,'account','member_skills'),(14,'account','role'),(15,'account','salutation'),(16,'account','skill'),(17,'account','social_media'),(24,'account','usergroup'),(1,'admin','logentry'),(3,'auth','group'),(2,'auth','permission'),(4,'auth','user'),(5,'contenttypes','contenttype'),(39,'event_portal','event'),(35,'event_portal','eventcategory'),(37,'event_portal','eventcomment'),(34,'event_portal','eventlike'),(40,'event_portal','eventquestion'),(38,'event_portal','eventregistration'),(41,'event_portal','question'),(36,'event_portal','registrationresponse'),(29,'help_desk','ticket'),(30,'help_desk','ticketassignment'),(32,'help_desk','ticketcategory'),(31,'help_desk','ticketreply'),(33,'help_desk','ticketstatus'),(28,'job_portal','application'),(25,'job_portal','businessdirectory'),(26,'job_portal','jobcomment'),(27,'job_portal','jobpost'),(6,'sessions','session');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=37 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2024-09-25 11:56:45.256103'),(2,'contenttypes','0002_remove_content_type_name','2024-09-25 11:56:45.480900'),(3,'auth','0001_initial','2024-09-25 11:56:47.668815'),(4,'auth','0002_alter_permission_name_max_length','2024-09-25 11:56:47.883248'),(5,'auth','0003_alter_user_email_max_length','2024-09-25 11:56:47.965043'),(6,'auth','0004_alter_user_username_opts','2024-09-25 11:56:47.980035'),(7,'auth','0005_alter_user_last_login_null','2024-09-25 11:56:48.188003'),(8,'auth','0006_require_contenttypes_0002','2024-09-25 11:56:48.199003'),(9,'auth','0007_alter_validators_add_error_messages','2024-09-25 11:56:48.217984'),(10,'auth','0008_alter_user_username_max_length','2024-09-25 11:56:48.451458'),(11,'auth','0009_alter_user_last_name_max_length','2024-09-25 11:56:48.668464'),(12,'auth','0010_alter_group_name_max_length','2024-09-25 11:56:48.741273'),(13,'auth','0011_update_proxy_permissions','2024-09-25 11:56:48.763274'),(14,'auth','0012_alter_user_first_name_max_length','2024-09-25 11:56:48.972492'),(15,'account','0001_initial','2024-09-25 11:56:55.166606'),(16,'admin','0001_initial','2024-09-25 11:56:55.696981'),(17,'admin','0002_logentry_remove_auto_add','2024-09-25 11:56:55.719993'),(18,'admin','0003_logentry_add_action_flag_choices','2024-09-25 11:56:55.746228'),(19,'sessions','0001_initial','2024-09-25 11:56:55.863799'),(20,'account','0002_alter_member_batch_alter_member_blood_group_and_more','2024-09-27 07:34:29.117664'),(21,'account','0003_alter_member_user','2024-09-28 06:56:45.079112'),(22,'account','0004_remove_member_department_and_more','2024-10-01 12:03:48.099946'),(23,'account','0005_alumni_counrty','2024-10-07 11:20:02.897075'),(24,'account','0006_remove_alumni_counrty','2024-10-07 11:29:05.468050'),(25,'account','0007_alter_alumni_linked_in_alter_alumni_website','2024-10-07 12:24:01.102822'),(26,'account','0008_alter_alumni_linked_in_alter_alumni_website','2024-10-07 12:27:46.622901'),(27,'job_portal','0001_initial','2024-10-08 04:35:04.630900'),(28,'job_portal','0002_application_job_post','2024-10-09 04:28:03.741549'),(29,'help_desk','0001_initial','2024-10-09 10:15:13.275646'),(30,'account','0009_alter_member_skills_member','2024-10-14 07:23:56.773588'),(31,'account','0010_alter_alumni_member_alter_member_education_member_and_more','2024-10-14 07:28:58.189779'),(32,'help_desk','0002_remove_ticket_assign_to_ticketassignment_message','2024-10-15 04:38:17.463223'),(33,'help_desk','0003_alter_ticketassignment_message','2024-10-15 04:38:17.634610'),(34,'event_portal','0001_initial','2024-10-19 11:01:42.664818'),(35,'event_portal','0002_event_is_active','2024-10-21 05:26:59.851515'),(36,'event_portal','0003_eventquestion_event','2024-10-21 09:54:11.621696');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('5qq22f8oxx8myl2pzs14x65wiwmr3ors','.eJxVjMsOgjAQRf-la9P0AZVx6Z5vIPPoWNRAQmFl_HclYaHbe865LzPgtpZhq3kZRjEX483pdyPkR552IHecbrPleVqXkeyu2INW28-Sn9fD_TsoWMu3ThwwtmcKiVPDoU0Nqip1xE5adcE7AFIQRwgsIaIieQCN4iEG7sz7A_cHOIo:1stg57:cIUAxbHq1KLYTDoMPAQ-bAHJnCJtWVLZtVMclA3DYeM','2024-10-10 04:26:21.879386'),('6mrvsxlalad7bhi6mq02hlioaf308dzz','.eJxVjMsOgjAQRf-la9P0AZVx6Z5vIPPoWNRAQmFl_HclYaHbe865LzPgtpZhq3kZRjEX483pdyPkR552IHecbrPleVqXkeyu2INW28-Sn9fD_TsoWMu3ThwwtmcKiVPDoU0Nqip1xE5adcE7AFIQRwgsIaIieQCN4iEG7sz7A_cHOIo:1t1P6z:Wip7VSAD6fjYFzCpT7eLnP3W7D-rk2kaGlyWWJaIUts','2024-10-31 11:56:13.626379'),('8679tz7y8x3qea95l18xw7585ekwn4xu','.eJxVjMsOgjAQRf-la9P0AZVx6Z5vIPPoWNRAQmFl_HclYaHbe865LzPgtpZhq3kZRjEX483pdyPkR552IHecbrPleVqXkeyu2INW28-Sn9fD_TsoWMu3ThwwtmcKiVPDoU0Nqip1xE5adcE7AFIQRwgsIaIieQCN4iEG7sz7A_cHOIo:1stQkq:V-SrB_lH-eQLUGDONdyeJzpdf2L_Yi3kBnsskbfhg0c','2024-10-09 12:04:24.786574'),('87zz1sx29b5yl32lx4685kztxuv0o7i6','.eJxVjMsOgjAQRf-la9P0AZVx6Z5vIPPoWNRAQmFl_HclYaHbe865LzPgtpZhq3kZRjEX483pdyPkR552IHecbrPleVqXkeyu2INW28-Sn9fD_TsoWMu3ThwwtmcKiVPDoU0Nqip1xE5adcE7AFIQRwgsIaIieQCN4iEG7sz7A_cHOIo:1t3qXR:mXcJ8W2GGPrzXqGYpaQ4gpkwMynhQmrtzCtO94t5taw','2024-11-07 05:37:37.733186'),('ag5mmm55ivuxkmoog4ac1dztvamobwlt','.eJxVjMsOgjAQRf-la9P0AZVx6Z5vIPPoWNRAQmFl_HclYaHbe865LzPgtpZhq3kZRjEX483pdyPkR552IHecbrPleVqXkeyu2INW28-Sn9fD_TsoWMu3ThwwtmcKiVPDoU0Nqip1xE5adcE7AFIQRwgsIaIieQCN4iEG7sz7A_cHOIo:1t3wgt:xlSnydas3uR4IOAEu10WZvUH6EobOEPjkEmL2YQr4_g','2024-11-07 12:11:47.347614'),('aujiz2zht43tymlu8t770hykgppd7lej','.eJxVjMsOgjAQRf-la9P0AZVx6Z5vIPPoWNRAQmFl_HclYaHbe865LzPgtpZhq3kZRjEX483pdyPkR552IHecbrPleVqXkeyu2INW28-Sn9fD_TsoWMu3ThwwtmcKiVPDoU0Nqip1xE5adcE7AFIQRwgsIaIieQCN4iEG7sz7A_cHOIo:1suRvS:xSGVxQf4Kcjenl4IuXpvb0gDFT7JFtfM2MaM9QBaCk8','2024-10-12 07:31:34.106958'),('c5ufycyc352acrms2kbr3fppix0u1l6g','.eJxVjMsOgjAQRf-la9P0AZVx6Z5vIPPoWNRAQmFl_HclYaHbe865LzPgtpZhq3kZRjEX483pdyPkR552IHecbrPleVqXkeyu2INW28-Sn9fD_TsoWMu3ThwwtmcKiVPDoU0Nqip1xE5adcE7AFIQRwgsIaIieQCN4iEG7sz7A_cHOIo:1su4U7:VzuNKNCjNpZXexxbH-SvhyiVuaCi3gzsVTjpbNRGzL8','2024-10-11 06:29:47.828406'),('d2s2r1yuwq3d3vib3lzip06l707m0vgj','.eJxVjMsOgjAQRf-la9P0AZVx6Z5vIPPoWNRAQmFl_HclYaHbe865LzPgtpZhq3kZRjEX483pdyPkR552IHecbrPleVqXkeyu2INW28-Sn9fD_TsoWMu3ThwwtmcKiVPDoU0Nqip1xE5adcE7AFIQRwgsIaIieQCN4iEG7sz7A_cHOIo:1t38sw:w5t24-CPI5WNjhnDwO0twoPxnb3dO7_QjMN2Zn54iM4','2024-11-05 07:00:54.965515'),('eibkpyi2137dllar6jbw13aticjjso2x','.eJxVjMsOgjAQRf-la9P0AZVx6Z5vIPPoWNRAQmFl_HclYaHbe865LzPgtpZhq3kZRjEX483pdyPkR552IHecbrPleVqXkeyu2INW28-Sn9fD_TsoWMu3ThwwtmcKiVPDoU0Nqip1xE5adcE7AFIQRwgsIaIieQCN4iEG7sz7A_cHOIo:1t12ku:2es8hbI9MZKR7N5pNSlZI6tjTu0oNUEAfF7W8wSJMCo','2024-10-30 12:03:56.102468'),('fh4d221d7h5w712yxju9xj60axgiz9g4','.eJxVjMsOgjAQRf-la9P0AZVx6Z5vIPPoWNRAQmFl_HclYaHbe865LzPgtpZhq3kZRjEX483pdyPkR552IHecbrPleVqXkeyu2INW28-Sn9fD_TsoWMu3ThwwtmcKiVPDoU0Nqip1xE5adcE7AFIQRwgsIaIieQCN4iEG7sz7A_cHOIo:1svZMt:GgpaOgbyl-zeuxjciS0eTqtwfcSqqQrY_db14_TIbjY','2024-10-15 09:40:31.961062'),('g1b28oxlbwro7xf4yhdisbaqghgyn63v','.eJxVjMsOgjAQRf-la9P0AZVx6Z5vIPPoWNRAQmFl_HclYaHbe865LzPgtpZhq3kZRjEX483pdyPkR552IHecbrPleVqXkeyu2INW28-Sn9fD_TsoWMu3ThwwtmcKiVPDoU0Nqip1xE5adcE7AFIQRwgsIaIieQCN4iEG7sz7A_cHOIo:1su4U8:MeZJlmHEvUdWh1BaYI1LdMbF-hlJnWD_Za9N_YJCo68','2024-10-11 06:29:48.999710'),('lwcswnwqjwdbt1tz0fyod4wox8wjjvn3','.eJxVjMsOgjAQRf-la9P0AZVx6Z5vIPPoWNRAQmFl_HclYaHbe865LzPgtpZhq3kZRjEX483pdyPkR552IHecbrPleVqXkeyu2INW28-Sn9fD_TsoWMu3ThwwtmcKiVPDoU0Nqip1xE5adcE7AFIQRwgsIaIieQCN4iEG7sz7A_cHOIo:1swKDo:mJkQgOhjRIvd9GdZEY-mpp7rl5YbBcmq-uSs9S2hk3U','2024-10-17 11:42:16.349429'),('t6u700gaxs7wnhqmubod39vl4b1rsvh4','.eJxVjMsOgjAQRf-la9P0AZVx6Z5vIPPoWNRAQmFl_HclYaHbe865LzPgtpZhq3kZRjEX483pdyPkR552IHecbrPleVqXkeyu2INW28-Sn9fD_TsoWMu3ThwwtmcKiVPDoU0Nqip1xE5adcE7AFIQRwgsIaIieQCN4iEG7sz7A_cHOIo:1t1fSL:8fA74H4KbMBQWNdK8BVzWeZR-fyniSfZGl3U9WIUC1M','2024-11-01 05:23:21.912458'),('wozm3t1npjuvd3c2l1qwxog6otqv8lpi','.eJxVjMsOgjAQRf-la9P0AZVx6Z5vIPPoWNRAQmFl_HclYaHbe865LzPgtpZhq3kZRjEX483pdyPkR552IHecbrPleVqXkeyu2INW28-Sn9fD_TsoWMu3ThwwtmcKiVPDoU0Nqip1xE5adcE7AFIQRwgsIaIieQCN4iEG7sz7A_cHOIo:1t1jAQ:b2kU08TwBVjAC1a2oeBTNeUgY13Mz_7mpmXeF___NgY','2024-11-01 09:21:06.363182');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `event_portal_event`
--

DROP TABLE IF EXISTS `event_portal_event`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `event_portal_event` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `title` varchar(255) NOT NULL,
  `start_date` date NOT NULL,
  `start_time` time(6) NOT NULL,
  `venue` varchar(225) NOT NULL,
  `address` longtext,
  `link` varchar(255) DEFAULT NULL,
  `is_public` tinyint(1) NOT NULL,
  `need_registration` tinyint(1) NOT NULL,
  `registration_close_date` date DEFAULT NULL,
  `description` longtext,
  `event_wallpaper` varchar(100) DEFAULT NULL,
  `instructions` longtext,
  `posted_on` date NOT NULL,
  `posted_by_id` int NOT NULL,
  `category_id` bigint NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `event_portal_event_posted_by_id_d23aacc6_fk_auth_user_id` (`posted_by_id`),
  KEY `event_portal_event_category_id_d5478054_fk_event_por` (`category_id`),
  CONSTRAINT `event_portal_event_category_id_d5478054_fk_event_por` FOREIGN KEY (`category_id`) REFERENCES `event_portal_eventcategory` (`id`),
  CONSTRAINT `event_portal_event_posted_by_id_d23aacc6_fk_auth_user_id` FOREIGN KEY (`posted_by_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `event_portal_event`
--

LOCK TABLES `event_portal_event` WRITE;
/*!40000 ALTER TABLE `event_portal_event` DISABLE KEYS */;
INSERT INTO `event_portal_event` VALUES (1,'Sample Event but ok','2024-10-25','15:00:00.000000','Main Hall','123 Main St','http://example.com',1,1,'2024-10-20','This is a sample event.','events/wallpapers/3135715.png','Please arrive 30 minutes early.','2024-10-21',2,1,1),(2,'event 2','2024-10-21','08:59:50.000000','tikvhj','k vhjk,l',NULL,1,1,'2024-10-31','','events/wallpapers/background.jpg','kbk','2024-10-21',2,2,1),(3,'event 3','2024-10-22','11:47:56.000000','yjy','yjjyj',NULL,1,1,'2024-10-22','etjtj','','jrj','2024-10-22',2,1,1);
/*!40000 ALTER TABLE `event_portal_event` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `event_portal_eventcategory`
--

DROP TABLE IF EXISTS `event_portal_eventcategory`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `event_portal_eventcategory` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `title` varchar(225) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `event_portal_eventcategory`
--

LOCK TABLES `event_portal_eventcategory` WRITE;
/*!40000 ALTER TABLE `event_portal_eventcategory` DISABLE KEYS */;
INSERT INTO `event_portal_eventcategory` VALUES (1,'All Event'),(2,'Reunion'),(3,'Webinars');
/*!40000 ALTER TABLE `event_portal_eventcategory` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `event_portal_eventcomment`
--

DROP TABLE IF EXISTS `event_portal_eventcomment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `event_portal_eventcomment` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `comment_text` longtext NOT NULL,
  `commented_on` datetime(6) NOT NULL,
  `event_id` bigint NOT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `event_portal_eventco_event_id_912ff714_fk_event_por` (`event_id`),
  KEY `event_portal_eventcomment_user_id_af80c6ad_fk_auth_user_id` (`user_id`),
  CONSTRAINT `event_portal_eventco_event_id_912ff714_fk_event_por` FOREIGN KEY (`event_id`) REFERENCES `event_portal_event` (`id`),
  CONSTRAINT `event_portal_eventcomment_user_id_af80c6ad_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `event_portal_eventcomment`
--

LOCK TABLES `event_portal_eventcomment` WRITE;
/*!40000 ALTER TABLE `event_portal_eventcomment` DISABLE KEYS */;
/*!40000 ALTER TABLE `event_portal_eventcomment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `event_portal_eventlike`
--

DROP TABLE IF EXISTS `event_portal_eventlike`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `event_portal_eventlike` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `liked_on` datetime(6) NOT NULL,
  `event_id` bigint NOT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `event_portal_eventlike_event_id_user_id_43f95d69_uniq` (`event_id`,`user_id`),
  KEY `event_portal_eventlike_user_id_80d75422_fk_auth_user_id` (`user_id`),
  CONSTRAINT `event_portal_eventli_event_id_21c1a270_fk_event_por` FOREIGN KEY (`event_id`) REFERENCES `event_portal_event` (`id`),
  CONSTRAINT `event_portal_eventlike_user_id_80d75422_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `event_portal_eventlike`
--

LOCK TABLES `event_portal_eventlike` WRITE;
/*!40000 ALTER TABLE `event_portal_eventlike` DISABLE KEYS */;
/*!40000 ALTER TABLE `event_portal_eventlike` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `event_portal_eventquestion`
--

DROP TABLE IF EXISTS `event_portal_eventquestion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `event_portal_eventquestion` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `question_id` varchar(225) NOT NULL,
  `event_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `event_portal_eventqu_event_id_d2f8a246_fk_event_por` (`event_id`),
  CONSTRAINT `event_portal_eventqu_event_id_d2f8a246_fk_event_por` FOREIGN KEY (`event_id`) REFERENCES `event_portal_event` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `event_portal_eventquestion`
--

LOCK TABLES `event_portal_eventquestion` WRITE;
/*!40000 ALTER TABLE `event_portal_eventquestion` DISABLE KEYS */;
INSERT INTO `event_portal_eventquestion` VALUES (3,'1',1),(4,'2',1),(5,'2',2),(6,'1',3),(7,'3',3);
/*!40000 ALTER TABLE `event_portal_eventquestion` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `event_portal_eventregistration`
--

DROP TABLE IF EXISTS `event_portal_eventregistration`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `event_portal_eventregistration` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `applied_on` date NOT NULL,
  `event_id` bigint NOT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `event_portal_eventre_event_id_a806513f_fk_event_por` (`event_id`),
  KEY `event_portal_eventregistration_user_id_a8d7e3fb_fk_auth_user_id` (`user_id`),
  CONSTRAINT `event_portal_eventre_event_id_a806513f_fk_event_por` FOREIGN KEY (`event_id`) REFERENCES `event_portal_event` (`id`),
  CONSTRAINT `event_portal_eventregistration_user_id_a8d7e3fb_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `event_portal_eventregistration`
--

LOCK TABLES `event_portal_eventregistration` WRITE;
/*!40000 ALTER TABLE `event_portal_eventregistration` DISABLE KEYS */;
INSERT INTO `event_portal_eventregistration` VALUES (1,'2024-10-21',1,2);
/*!40000 ALTER TABLE `event_portal_eventregistration` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `event_portal_question`
--

DROP TABLE IF EXISTS `event_portal_question`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `event_portal_question` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `question` varchar(225) NOT NULL,
  `options` varchar(225) DEFAULT NULL,
  `help_text` varchar(225) DEFAULT NULL,
  `is_faq` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `event_portal_question`
--

LOCK TABLES `event_portal_question` WRITE;
/*!40000 ALTER TABLE `event_portal_question` DISABLE KEYS */;
INSERT INTO `event_portal_question` VALUES (1,'What is your favorite color?','Red, Blue, Green','Choose one of the fav colour.',0),(2,'What is your favorite furit?','apple, grape, banana','Choose one of the fav furit.',0),(3,'like me','yes no','Choose one',0);
/*!40000 ALTER TABLE `event_portal_question` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `event_portal_registrationresponse`
--

DROP TABLE IF EXISTS `event_portal_registrationresponse`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `event_portal_registrationresponse` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `response` varchar(255) NOT NULL,
  `question_id` bigint NOT NULL,
  `registered_event_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `event_portal_registr_question_id_7b0a48c1_fk_event_por` (`question_id`),
  KEY `event_portal_registr_registered_event_id_286faaa8_fk_event_por` (`registered_event_id`),
  CONSTRAINT `event_portal_registr_question_id_7b0a48c1_fk_event_por` FOREIGN KEY (`question_id`) REFERENCES `event_portal_eventquestion` (`id`),
  CONSTRAINT `event_portal_registr_registered_event_id_286faaa8_fk_event_por` FOREIGN KEY (`registered_event_id`) REFERENCES `event_portal_eventregistration` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `event_portal_registrationresponse`
--

LOCK TABLES `event_portal_registrationresponse` WRITE;
/*!40000 ALTER TABLE `event_portal_registrationresponse` DISABLE KEYS */;
/*!40000 ALTER TABLE `event_portal_registrationresponse` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `help_desk_ticket`
--

DROP TABLE IF EXISTS `help_desk_ticket`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `help_desk_ticket` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `priority` varchar(225) NOT NULL,
  `due_date` date DEFAULT NULL,
  `last_status_on` date NOT NULL,
  `content` longtext NOT NULL,
  `alumni_id` bigint NOT NULL,
  `category_id` bigint NOT NULL,
  `status_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `help_desk_ticket_alumni_id_e8b6ed39_fk_account_alumni_id` (`alumni_id`),
  KEY `help_desk_ticket_category_id_1c86990f_fk_help_desk` (`category_id`),
  KEY `help_desk_ticket_status_id_31db37d0_fk_help_desk_ticketstatus_id` (`status_id`),
  CONSTRAINT `help_desk_ticket_alumni_id_e8b6ed39_fk_account_alumni_id` FOREIGN KEY (`alumni_id`) REFERENCES `account_alumni` (`id`),
  CONSTRAINT `help_desk_ticket_category_id_1c86990f_fk_help_desk` FOREIGN KEY (`category_id`) REFERENCES `help_desk_ticketcategory` (`id`),
  CONSTRAINT `help_desk_ticket_status_id_31db37d0_fk_help_desk_ticketstatus_id` FOREIGN KEY (`status_id`) REFERENCES `help_desk_ticketstatus` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `help_desk_ticket`
--

LOCK TABLES `help_desk_ticket` WRITE;
/*!40000 ALTER TABLE `help_desk_ticket` DISABLE KEYS */;
INSERT INTO `help_desk_ticket` VALUES (1,'Low','2024-12-31','2024-10-25','This is a test ticket.',3,1,7),(5,'M','2024-10-19','2024-10-19','ok to process',2,1,2);
/*!40000 ALTER TABLE `help_desk_ticket` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `help_desk_ticketassignment`
--

DROP TABLE IF EXISTS `help_desk_ticketassignment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `help_desk_ticketassignment` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `response` longtext,
  `assigned_on` date NOT NULL,
  `respond_on` date DEFAULT NULL,
  `assigned_to_id` int NOT NULL,
  `ticket_id` bigint NOT NULL,
  `message` longtext,
  PRIMARY KEY (`id`),
  KEY `help_desk_ticketassi_assigned_to_id_a9d4328d_fk_auth_user` (`assigned_to_id`),
  KEY `help_desk_ticketassi_ticket_id_a1f4f67d_fk_help_desk` (`ticket_id`),
  CONSTRAINT `help_desk_ticketassi_assigned_to_id_a9d4328d_fk_auth_user` FOREIGN KEY (`assigned_to_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `help_desk_ticketassi_ticket_id_a1f4f67d_fk_help_desk` FOREIGN KEY (`ticket_id`) REFERENCES `help_desk_ticket` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `help_desk_ticketassignment`
--

LOCK TABLES `help_desk_ticketassignment` WRITE;
/*!40000 ALTER TABLE `help_desk_ticketassignment` DISABLE KEYS */;
INSERT INTO `help_desk_ticketassignment` VALUES (7,'gnhjfgjfgj','2024-10-18',NULL,25,1,'important'),(16,NULL,'2024-10-24',NULL,49,1,'Please address this ticket.'),(17,'gsfnhjfgn','2024-10-24',NULL,55,1,'Please address this ticket.');
/*!40000 ALTER TABLE `help_desk_ticketassignment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `help_desk_ticketcategory`
--

DROP TABLE IF EXISTS `help_desk_ticketcategory`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `help_desk_ticketcategory` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `category` varchar(225) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `help_desk_ticketcategory`
--

LOCK TABLES `help_desk_ticketcategory` WRITE;
/*!40000 ALTER TABLE `help_desk_ticketcategory` DISABLE KEYS */;
INSERT INTO `help_desk_ticketcategory` VALUES (1,'cat 1'),(2,'cat 2'),(3,'cat 3');
/*!40000 ALTER TABLE `help_desk_ticketcategory` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `help_desk_ticketreply`
--

DROP TABLE IF EXISTS `help_desk_ticketreply`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `help_desk_ticketreply` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `message` longtext NOT NULL,
  `posted_on` date NOT NULL,
  `posted_by_id` int NOT NULL,
  `ticket_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `help_desk_ticketreply_posted_by_id_03421f1d_fk_auth_user_id` (`posted_by_id`),
  KEY `help_desk_ticketreply_ticket_id_6c39492e_fk_help_desk_ticket_id` (`ticket_id`),
  CONSTRAINT `help_desk_ticketreply_posted_by_id_03421f1d_fk_auth_user_id` FOREIGN KEY (`posted_by_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `help_desk_ticketreply_ticket_id_6c39492e_fk_help_desk_ticket_id` FOREIGN KEY (`ticket_id`) REFERENCES `help_desk_ticket` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `help_desk_ticketreply`
--

LOCK TABLES `help_desk_ticketreply` WRITE;
/*!40000 ALTER TABLE `help_desk_ticketreply` DISABLE KEYS */;
INSERT INTO `help_desk_ticketreply` VALUES (1,'nall iruku','2024-10-15',2,1),(2,'analum mudila','2024-10-15',2,1),(3,'do well','2024-10-19',25,5);
/*!40000 ALTER TABLE `help_desk_ticketreply` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `help_desk_ticketstatus`
--

DROP TABLE IF EXISTS `help_desk_ticketstatus`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `help_desk_ticketstatus` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `status` varchar(225) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `help_desk_ticketstatus`
--

LOCK TABLES `help_desk_ticketstatus` WRITE;
/*!40000 ALTER TABLE `help_desk_ticketstatus` DISABLE KEYS */;
INSERT INTO `help_desk_ticketstatus` VALUES (2,'Closed'),(4,'Open'),(5,'Replied'),(6,'On Hold'),(7,'Assigned');
/*!40000 ALTER TABLE `help_desk_ticketstatus` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `job_portal_application`
--

DROP TABLE IF EXISTS `job_portal_application`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `job_portal_application` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `full_name` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `mobile_number` varchar(25) DEFAULT NULL,
  `total_years_of_experience` double NOT NULL,
  `resume` varchar(100) NOT NULL,
  `notes_to_recruiter` longtext,
  `applied_on` date NOT NULL,
  `current_industry_id` bigint NOT NULL,
  `current_role_id` bigint NOT NULL,
  `job_post_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `job_portal_applicati_current_industry_id_996d75ae_fk_account_i` (`current_industry_id`),
  KEY `job_portal_applicati_current_role_id_94d00b48_fk_account_r` (`current_role_id`),
  KEY `job_portal_applicati_job_post_id_30063328_fk_job_porta` (`job_post_id`),
  CONSTRAINT `job_portal_applicati_current_industry_id_996d75ae_fk_account_i` FOREIGN KEY (`current_industry_id`) REFERENCES `account_industry` (`id`),
  CONSTRAINT `job_portal_applicati_current_role_id_94d00b48_fk_account_r` FOREIGN KEY (`current_role_id`) REFERENCES `account_role` (`id`),
  CONSTRAINT `job_portal_applicati_job_post_id_30063328_fk_job_porta` FOREIGN KEY (`job_post_id`) REFERENCES `job_portal_jobpost` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `job_portal_application`
--

LOCK TABLES `job_portal_application` WRITE;
/*!40000 ALTER TABLE `job_portal_application` DISABLE KEYS */;
INSERT INTO `job_portal_application` VALUES (1,'samy','john@example.com','455545443',3,'resumes/Birth_Certificate.pdf','text','2024-10-09',1,1,2),(2,'samy','john@example.com','455545443',3,'resumes/Birth_Certificate_pU85xx8.pdf','text','2024-10-09',1,1,2);
/*!40000 ALTER TABLE `job_portal_application` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `job_portal_application_skills`
--

DROP TABLE IF EXISTS `job_portal_application_skills`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `job_portal_application_skills` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `application_id` bigint NOT NULL,
  `skill_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `job_portal_application_s_application_id_skill_id_09968aba_uniq` (`application_id`,`skill_id`),
  KEY `job_portal_applicati_skill_id_26fe7c3a_fk_account_s` (`skill_id`),
  CONSTRAINT `job_portal_applicati_application_id_1564e5af_fk_job_porta` FOREIGN KEY (`application_id`) REFERENCES `job_portal_application` (`id`),
  CONSTRAINT `job_portal_applicati_skill_id_26fe7c3a_fk_account_s` FOREIGN KEY (`skill_id`) REFERENCES `account_skill` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `job_portal_application_skills`
--

LOCK TABLES `job_portal_application_skills` WRITE;
/*!40000 ALTER TABLE `job_portal_application_skills` DISABLE KEYS */;
/*!40000 ALTER TABLE `job_portal_application_skills` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `job_portal_businessdirectory`
--

DROP TABLE IF EXISTS `job_portal_businessdirectory`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `job_portal_businessdirectory` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `business_name` varchar(255) NOT NULL,
  `description` longtext NOT NULL,
  `website` varchar(255) DEFAULT NULL,
  `location` varchar(255) NOT NULL,
  `contact_email` varchar(255) NOT NULL,
  `contact_number` varchar(25) DEFAULT NULL,
  `are_you_part_of_management` tinyint(1) NOT NULL,
  `logo` varchar(100) DEFAULT NULL,
  `listed_on` date NOT NULL,
  `country_code_id` bigint NOT NULL,
  `industry_type_id` bigint NOT NULL,
  `listed_by_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `job_portal_businessd_country_code_id_240a15d7_fk_account_c` (`country_code_id`),
  KEY `job_portal_businessd_industry_type_id_2ca1d019_fk_account_i` (`industry_type_id`),
  KEY `job_portal_businessd_listed_by_id_078255e2_fk_auth_user` (`listed_by_id`),
  CONSTRAINT `job_portal_businessd_country_code_id_240a15d7_fk_account_c` FOREIGN KEY (`country_code_id`) REFERENCES `account_country` (`id`),
  CONSTRAINT `job_portal_businessd_industry_type_id_2ca1d019_fk_account_i` FOREIGN KEY (`industry_type_id`) REFERENCES `account_industry_type` (`id`),
  CONSTRAINT `job_portal_businessd_listed_by_id_078255e2_fk_auth_user` FOREIGN KEY (`listed_by_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `job_portal_businessdirectory`
--

LOCK TABLES `job_portal_businessdirectory` WRITE;
/*!40000 ALTER TABLE `job_portal_businessdirectory` DISABLE KEYS */;
INSERT INTO `job_portal_businessdirectory` VALUES (1,'bussiness 1','nothing','https//examble.com','Business Location','email@example.com','1234567890',1,'logos/2713372.jpg','2024-10-08',1,1,2),(2,'bussiness 2','nothing','https//examble.com','Business Location','email@example.com','1234567890',1,'logos/2713372_6D4pHIq.jpg','2024-10-08',1,1,2),(3,'bussiness 3','nothing','https//examble.com','Business Location is','email@example.com','1234567890',1,'logos/2713372_W69S0zM.jpg','2024-10-08',1,1,2);
/*!40000 ALTER TABLE `job_portal_businessdirectory` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `job_portal_jobcomment`
--

DROP TABLE IF EXISTS `job_portal_jobcomment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `job_portal_jobcomment` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `comment` longtext NOT NULL,
  `comment_by_id` int NOT NULL,
  `job_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `job_portal_jobcomment_comment_by_id_69decb03_fk_auth_user_id` (`comment_by_id`),
  KEY `job_portal_jobcomment_job_id_f6beab81_fk_job_portal_jobpost_id` (`job_id`),
  CONSTRAINT `job_portal_jobcomment_comment_by_id_69decb03_fk_auth_user_id` FOREIGN KEY (`comment_by_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `job_portal_jobcomment_job_id_f6beab81_fk_job_portal_jobpost_id` FOREIGN KEY (`job_id`) REFERENCES `job_portal_jobpost` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `job_portal_jobcomment`
--

LOCK TABLES `job_portal_jobcomment` WRITE;
/*!40000 ALTER TABLE `job_portal_jobcomment` DISABLE KEYS */;
INSERT INTO `job_portal_jobcomment` VALUES (3,'nice job',2,2),(4,'try this job',2,2),(5,'i am waiting for this job',2,2);
/*!40000 ALTER TABLE `job_portal_jobcomment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `job_portal_jobpost`
--

DROP TABLE IF EXISTS `job_portal_jobpost`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `job_portal_jobpost` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `job_title` varchar(255) NOT NULL,
  `experience_level_from` int NOT NULL,
  `experience_level_to` int NOT NULL,
  `location` varchar(255) NOT NULL,
  `contact_email` varchar(255) NOT NULL,
  `contact_link` varchar(255) DEFAULT NULL,
  `salary_package` varchar(255) DEFAULT NULL,
  `dead_line` date NOT NULL,
  `job_description` longtext NOT NULL,
  `file` varchar(100) DEFAULT NULL,
  `post_type` varchar(225) NOT NULL,
  `posted_on` date NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `industry_id` bigint NOT NULL,
  `posted_by_id` int NOT NULL,
  `role_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `job_portal_jobpost_industry_id_9f13bc65_fk_account_industry_id` (`industry_id`),
  KEY `job_portal_jobpost_posted_by_id_257d4f0e_fk_auth_user_id` (`posted_by_id`),
  KEY `job_portal_jobpost_role_id_8e6fc9af_fk_account_role_id` (`role_id`),
  CONSTRAINT `job_portal_jobpost_industry_id_9f13bc65_fk_account_industry_id` FOREIGN KEY (`industry_id`) REFERENCES `account_industry` (`id`),
  CONSTRAINT `job_portal_jobpost_posted_by_id_257d4f0e_fk_auth_user_id` FOREIGN KEY (`posted_by_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `job_portal_jobpost_role_id_8e6fc9af_fk_account_role_id` FOREIGN KEY (`role_id`) REFERENCES `account_role` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `job_portal_jobpost`
--

LOCK TABLES `job_portal_jobpost` WRITE;
/*!40000 ALTER TABLE `job_portal_jobpost` DISABLE KEYS */;
INSERT INTO `job_portal_jobpost` VALUES (2,'title 3',0,0,'San Francisco, CA','example@example.com','http://example.com','$80,000 - $100,000','2024-12-31','title1','job_files/deadpool-logo-3826-x-1750-eapj2mhbb1h7fp2i_kvalvP6.jpg','Internship','2024-10-08',1,1,2,1),(4,'title 3',1,2,'New York, NY','example@example.com','http://example@gmail.com','$80,000 - $100,000','2024-12-31','title1','','Internship','2024-10-08',1,1,24,1),(6,'title 4',0,0,'chennai','midhung2015@gmail.com','http://mitun@gmail.com','220000','2024-10-08','hgfcvk','','Job','2024-10-18',1,1,2,1);
/*!40000 ALTER TABLE `job_portal_jobpost` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `job_portal_jobpost_skills`
--

DROP TABLE IF EXISTS `job_portal_jobpost_skills`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `job_portal_jobpost_skills` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `jobpost_id` bigint NOT NULL,
  `skill_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `job_portal_jobpost_skills_jobpost_id_skill_id_86dc1936_uniq` (`jobpost_id`,`skill_id`),
  KEY `job_portal_jobpost_skills_skill_id_a804c088_fk_account_skill_id` (`skill_id`),
  CONSTRAINT `job_portal_jobpost_s_jobpost_id_da9da627_fk_job_porta` FOREIGN KEY (`jobpost_id`) REFERENCES `job_portal_jobpost` (`id`),
  CONSTRAINT `job_portal_jobpost_skills_skill_id_a804c088_fk_account_skill_id` FOREIGN KEY (`skill_id`) REFERENCES `account_skill` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `job_portal_jobpost_skills`
--

LOCK TABLES `job_portal_jobpost_skills` WRITE;
/*!40000 ALTER TABLE `job_portal_jobpost_skills` DISABLE KEYS */;
INSERT INTO `job_portal_jobpost_skills` VALUES (1,2,1),(2,2,2),(18,2,3),(19,2,4),(5,4,1),(6,4,2),(20,6,1);
/*!40000 ALTER TABLE `job_portal_jobpost_skills` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-10-26 10:01:17
