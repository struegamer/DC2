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

tbl_systemusers=Table(MONGOS["dc2db"]["database"].get_table("defaultsystemusers"))

SYSUSERS_RECORD = {
   'username':True,
   'realname':True,
   'uid':False,
   'gid':False,
   'cryptpw':True,
   'ssh_pubkey':False,
   'is_admin':True,
}

@rpcmethod(name="dc2.configuration.systemusers.list",returns={},params={},is_xmlrpc=True,is_jsonrpc=True)
def dc2_configuration_systemusers_list(search=None):
    result=[]
    if search is not None and type(search) is types.DictType:
        for k in search.keys():
            a=re.compile('%s' % search[k],re.IGNORECASE)
            search[k]=a
        result=tbl_systemusers.find(search)
    else:
        result=tbl_systemusers.find()
    return result

@rpcmethod(name="dc2.configuration.systemusers.add",params={},returns={},is_xmlrpc=True,is_jsonrpc=True)
def dc2_configuration_systemusers_add(rec=None):
    if rec is not None and type(rec) is types.DictType:
        if check_record(rec,SYSUSERS_RECORD) and rec.has_key('username') and tbl_systemusers.find_one({'username':rec["username"]}) is None:
            doc_id=tbl_systemusers.save(rec)
            return doc_id
    return xmlrpclib.Fault(-32501,'Record could not be added')


@rpcmethod(name="dc2.configuration.systemusers.update",params={},returns={},is_xmlrpc=True,is_jsonrpc=True)
def dc2_configuration_systemusers_update(rec=None):
    if rec is not None and type(rec) is types.DictType:
        if check_record(rec,SYSUSERS_RECORD) and rec.has_key('username') and tbl_systemusers.find_one({'username':rec["username"]}) is not None:
            doc_id=tbl_systemusers.save(rec)
            return doc_id
    return xmlrpclib.Fault(-32501,"Record could not be updated")


@rpcmethod(name="dc2.configuration.systemusers.delete",params={},returns={},is_xmlrpc=True,is_jsonrpc=True)
def dc2_configuration_systemusers_delete(rec=None):
    if rec is not None and type(rec) is types.DictType:
        if rec.has_key('_id'):
            response=tbl_systemusers.remove(rec)
            if response is False:
                return xmlrpclib.Fault(-32503, "Record(s) couldn't be deleted")
            return True
    return xmlrpclib.Fault(-32503, "Record(s) couldn't be deleted")

