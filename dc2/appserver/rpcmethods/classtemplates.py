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


tbl_templates = Table(MONGOS["dc2db"]["database"].get_table("classtemplates"))

TEMPLATE_RECORD = {
    "name": True,
    "description": True,
    "classes": True,
}


@rpcmethod(
    name="dc2.configuration.classtemplates.find",
    params={}, returns={}, is_xmlrpc=True, is_jsonrpc=True)
def dc2_configuration_classtemplates_find(search=None):
    if search is not None and type(search) is types.DictType:
        for k in search.keys():
            a = re.compile('{0}'.format(search[k]), re.IGNORECASE)
            search[k] = a
        result = tbl_templates.find(search)
    else:
        result = tbl_templates.find()
    return result


@rpcmethod(
    name="dc2.configuration.classtemplates.list",
    params={}, returns={}, is_xmlrpc=True, is_jsonrpc=True)
def dc2_configuration_classtemplates_list():
    result = dc2_configuration_classtemplates_find()
    return result


@rpcmethod(
    name="dc2.configuration.classtemplates.add",
    params={}, returns={}, is_xmlrpc=True, is_jsonrpc=True)
def dc2_configuration_classtemplates_add(record=None):
    if record is not None and type(record) is types.DictType:
        if (check_record(record, TEMPLATE_RECORD) and
                "name" in record and
                tbl_templates.find_one({"name": record["name"]}) is None):
            try:
                doc_id = tbl_templates.save(record)
                return doc_id
            except Exception as e:
                return xmlrpclib.Fault(
                    -32501,
                    "Record couldn't be added {0}".format(e))
    return xmlrpclib.Fault(-32501, "Record couldn't be added")


@rpcmethod(
    name="dc2.configuration.classtemplates.update",
    params={}, returns={}, is_xmlrpc=True, is_jsonrpc=True)
def dc2_configuration_classtemplates_update(record=None):
    if record is not None and type(record) is types.DictType:
        if (check_record(record, TEMPLATE_RECORD) and
            'name' in record and
            '_id' in record and
                tbl_templates.find_one({"name": record["name"]}) is not None):
            try:
                doc_id = tbl_templates.save(record)
                return doc_id
            except Exception as e:
                return xmlrpclib.Fault(
                    -32501,
                    "Record couldn't be added {0}".format(e))
    return xmlrpclib.Fault(-32501, "Record couldn't be added")


@rpcmethod(
    name="dc2.configuration.classtemplates.get",
    params={}, returns={}, is_xmlrpc=True, is_jsonrpc=True)
def dc2_configuration_classtemplates_get(id=None):
    if id is not None:
        record = tbl_templates.find_one({"_id": id})
        if record is not None:
            return record
    return None


@rpcmethod(
    name="dc2.configuration.classtemplates.remove",
    params={}, returns={}, is_xmlrpc=True, is_jsonrpc=True)
def dc2_configuration_classtemplates_remove(record=None):
    if record is not None and type(record) is types.DictType:
        if '_id' in record:
            response = tbl_templates.remove(record)
            if response is False:
                return xmlrpclib.Fault(-32503, "Record(s) couldn't be deleted")
            return True
    return xmlrpclib.Fault(-32503, "Record(s) couldn't be deleted")
