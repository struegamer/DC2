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


tbl_server = Table(MONGOS["dc2db"]["database"].get_table("servers"))
tbl_host=Table(MONGOS["dc2db"]["database"].get_table("hosts"))
tbl_installstatus=Table(MONGOS["dc2db"]["database"].get_table("installstatus"))

INSTALLSTATUS_RECORD={
                      "server_id":True,
                      "host_id":True,
                      "hostname":True,
                      "progress":False,
                      "status":True
}

@rpcmethod(name="dc2.deployment.installstate.find",params={},returns={},is_xmlrpc=True,is_jsonrpc=True)
def dc2_deployment_installstate_find(search=None): 
    if search is not None and type(search) is types.DictType:
        for k in search.keys():
            a = re.compile('%s' % search[k], re.IGNORECASE)
            search[k] = a
        result = tbl_installstatus.find(search)
    else:
        result = tbl_installstatus.find();
    return result    

@rpcmethod(name='dc2.deployment.installstate.list', params={},returns={},is_xmlrpc=True,is_jsonrpc=True)
def dc2_deployment_installstate_list():
    result=dc2_deployment_installstate_find()
    return result

@rpcmethod(name="dc2.deployment.installstate.get",params={},returns={},is_xmlrpc=True,is_jsonrpc=True)
def dc2_deployment_installstate_get(record=None):
    if record is not None and type(record) is types.DictType:
        if record.has_key("_id") or record.has_key("server_id") or record.has_key("host_id"):
            install_record=tbl_installstatus.find_one(record)
            return install_record
    return None


@rpcmethod(name="dc2.deployment.installstate.add",params={},returns={},is_xmlrpc=True,is_jsonrpc=True)
def dc2_deployment_installstate_add(record=None):
    if record is not None and type(record) is types.DictType:
        if check_record(record,INSTALLSTATUS_RECORD) and tbl_installstatus.find_one({"server_id":record["server_id"],"host_id":record["host_id"]}) is None:
            doc_id=tbl_installstatus.save(record)
            return doc_id
    return xmlrpclib.Fault(-32501, "Record couldn't be added")

@rpcmethod(name="dc2.deployment.installstate.update",params={},returns={},is_xmlrpc=True,is_jsonrpc=True)
def dc2_deployment_installstate_update(record=None):
    if record is not None and type(record) is types.DictType:
        if check_record(record,INSTALLSTATUS_RECORD) and tbl_installstatus.find_one({"server_id":record["server_id"],"host_id":record["host_id"]}) is not None:
            doc_id=tbl_installstatus.save(record)
            return doc_id
    return xmlrpclib.Fault(-32501, "Record couldn't be updated ")
    
@rpcmethod(name="dc2.deployment.installstate.remove",params={},returns={},is_xmlrpc=True,is_jsonrpc=True)    
def dc2_deployment_installstate_delete(record=None):
    if record is not None and type(record) is types.DictType:
        if record.has_key("_id") or record.has_key("server_id") or record.has_key("host_id"):
            tbl_installstatus.remove(record)
            return True
    return False
            
