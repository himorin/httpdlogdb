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

  def AddLogRaw(self, site, atime, method, dir, query, refer, browser):
    cursor = self._get_new_cursor()
    cursor.execute('INSERT INTO rawlog (site, atime, method, dir, query, refer, browser) VALUES (%s, %s, %s, %s, %s, %s, %s)', [site, atime, method, dir, query, refer, browser])

  def AddLogError(self, site, line):
    cursor = self._get_new_cursor()
    cursor.execute('INSERT INTO log_error (site, logline) VALUES (%s, %s)', [site, line])

  def AddAnaPage(self, site, date, dir):
    cursor = self._get_new_cursor()
    cursor.execute('SELECT * FROM ana_page WHERE site = %s AND target = %s and dir = %s', [site, date, dir])
    dat = cursor.fetchall()
    if len(dat) == 0:
      cursor.execute('INSERT INTO ana_page (site, target, dir, value) VALUES (%s, %s, %s, 1)', [site, date, dir])
    else:
      cursor.execute('UPDATE ana_page SET value = value + 1 WHERE site = %s AND target = %s AND dir = %s', [site, date, dir])
    self.cnx.commit()

  def AddAnaRef(self, site, date, dir, refer):
    cursor = self._get_new_cursor()
    cursor.execute('SELECT * FROM ana_ref WHERE site = %s AND target = %s and dir = %s AND refer = %s', [site, date, dir, refer])
    dat = cursor.fetchall()
    if len(dat) == 0:
      cursor.execute('INSERT INTO ana_ref (site, target, dir, refer, value) VALUES (%s, %s, %s, %s, 1)', [site, date, dir, refer])
    else:
      cursor.execute('UPDATE ana_ref SET value = value + 1 WHERE site = %s AND target = %s AND dir = %s AND refer = %s', [site, date, dir, refer])
    self.cnx.commit()

  def AddAnaBrowser(self, site, date, dir, browser):
    cursor = self._get_new_cursor()
    cursor.execute('SELECT * FROM ana_pagebr WHERE site = %s AND target = %s and dir = %s AND browser = %s', [site, date, dir, browser])
    dat = cursor.fetchall()
    if len(dat) == 0:
      cursor.execute('INSERT INTO ana_pagebr (site, target, dir, browser, value) VALUES (%s, %s, %s, %s, 1)', [site, date, dir, browser])
    else:
      cursor.execute('UPDATE ana_pagebr SET value = value + 1 WHERE site = %s AND target = %s AND dir = %s AND browser = %s', [site, date, dir, browser])
    self.cnx.commit()


