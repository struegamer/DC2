# -*- coding: utf-8 -*-
###############################################################################
#
#    (DC)² - DataCenter Deployment Control
#    Copyright (C) 2010, 2011, 2012  Stephan Adig <sh@sourcecode.de>
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License along
#    with this program; if not, write to the Free Software Foundation, Inc.,
#    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
###############################################################################

import sys
import multiprocessing

try:
    from pymongo import Connection
except ImportError:
    print "You don't have pymongo python library installed"
    sys.exit(1)

class ConnectionError(Exception):
    pass

class ConnectionPool(object):
    def __init__(self):
        self._process = {}
        self._hostname = "localhost"
        self._port = 27017

    def connect(self, name=None, host=None, port=None):
        if not self._process.has_key(self._get_instance_pid()):
            self._process[self._get_instance_pid()] = {}
            if host is None or host == "":
                host = self._hostname
            if port is None or port == 0:
                port = self._port
            if name is None or name == "":
                name = "default"
            try:
                self._process[self._get_instance_pid()]["connection"] = Connection(host, port)
                self._process[self._get_instance_pid()]["name"] = name
                return True
            except:
                raise ConnectionError('Cannot connect to database on host %s:%s' % (host, port))


    def _get_instance_pid(self):
        return multiprocessing.current_process().pid
    def get_connection(self):
        if self._process.has_key(self._get_instance_pid()):
            return self._process[self._get_instance_pid()]["connection"]
        return None
