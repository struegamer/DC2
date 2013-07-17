# -*- coding: utf-8 -*-
#################################################################################
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
#################################################################################

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
    from dc2.lib.db.mongo import Database
    from dc2.lib.db.mongo import Table
    from dc2.helpers import check_record
    from dc2.rpc import rpcmethod
    from dc2.addons.xen.lib import *
except ImportError:
    print "You don't have DC² correctly installed"
    sys.exit(1)

try:
    from settings import MONGOS
except ImportError:
    print "You don't have a settings file"
    sys.exit(1)


tbl_xenserver=Table(MONGOS["xendb"]["database"].get_table("xenserver"))


@rpcmethod(name="dc2.inventory.xen.networks.list",params={},returns={},is_xmlrpc=True,is_jsonrpc=True)
def dc2_inventory_xen_networks_list(xenhost=None,session_id=None):
    if xenhost is not None and session_id is not None and xenhost != "" and session_id != "":
        network_list=xenserver_network_list(xenhost,session_id)
        if network_list:
            return network_list
    return None

@rpcmethod(name="dc2.inventory.xen.networks.get",params={},returns={},is_xmlrpc=True,is_jsonrpc=True)
def dc2_inventory_xen_networks_get(xenhost=None, session_id=None, network_id=None):
    if xenhost is not None and session_id is not None and network_id is not None and xenhost != "" and session_id != "" and network_id != "":
        network_record=xenserver_network_get(xenhost,session_id,network_id)
        if network_record:
            return network_record
    return None


