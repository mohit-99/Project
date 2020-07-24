/*
SQLyog Ultimate v11.11 (64 bit)
MySQL - 5.0.27-community-nt : Database - pythondb
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
CREATE DATABASE /*!32312 IF NOT EXISTS*/`pythondb` /*!40100 DEFAULT CHARACTER SET latin1 */;

USE `pythondb`;

/*Table structure for table `areamaster` */

DROP TABLE IF EXISTS `areamaster`;

CREATE TABLE `areamaster` (
  `areaId` int(11) NOT NULL auto_increment,
  `areaName` varchar(100) default NULL,
  `areaPincode` int(11) default NULL,
  PRIMARY KEY  (`areaId`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*Data for the table `areamaster` */

insert  into `areamaster`(`areaId`,`areaName`,`areaPincode`) values (1,'Satellite',380015),(2,'Jivraj',380051),(3,'Vejalpur',300511),(4,'Bodakdev',380016),(5,'Vastral',382418);

/*Table structure for table `branchmaster` */

DROP TABLE IF EXISTS `branchmaster`;

CREATE TABLE `branchmaster` (
  `branchId` int(11) NOT NULL auto_increment,
  `branchCode` int(11) default NULL,
  `branchName` varchar(100) default NULL,
  `branch_AreaId` int(11) default NULL,
  `branch_RestaurantId` int(11) default NULL,
  PRIMARY KEY  (`branchId`),
  KEY `branch_AreaId` (`branch_AreaId`),
  KEY `branch_RestaurantId` (`branch_RestaurantId`),
  CONSTRAINT `branchmaster_ibfk_1` FOREIGN KEY (`branch_AreaId`) REFERENCES `areamaster` (`areaId`),
  CONSTRAINT `branchmaster_ibfk_2` FOREIGN KEY (`branch_RestaurantId`) REFERENCES `restaurantmaster` (`restaurantId`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*Data for the table `branchmaster` */

insert  into `branchmaster`(`branchId`,`branchCode`,`branchName`,`branch_AreaId`,`branch_RestaurantId`) values (2,123123,'Garden',2,1),(3,123456,'Mall',1,1);

/*Table structure for table `complainmaster` */

DROP TABLE IF EXISTS `complainmaster`;

CREATE TABLE `complainmaster` (
  `complainId` int(11) NOT NULL auto_increment,
  `complainSubject` varchar(100) NOT NULL,
  `complainDescription` varchar(500) default NULL,
  `complainDate` varchar(100) default NULL,
  `complainTime` varchar(100) default NULL,
  `complainStatus` varchar(100) default NULL,
  `complainFileName` varchar(100) default NULL,
  `complainFilePath` varchar(200) default NULL,
  `complainTo_LoginId` int(11) default NULL,
  `complainFrom_LoginId` int(11) default NULL,
  `replySubject` varchar(100) default NULL,
  `replyMessage` varchar(500) default NULL,
  `replyFileName` varchar(100) default NULL,
  `replyFilePath` varchar(100) default NULL,
  `replyDate` varchar(100) default NULL,
  `replyTime` varchar(100) default NULL,
  PRIMARY KEY  (`complainId`),
  KEY `complainTo_LoginId` (`complainTo_LoginId`),
  KEY `complainFrom_LoginId` (`complainFrom_LoginId`),
  CONSTRAINT `complainmaster_ibfk_1` FOREIGN KEY (`complainTo_LoginId`) REFERENCES `loginmaster` (`loginId`),
  CONSTRAINT `complainmaster_ibfk_2` FOREIGN KEY (`complainFrom_LoginId`) REFERENCES `loginmaster` (`loginId`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*Data for the table `complainmaster` */

insert  into `complainmaster`(`complainId`,`complainSubject`,`complainDescription`,`complainDate`,`complainTime`,`complainStatus`,`complainFileName`,`complainFilePath`,`complainTo_LoginId`,`complainFrom_LoginId`,`replySubject`,`replyMessage`,`replyFileName`,`replyFilePath`,`replyDate`,`replyTime`) values (1,'Trash Services','ASDFGHKL;/','2020-03-09','11:29:51','Replied','02fdb71b1bee428ffc0a386a67e1f1fa-6-1920x1080.jpg','../static/userResources/complainAttachment/',2,4,'xnbmn,.','zdxfm,./','987-game-of-thrones-game-of-thrones.jpg','../static/adminResources/replyAttachment/','2020-03-09','11:31:03'),(2,'sxcvbhnjkm','vcb ,., . ;.k','2020-04-09','17:05:03','Pending','0d2035688d92c49eeabdfa5197a5a786.jpg','../static/userResources/complainAttachment/',NULL,4,NULL,NULL,NULL,NULL,NULL,NULL);

/*Table structure for table `datasetmaster` */

DROP TABLE IF EXISTS `datasetmaster`;

CREATE TABLE `datasetmaster` (
  `datasetId` int(11) NOT NULL auto_increment,
  `datasetFilename` varchar(100) default NULL,
  `datasetFilepath` varchar(100) default NULL,
  `datasetUploadDate` varchar(100) default NULL,
  `datasetUploadTime` varchar(100) default NULL,
  PRIMARY KEY  (`datasetId`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*Data for the table `datasetmaster` */

insert  into `datasetmaster`(`datasetId`,`datasetFilename`,`datasetFilepath`,`datasetUploadDate`,`datasetUploadTime`) values (1,'02fdb71b1bee428ffc0a386a67e1f1fa-6-1920x1080.jpg','../static/adminResources/dataset/','2020-01-29','12:24:48'),(2,'992-game-of-thrones-game-of-thrones.jpg','../static/adminResources/dataset/','2020-02-01','10:05:16'),(3,'PicsArt_01-30-10.30.21.png','../static/adminResources/dataset/','2020-02-06','09:56:13');

/*Table structure for table `feedbackmaster` */

DROP TABLE IF EXISTS `feedbackmaster`;

CREATE TABLE `feedbackmaster` (
  `feedbackId` int(11) NOT NULL auto_increment,
  `feedbackSubject` varchar(100) NOT NULL,
  `feedbackDescription` varchar(500) default NULL,
  `feedbackRating` int(11) default NULL,
  `feedbackDate` varchar(100) default NULL,
  `feedbackTime` varchar(100) default NULL,
  `feedbackTo_LoginId` int(11) default NULL,
  `feedbackFrom_LoginId` int(11) default NULL,
  PRIMARY KEY  (`feedbackId`),
  KEY `feedbackTo_LoginId` (`feedbackTo_LoginId`),
  KEY `feedbackFrom_LoginId` (`feedbackFrom_LoginId`),
  CONSTRAINT `feedbackmaster_ibfk_1` FOREIGN KEY (`feedbackTo_LoginId`) REFERENCES `loginmaster` (`loginId`),
  CONSTRAINT `feedbackmaster_ibfk_2` FOREIGN KEY (`feedbackFrom_LoginId`) REFERENCES `loginmaster` (`loginId`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*Data for the table `feedbackmaster` */

insert  into `feedbackmaster`(`feedbackId`,`feedbackSubject`,`feedbackDescription`,`feedbackRating`,`feedbackDate`,`feedbackTime`,`feedbackTo_LoginId`,`feedbackFrom_LoginId`) values (5,'saAS','SASD',2,'2020-02-24','11:18:56',2,4),(6,'Sample Feedback','dfsghjkl/;',5,'2020-03-09','11:32:03',2,4),(7,'Sample Feedback','asdfghjkl',3,'2020-04-09','17:18:51',2,5);

/*Table structure for table `loginmaster` */

DROP TABLE IF EXISTS `loginmaster`;

CREATE TABLE `loginmaster` (
  `loginId` int(11) NOT NULL auto_increment,
  `loginUsername` varchar(100) default NULL,
  `loginPassword` varchar(100) default NULL,
  `loginRole` varchar(100) default NULL,
  `loginStatus` varchar(100) default NULL,
  PRIMARY KEY  (`loginId`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*Data for the table `loginmaster` */

insert  into `loginmaster`(`loginId`,`loginUsername`,`loginPassword`,`loginRole`,`loginStatus`) values (2,'admin@gmail.com','admin12345','admin','active'),(4,'khushaws@gmail.com','rest12345','user','active'),(5,'preetbhatt.p@gmail.com','a4FvWx1j','user','active'),(6,'preetbhatt.p@gmail.com','pUeYOYhx','user','inactive');

/*Table structure for table `packagemaster` */

DROP TABLE IF EXISTS `packagemaster`;

CREATE TABLE `packagemaster` (
  `packageId` int(11) NOT NULL auto_increment,
  `packageName` varchar(100) default NULL,
  `packageDuration` varchar(100) default NULL,
  `packagePrice` int(11) default NULL,
  PRIMARY KEY  (`packageId`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*Data for the table `packagemaster` */

insert  into `packagemaster`(`packageId`,`packageName`,`packageDuration`,`packagePrice`) values (1,'Silver','3 Months',5000),(2,'Gold','8 Months',8000),(3,'Platinum','12 Months',10000);

/*Table structure for table `purchasemaster` */

DROP TABLE IF EXISTS `purchasemaster`;

CREATE TABLE `purchasemaster` (
  `purchaseId` int(11) NOT NULL auto_increment,
  `purchase_PackageId` int(11) default NULL,
  `purchase_LoginId` int(11) default NULL,
  `purchaseDate` varchar(100) default NULL,
  `purchaseTime` varchar(100) default NULL,
  PRIMARY KEY  (`purchaseId`),
  KEY `purchase_PackageId` (`purchase_PackageId`),
  KEY `purchase_LoginId` (`purchase_LoginId`),
  CONSTRAINT `purchasemaster_ibfk_1` FOREIGN KEY (`purchase_PackageId`) REFERENCES `packagemaster` (`packageId`),
  CONSTRAINT `purchasemaster_ibfk_2` FOREIGN KEY (`purchase_LoginId`) REFERENCES `loginmaster` (`loginId`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*Data for the table `purchasemaster` */

insert  into `purchasemaster`(`purchaseId`,`purchase_PackageId`,`purchase_LoginId`,`purchaseDate`,`purchaseTime`) values (1,3,4,'2020-04-06','20:58:06');

/*Table structure for table `regionfourmaster` */

DROP TABLE IF EXISTS `regionfourmaster`;

CREATE TABLE `regionfourmaster` (
  `regionFourId` int(11) NOT NULL auto_increment,
  `regionFourPerson` int(11) default NULL,
  `regionFourTime` int(11) default NULL,
  `regionFour_VideoId` int(11) default NULL,
  PRIMARY KEY  (`regionFourId`),
  KEY `regionFour_VideoId` (`regionFour_VideoId`),
  CONSTRAINT `regionfourmaster_ibfk_1` FOREIGN KEY (`regionFour_VideoId`) REFERENCES `videomaster` (`videoId`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*Data for the table `regionfourmaster` */

insert  into `regionfourmaster`(`regionFourId`,`regionFourPerson`,`regionFourTime`,`regionFour_VideoId`) values (2,1,40,2);

/*Table structure for table `regiononemaster` */

DROP TABLE IF EXISTS `regiononemaster`;

CREATE TABLE `regiononemaster` (
  `regionOneId` int(11) NOT NULL auto_increment,
  `regionOnePerson` int(11) default NULL,
  `regionOneTime` int(11) default NULL,
  `regionOne_VideoId` int(11) default NULL,
  PRIMARY KEY  (`regionOneId`),
  KEY `regionOne_VideoId` (`regionOne_VideoId`),
  CONSTRAINT `regiononemaster_ibfk_1` FOREIGN KEY (`regionOne_VideoId`) REFERENCES `videomaster` (`videoId`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*Data for the table `regiononemaster` */

/*Table structure for table `regionthreemaster` */

DROP TABLE IF EXISTS `regionthreemaster`;

CREATE TABLE `regionthreemaster` (
  `regionThreeId` int(11) NOT NULL auto_increment,
  `regionThreePerson` int(11) default NULL,
  `regionThreeTime` int(11) default NULL,
  `regionThree_VideoId` int(11) default NULL,
  PRIMARY KEY  (`regionThreeId`),
  KEY `regionThree_VideoId` (`regionThree_VideoId`),
  CONSTRAINT `regionthreemaster_ibfk_1` FOREIGN KEY (`regionThree_VideoId`) REFERENCES `videomaster` (`videoId`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*Data for the table `regionthreemaster` */

/*Table structure for table `regiontwomaster` */

DROP TABLE IF EXISTS `regiontwomaster`;

CREATE TABLE `regiontwomaster` (
  `regionTwoId` int(11) NOT NULL auto_increment,
  `regionTwoPerson` int(11) default NULL,
  `regionTwoTime` int(11) default NULL,
  `regionTwo_VideoId` int(11) default NULL,
  PRIMARY KEY  (`regionTwoId`),
  KEY `regionTwo_VideoId` (`regionTwo_VideoId`),
  CONSTRAINT `regiontwomaster_ibfk_1` FOREIGN KEY (`regionTwo_VideoId`) REFERENCES `videomaster` (`videoId`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*Data for the table `regiontwomaster` */

insert  into `regiontwomaster`(`regionTwoId`,`regionTwoPerson`,`regionTwoTime`,`regionTwo_VideoId`) values (2,2,40,2),(3,1,20,3),(4,1,13,3);

/*Table structure for table `restaurantmaster` */

DROP TABLE IF EXISTS `restaurantmaster`;

CREATE TABLE `restaurantmaster` (
  `restaurantId` int(11) NOT NULL auto_increment,
  `restaurantName` varchar(100) NOT NULL,
  `restaurantNumber` decimal(10,0) NOT NULL,
  `restaurantOwner` varchar(100) NOT NULL,
  `restaurant_AreaId` int(11) default NULL,
  `restaurant_LoginId` int(11) default NULL,
  PRIMARY KEY  (`restaurantId`),
  KEY `restaurant_AreaId` (`restaurant_AreaId`),
  KEY `restaurant_LoginId` (`restaurant_LoginId`),
  CONSTRAINT `restaurantmaster_ibfk_1` FOREIGN KEY (`restaurant_AreaId`) REFERENCES `areamaster` (`areaId`),
  CONSTRAINT `restaurantmaster_ibfk_2` FOREIGN KEY (`restaurant_LoginId`) REFERENCES `loginmaster` (`loginId`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*Data for the table `restaurantmaster` */

insert  into `restaurantmaster`(`restaurantId`,`restaurantName`,`restaurantNumber`,`restaurantOwner`,`restaurant_AreaId`,`restaurant_LoginId`) values (1,'Starbucks',7802948846,'Khush Upadhyay',1,4),(2,'HoneyCube',9638520741,'Preet',1,6);

/*Table structure for table `videomaster` */

DROP TABLE IF EXISTS `videomaster`;

CREATE TABLE `videomaster` (
  `videoId` int(11) NOT NULL auto_increment,
  `inputVideoFileName` varchar(100) default NULL,
  `inputVideoFilePath` varchar(100) default NULL,
  `inputVideoUploadDate` varchar(100) default NULL,
  `inputVideoUploadTime` varchar(100) default NULL,
  `outputVideoFileName` varchar(100) default NULL,
  `outputVideoFilePath` varchar(100) default NULL,
  `outputVideoUploadDate` varchar(100) default NULL,
  `outputVideoUploadTime` varchar(100) default NULL,
  `video_BranchId` int(11) default NULL,
  `video_AreaId` int(11) default NULL,
  `video_LoginId` int(11) default NULL,
  PRIMARY KEY  (`videoId`),
  KEY `video_BranchId` (`video_BranchId`),
  KEY `video_AreaId` (`video_AreaId`),
  KEY `video_LoginId` (`video_LoginId`),
  CONSTRAINT `videomaster_ibfk_1` FOREIGN KEY (`video_BranchId`) REFERENCES `branchmaster` (`branchId`),
  CONSTRAINT `videomaster_ibfk_2` FOREIGN KEY (`video_AreaId`) REFERENCES `areamaster` (`areaId`),
  CONSTRAINT `videomaster_ibfk_3` FOREIGN KEY (`video_LoginId`) REFERENCES `loginmaster` (`loginId`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*Data for the table `videomaster` */

insert  into `videomaster`(`videoId`,`inputVideoFileName`,`inputVideoFilePath`,`inputVideoUploadDate`,`inputVideoUploadTime`,`outputVideoFileName`,`outputVideoFilePath`,`outputVideoUploadDate`,`outputVideoUploadTime`,`video_BranchId`,`video_AreaId`,`video_LoginId`) values (2,'Three_People_Eating_Food_For_Two_Hours_HD_1_1.mp4','../static/userResources/video/','2020-05-09','13:51:29','Three_People_Eating_Food_For_Two_Hours_HD_1_1.webm','../static/userResources/video/output/','2020-05-09','14:17:09',3,1,4),(3,'V111.mp4','../static/userResources/video/','2020-05-09','14:22:24','V111.webm','../static/userResources/video/output/','2020-05-09','14:41:00',3,1,4),(4,'Sushi_restaurant.mp4','../static/userResources/video/','2020-06-03','14:54:56','Sushi_restaurant.webm','../static/userResources/video/output/','2020-06-03','14:58:12',2,2,4);

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
