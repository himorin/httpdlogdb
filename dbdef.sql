CREATE DATABASE httpdlogdb;
GRANT delete,insert,lock tables,select,update,drop,create,index,references,CREATE TEMPORARY TABLES, alter on httpdlogdb.* to httpdlogdb@localhost identified by 'XXX';

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
  site             int UNSIGNED NOT NULL UNIQUE AUTO_INCREMENT    ,
  sitename         text         NOT NULL                          ,
  url              text         NOT NULL                          ,
  memo             text         NOT NULL                          
) DEFAULT CHARSET=utf8;

CREATE TABLE methodid (
  method           tinyint UNSIGNED NOT NULL UNIQUE AUTO_INCREMENT ,
  http             text         NOT NULL                          ,
  code             smallint     NOT NULL                          
) DEFAULT CHARSET=utf8;

CREATE TABLE dirid (
  dir              int UNSIGNED NOT NULL UNIQUE AUTO_INCREMENT    ,
  name             text         NOT NULL                          
) DEFAULT CHARSET=utf8;

CREATE TABLE referid (
  refer            int UNSIGNED NOT NULL UNIQUE AUTO_INCREMENT    ,
  url              text         NOT NULL                          
) DEFAULT CHARSET=utf8;

CREATE TABLE browserid (
  browser          int UNSIGNED NOT NULL UNIQUE AUTO_INCREMENT    ,
  brstring         text         NOT NULL                          
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

