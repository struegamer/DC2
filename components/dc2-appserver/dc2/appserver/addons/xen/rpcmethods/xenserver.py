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

tbl_xenserver = Table(MONGOS["xendb"]["database"].get_table("xenserver"))

XENSERVER_RECORD = {
    "xen_host":True,
    "xen_username":True,
    "xen_password":True
}

@rpcmethod(name="dc2.inventory.xenserver.list", params={}, returns={}, is_xmlrpc=True, is_jsonrpc=True)
def dc2_inventory_xenserver_list(search=None):
    if search is not None and type(search) is types.DictType:
        for k in search.keys():
            a = re.compile('%s' % search[k], re.IGNORECASE)
            search[k] = a
        result = tbl_xenserver.find(search)
    else:
        result = tbl_xenserver.find();
    return result

@rpcmethod(name="dc2.inventory.xenserver.add", params={}, returns={}, is_xmlrpc=True, is_jsonrpc=True)
def dc2_inventory_xenserver_add(record=None):
    if record is not None and type(record) is types.DictType:
        if check_record(record, XENSERVER_RECORD) and tbl_xenserver.find_one({"xen_host":record["xen_host"]}) is None:
            doc_id = tbl_xenserver.save(record)
            return doc_id
    return xmlrpclib.Fault(-32501, "Record wasn't added!")

@rpcmethod(name="dc2.inventory.xenserver.update", params={}, returns={}, is_xmlrpc=True, is_jsonrpc=True)
def dc2_inventory_xenserver_update(record=None):
    if record is not None and type(record) is types.DictType:
        if check_record(record, XENSERVER_RECORD) and tbl_xenserver.find_one({"xen_host":record["xen_host"]}) is not None:
            doc_id = tbl_xenserver.save(record)
            return doc_id
    return xmlrpclib.Fault(-32501, "Record wasn't update!")

@rpcmethod(name="dc2.inventory.xenserver.remove", params={}, returns={}, is_xmlrpc=True, is_jsonrpc=True)
def dc2_inventory_xenserver_delete(record=None):
    if record is not None and type(record) is types.DictType:
        if record.has_key("_id"):
            response = tbl_xenserver.remove(record)
            if response is False:
                return xmlrpclib.Fault(-32503, "Record couldn't be deleted")
        return True
    return xmlrpclib.Fault(-32503, "Record(s) couldn't be deleted")

@rpcmethod(name="dc2.inventory.xenserver.get", params={}, returns={}, is_xmlrpc=True, is_jsonrpc=True)
def dc2_inventory_xenserver_get(record=None):
    if record is not None and type(record) is types.DictType:
        xenserver_record = tbl_xenserver.find_one(record)
        if xenserver_record is not None:
            return xenserver_record
    return None

@rpcmethod(name="dc2.inventory.xenserver.login", params={}, returns={}, is_xmlrpc=True, is_jsonrpc=True)
def dc2_inventory_xenserver_login(record=None):
    if record is not None and type(record) is types.DictType:
        xenserver_record = tbl_xenserver.find_one(record)
        if xenserver_record is not None:
            response = xenserver_login(str(xenserver_record["xen_host"]), xenserver_record["xen_username"], xenserver_record["xen_password"])
            return response
    return None

@rpcmethod(name="dc2.inventory.xenserver.logout", params={}, returns={}, is_xmlrpc=True, is_jsonrpc=True)
def dc2_inventory_xenserver_logout(xenhost=None, session_id=None):
    if xenhost is not None and session_id is not None:
        xenserver_record = tbl_xenserver.find_one({"xen_host":xenhost})
        if xenserver_record is not None:
            response = xenserver_logout(xenhost, session_id)
            return response
    return None
