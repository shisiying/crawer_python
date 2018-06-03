/*
Navicat MySQL Data Transfer

Source Server         : 5kcrm
Source Server Version : 50505
Source Host           : localhost:3306
Source Database       : eth

Target Server Type    : MYSQL
Target Server Version : 50505
File Encoding         : 65001

Date: 2018-06-02 13:45:15
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for `tradelist`
-- ----------------------------
DROP TABLE IF EXISTS `tradelist`;
CREATE TABLE `tradelist` (
  `id` int(8) NOT NULL AUTO_INCREMENT COMMENT 'id',
  `txHash` varchar(70) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT '交易哈希',
  `blockHeight` varchar(10) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT '高度',
  `amount` varchar(30) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT '金额变化数量',
  `originatorAdress` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT '发送方地址',
  `recevierAdress` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT '接受者地址',
  `confirmTime` datetime DEFAULT NULL COMMENT '确认时间',
  `brokerage` varchar(15) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT '矿工费',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- ----------------------------
-- Records of tradelist
-- ----------------------------
