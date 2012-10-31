# -*- coding: utf-8 -*-
###############################################################################
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
###############################################################################

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


from macaddresses import *
from rib import *
from host import *
from installstate import *

tbl_server = Table(MONGOS["dc2db"]["database"].get_table("servers"))
tbl_hosts = Table(MONGOS["dc2db"]["database"].get_table("hosts"))

SERVER_RECORD = {
    "uuid":True,
    "serial_no":True,
    "product_name":False,
    "manufacturer":False,
    "location":False,
    "asset_tags":False }

@rpcmethod(name="dc2.inventory.servers.list",
           returns={'list servers':'List of Server Records'},
           params={"norows":"Number of Rows, Default 0",
                   "skip":"Skip number of records, default 0",
                   "search":"Search Term"}, is_xmlrpc=True, is_jsonrpc=True)
def dc2_servers_list(norows=0, skip=0, search=None):
    if search is not None and type(search) is types.DictType:
        for k in search.keys():
            a = re.compile('%s' % search[k], re.IGNORECASE)
            search[k] = a
        result = tbl_server.find(search)
    else:
        result = tbl_server.find();
    return result

@rpcmethod(name="dc2.inventory.servers.add",
           returns={'string doc_id':'Document ID of newly added record'},
           params={"dict rec_server":"Record Dictionary"},
           is_xmlrpc=True, is_jsonrpc=True)
def dc2_servers_add(rec_server=None):
    if rec_server is not None and type(rec_server) is types.DictType:
        if (check_record(rec_server, SERVER_RECORD) and
            tbl_server.find_one({"uuid":rec_server["uuid"]}) is None):
            doc_id = tbl_server.save(rec_server)
            return doc_id
    return xmlrpclib.Fault(-32501, "Record wasn't added!")

@rpcmethod(name="dc2.inventory.servers.update",
           returns={"string doc_id":"Document ID of updated record"},
           params={"dict rec_server":"Pre-Filled Record dictionary"},
           is_xmlrpc=True, is_jsonrpc=True)
def dc2_servers_update(rec_server=None):
    if rec_server is not None and type(rec_server) is types.DictType:
        if (check_record(rec_server, SERVER_RECORD) and
            tbl_server.find_one({"_id":rec_server["_id"],
                                 "uuid":rec_server["uuid"]}) is not None):
            doc_id = tbl_server.save(rec_server)
            return doc_id
    return xmlrpclib.Fault(-32504, "Record couldn't be updated")

@rpcmethod(name="dc2.inventory.servers.find",
           returns={"list servers":"List of found server records"},
           params={"dict rec_server":
                   "Pre-Filled record dictionary with search terms"},
           is_xmlrpc=True, is_jsonrpc=True)
def dc2_servers_find(rec_server=None):
    if rec_server is not None and type(rec_server) is types.DictType:
        response = tbl_server.find(rec_server)
        return response
    return xmlrpclib.Fault(-32502, "Record wasn't found!")

@rpcmethod(name="dc2.inventory.servers.delete",
           returns={"bool success":"True if action was successful"},
           params={"dict rec_server":
                   "Pre-Filled record dictionary with key _id"},
           is_xmlrpc=True, is_jsonrpc=True)
def dc2_servers_delete(rec_server=None):
    if rec_server is not None and type(rec_server) is types.DictType:
        if rec_server.has_key("_id"):
            server_id = rec_server["_id"]
            m = {}
            m["server_id"] = server_id
            try:
                dc2_servers_macaddr_delete(m)
                dc2_servers_rib_delete(m)
                response = tbl_server.remove(rec_server)
                if response is False:
                    return xmlrpclib.Fault(-32503,
                                           "Record couldn't be deleted")
                return True
            except Exception, e:
                return xmlrpclib.Fault(-32503, "Record(s) couldn't be deleted")
    return xmlrpclib.Fault(-32503, "Record(s) couldn't be deleted")

@rpcmethod(name="dc2.inventory.servers.delete_complete",
           returns={"boot success":"True if action as successful"},
           params={"dict rec_server":
                   "pre_filled record dictionary with key _id"},
           is_xmlrpc=True, is_jsonrpc=True)
def dc2_servers_delete_complete(rec_server=None):
    if rec_server is not None and type(rec_server) is types.DictType:
        if rec_server.has_key("_id"):
            server_id = rec_server["_id"]
            m = {}
            m["server_id"] = server_id
            try:
                dc2_servers_delete(rec_server)
                dc2_inventory_hosts_remove(m)
                dc2_deployment_installstate_delete(m)
                return True
            except Exception, e:
                web.debug(e)
                return None

    return False

@rpcmethod(name="dc2.inventory.servers.list_without_hosts",
           params={},
           returns={},
           is_xmlrpc=True,
           is_jsonrpc=True)
def dc2_servers_list_servers_without_hosts():
    server_list = tbl_server.find()
    servers_without_hosts = []
    if len(server_list) > 0:
        for server in server_list:
            try:
                host_rec = tbl_hosts.find_one({"server_id":server["_id"]})
                if host_rec is None:
                    servers_without_hosts.append(server)
            except Exception, e:
                web.debug(e)
    return servers_without_hosts


