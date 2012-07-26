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

@rpcmethod(name="dc2.inventory.xenvms.list",params={},returns={},is_xmlrpc=True,is_jsonrpc=True)
def dc2_inventory_xenserver_mgmt_list(xenhost=None,session_id=None,vm_type=None):
    if xenhost is None:
        return None
    if session_id is None:
        return None    
    if vm_type is None:
        return None
    if vm_type != "template" and vm_type != "vms" and vm_type != "both":
        return None    
    vmlist_dict=xenserver_get_vms(xenhost,session_id,vm_type)
    if vmlist_dict is not None and vmlist_dict is not False:
        return vmlist_dict
    return None


@rpcmethod(name="dc2.inventory.xenvms.get",params={},returns={},is_xmlrpc=True,is_jsonrpc=True)
def dc2_inventory_xenserver_mgmt_get(xenhost=None,session_id=None,vm_id=None):
    if xenhost is not None and session_id is not None and vm_id is not None:
        vm_record=xenserver_get_vms_record(xenhost,session_id,vm_id)
        if vm_record is not None:
            return vm_record
    return None

