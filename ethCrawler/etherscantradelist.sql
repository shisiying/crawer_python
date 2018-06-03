/*
Navicat MySQL Data Transfer

Source Server         : 5kcrm
Source Server Version : 50505
Source Host           : localhost:3306
Source Database       : eth

Target Server Type    : MYSQL
Target Server Version : 50505
File Encoding         : 65001

Date: 2018-06-03 20:57:19
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for `etherscantradelist`
-- ----------------------------
DROP TABLE IF EXISTS `etherscantradelist`;
CREATE TABLE `etherscantradelist` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `txHash` varchar(70) COLLATE utf8_unicode_ci DEFAULT NULL,
  `age` varchar(30) COLLATE utf8_unicode_ci DEFAULT NULL,
  `fromadress` varchar(42) COLLATE utf8_unicode_ci DEFAULT NULL,
  `to` varchar(42) COLLATE utf8_unicode_ci DEFAULT NULL,
  `value` varchar(20) COLLATE utf8_unicode_ci DEFAULT NULL,
  `token` varchar(42) COLLATE utf8_unicode_ci DEFAULT NULL,
  `name` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- ----------------------------
-- Records of etherscantradelist
-- ----------------------------
