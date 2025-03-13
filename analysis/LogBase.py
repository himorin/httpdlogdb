#! /usr/bin/env python3

import sys

class LogBase:
  obj_db = None

  def __init__(self, c_db):
    obj_db = c_db

  def ParseFile(self, fname):
    with open(fname, encoding="utf-8") as f:
      for fline in f:
        c_lh = self.ParseLine(fline)
        if c_lh != None:
          print(c_lh['date'].strftime('%Y%m%d%H%M%S') + ' ' + c_lh['path'])

  def ParseLine(self, ctxt):
    return {}

