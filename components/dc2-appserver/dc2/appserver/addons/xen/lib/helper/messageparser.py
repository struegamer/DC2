# -*- coding: utf-8 -*-
#
# (DC)² - DataCenter Deployment Control
# Copyright (C) 2010, 2011, 2012, 2013, 2014 Stephan Adig <sh@sourcecode.de>
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#

import xmlrpclib
import types


def parse_output(message=None):
    if message is not None and isinstance(message, dict):
        if 'Status' in message and message["Status"] == "Success":
            if 'Value' in message:
                return message["Value"]
            else:
                return xmlrpclib.Fault(
                    500,
                    "Missing Value in response from server")
        if 'Status' in message and message["Status"] == "Failure":
            if 'ErrorDescription' in message:
                return xmlrpclib.Fault(
                    500,
                    "Error: %{0} ({1})".format(
                        message["ErrorDescription"][0],
                        message["ErrorDescription"][1]))
