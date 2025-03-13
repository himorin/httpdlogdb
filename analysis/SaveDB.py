#! /usr/bin/env python3

import sys

import mysql.connector
from mysql.connector import errorcode

class LogDBConn:

  # place holders for string
  cid_site = {}
  cid_method = {}
  cid_dir = {}
  cid_refer = {}
  cid_browser = {}

  def Connect(self, conf):
    db_dsn = {
      'user': conf['db_user'],
      'password': conf['db_pass'],
      'host': conf['db_host'],
      'database': conf['db_name'],
      'port': conf['db_port'],
    }
    try:
      self.cnx = mysql.connector.connect(**db_dsn)
    except: mysql.connector.Error as err:
      if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        raise Exception('Database access denied')
      elif err.errno == errorcode.ER_BAD_DB_ERROR:
        raise Exception('Specified database does not exist')
      else
        raise Exception('Error occured on DB connection')
      self.cnx = None

  def _get_new_cursor(self):
    if self.cnx == None:
      raise Exception('Database not connected')
    return self.cnx.cursor()

  def Close(self):
    if self.cnx != None:
      self.cnx.Close()
      self.cnx = None

  # for dir, refer, browser
  def _get_id_string(self, arr, table, string):
    if string in arr:
      return arr[string]
    cursor = self._get_new_cursor()
    cursor.execute("SELECT * FROM %s WHERE val = %s", [table + 'id', string])
    dat = cursor.fetchall()
    if len(dat) == 0:
      cursor.execute("INSERT INTO %s (val) VALUES (%s)", [table + 'id', string])
      cursor.execute("SELECT * FROM %s WHERE val = %s", [table + 'id', string])
      dat = cursor.fetchall()
    row_ids = cursor.column_names
    dat_d = dict(zip(row_ids, dat[0]))
    arr[string] = ret_d['id']
    return arr[string]

  def GetIDDir(self, string):
    return self._get_id_string(cid_dir, 'dir', string)

  def GetIDRefer(self, string):
    return self._get_id_string(cid_refer, 'refer', string)

  def GetIDBrowser(self, string):
    return self._get_id_string(cid_browser, 'browser', string)

  def GetIDSite(self, string):
    if string in cid_site:
      return cid_site[string]
    cursor = self._get_new_cursor()
    cursor.execute("SELECT * FROM siteid WHERE val = %s", [string])
    dat = cursor.fetchall()
    if len(dat) == 0:
      cursor.execute("INSERT INTO siteid (val, url, memo) VALUES (%s, '', '')", [string])
      cursor.execute("SELECT * FROM siteid WHERE val = %s", [string])
      dat = cursor.fetchall()
    row_ids = cursor.column_names
    dat_d = dict(zip(row_ids, dat[0]))
    cid_site[string] = ret_d['id']
    return cid_site[string]

  def GetIDMethod(self, http, code):
    cid = http + '_' + code
    if cid in cid_method:
      return cid_method[cid]
    cursor = self._get_new_cursor()
    cursor.execute("SELECT * FROM methodid WHERE http = %s AND code = %s", [http, code])
    dat = cursor.fetchall()
    if len(dat) == 0:
      cursor.execute("INSERT INTO methodid (http, code) VALUES (%s, %s)", [http, code])
      cursor.execute("SELECT * FROM methodid WHERE http = %s AND code = %s", [http, code])
      dat = cursor.fetchall()
    row_ids = cursor.column_names
    dat_d = dict(zip(row_ids, dat[0]))
    cid_method[cid] = ret_d['id']
    return cid_method[cid]





