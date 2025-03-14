#! /usr/bin/env python3

import sys
import json

from LogApache import LogApache
from SaveDB import SaveDB

DEF_CONF_NAME = '../common/siteconfig.json'

site_config = {}

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


if __name__ == "__main__":
  site_config = LoadConfig()
  o_db = SaveDB()
  o_db.Connect(site_config)
  o_log = LogApache(o_db)
  if sys.argv[1][-3:] == '.gz':
    o_log.LoadFileGz(sys.argv[1], sys.argv[2], site_config['log_tz'])
  else:
    o_log.LoadFile(sys.argv[1], sys.argv[2], site_config['log_tz'])
  o_db.Close()


