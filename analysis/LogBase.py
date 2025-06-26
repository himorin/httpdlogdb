#! /usr/bin/env python3

import sys

import gzip
from pytz import timezone
from SaveDB import SaveDB

class LogBase:
  obj_db = None

  def __init__(self, c_db):
    self.obj_db = c_db

  def LoadFile(self, fname, site, logtz):
    with open(fname, encoding="utf-8") as f:
      self.ParseFile(f, site, logtz)

  def LoadFileGz(self, fname, site, logtz):
    with gzip.open(fname, mode='rt', encoding="utf-8") as f:
      self.ParseFile(f, site, logtz)

  def ParseFile(self, f, site, logtz):
    siteid = self.obj_db.GetIDSite(site)
    for fline in f:
      c_lh = self.ParseLine(fline)
      if c_lh != None:
        if 'error' not in c_lh:
          # if error exists, just ignore?
          cid_method = self.obj_db.GetIDMethod(c_lh['method'], c_lh['code'])
          cid_dir = self.obj_db.GetIDDir(c_lh['path'])
          cid_refer = self.obj_db.GetIDRefer(c_lh['refer'])
          cid_ua = self.obj_db.GetIDBrowser(c_lh['ua'])
          atime_utc = c_lh['date'].astimezone(timezone('UTC')).strftime('%Y-%m-%d %H:%M:%S')
          atime_log = c_lh['date'].astimezone(timezone(logtz)).strftime('%Y-%m-%d')
          self.obj_db.AddLogRaw(siteid, c_lh['date'], cid_method, cid_dir, c_lh['query'], cid_refer, cid_ua)
          self.obj_db.AddAnaPage(siteid, atime_log, cid_dir)
          self.obj_db.AddAnaRef(siteid, atime_log, cid_dir, cid_refer)
          self.obj_db.AddAnaBrowser(siteid, atime_log, cid_dir, cid_ua)
        else:
          # c_lh['error'] contains query, usually GET to HTTP/*
          c_hd = c_lh['error'] # shorthand
          if c_hd == '' or c_hd == '-':
            pass # nothing supplied
          elif c_hd[0] == '{' and c_hd[-1] == '}':
            pass # json data attack
          else:
            try: # for catching .index error
              c_hd_idx = c_hd.index(' ')
              if c_hd_idx > -1 and c_hd.index(' ', c_hd_idx + 1) > -1:
                # could be normal one, register to log_error
                self.obj_db.AddLogError(siteid, fline)
            except Exception as e:
              pass # no or one white space, should be attack
      else:
        self.obj_db.AddLogError(siteid, fline)
    self.obj_db.AnaCommit()

  def ParseLine(self, ctxt):
    return {}

