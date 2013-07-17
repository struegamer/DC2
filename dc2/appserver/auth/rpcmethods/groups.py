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

tbl_groups=Table(MONGOS["userdb"]["database"].get_table("groups"))

GROUP_RECORD={
    "groupname":True,
    "description":True,
    "users":False,
}

@rpcmethod(name="dc2.configuration.groups.list",params={},returns={},is_xmlrpc=True,is_jsonrpc=True)
def dc2_authentication_groups_list(search=None):
    if search is not None and type(search) is types.DictType:
        for k in search.keys():
            a = re.compile('%s' % search[k], re.IGNORECASE)
            search[k] = a
        result = tbl_groups.find(search)
    else:
        result = tbl_groups.find();
    return result

@rpcmethod(name="dc2.configuration.groups.add",params={},returns={},is_xmlrpc=True,is_jsonrpc=True)
def dc2_authentication_groups_add(record=None):
    if record is not None and type(record) is types.DictType:
        if check_record(record,GROUP_RECORD) and tbl_groups.find_one({"groupname":record["groupname"]}) is None:
            doc_id=tbl_groups.save(record)
            return doc_id
    return xmlrpclib.Fault(-32501, "Record couldn't be added")

@rpcmethod(name="dc2.configuration.groups.update",params={},returns={},is_xmlrpc=True,is_jsonrpc=True)
def dc2_authentication_groups_update(record=None):
    if record is not None and type(record) is types.DictType:
        if check_record(record,GROUP_RECORD) and tbl_groups.find_one({"groupname":record["groupname"]}) is not None:
            doc_id=tbl_groups.save(record)
            return doc_id
    return xmlrpclib.Fault(-32501, "Record couldn't be updated")

@rpcmethod(name="dc2.configuration.groups.delete",params={},returns={},is_xmlrpc=True,is_jsonrpc=True)
def dc2_authentication_groups_delete(record=None):
    if record is not None and type(record) is types.DictType:
        if record.has_key("_id") or record.has_key("groupname"):
            tbl_groups.remove(record)
            return True
    return False

@rpcmethod(name="dc2.configuration.groups.get",params={},returns={},is_xmlrpc=True,is_jsonrpc=True)
def dc2_authentication_groups_get(record=None):
    if record is not None and type(record) is types.DictType:
        if record.has_key("_id") or record.has_key("groupname"):
            user_rec=tbl_groups.find_one(record)
            return user_rec
    return None
