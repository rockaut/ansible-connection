# Copyright (c) 2018 Cisco and/or its affiliates.
#
# This file is part of Ansible
#
# Ansible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.
#

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = """
author: Ansible Networking Team
httpapi: restconf
short_description: HttpApi Plugin for devices supporting Restconf API
description:
- This HttpApi plugin provides methods to connect to Restconf API endpoints.
version_added: 1.0.0
options:
  root_path:
    type: str
    description:
    - Specifies the location of the Restconf root.
    default: /restconf
    vars:
    - name: ansible_httpapi_restconf_root
"""

import json

from ansible.plugins.httpapi import HttpApiBase

import ansible_collections.rockaut.conntest.plugins.module_utils.helpers as helpers
helpers.ptvsd_wait_for_attach()

class HttpApi(HttpApiBase):
  def __init__(self, connection):
      super(HttpApi, self).__init__(connection)
      a = 1
  def send_request(self, data, **message_kwargs):
      a = 1