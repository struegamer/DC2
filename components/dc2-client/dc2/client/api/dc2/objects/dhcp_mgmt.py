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
import xmlrpclib

try:
    import netaddr
except ImportError:
    print "You need to have the python-netaddr module installed"
    sys.exit(1)


class DHCPMgmt(object):

    def __init__(self, rpcurl=None):
        self._rpcurl = rpcurl
        self._proxy = xmlrpclib.ServerProxy(self._rpcurl, allow_none=True)

    def find_entry_by_ip(self, ipaddr=None):
        ip = None
        if ipaddr is not None:
            try:
                ip = netaddr.IPAddress(ipaddr)
            except Exception:
                return False
        network_list = self._proxy.dc2.dhcp.mgmt.list()
        for network in network_list:
            try:
                ipnetwork = netaddr.IPNetwork(network['ipspace'])
            except Exception:
                return False
            if ip in ipnetwork:
                return network
        return False
