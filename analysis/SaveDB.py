#! /usr/bin/env python3

import sys

import mysql.connector
from mysql.connector import errorcode

class SaveDB:

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
    except mysql.connector.Error as err:
      if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        raise Exception('Database access denied')
      elif err.errno == errorcode.ER_BAD_DB_ERROR:
        raise Exception('Specified database does not exist')
      else:
        raise Exception('Error occured on DB connection')
      self.cnx = None

  def _get_new_cursor(self):
    if self.cnx == None:
      raise Exception('Database not connected')
    return self.cnx.cursor()

  def Close(self):
    if self.cnx != None:
      self.cnx.commit()
      self.cnx.close()
      self.cnx = None

  # for dir, refer, browser
  def _get_id_string(self, arr, table, string):
    if string in arr:
      return arr[string]
    cursor = self._get_new_cursor()
    cursor.execute("SELECT * FROM {} WHERE val = %s;".format(table), [string])
    dat = cursor.fetchall()
    if len(dat) == 0:
      cursor.execute("INSERT INTO {} (val) VALUES (%s)".format(table), [string])
      if cursor.rowcount == 1:
        arr[string] = cursor.lastrowid
      dat = cursor.fetchall()
    else:
      row_ids = cursor.column_names
      dat_d = dict(zip(row_ids, dat[0]))
      arr[string] = dat_d['id']
    cursor.close()
    return arr[string]

  def GetIDDir(self, string):
    return self._get_id_string(self.cid_dir, 'dirid', string)

  def GetIDRefer(self, string):
    return self._get_id_string(self.cid_refer, 'referid', string)

  def GetIDBrowser(self, string):
    return self._get_id_string(self.cid_browser, 'browserid', string)

  def GetIDSite(self, string):
    if string in self.cid_site:
      return self.cid_site[string]
    cursor = self._get_new_cursor()
    cursor.execute("SELECT * FROM siteid WHERE val = %s", [string])
    dat = cursor.fetchall()
    if len(dat) == 0:
      cursor.execute("INSERT INTO siteid (val, url, memo) VALUES (%s, '', '')", [string])
      cursor.execute("SELECT * FROM siteid WHERE val = %s", [string])
      dat = cursor.fetchall()
    row_ids = cursor.column_names
    dat_d = dict(zip(row_ids, dat[0]))
    self.cid_site[string] = dat_d['id']
    cursor.close()
    return self.cid_site[string]

  def GetIDMethod(self, http, code):
    cid = http + '_' + code
    if cid in self.cid_method:
      return self.cid_method[cid]
    cursor = self._get_new_cursor()
    cursor.execute("SELECT * FROM methodid WHERE http = %s AND code = %s", [http, code])
    dat = cursor.fetchall()
    if len(dat) == 0:
      cursor.execute("INSERT INTO methodid (http, code) VALUES (%s, %s)", [http, code])
      cursor.execute("SELECT * FROM methodid WHERE http = %s AND code = %s", [http, code])
      dat = cursor.fetchall()
    row_ids = cursor.column_names
    dat_d = dict(zip(row_ids, dat[0]))
    self.cid_method[cid] = dat_d['id']
    cursor.close()
    return self.cid_method[cid]




  def Dump(self):
    print(self.cid_dir)
    print(self.cid_refer)
