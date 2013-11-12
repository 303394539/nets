-- MySQL dump 10.13  Distrib 5.5.27, for Win32 (x86)
--
-- Host: localhost    Database: nets
-- ------------------------------------------------------
-- Server version	5.5.27

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `cinema_gewara`
--

DROP TABLE IF EXISTS `cinema_gewara`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `cinema_gewara` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `city_en` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cinema_gewara`
--

LOCK TABLES `cinema_gewara` WRITE;
/*!40000 ALTER TABLE `cinema_gewara` DISABLE KEYS */;
/*!40000 ALTER TABLE `cinema_gewara` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cinema_mtime`
--

DROP TABLE IF EXISTS `cinema_mtime`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `cinema_mtime` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `city_id` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cinema_mtime`
--

LOCK TABLES `cinema_mtime` WRITE;
/*!40000 ALTER TABLE `cinema_mtime` DISABLE KEYS */;
/*!40000 ALTER TABLE `cinema_mtime` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `city`
--

DROP TABLE IF EXISTS `city`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `city` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `province` varchar(255) NOT NULL,
  `gps` varchar(255) NOT NULL,
  `en` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `city`
--

LOCK TABLES `city` WRITE;
/*!40000 ALTER TABLE `city` DISABLE KEYS */;
/*!40000 ALTER TABLE `city` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `city_gewara`
--

DROP TABLE IF EXISTS `city_gewara`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `city_gewara` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `en` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `city_gewara`
--

LOCK TABLES `city_gewara` WRITE;
/*!40000 ALTER TABLE `city_gewara` DISABLE KEYS */;
/*!40000 ALTER TABLE `city_gewara` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `city_meituan`
--

DROP TABLE IF EXISTS `city_meituan`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `city_meituan` (
  `m_id` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `latitude` varchar(255) NOT NULL,
  `longtitude` varchar(255) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `city_meituan`
--

LOCK TABLES `city_meituan` WRITE;
/*!40000 ALTER TABLE `city_meituan` DISABLE KEYS */;
/*!40000 ALTER TABLE `city_meituan` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `city_mtime`
--

DROP TABLE IF EXISTS `city_mtime`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `city_mtime` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `en` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `city_mtime`
--

LOCK TABLES `city_mtime` WRITE;
/*!40000 ALTER TABLE `city_mtime` DISABLE KEYS */;
/*!40000 ALTER TABLE `city_mtime` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `movie_gewara`
--

DROP TABLE IF EXISTS `movie_gewara`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `movie_gewara` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `url` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `movie_gewara`
--

LOCK TABLES `movie_gewara` WRITE;
/*!40000 ALTER TABLE `movie_gewara` DISABLE KEYS */;
/*!40000 ALTER TABLE `movie_gewara` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `movie_mtime`
--

DROP TABLE IF EXISTS `movie_mtime`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `movie_mtime` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `url` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `movie_mtime`
--

LOCK TABLES `movie_mtime` WRITE;
/*!40000 ALTER TABLE `movie_mtime` DISABLE KEYS */;
/*!40000 ALTER TABLE `movie_mtime` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `showtime_gewara`
--

DROP TABLE IF EXISTS `showtime_gewara`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `showtime_gewara` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `cinema_id` int(11) NOT NULL,
  `movie_id` int(11) NOT NULL,
  `date` varchar(255) NOT NULL,
  `showtime` text NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `showtime_gewara`
--

LOCK TABLES `showtime_gewara` WRITE;
/*!40000 ALTER TABLE `showtime_gewara` DISABLE KEYS */;
/*!40000 ALTER TABLE `showtime_gewara` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `showtime_mtime`
--

DROP TABLE IF EXISTS `showtime_mtime`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `showtime_mtime` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `cinema_id` int(11) NOT NULL,
  `movie_id` int(11) NOT NULL,
  `date` varchar(255) NOT NULL,
  `showtime` text NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `showtime_mtime`
--

LOCK TABLES `showtime_mtime` WRITE;
/*!40000 ALTER TABLE `showtime_mtime` DISABLE KEYS */;
/*!40000 ALTER TABLE `showtime_mtime` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2013-11-12 15:07:48
