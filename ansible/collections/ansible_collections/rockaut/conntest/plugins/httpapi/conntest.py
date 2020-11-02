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
httpapi: rockaut.conntest.conntest
short_description: HttpApi Plugin for devices supporting conntest API
description:
- This HttpApi plugin provides methods to connect to conntest API endpoints.
version_added: 1.0.0
options:
  root_path:
    type: str
    description:
    - Specifies the location of the conntest root.
    default: /
    vars:
    - name: ansible_httpapi_conntest_root
"""

import json

from ansible.module_utils._text import to_text
from ansible.module_utils.connection import ConnectionError
from ansible.module_utils.six.moves.urllib.error import HTTPError
from ansible.plugins.httpapi import HttpApiBase

import q


CONTENT_TYPE = "application/json"

# look at https://github.com/ansible/ansible/blob/devel/lib/ansible/plugins/httpapi/__init__.py

class HttpApi(HttpApiBase):
    @q
    def send_request(self, data, **message_kwargs):
        path = "/".join(
            [
                self.get_option("root_path").rstrip("/"),
                message_kwargs.get("path", "").lstrip("/"),
            ]
        )

        headers = {
            "Content-Type": message_kwargs.get("content_type") or CONTENT_TYPE,
            "Accept": message_kwargs.get("accept") or CONTENT_TYPE,
        }
        response, response_data = self.connection.send(
            path, data, headers=headers, method=message_kwargs.get("method")
        )

        return handle_response(response, response_data)

    @q
    def update_auth(self, response, response_text):
        """Return per-request auth token.
        The response should be a dictionary that can be plugged into the
        headers of a request. The default implementation uses cookie data.
        If no authentication data is found, return None
        """
        cookie = response.info().get('Set-Cookie')
        if cookie:
            return {'Cookie': cookie}

        return None

    @q
    def login(self, username, password):
        """Call a defined login endpoint to receive an authentication token.
        This should only be implemented if the API has a single endpoint which
        can turn HTTP basic auth into a token which can be reused for the rest
        of the calls for the session.
        """
        pass

    @q
    def logout(self):
        """ Call to implement session logout.
        Method to clear session gracefully e.g. tokens granted in login
        need to be revoked.
        """
        pass

    @q
    def handle_httperror(self, exc):
        """Overridable method for dealing with HTTP codes.
        This method will attempt to handle known cases of HTTP status codes.
        If your API uses status codes to convey information in a regular way,
        you can override this method to handle it appropriately.
        :returns:
            * True if the code has been handled in a way that the request
            may be resent without changes.
            * False if the error cannot be handled or recovered from by the
            plugin. This will result in the HTTPError being raised as an
            exception for the caller to deal with as appropriate (most likely
            by failing).
            * Any other value returned is taken as a valid response from the
            server without making another request. In many cases, this can just
            be the original exception.
            """
        if exc.code == 401:
            if self.connection._auth:
                # Stored auth appears to be invalid, clear and retry
                self.connection._auth = None
                self.login(self.connection.get_option('remote_user'), self.connection.get_option('password'))
                return True
            else:
                # Unauthorized and there's no token. Return an error
                return False

        return exc


def handle_response(response, response_data):
    try:
        response_data = json.loads(response_data.read())
    except ValueError:
        response_data = response_data.read()

    if isinstance(response, HTTPError):
        if response_data:
            if "errors" in response_data:
                errors = response_data["errors"]["error"]
                error_text = "\n".join(
                    (error["error-message"] for error in errors)
                )
            else:
                error_text = response_data

            raise ConnectionError(error_text, code=response.code)
        raise ConnectionError(to_text(response), code=response.code)

    return response_data
