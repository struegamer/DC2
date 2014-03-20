# -*- coding: utf-8 -*-
#################################################################################
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
#################################################################################

import xmlrpclib
from servers import Servers

class Hosts(object):
    def __init__(self,rpcurl=None):
        self._rpcurl=rpcurl
        self._proxy=xmlrpclib.ServerProxy(self._rpcurl,allow_none=True)

    def find_by_server_serial(self,serial_no=None):
        if serial_no is not None:
            s=Servers(self._rpcurl)
            server_rec=s.find_by_serial_no(serial_no)
            if server_rec is not None:
                host_list=self._proxy.dc2.inventory.hosts.find({"server_id":server_rec["_id"]})
                if host_list is not None and len(host_list)>0 and host_list[0] is not None:
                    return host_list[0]
        return None

    def find_by_server_mac(self,mac_addr=None):
        if mac_addr is not None:
            s=Servers(self._rpcurl)
            server_rec=s.find_by_mac(mac_addr)
            if server_rec is not None:
                host_list=self._proxy.dc2.inventory.hosts.find({"server_id":server_rec["_id"]})
                if host_list is not None and len(host_list)>0 and host_list[0] is not None:
                    return host_list[0]
        return None

    def find_by_hostname(self,hostname=None,domainname=None):
        if hostname is not None and domainname is not None:
            host_list=self._proxy.dc2.inventory.hosts.find({"hostname":hostname,"domainname":domainname})
            if host_list is not None and len(host_list)>0 and host_list[0] is not None:
                return host_list[0]
        return None


    def write_network_config(self,interface_type=None,host=None):
        try:
            exec "from interfaces.%s import write_host_network_configuration" % interface_type
            write_host_network_configuration(host,self._rpcurl)
        except ImportError:
            print "Can't find module for %s" % interface_type







