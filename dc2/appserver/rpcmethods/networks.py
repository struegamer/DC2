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
    from dc2.lib.db.mongo import Database
    from dc2.lib.db.mongo import Table
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


tbl_server = Table(MONGOS["dc2db"]["database"].get_table("networks"))

NETWORK_RECORD = {
    "network":True,
    "name":True,
    "description":True,
    "gateway":True,
    "broadcast":False,
    "blocked_ips":True,
    "first_ip":False,
    "vlan_no":False,
}

@rpcmethod(name="dc2.inventory.networks.list", returns={"list networks":"List of Network Records"}, params={"dict network_record":"dict of network records, can be None"}, is_xmlrpc=True, is_jsonrpc=True)
def dc2_inventory_networks_list(search=None):
    result = []
    if search is not None and type(search) is types.DictType:
        for k in search.keys():
            a = re.compile('%s' % search[k], re.IGNORECASE)
            search[k] = a
        result = tbl_server.find(search)
    else:
        result = tbl_server.find()
    return result

@rpcmethod(name="dc2.inventory.networks.add", returns={}, params={}, is_xmlrpc=True, is_jsonrpc=True)    
def dc2_inventory_networks_add(record=None):
    if record is not None and type(record) is types.DictType:
        if check_record(record, NETWORK_RECORD):
            doc_id = tbl_server.save(record)
            return doc_id
    return xmlrpclib.Fault(-32501, "Record couldn't be added")

@rpcmethod(name="dc2.inventory.networks.update", returns={}, params={}, is_xmlrpc=True, is_jsonrpc=True)
def dc2_inventory_networks_update(record=None):
    if record is not None and type(record) is types.DictType:
        if check_record(record, NETWORK_RECORD) and tbl_server.find_one({"_id":record["_id"]}) is not None:
            doc_id = tbl_server.save(record)
            return doc_id
    return xmlrpclib.Fault(-32504, "Record couldn't be updated")

@rpcmethod(name="dc2.inventory.networks.delete", returns={}, params={}, is_xmlrpc=True, is_jsonrpc=True)            
def dc2_inventory_networks_delete(record=None):
    if record is not None and type(record) is types.DictType:
        if record.has_key("_id"):
            response = tbl_server.remove(record)
            if response is False:
                return xmlrpclib.Fault(-32503, "Record(s) couldn't be deleted")
        return True
    return xmlrpclib.Fault(-32503, "Record(s) couldn't be deleted")
            
