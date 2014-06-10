# -*- coding: utf-8 -*-
#################################################################################
#
#    (DC)² - DataCenter Deployment Control
#    Copyright (C) 2010, 2011  Stephan Adig <sh@sourcecode.de>
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
import types
import xmlrpclib
import re
from settings import MONGOS
from mongodb import Database, Table
import uuid
from helpers import check_record, datetime_isoformat
from rpc import rpcmethod
import web
from ssllib import *

tbl_csrs = Table(MONGOS["cs2broker"]["database"].get_table("csrs"))
tbl_keys = Table(MONGOS["cs2broker"]["database"].get_table("keys"))

@rpcmethod(name="cs2.ssl.csrs.list", returns={}, params={}, is_xmlrpc=True, is_jsonrpc=True)
def cs2_ssl_csrs_list():
    csr_list = tbl_csrs.find()
    return csr_list

@rpcmethod(name="cs2.ssl.csrs.retrieve", returns={}, params={}, is_xmlrpc=True, is_jsonrpc=True)
def cs2_ssl_csrs_get(commonname=None):
    csr_entry = tbl_csrs.find_one({"commonname":commonname})
    return csr_entry

@rpcmethod(name="cs2.ssl.csrs.create", returns={}, params={}, is_xmlrpc=True, is_jsonrpc=True)
def cs2_ssl_csrs_create(commonname=None, keyname=None, passphrase=None, digest="sha1", subjects=None):
    
    #
    # Check arguments
    #
    web.debug("passphrase: %s" % passphrase)
    if commonname is None:
        return xmlrpclib.Fault(-32500, "Commonname is not set")
    if keyname is None:
        return xmlrpclib.Fault(-32500, "Keyname is not set")
    if digest not in CSR_DIGESTS:
        return xmlrpclib.Fault(-32500, "CSR Digest not in CSR_DIGESTS")
    if subjects is None:
        return xmlrpclib.Fault(-32500, "Subjects can't be None")
    if type(subjects) is not types.DictType:
        return xmlrpclib.Fault(-32500, "Subjects needs to be a DICT Type")
    for k in subjects.keys():
        if k not in SUBJECTS:
            return xmlrpclib.Fault(-32500, "Subject '%s' is not valid" % k)
    
    #
    # Get Key
    #
    key_entry = tbl_keys.find_one({"keyname":keyname})
    web.debug(key_entry)
    if key_entry is None:
        return xmlrpclib.Fault(-32500, "Key with keyname '%s' not found" % keyname)
    # 
    # Get PKey Instance of key_entry["key_pem"]
    #
    web.debug("Key Pem: %s " % key_entry["key_pem"])
    try:        
        key_obj = ssl_key_import(key_entry["key_pem"], passphrase)
    except:
        return xmlrpclib.Fault(-32500, "Can't import Keyname %s" % keyname)
    #
    # Generate CSR
    #
    csr_obj = ssl_csr_create(key_obj, digest, subjects)
    
    #
    # Export CSR Instance into PEM Format
    #
    csr_pem = ssl_csr_export(csr_obj)
    
    #
    # Check if a CSR request of name "commonname" already exists
    #
    if tbl_csrs.find_one({"commonname":commonname}) is None:
        csr_entry = {}
        csr_entry["commonname"] = commonname
        csr_entry["csr_with_key"] = keyname
        csr_entry["date_created"] = datetime_isoformat()["date"]
        csr_entry["time_created"] = datetime_isoformat()["time"]
        csr_entry["csr_pem"] = csr_pem
        tbl_csrs.save(csr_entry)
        return csr_entry
    else:
        return xmlrpclib.Fault(-32500, "Certificate Signing Request with name '%s' already exists" % commonname)
    
    return xmlrpclib.Fault(-32500, "Something went really really wrong!")
        
@rpcmethod(name="cs2.ssl.csrs.remove", returns={}, params={}, is_xmlrpc=True, is_jsonrpc=True)
def cs2_ssl_csrs_remove(commonname=None):
    if commonname is None:
        return xmlrpclib.Fault(-32500, "Commonname is not set")
    #
    # Check for CSR Entry in Database
    #
    csr_entry = tbl_csrs.find_one({"commonname":commonname})
    if csr_entry is not None:
        tbl_csrs.remove(csr_entry)
        return True
    else:
        return False
    return xmlrpclib.Fault(-32500, "Something went really really wrong!")        
