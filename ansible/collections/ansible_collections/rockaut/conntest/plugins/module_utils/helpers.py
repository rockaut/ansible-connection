# (c) 2018 Red Hat Inc.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import ptvsd
ptvsd.enable_attach(address = ('0.0.0.0', 5678))

def ptvsd_enable_attach():
  ptvsd.enable_attach(address = ('0.0.0.0', 5678))
  a = 1

def ptvsd_wait_for_attach():
  ptvsd.wait_for_attach()
  a = 1

def ptvsd_break_into_debugger():
  ptvsd.break_into_debugger()
  a = 1
