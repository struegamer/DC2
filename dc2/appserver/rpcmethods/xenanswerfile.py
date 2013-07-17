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


tbl_xenanswerfiles=Table(MONGOS["dc2db"]["database"].get_table("xen_answerfile"))

XEN_RECORD = {
    "filename":True,
    "anwerfile":True,
}

@rpcmethod(name="dc2.configuration.xen.answerfile.list",params={},returns={},is_xmlrpc=True,is_jsonrpc=True)
def dc2_configuration_xenanswerfile_list(search=None):
    result=[]
    if search is not None and type(search) is types.DictType:
        for k in search.keys():
            a=re.compile('%s' % search[k], re.IGNORECASE)
            search[k]=a
        result=tbl_xenanswerfiles.find(search)
    else:
        result=tbl_xenanswerfiles.find()
    return result

@rpcmethod(name="dc2.configuration.xen.answerfile.add",params={},returns={},is_xmlrpc=True,is_jsonrpc=True)
def dc2_configuration_xenanswerfile_add(rec=None):
    if rec is not None and type(rec) is types.DictType:
        if check_record(rec,XEN_RECORD) and rec.has_key("filename") and tbl_xenanswerfiles.find_one({"filename":rec["filename"]}) is None:
            doc_id=tbl_xenanswerfiles.save(rec)
            return doc_id
    return xmlrpclib.Fault(-32501,"Record could not be added")


@rpcmethod(name="dc2.configuration.xen.answerfile.update",params={},returns={},is_xmlrpc=True,is_jsonrpc=True)
def dc2_configuration_xenanswerfile_update(rec=None):
    if rec is not None and type(rec) is types.DictType:
        if check_record(rec,XEN_RECORD) and rec.has_key("filename") and tbl_xenanswerfiles.find_fond({"filename":rec["filename"]}) is not None:
            doc_id=tbl_xenanswerfiles.save(rec)
            return doc_id
    return xmlrpclib.Fault(-32501,"Record could not be updates")

@rpcmethod(name="dc2.configuration.xen.answerfile.delete",params={},returns={},is_xmlrpc=True,is_jsonrpc=True)
def dc2_configuration_xenanswerfiles_delete(rec=None):
    if rec is not None and type(rec) is types.DictType:
        if rec.has_key("_id"):
            response=tbl_xenanserfiles.remove(rec)
            if response is False:
                return xmlrpclib.Fault(-32501,"Record(s) could not be deleted")
            return True
    return xmlrpclib.Fault(-32501,"Record(s) could not be deleted")

@rpcmethod(name="dc2.configuration.xen.answerfile.get",params={},returns={},is_xmlrpc=True,is_jsonrpc=True)
def dc2_configuration_xenanswerfiles_get(rec=None):
    if rec is not None and type(rec) is types.DictType:
        if rec.has_key("filename") or rec.has_key("_id"):
            doc=tbl_xenanswerfiles.find_one(rec)
            if doc is not None:
                return doc
    return xmlrpclib.Fault(-32501,"Unable to find record")

