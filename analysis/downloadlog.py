#! /usr/bin/env python3

import requests
import sys
import json

DEF_H_FNAME = 'filename='

site_list = {}

def LoadConfig(conf):
  try:
    fjson = open(conf, 'r')
  except IOError as e:
    raise Exception("File '%s' open error: %s" % (conf, e))
  try:
    site_config = json.load(fjson)
  except:
     raise Exception("json format parse error for '%s'" % (conf))
  return site_config

def DownloadLog(confname, date, tdir):
  o_ses = requests.Session()
  o_date = date
  o_conf = LoadConfig(confname)
  o_ret = o_ses.get(o_conf["init"]["url"])
  o_ret = o_ses.post(o_conf["login"]["url"], data = o_conf["login"]["opt"])
  o_ret = o_ses.get(o_conf["data"]["referer"])
  o_head = {
    "Referer": o_conf["data"]["referer"]
  }
  o_dat = {
    o_conf["data"]["opt"]: o_date
  }
  o_ret = o_ses.post(o_conf["data"]["url"], headers = o_head, data = o_dat)
  if o_ret.headers["content-type"] != "application/octet-stream":
    raise Exception("Error on loading log: %s" % (o_ret.text))
  o_fn = o_ret.headers["content-disposition"]
  o_fn = o_fn[o_fn.find(DEF_H_FNAME) + len(DEF_H_FNAME):]
  if o_fn[0:1] == '"':
    o_fn = o_fn[1:-1]
  c_tfname = tdir + '/' + o_fn
  with open(c_tfname, "wb") as sf:
    sf.write(o_ret.content)
  return c_tfname

if __name__ == "__main__":
  c_dir = '.'
  if len(sys.argv) == 4:
    c_dir = sys.argv[3]
  elif len(sys.argv) != 3:
    raise Exception("Invalid parameter: command <config> <date> <savedir>")
  print(DownloadLog(sys.argv[1], sys.argv[2], c_dir))

