#! /usr/bin/env python3

import requests
import sys
import json

import downloadlog
import parse_file
import datetime

DEF_CONF_DIR = '../common/'

def LoadTargets(conf):
  try:
    fjson = open(conf, 'r')
  except IOError as e:
    raise Exception("File '%s' open error: %s" % (conf, e))
  try:
    targets = json.load(fjson)
  except: 
    raise Exception("json format parse error for '%s'" % (conf))
  return targets

def DownImport(confname):
  o_tgt = LoadTargets(confname)
  td = datetime.date.today() - datetime.timedelta(days=1)
  for c_tgt in o_tgt:
    c_td = td.strftime(c_tgt['date'])
    try:
      cfname = downloadlog.DownloadLog(DEF_CONF_DIR + c_tgt['srv'] + '.json', c_td, c_tgt['save'])
    except e:
      print("Download error for '%s' - %s" % (c_tgt['srv'], e))
    try:
      parse_file.LoadFile(cfname, c_tgt['srv'])
    except e:
      print("Load log error for '%s' - %s" % (c_tgt['srv'], e))

if __name__ == "__main__":
  if len(sys.argv) != 2:
    raise Exception("Invalid parameter: command <config>")
  DownImport(sys.argv[1])

