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

tbl_server = Table(MONGOS["dc2db"]["database"].get_table("default_classes"))
tbl_hosts = Table(MONGOS["dc2db"]["database"].get_table("hosts"))

DEFCLASSES_RECORD = {
    "classname":True,
    "description":False,
}


@rpcmethod(name="dc2.configuration.defaultclasses.list", returns={"list defaultclasses":"List of type defaultclasses record"}, params={"dict defclasses_rec":"Defclasses record"}, is_xmlrpc=True, is_jsonrpc=True)
def dc2_configuration_defaultclasses_list(search=None):
    result = []
    if search is not None and type(search) is types.DictType:
        for k in search.keys():
            a = re.compile('%s' % search[k], re.IGNORECASE)
            search[k] = a
        result = tbl_server.find(search,sort_fieldname="classname")
    else:
        result = tbl_server.find(sort_fieldname="classname")
    return result

@rpcmethod(name="dc2.configuration.defaultclasses.add", returns={"string doc_id":"Document ID"}, params={"dict defclasses_rec":"Defclasses record"}, is_xmlrpc=True, is_jsonrpc=True)
def dc2_configuration_defaultclasses_add(defclass_rec=None):
    if defclass_rec is not None and type(defclass_rec) is types.DictType:
        if check_record(defclass_rec, DEFCLASSES_RECORD) and defclass_rec.has_key("classname") and tbl_server.find_one({"classname":defclass_rec["classname"]}) is None:
            doc_id = tbl_server.save(defclass_rec)
            return doc_id
    return xmlrpclib.Fault(-32501, "Record couldn't be added")

@rpcmethod(name="dc2.configuration.defaultclasses.update", returns={"string doc_id":"Document ID"}, params={"dict defclasses_rec":"Defclasses record"}, is_xmlrpc=True, is_jsonrpc=True)
def dc2_configuration_defaultclasses_update(defclass_rec=None):
    if defclass_rec is not None and type(defclass_rec) is types.DictType:
        if check_record(defclass_rec, DEFCLASSES_RECORD) and defclass_rec.has_key("_id") and tbl_server.find_one({"_id":defclass_rec["_id"]}) is not None:
            #
            # Get record of old defaultclasses
            #
            old_record=tbl_server.find_one({"_id":defclass_rec["_id"]})
            doc_id = tbl_server.save(defclass_rec)
            #
            # Check if we are updating
            #
            if doc_id == old_record["_id"]:
                #
                # Get hostlist
                #
                hostlist=tbl_hosts.find()
                for host in hostlist:
                    if host.has_key("hostclasses"):
                        if old_record["classname"] in host["hostclasses"]:
                            #
                            # Replace old classname in host records with new defaultclass name
                            #
                            host["hostclasses"][host["hostclasses"].index(old_record["classname"])]=defclass_rec["classname"]
                            tbl_hosts.save(host)
            return doc_id
    return xmlrpclib.Fault(-32502, "Record couldn't be updated")

@rpcmethod(name="dc2.configuration.defaultclasses.delete", returns={"bool success":"Document ID"}, params={"dict defclasses_rec":"Defclasses record"}, is_xmlrpc=True, is_jsonrpc=True)
def dc2_configuration_defaultclasses_delete(defclass_rec=None):
    if defclass_rec is not None and type(defclass_rec) is types.DictType:
        if defclass_rec.has_key("_id"):
            response = tbl_server.remove(defclass_rec)
            if response is False:
                return xmlrpclib.Fault(-32503, "Record(s) couldn't be deleted")
            return True
    return xmlrpclib.Fault(-32503, "Record(s) couldn't be deleted")

