# -*- coding: utf-8 -*-
#
#
# (DC)² - DataCenter Deployment Control
# Copyright (C) 2010, 2011, 2012, 2013, 2014  Stephan Adig <sh@sourcecode.de>
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

import sys

try:
    from socketIO_client import BaseNamespace
except ImportError as e:
    print(1)
    sys.exit(1)


class CommandNamespace(BaseNamespace):
    pass


class Commands(object):

    def __init__(self, client):
        self._client = client
        self._ns = self._client.socketio.define(CommandNamespace, '/commands')

    def send_discovered(self, data=None):
        if data is not None:
            if isinstance(data, dict):
                self._ns.emit('discovered', data)
            elif isinstance(data, list):
                for date in data:
                    if isinstance(date, dict):
                        self._ns.emit('discovered', date)
        self._client.socketio.wait(seconds=2)
        return True
