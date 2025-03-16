#! /usr/bin/env python3

import sys
import json

from LogApache import LogApache
from SaveDB import SaveDB

DEF_CONF_NAME = '../common/siteconfig.json'
DEF_CONF_LIST = '../common/sitelist.json'

site_config = {}
site_list = {}

def LoadConfig():
  try:
    fjson = open(DEF_CONF_NAME, 'r')
  except IOError as e:
    raise Exception("File '%s' open error: %s" % (DEF_CONF_NAME, e))
  try:
    site_config = json.load(fjson)
  except:
    raise Exception("json format parse error for '%s'" % (DEF_CONF_NAME))
  return site_config

def LoadSitelist():
  try:
    fjson = open(DEF_CONF_LIST, 'r')
  except IOError as e:
    raise Exception("File '%s' open error: %s" % (DEF_CONF_NAME, e))
  try:
    site_list = json.load(fjson)
  except:
    raise Exception("json format parse error for '%s'" % (DEF_CONF_NAME))
  return site_list

if __name__ == "__main__":
  site_config = LoadConfig()
  site_list = LoadSitelist()
  o_db = SaveDB()
  o_db.Connect(site_config)
  o_log = LogApache(o_db)
  for site in site_list.keys():
    o_log.LoadFile(site_list[site] + '/' + site_config['log_fname'], site, site_config['log_tz'])
  o_db.Close()


