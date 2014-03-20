# -*- coding: utf-8 -*-
###############################################################################
#
#    (DC)² - DataCenter Deployment Control
#    Copyright (C) 2010, 2011, 2012, 2013, 2014  Stephan Adig <sh@sourcecode.de>
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

import types
from dc2.api import RPCClient


class Hosts(RPCClient):

    def find(self, rec=None):
        hostlist = []
        if rec is None:
            hostlist = self._proxy.dc2.inventory.hosts.list()
            return hostlist
        if rec is not None:
            if type(rec) is not types.DictType:
                # TODO: Add Real Exception
                raise Exception('The search argument is not a dictionary')
            hostlist = self._proxy.dc2.inventory.hosts.find(rec)
        return hostlist

    def list(self):
        hostlist = self.find()
        return hostlist

    def count(self):
        # TODO: Add a rpc call to appserver for counting
        hostlist = self.find()
        return len(hostlist)

    def get(self, *args, **kwargs):
        host = {}
        if 'id' in kwargs:
            host['_id'] = kwargs.get('id', None)
        if 'server_id' in kwargs:
            host['server_id'] = kwargs.get('server_id', None)
        if len(host) != 0:
            host_entries = self._proxy.dc2.inventory.hosts.find(host)
            if host_entries is not None and len(host_entries) == 1:
                return host_entries[0]
        return None

    def update(self, *args, **kwargs):
        host = {}
        if 'host' in kwargs:
            host = kwargs.get('host', None)
        doc_id = self._proxy.dc2.inventory.hosts.update(host)
        return doc_id
