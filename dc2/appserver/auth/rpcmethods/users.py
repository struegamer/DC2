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


tbl_users=Table(MONGOS["userdb"]["database"].get_table("users"))

USER_RECORD={
    "username":True,
    "password":True,
    "name":True,
}

@rpcmethod("dc2.configuration.users.list",params={},returns={},is_xmlrpc=True,is_jsonrpc=True)
def dc2_authentication_users_list(search=None):
    if search is not None and type(search) is types.DictType:
        for k in search.keys():
            a = re.compile('%s' % search[k], re.IGNORECASE)
            search[k] = a
        result = tbl_users.find(search)
    else:
        result = tbl_users.find();
    return result

@rpcmethod("dc2.configuration.users.add",params={},returns={},is_xmlrpc=True,is_jsonrpc=True)
def dc2_authentication_users_add(record=None):
    if record is not None and type(record) is types.DictType:
        if check_record(record,USER_RECORD) and tbl_users.find_one({"username":record["username"]}) is None:
            doc_id=tbl_users.save(record)
            return doc_id
    return xmlrpclib.Fault(-32501, "Record couldn't be added")

@rpcmethod("dc2.configuration.users.update",params={},returns={},is_xmlrpc=True,is_jsonrpc=True)
def dc2_authentication_users_update(record=None):
    if record is not None and type(record) is types.DictType:
        if check_record(record,USER_RECORD) and tbl_users.find_one({"username":record["useranme"]}) is not None:
            doc_id=tbl_users.save(record)
            return doc_id
    return xmlrpclib.Fault(-32501, "Record couldn't be updated")

@rpcmethod("dc2.configuration.users.delete",params={},returns={},is_xmlrpc=True,is_jsonrpc=True)
def dc2_authentication_users_delete(record=None):
    if record is not None and type(record) is types.DictType:
        if record.has_key("_id") or record.has_key("username"):
            tbl_users.remove(record)
            return True
    return False


@rpcmethod("dc2.configuration.users.get",params={},returns={},is_xmlrpc=True,is_jsonrpc=True)
def dc2_authentication_users_get(record=None):
    if record is not None and type(record) is types.DictType:
        if record.has_key("_id") or record.has_key("username"):
            user_rec=tbl_users.find_one(record)
            return user_rec
    return None

