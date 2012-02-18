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

#
# Std. Python Libs
#
import sys
import types
import xmlrpclib
import re
import uuid


try:
    import web
except ImportError:
    print "You don't have web.py installed"
    sys.exit(1)

try:
    from dc2.appserver.mongodb import Database
    from dc2.appserver.mongodb import Table
    from dc2.appserver.helpers import check_record
    from dc2.appserver.rpc import rpcmethod
except ImportError:
    print "You don't have DC² correctly installed"
    sys.exit(1)

try:
    from settings import MONGOS
except ImportError:
    print "You don't have a settings file"
    sys.exit(1)


try:
    import netaddr
except ImportError:
    print "You need to have the python-netaddr module installed"
    sys.exit(1)

@rpcmethod(name="dc2.utils.ipcalc.show_ip_info", params={}, returns={}, is_xmlrpc=True, is_jsonrpc=True)
def dc2_ipcalc_show_ip_info(ipaddress=None):
    if ipaddress is None:
        return None
    ip = netaddr.IPNetwork(ipaddress)
    result = {}
    result["network"] = ip.network.__str__()
    result["netmask"] = ip.netmask.__str__()
    result["broadcast"] = ip.broadcast.__str__()
    result["cidr_prefix"] = ip.prefixlen
    result["first_ip"] = netaddr.IPAddress(ip.first).__str__()
    result["last_ip"] = netaddr.IPAddress(ip.last).__str__()
    result["hostmask"] = ip.hostmask.__str__()
    result["network_size"] = ip.size
    return result
        
    
