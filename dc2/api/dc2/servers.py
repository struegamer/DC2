# -*- coding: utf-8 -*-
#################################################################################
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
#################################################################################

import xmlrpclib

class Servers(object):
    def __init__(self, rpcurl=None):
        if rpcurl is None:
            # TODO: Add Real Exception
            raise Exception('No RPCUrl given')
        self._rpcurl=rpcurl
        self._proxy=xmlrpclib.ServerProxy(self._rpcurl,allow_none=True)

    def find_servers(self,rec=None):
        if rec is None:
            serverlist=self._proxy.dc2.inventory.servers.list()
            return serverlist
        if rec is not None:
            if type(rec) is not types.DictType:
                # TODO: Add Real Exception
                raise Exception('The search argument is not a dictionary')
            serverlist=self._proxy.dc2.inventory.servers.find(rec)
            return serverlist

