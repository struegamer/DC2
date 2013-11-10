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
import re

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

tbl_server = Table(MONGOS["dc2db"]["database"].get_table("servers"))
tbl_host = Table(MONGOS["dc2db"]["database"].get_table("hosts"))
tbl_installstate = Table(
    MONGOS["dc2db"]["database"].get_table("installstatus"))

HOST_RECORD = {
    "server_id": True,
    "hostname": True,
    "domainname": True,
    "hostclasses": True,
    "environments": True,
}


@rpcmethod(
    name="dc2.inventory.hosts.list",
    params={}, returns={}, is_xmlrpc=True, is_jsonrpc=True)
def dc2_deployment_hosts_list(search=None):
    if search is not None and type(search) is types.DictType:
        for k in search.keys():
            a = re.compile('%s' % search[k], re.IGNORECASE)
            search[k] = a
        result = tbl_host.find(search)
    else:
        result = tbl_host.find()
    return result


@rpcmethod(
    name="dc2.inventory.hosts.find",
    params={}, returns={}, is_xmlrpc=True, is_jsonrpc=True)
def dc2_deployment_hosts_find(search=None):
    return dc2_deployment_hosts_list(search)


@rpcmethod(
    name="dc2.inventory.hosts.get",
    params={}, returns={}, is_xmlrpc=True, is_jsonrpc=True)
def dc2_deployment_hosts_get(host_id=None):
    if host_id is not None and host_id != "":
        host_record = tbl_host.find_one({"_id": host_id})
        if host_record is not None:
            return host_record
    return None


@rpcmethod(
    name="dc2.inventory.hosts.add",
    params={}, returns={}, is_xmlrpc=True, is_jsonrpc=True)
def dc2_deployment_hosts_add(record=None):
    if record is not None and type(record) is types.DictType:
        if (check_record(record, HOST_RECORD) and
                tbl_host.find_one({"server_id": record["server_id"]}) is None):
            doc_id = tbl_host.save(record)
            return doc_id
    return xmlrpclib.Fault(-32501, "Record couldn't be added")


@rpcmethod(
    name="dc2.inventory.hosts.update",
    params={}, returns={}, is_xmlrpc=True, is_jsonrpc=True)
def dc2_deployment_hosts_update(record=None):
    if record is not None and type(record) is types.DictType:
        if check_record(record, HOST_RECORD):
            doc_id = None
            old_host_record = tbl_host.find_one({"_id": record["_id"]})
            if (old_host_record is not None and
                    old_host_record["server_id"] == record["server_id"]):
                doc_id = tbl_host.save(record)
                install_rec = tbl_installstate.find_one(
                    {"server_id": record["server_id"]})
                if (install_rec["hostname"] != "{0}.{1}".format(
                        record["hostname"], record["domainname"])):
                    install_rec["hostname"] = "{0}.{1}".format(
                        record["hostname"], record["domainname"])
                    tbl_installstate.save(install_rec)
            else:
                #
                # Check for double host server id
                #
                if tbl_host.find_one(
                        {"server_id": record["server_id"]}) is not None:
                    return xmlrpclib.Fault(
                        -32501, "The Server already has a host attached.")
                doc_id = tbl_host.save(record)
                install_rec = tbl_installstate.find_one(
                    {"host_id": record["_id"]})
                if install_rec is not None:
                    install_rec["server_id"] = record["server_id"]
                    tbl_installstate.save(install_rec)
            return doc_id
    return xmlrpclib.Fault(-32501, "Record couldn't be updated")


@rpcmethod(
    name="dc2.inventory.hosts.remove",
    params={}, returns={}, is_xmlrpc=True, is_jsonrpc=True)
def dc2_inventory_hosts_remove(record=None):
    if record is not None and type(record) is types.DictType:
        if '_id' in record or 'server_id' in record:
            rec = tbl_host.find_one(record)
            if rec is not None:
                tbl_host.remove(rec)
                return True
    return xmlrpclib.Fault(-32503, "Record(s) couldn't be deleted")
