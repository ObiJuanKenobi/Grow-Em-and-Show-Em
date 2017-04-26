-- --------------------------------------------------------
-- Host:                         sddb.ece.iastate.edu
-- Server version:               10.1.19-MariaDB - MariaDB Server
-- Server OS:                    Linux
-- HeidiSQL Version:             9.4.0.5125
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;


-- Dumping database structure for may1713_PrisonGardenApp
CREATE DATABASE IF NOT EXISTS `may1713_PrisonGardenApp` /*!40100 DEFAULT CHARACTER SET latin1 */;
USE `may1713_PrisonGardenApp`;

-- Dumping structure for table may1713_PrisonGardenApp.auth_group
CREATE TABLE IF NOT EXISTS `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(80) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Data exporting was unselected.
-- Dumping structure for table may1713_PrisonGardenApp.auth_group_permissions
CREATE TABLE IF NOT EXISTS `auth_group_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Data exporting was unselected.
-- Dumping structure for table may1713_PrisonGardenApp.auth_permission
CREATE TABLE IF NOT EXISTS `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=28 DEFAULT CHARSET=latin1;

-- Data exporting was unselected.
-- Dumping structure for table may1713_PrisonGardenApp.auth_user
CREATE TABLE IF NOT EXISTS `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(30) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;

-- Data exporting was unselected.
-- Dumping structure for table may1713_PrisonGardenApp.auth_user_groups
CREATE TABLE IF NOT EXISTS `auth_user_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Data exporting was unselected.
-- Dumping structure for table may1713_PrisonGardenApp.auth_user_user_permissions
CREATE TABLE IF NOT EXISTS `auth_user_user_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Data exporting was unselected.
-- Dumping structure for table may1713_PrisonGardenApp.Bed_Plans
CREATE TABLE IF NOT EXISTS `Bed_Plans` (
  `PlanID` int(11) NOT NULL AUTO_INCREMENT,
  `Bed_Name` varchar(45) NOT NULL,
  `Bed_Plan` varchar(255) NOT NULL,
  `Bed_Canvas` text NOT NULL,
  `Updated_At` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `Created_At` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`PlanID`),
  UNIQUE KEY `PlanID_UNIQUE` (`PlanID`)
) ENGINE=InnoDB AUTO_INCREMENT=39 DEFAULT CHARSET=latin1;

-- Data exporting was unselected.
-- Dumping structure for table may1713_PrisonGardenApp.Courses
CREATE TABLE IF NOT EXISTS `Courses` (
  `CourseID` int(11) NOT NULL AUTO_INCREMENT,
  `Course_Name` varchar(45) NOT NULL DEFAULT 'course',
  `Course_Order` int(11) DEFAULT NULL,
  `Course_HTML_Path` varchar(255) DEFAULT NULL,
  `Course_Color` varchar(45) NOT NULL DEFAULT '000000',
  `Has_Quiz` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`CourseID`),
  UNIQUE KEY `Course_Name_UNIQUE` (`Course_Name`)
) ENGINE=InnoDB AUTO_INCREMENT=54 DEFAULT CHARSET=latin1;

-- Data exporting was unselected.
-- Dumping structure for table may1713_PrisonGardenApp.Daily_Records
CREATE TABLE IF NOT EXISTS `Daily_Records` (
  `Record_ID` int(11) NOT NULL AUTO_INCREMENT,
  `Username` varchar(45) NOT NULL,
  `Plant` varchar(45) DEFAULT NULL,
  `Quantity` varchar(45) DEFAULT NULL,
  `Record_Date` datetime DEFAULT NULL,
  `Notes` varchar(1000) DEFAULT NULL,
  `Location` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`Record_ID`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=latin1;

-- Data exporting was unselected.
-- Dumping structure for table may1713_PrisonGardenApp.django_admin_log
CREATE TABLE IF NOT EXISTS `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;

-- Data exporting was unselected.
-- Dumping structure for table may1713_PrisonGardenApp.django_content_type
CREATE TABLE IF NOT EXISTS `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=latin1;

-- Data exporting was unselected.
-- Dumping structure for table may1713_PrisonGardenApp.django_migrations
CREATE TABLE IF NOT EXISTS `django_migrations` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=latin1;

-- Data exporting was unselected.
-- Dumping structure for table may1713_PrisonGardenApp.django_session
CREATE TABLE IF NOT EXISTS `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Data exporting was unselected.
-- Dumping structure for table may1713_PrisonGardenApp.gardens
CREATE TABLE IF NOT EXISTS `gardens` (
  `gardenid` int(11) NOT NULL AUTO_INCREMENT,
  `garden_name` varchar(45) NOT NULL,
  PRIMARY KEY (`gardenid`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;

-- Data exporting was unselected.
-- Dumping structure for table may1713_PrisonGardenApp.Lessons
CREATE TABLE IF NOT EXISTS `Lessons` (
  `LessonID` int(11) NOT NULL AUTO_INCREMENT,
  `Lesson_Name` varchar(45) DEFAULT NULL,
  `Course_Name` varchar(45) NOT NULL,
  `Lesson_File_Path` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`LessonID`),
  KEY `Course_Name_idx` (`Course_Name`),
  CONSTRAINT `Course_Name` FOREIGN KEY (`Course_Name`) REFERENCES `Courses` (`Course_Name`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=50 DEFAULT CHARSET=latin1;

-- Data exporting was unselected.
-- Dumping structure for table may1713_PrisonGardenApp.Quiz_Answers
CREATE TABLE IF NOT EXISTS `Quiz_Answers` (
  `AnswerID` int(11) NOT NULL AUTO_INCREMENT,
  `QuestionID` int(11) NOT NULL,
  `Answer_Text` varchar(255) DEFAULT NULL,
  `Is_Correct` bit(1) DEFAULT NULL,
  PRIMARY KEY (`AnswerID`),
  KEY `fk_QuizQuestionID_idx` (`QuestionID`),
  CONSTRAINT `fk_QuizQuestionID` FOREIGN KEY (`QuestionID`) REFERENCES `Quiz_Questions` (`QuestionID`) ON DELETE CASCADE ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=1393 DEFAULT CHARSET=latin1;

-- Data exporting was unselected.
-- Dumping structure for table may1713_PrisonGardenApp.Quiz_Attempts
CREATE TABLE IF NOT EXISTS `Quiz_Attempts` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `Username` varchar(45) DEFAULT NULL,
  `Passed` bit(1) DEFAULT NULL,
  `CourseID` int(11) DEFAULT NULL,
  `Course_Name` varchar(45) DEFAULT NULL,
  `Question1_ID` int(11) DEFAULT NULL,
  `Answer1_ID` int(11) DEFAULT NULL,
  `Question2_ID` int(11) DEFAULT NULL,
  `Answer2_ID` int(11) DEFAULT NULL,
  `Question3_ID` int(11) DEFAULT NULL,
  `Answer3_ID` int(11) DEFAULT NULL,
  `Question4_ID` int(11) DEFAULT NULL,
  `Answer4_ID` int(11) DEFAULT NULL,
  `Question5_ID` int(11) DEFAULT NULL,
  `Answer5_ID` int(11) DEFAULT NULL,
  `Question6_ID` int(11) DEFAULT NULL,
  `Answer6_ID` int(11) DEFAULT NULL,
  `Question7_ID` int(11) DEFAULT NULL,
  `Answer7_ID` int(11) DEFAULT NULL,
  `Question8_ID` int(11) DEFAULT NULL,
  `Answer8_ID` int(11) DEFAULT NULL,
  `Question9_ID` int(11) DEFAULT NULL,
  `Answer9_ID` int(11) DEFAULT NULL,
  `Question10_ID` int(11) DEFAULT NULL,
  `Answer10_ID` int(11) DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=41 DEFAULT CHARSET=latin1;

-- Data exporting was unselected.
-- Dumping structure for table may1713_PrisonGardenApp.Quiz_Questions
CREATE TABLE IF NOT EXISTS `Quiz_Questions` (
  `QuestionID` int(11) NOT NULL AUTO_INCREMENT,
  `Question_Text` varchar(255) DEFAULT NULL,
  `Course_Name` varchar(45) NOT NULL,
  PRIMARY KEY (`QuestionID`),
  KEY `Course_Name_idx` (`Course_Name`),
  KEY `fk_CourseName_idx` (`Course_Name`),
  CONSTRAINT `fk_CourseName` FOREIGN KEY (`Course_Name`) REFERENCES `Courses` (`Course_Name`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=131 DEFAULT CHARSET=latin1;

-- Data exporting was unselected.
-- Dumping structure for table may1713_PrisonGardenApp.Users
CREATE TABLE IF NOT EXISTS `Users` (
  `UserID` int(11) NOT NULL,
  `Username` varchar(45) NOT NULL DEFAULT 'user',
  `Password` varchar(45) DEFAULT NULL,
  `First_Name` varchar(45) DEFAULT NULL,
  `Last_Name` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`Username`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Data exporting was unselected.
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IF(@OLD_FOREIGN_KEY_CHECKS IS NULL, 1, @OLD_FOREIGN_KEY_CHECKS) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
