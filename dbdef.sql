/*
CREATE DATABASE httpdlogdb;
GRANT delete,insert,lock tables,select,update,drop,create,index,references,CREATE TEMPORARY TABLES, alter on httpdlogdb.* to httpdlogdb@localhost identified by 'XXX';
*/

CREATE TABLE rawlog (
  site             int UNSIGNED NOT NULL                          ,
  atime            DATETIME     NOT NULL                          ,
  method           tinyint UNSIGNED NOT NULL                      ,
  dir              int UNSIGNED NOT NULL                          ,
  query            text             NULL                          ,
  refer            int UNSIGNED NOT NULL                          ,
  browser          int UNSIGNED NOT NULL                          
) DEFAULT CHARSET=utf8;

CREATE TABLE siteid (
  id               int UNSIGNED NOT NULL UNIQUE AUTO_INCREMENT    ,
  val              text         NOT NULL                          ,
  url              text         NOT NULL                          ,
  memo             text         NOT NULL                          
) DEFAULT CHARSET=utf8;

CREATE TABLE methodid (
  id               tinyint UNSIGNED NOT NULL UNIQUE AUTO_INCREMENT ,
  http             text         NOT NULL                          ,
  code             smallint     NOT NULL                          
) DEFAULT CHARSET=utf8;

CREATE TABLE dirid (
  id               int UNSIGNED NOT NULL UNIQUE AUTO_INCREMENT    ,
  val              text         NOT NULL                          
) DEFAULT CHARSET=utf8;

CREATE TABLE referid (
  id               int UNSIGNED NOT NULL UNIQUE AUTO_INCREMENT    ,
  val              text         NOT NULL                          
) DEFAULT CHARSET=utf8;

CREATE TABLE browserid (
  id               int UNSIGNED NOT NULL UNIQUE AUTO_INCREMENT    ,
  val              text         NOT NULL                          
) DEFAULT CHARSET=utf8;

CREATE TABLE ana_page (
  site             int UNSIGNED NOT NULL                          ,
  target           DATE         NOT NULL                          ,
  dir              int UNSIGNED NOT NULL                          ,
  value            int UNSIGNED NOT NULL                          
) DEFAULT CHARSET=utf8;

CREATE TABLE ana_ref (
  site             int UNSIGNED NOT NULL                          ,
  target           DATE         NOT NULL                          ,
  dir              int UNSIGNED NOT NULL                          ,
  refer            int UNSIGNED NOT NULL                          ,
  value            int UNSIGNED NOT NULL                          
) DEFAULT CHARSET=utf8;

CREATE TABLE ana_pagebr (
  site             int UNSIGNED NOT NULL                          ,
  target           DATE         NOT NULL                          ,
  dir              int UNSIGNED NOT NULL                          ,
  browser          int UNSIGNED NOT NULL                          ,
  value            int UNSIGNED NOT NULL                          
) DEFAULT CHARSET=utf8;

CREATE TABLE log_error (
  site             int UNSIGNED NOT NULL                          ,
  logline          text         NOT NULL                          
) DEFAULT CHARSET=utf8;

