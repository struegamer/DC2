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



tbl_keys = Table(MONGOS["cs2broker"]["database"].get_table("keys"))



@rpcmethod(name="cs2.ssl.keys.list", returns={"list keys":"List ssl key records"}, params={"dict key_record":"Type record"}, is_xmlrpc=True, is_jsonrpc=True)
def cs2_ssl_keys_list():
    key_list = tbl_keys.find()
    return key_list

@rpcmethod(name="cs2.ssl.keys.retrieve", returns={}, params={}, is_xmlrpc=True, is_jsonrpc=True)
def cs2_ssl_keys_get(keyname=None):
    if keyname is None:
        return None
    key_entry = tbl_keys.find_one({"keyname":keyname})
    return key_entry

@rpcmethod(name="cs2.ssl.keys.create", returns={}, params={}, is_xmlrpc=True, is_jsonrpc=True)
def cs2_ssl_keys_create(keyname=None, description=None, key_type=TYPE_DSA, key_bits=2048, cipher="des3", passphrase=None):
    """
        Creates an SSL Key and persists it in the database.
    """
    if keyname is None:
        return xmlrpclib.Fault(-32099, "Keyname is not set")
    if int(key_type) != TYPE_DSA and int(key_type) != TYPE_RSA:
        return xmlrpclib.Fault(-32099, "SSL Key Type is not TYPE_DSA or TYPE_RSA")
    if int(key_bits) is None or int(key_bits) == 0:
        return xmlrpclib.Fault(-32099, "SSL Key Bits is not allowed to be None or 0")
    if passphrase is not None:
        if cipher is None:
            return xmlrpclib.Fault(-32099, "SSL Key Cipher is not allowed to be None when passphrase is set")
        if not cipher in KEY_CIPHERS:
            return xmlrpclib.Fault(-32099, "SSL Key Cipher needs to be a value from %s" % KEY_CIPHERS)
    if description is None:
        description = ""
    # 
    # Check for Keyname in Database
    #
    try:
        if tbl_keys.find_one({"keyname":keyname}) is None:
            #
            # Generate Key and store it
            #
            ssl_key = ssl_key_create(int(key_type), int(key_bits))
            if cipher is None:
                ssl_key_pem=ssl_key_export(ssl_key)
            else:
                ssl_key_pem = ssl_key_export(ssl_key, cipher, str(passphrase))
            key_entry = {}
            key_entry["date_created"] = datetime_isoformat()["date"]
            key_entry["time_created"] = datetime_isoformat()["time"]
            key_entry["keyname"] = keyname
            key_entry["description"] = description
            key_entry["key_pem"] = ssl_key_pem
            web.debug("saving")
            tbl_keys.save(key_entry)        
            return key_entry
        else:
            return xmlrpclib.Fault(-32099, "SSL Key with keyname '%s' already exists" % keyname)
    except Exception,e:
        return xmlrpclib.Fault(-32099, "Something went really really wrong! %s" % e)
    return xmlrpclib.Fault(-32099, "Something went really really wrong!")

@rpcmethod(name="cs2.ssl.keys.remove", returns={}, params={}, is_xmlrpc=True, is_jsonrpc=True)
def cs2_ssl_keys_remove(keyname=None):
    if keyname is None:
        return xmlrpclib.Fault(-32500, "Keyname is not set")
    key_entry = tbl_keys.find_one({"keyname":keyname})
    if key_entry is not None:
        tbl_keys.remove(key_entry)
        return True
    else:
        return False
    return xmlrpclib.Fault(-32500, "SSL Key with keyname '%s' not found")

@rpcmethod(name="cs2.ssl.keys.import_pem", returns={}, params={}, is_xmlrpc=True, is_jsonrpc=True)
def cs2_ssl_keys_import(keyname=None, key_pem=None):
    if keyname is None:
        return xmlrpclib.Fault(-32500, "Keyname is not set")
    if key_pem is None:
        return xmlrpclib.Fault(-32500, "key_pem is not set")
    
    #
    # Check if Key with keyname already exists in database
    #
    if tbl_keys.find_one({"keyname":keyname}) is not None:
        return xmlrpclib.Fault(-32500, "SSL Key with keyname '%s' already exists")
    key_entry = {}
    key_entry["keyname"] = keyname
    key_entry["key_pem"] = key_pem
    key_entry["description"] = "Imported"
    key_entry["date_created"] = datetime_isoformat()["date"]
    key_entry["time_created"] = datetime_isoformat()["time"]
    tbl_keys.save(key_entry)
    return key_entry

        
