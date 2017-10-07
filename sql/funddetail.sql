/*
Navicat MySQL Data Transfer

Source Server         : 5kcrm
Source Server Version : 50505
Source Host           : localhost:3306
Source Database       : jijin

Target Server Type    : MYSQL
Target Server Version : 50505
File Encoding         : 65001

Date: 2017-10-07 22:00:34
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for `funddetail`
-- ----------------------------
DROP TABLE IF EXISTS `funddetail`;
CREATE TABLE `funddetail` (
  `id` int(11) NOT NULL COMMENT '自增字段',
  `fcode` varchar(10) NOT NULL COMMENT '基金编码',
  `fdate` datetime DEFAULT NULL COMMENT '基金日期',
  `NAV` decimal(10,4) DEFAULT NULL COMMENT '单位净值',
  `ACCNAV` decimal(10,4) DEFAULT NULL COMMENT '累计净值',
  `DGR` varchar(20) DEFAULT NULL COMMENT '日增长率',
  `pstate` varchar(20) DEFAULT NULL COMMENT '申购状态',
  `rstate` varchar(20) DEFAULT NULL COMMENT '赎回状态',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of funddetail
-- ----------------------------
