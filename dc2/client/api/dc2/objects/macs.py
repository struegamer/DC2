# -*- coding: utf-8 -*-
#
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
#

import xmlrpclib


class MACs(object):

    def __init__(self, rpcurl=None):
        self._rpcurl = rpcurl
        self._proxy = xmlrpclib.ServerProxy(self._rpcurl, allow_none=True)

    def find(self, mac_addr=None):
        if mac_addr is not None:
            mac_list = self._proxy.dc2.inventory.servers.macaddr.find({"mac_addr": mac_addr})
            if mac_list is not None and len(mac_list) > 0 and mac_list[0] is not None:
                return mac_list[0]
        return None

    def find_by_device_name(self, server_id=None, device_name=None):
        if server_id is not None and device_name is not None:
            mac_list = self._proxy.dc2.inventory.servers.macaddr.find({'server_id': server_id, 'device_name': device_name})
            if mac_list is not None and len(mac_list) > 0 and mac_list[0] is not None:
                return mac_list[0]
