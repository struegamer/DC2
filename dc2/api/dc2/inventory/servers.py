# -*- coding: utf-8 -*-
###############################################################################
#
#    (DC)² - DataCenter Deployment Control
#    Copyright (C) 2010, 2011, 2012, 2013  Stephan Adig <sh@sourcecode.de>
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


class Servers(RPCClient):

    def find(self, rec=None):
        if rec is None:
            serverlist = self._proxy.dc2.inventory.servers.list()
            return serverlist
        if rec is not None:
            if type(rec) is not types.DictType:
                # TODO: Add Real Exception
                raise Exception('The search argument is not a dictionary')
            serverlist = self._proxy.dc2.inventory.servers.find(rec)
            return serverlist

    def list(self):
        serverlist = self.find()
        return serverlist

    def count(self):
        # TODO: Add a rpc call to appserver for counting
        serverlist = self.find()
        return len(serverlist)

    def get(self, *args, **kwargs):
        rec = {}
        if 'id' in kwargs:
            rec['_id'] = kwargs.get('id', None)
        if 'serial_no' in kwargs:
            rec['serial_no'] = kwargs.get('serial_no', None)
        server = self._proxy.dc2.inventory.servers.find(rec)
        if len(server) == 1:
            return server[0]
        return []

    def add(self, *args, **kwargs):
        server_rec = kwargs.get('server', None)
        if server_rec is not None:
            return self._proxy.dc2.inventory.servers.add(server_rec)
        return False

    def update(self, *args, **kwargs):
        server_rec = kwargs.get('server', None)
        if server_rec is not None:
            return self._proxy.dc2.inventory.servers.update(server_rec)
        return False

    def delete(self, *args, **kwargs):
        server_rec = {}
        if 'server_id' in kwargs:
            server_rec['_id'] = kwargs.get('server_id', None)
        if 'serial_no' in kwargs:
            server_rec['serial_no'] = kwargs.get('serial_no', None)
        if len(server_rec) > 0:
            return self._proxy.dc2.inventory.servers.delete(server_rec)
        return False

    def delete_complete(self, *args, **kwargs):
        server_rec = {}
        if 'server_id' in kwargs:
            server_rec['_id'] = kwargs.get('server_id', None)
        if 'serial_no' in kwargs:
            server_rec['serial_no'] = kwargs.get('serial_no', None)
        if len(server_rec) > 0:
            return self._proxy.dc2.inventory.servers.delete_complete(server_rec)
        return False
