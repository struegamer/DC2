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
    from dc2.appserver.mongodb import Database
    from dc2.appserver.mongodb import Table
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

tbl_environments = Table(MONGOS["dc2db"]["database"].get_table("environments"))

ENVIRONMENT_RECORDS = {
    "name":True,
    "description":False,
    "variables":True
}

@rpcmethod(name="dc2.configuration.environments.list", returns={"list environment_recs":"List of type environment_records"}, params={"dict environment_rec":"Enviornment_record"}, is_xmlrpc=True, is_jsonrpc=True)
def dc2_deployment_environments_list(search=None):
    result = []
    if search is not None and type(search) is types.DictType:
        for k in search.keys():
            a = re.compile('%s' % search[k], re.IGNORECASE)
            search[k] = a
        result = tbl_environments.find(search)
    else:
        result = tbl_environments.find()
    return result

@rpcmethod(name="dc2.configuration.environments.find", returns={"list environment_recs":"List of type environment_records"}, params={"dict environment_rec":"Enviornment_record"}, is_xmlrpc=True, is_jsonrpc=True)
def dc2_deployment_environments_find(search=None):
    return dc2_deployment_environments_list(search)

@rpcmethod(name="dc2.configuration.environments.add", returns={"string doc_id":"Document ID"}, params={"dict environment_rec":"Dictionary of type ENVIRONMENT_RECORDS"}, is_xmlrpc=True, is_jsonrpc=True)
def dc2_deployment_environments_add(env_rec=None):
    if env_rec is not None and type(env_rec) is types.DictType:
        if check_record(env_rec, ENVIRONMENT_RECORDS) and env_rec.has_key("name") and tbl_environments.find_one({"name":env_rec["name"]}) is None:
            doc_id = tbl_environments.save(env_rec)
            return doc_id
    return xmlrpclib.Fault(-32501, "Record couldn't be added")

@rpcmethod(name="dc2.configuration.environments.update", returns={"string doc_id":"Document ID"}, params={"dict environment_rec":"Dictionary of type ENVIRONMENT_RECORDS"}, is_xmlrpc=True, is_jsonrpc=True)
def dc2_deployment_environments_update(env_rec=None):
    if env_rec is not None and type(env_rec) is types.DictType:
        if check_record(env_rec, ENVIRONMENT_RECORDS) and env_rec.has_key("_id") and tbl_environments.find_one({"_id":env_rec["_id"]}) is not None:
            doc_id = tbl_environments.save(env_rec)
            return doc_id
    return xmlrpclib.Fault(-32502, "Record couldn't be updated")
    
@rpcmethod(name="dc2.configuration.environments.delete", returns={"bool success":"Document ID"}, params={"dict env_rec":"environment record"}, is_xmlrpc=True, is_jsonrpc=True)
def dc2_deployment_environments_delete(env_rec=None):
    if env_rec is not None and type(env_rec) is types.DictType:
        if env_rec.has_key("_id"):
            response = tbl_environments.remove(env_rec)
            if response is False:
                return xmlrpclib.Fault(-32503, "Record(s) couldn't be deleted")
            return True
    return xmlrpclib.Fault(-32503, "Record(s) couldn't be deleted")                

@rpcmethod(name="dc2.configuration.environments.copy",returns={},params={},is_xmlrpc=True,is_jsonrpc=True)
def dc2_deployment_environments_copy(old_env=None,new_env=None):
    if old_env is not None and new_env is not None:
        if tbl_environments.find_one({"name":new_env}) is None:
            old_env_rec=tbl_environments.find_one({"name":old_env})
            old_env_rec["name"]=new_env
            del old_env_rec["_id"]
            tbl_environments.save(old_env_rec)
            return True
    return False
