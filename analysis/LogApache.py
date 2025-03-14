#! /usr/bin/env python3

import sys
import re

from datetime import datetime
from LogBase import LogBase

class LogApache(LogBase):
  o_re = None

  def __init__(self, c_db):
    super().__init__(c_db)
    self.o_re = re.compile(r'([0-9\.:]+) - ([^ ]+) \[([0-9a-zA-Z \/:\-\+]+)\] "([^ ]+) (.+) ([^ ]+)" ([0-9]+) ([0-9]+) "(.*)" "(.+)"')

  def ParseLine(self, line):
    c_ret = {}
    c_match = self.o_re.match(line, 0)
    if c_match == None:
      return None
    c_arr = c_match.groups()
    c_ret['ip'] = c_arr[0]
    if c_arr[1] == '-':
      c_ret['user'] = None
    else:
      c_ret['user'] = c_arr[1]
    c_ret['datestring'] = c_arr[2]
    c_ret['date'] = datetime.strptime(c_arr[2], '%d/%b/%Y:%H:%M:%S %z')
    c_ret['method'] = c_arr[3]
    c_ret['fullquery'] = c_arr[4]
    sep = c_ret['fullquery'].find('?')
    if sep > 0:
      c_ret['path'] = c_ret['fullquery'][0:sep]
      c_ret['query'] = c_ret['fullquery'][sep + 1:]
    else:
      c_ret['path'] = c_ret['fullquery']
      c_ret['query'] = ''
    c_ret['http'] = c_arr[5]
    c_ret['code'] = c_arr[6]
    c_ret['byte'] = c_arr[7]
    c_ret['refer'] = c_arr[8]
    c_ret['ua'] = c_arr[9]
    return c_ret


