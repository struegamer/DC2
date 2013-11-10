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

tbl_bootmethods = Table(MONGOS["dc2db"]["database"].get_table(
    "default_bootmethods"))
tbl_servers = Table(MONGOS["dc2db"]["database"].get_table("servers"))

DEFBOOT_RECORD = {
    "hardware_type": True,
    "pxe_bootmethod": False,
}


@rpcmethod(
    name="dc2.configuration.bootmethods.list",
    params={}, returns={}, is_xmlrpc=True, is_jsonrpc=True)
def dc2_configuration_defaultbootmethods_list(search=None):
    result = []
    if search is not None and type(search) is types.DictType:
        for k in search.keys():
            a = re.compile('{0}'.format(search[k]), re.IGNORECASE)
            search[k] = a
        result = tbl_bootmethods.find(search)
    else:
        result = tbl_bootmethods.find()
    return result


@rpcmethod(
    name="dc2.configuration.bootmethods.add",
    params={}, returns={}, is_xmlrpc=True, is_jsonrpc=True)
def dc2_configuration_defaultbootmethods_add(rec=None):
    if rec is not None and type(rec) is types.DictType:
        if (check_record(rec, DEFBOOT_RECORD) and
            'hardware_type' in rec and
            tbl_bootmethods.find_one(
                {"hardware_type": rec["hardware_type"]}) is None):
            doc_id = tbl_bootmethods.save(rec)
            return doc_id
    return xmlrpclib.Fault(-32501, "Record could not be added")


@rpcmethod(
    name="dc2.configuration.bootmethods.update",
    params={}, returns={}, is_xmlrpc=True, is_jsonrpc=True)
def dc2_configuration_defaultbootmethods_update(rec=None):
    if rec is not None and type(rec) is types.DictType:
        if (check_record(rec, DEFBOOT_RECORD) and
            'hardware_type' in rec and
                tbl_bootmethods.find_one(
                    {"hardware_type": rec["hardware_type"]}) is not None):
            doc_id = tbl_bootmethods.save(rec)
            return doc_id
    return xmlrpclib.Fault(-32501, "Record could not be updates")


@rpcmethod(
    name="dc2.configuration.bootmethods.delete",
    params={}, returns={}, is_xmlrpc=True, is_jsonrpc=True)
def dc2_configuration_defaultbootmethods_delete(rec=None):
    if rec is not None and type(rec) is types.DictType:
        if '_id' in rec:
            response = tbl_bootmethods.remove(rec)
            if response is False:
                return xmlrpclib.Fault(
                    -32501, "Record(s) could not be deleted")
            return True
    return xmlrpclib.Fault(-32501, "Record(s) could not be deleted")


@rpcmethod(
    name="dc2.configuration.bootmethods.update_hw_types",
    params={}, returns={}, is_xmlrpc=True, is_jsonrpc=True)
def dc2_configuration_defaultbootmethods_update_hardware_types():
    server_list = []
    server_list = tbl_servers.find()
    for server in server_list:
        if ('product_name' in server and
            server["product_name"] is not None and
                server["product_name"] != ""):
            if tbl_bootmethods.find_one(
                    {"hardware_type": server["product_name"]}) is None:
                dc2_configuration_defaultbootmethods_add(
                    {"hardware_type": server["product_name"],
                        "pxe_bootmethod": "none"})
    return True
