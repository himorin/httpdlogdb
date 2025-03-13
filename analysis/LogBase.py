#! /usr/bin/env python3

import sys

from SaveDB import SaveDB

class LogBase:
  obj_db = None

  def __init__(self, c_db):
    self.obj_db = c_db

  def ParseFile(self, fname):
    with open(fname, encoding="utf-8") as f:
      for fline in f:
        c_lh = self.ParseLine(fline)
        if c_lh != None:
          cid_method = self.obj_db.GetIDMethod(c_lh['method'], c_lh['code'])
          cid_dir = self.obj_db.GetIDDir(c_lh['path'])
          cid_refer = self.obj_db.GetIDRefer(c_lh['refer'])
          cid_ua = self.obj_db.GetIDBrowser(c_lh['ua'])
          print(c_lh['date'].strftime('%Y%m%d%H%M%S') + ' ' + c_lh['path'] + ' ' + c_lh['fullquery'] + ' ' + c_lh['query'] + ' ' + c_lh['refer'] + ' {} {}'.format(cid_dir, cid_refer))
    self.obj_db.Close()
    self.obj_db.Dump()

  def ParseLine(self, ctxt):
    return {}

