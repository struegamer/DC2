# -*- coding: utf-8 -*-
###############################################################################
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
###############################################################################

#
# Std. Python Libs
#
import sys
import types
import xmlrpclib

try:
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


tbl_server = Table(MONGOS["dc2db"]["database"].get_table("remoteinsightboard"))

RIB_RECORD = {
    "server_id": True,
    "remote_type": False,
    "remote_ip": False
}


@rpcmethod(
    name="dc2.inventory.servers.rib.list",
    returns={"list rib_rec": "List of RIB Records for a server"},
    params={}, is_xmlrpc=True, is_jsonrpc=True)
def dc2_servers_rib_list(search):
    if search is not None and type(search) is types.DictType:
        result = tbl_server.find(search)
    else:
        result = tbl_server.find()
    return result


@rpcmethod(
    name="dc2.inventory.servers.rib.add",
    returns={"string doc_id": "Document ID of new added record"},
    params={"dict rec_rib": "Record Dictionary"},
    is_xmlrpc=True, is_jsonrpc=True)
def dc2_servers_rib_add(rec_rib=None):
    if rec_rib is not None and type(rec_rib) is types.DictType:
        if check_record(rec_rib, RIB_RECORD):
            doc_id = tbl_server.save(rec_rib)
            return doc_id
    return xmlrpclib.Fault(-32501, "Record couldn't be added")


@rpcmethod(
    name="dc2.inventory.servers.rib.update",
    returns={"string doc_id": "Document ID of new added record"},
    params={"dict rec_rib": "Record Dictionary"},
    is_xmlrpc=True, is_jsonrpc=True)
def dc2_servers_rib_update(rec_rib=None):
    if rec_rib is not None and type(rec_rib) is types.DictType:
        if (check_record(rec_rib, RIB_RECORD) and
                tbl_server.find_one({
                    "_id": rec_rib["_id"],
                    "server_id": rec_rib["server_id"]}) is not None):
            doc_id = tbl_server.save(rec_rib)
            return doc_id
    return xmlrpclib.Fault(-32504, "Record couldn't be updated")


@rpcmethod(
    name="dc2.inventory.servers.rib.delete",
    returns={"bool success": "True if action was successful"},
    params={"dict rec_rib": "Prefilled record dictionary with key _id, "
            "or server_id to delete all RIB records attached to a server"},
    is_xmlrpc=True, is_jsonrpc=True)
def dc2_servers_rib_delete(rec_rib=None):
    if rec_rib is not None and type(rec_rib) is types.DictType:
        if '_id' in rec_rib or 'server_id' in rec_rib:
            response = tbl_server.remove(rec_rib)
            if response is False:
                return xmlrpclib.Fault(-32503, "Record(s) couldn't be deleted")
        return True
    return xmlrpclib.Fault(-32503, "Record(s) couldn't be deleted")


@rpcmethod(
    name="dc2.inventory.servers.rib.find",
    returns={"bool success": "True if action was successful"},
    params={"dict rec_rib": "Pre-Filled record dictionary with key _id"},
    is_xmlrpc=True, is_jsonrpc=True)
def dc2_servers_rib_find(rec_rib=None):
    if rec_rib is not None and type(rec_rib) is types.DictType:
        response = tbl_server.find(rec_rib)
        return response
    return xmlrpclib.Fault(-32502, "Record wasn't found!")
