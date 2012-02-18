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
from macs import MACs

class Servers(object):
    def __init__(self,rpcurl=None):
        self._rpcurl=rpcurl
        self._proxy=xmlrpclib.ServerProxy(self._rpcurl,allow_none=True)        
    
    def find_by_mac(self,mac_addr=None):
        if mac_addr is not None:
            m=MACs(self._rpcurl)
            mac_rec=m.find(mac_addr)
            if mac_rec is not None:
                server_list=self._proxy.dc2.inventory.servers.find({"_id":mac_rec["server_id"]})
                if server_list is not None and len(server_list)>0 and server_list[0] is not None:
                    return server_list[0]
        return None
    
    def find_by_serial_no(self,serial_no=None):
        if serial_no is not None:
            server_list=self._proxy.dc2.inventory.servers.find({"serial_no":serial_no})
            if server_list is not None and len(server_list)>0 and server_list[0] is not None:
                return server_list[0]
        return None
    

   
            
    