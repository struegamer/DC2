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
from globals import CA_KEY, CA_CERT
from mongodb import Database, Table
import uuid
from helpers import check_record, datetime_isoformat
from rpc import rpcmethod
import web
from ssllib import *

tbl_certs = Table(MONGOS["cs2broker"]["database"].get_table("certs"))
tbl_csrs = Table(MONGOS["cs2broker"]["database"].get_table("csrs"))
tbl_serials = Table(MONGOS["cs2broker"]["database"].get_table("serials"))

@rpcmethod(name="cs2.ssl.certs.list", returns={}, params={}, is_xmlrpc=True, is_jsonrpc=True)
def cs2_ssl_certs_list():
    cert_list = tbl_certs.find()
    return cert_list

@rpcmethod(name="cs2.ssl.certs.retrieve", returns={}, params={}, is_xmlrpc=True, is_jsonrpc=True)
def cs2_ssl_certs_get(commonname=None):
    if commonname is None:
        return xmlrpclib.Fault(-35000, "Commonname not set")
    cert_entry = tbl_certs.find_one({"commonname":commonname})
    if cert_entry is not None:
        return cert_entry
    else:
        return xmlrpclib.Fault(-35000, "Certificate for commonname '%s' not found" % commonname)

@rpcmethod(name="cs2.ssl.certs.create", returns={}, params={}, is_xmlrpc=True, is_jsonrpc=True)
def cs2_ssl_certs_create(commonname=None, serial_no=None, digest="sha1", notBefore=0, notAfter=0):
    #
    # Check Params
    #
    if commonname is None:
        return xmlrpclib.Fault(-35000, "Commonname not set")
    if serial_no is None:
        return xmlrpclib.Fault(-35000, "Serial Number not set")
    if digest not in CSR_DIGESTS:
        return xmlrpclib.Fault(-35000, "Digest not valid (digest: %s)" % digest)
    if notAfter == 0 or notAfter is None:
        return xmlrpclib.Fault(-35000, "Not after needs to be set")
    
    #
    # Check for Cert
    #
    if tbl_certs.find_one({"commonname":commonname}) is not None:
        return xmlrpclib.Fault(-35000, "Certificate for '%s' already created" % commonname)
    
    #
    # Find CSR
    #
    csr_entry = tbl_csrs.find_one({"commonname":commonname})
    if csr_entry is None:
        return xmlrpclib.Fault(-35000, "Certification Signing Request for '%s' not found" % commonname)
    
    #
    # Create CSR Object Instance
    #
    csr_obj = ssl_csr_import(csr_entry["csr_pem"])
    
    #
    # Create Cert
    #
    cert = ssl_cert_create(csr_obj, serial_no, digest, notBefore, notAfter, CA_KEY, CA_CERT)
    cert_pem = ssl_cert_export(cert)
    cert_entry = {}
    cert_entry["commonname"] = commonname
    cert_entry["cert_pem"] = cert_pem
    cert_entry["date_created"] = datetime_isoformat()["date"]
    cert_entry["time_created"] = datetime_isoformat()["time"]
    tbl_certs.save(cert_entry)
    tbl_csrs.remove(csr_entry)
    return cert_entry

@rpcmethod(name="cs2.ssl.certs.import_pem", returns={}, params={}, is_xmlrpc=True, is_jsonrpc=True)  
def cs2_ssl_certs_import(commonname=None, cert_pem=None):
    if commonname is None:
        return xmlrpclib.Fault(-35000, "Commonname not set")
    if cert_pem is None:
        return xmlrpclib.Fault(-35000, "CERT PEM not set")
    
    # 
    # Check if we have already a certificate with commonname as identification
    #
    if tbl_certs.find_one({"commonname":commonname}) is not None:
        return xmlrpclib.Fault(-35000, "A Certificate with Commonname '%s' already exists" % commonname)
    # 
    # Get Serial from Cert
    #
    cert_obj = ssl_cert_import(cert_pem)
    serial_no = long(cert_obj.get_serial_number())
    #
    # Check Serial Number
    #
    if tbl_serials.count() > 0:
        serial_record = tbl_serials.find(sort=[("serial", -1)], limit=1)
        if int(serial_record[0]["serial"]) < serial_no:
            #
            # update serial number
            # 
            serial_record[0]["serial"] = serial_no
            tbl_serials.save(serial_record[0])
    else:
        serial_record = {}
        serial_record["serial"] = serial_no
        serial_record["date_created"] = datetime_isoformat()["date"]
        serial_record["time_created"] = datetime_isoformat()["time"]
        tbl_serials.save(serial_record)
        
    cert_entry = {}
    cert_entry["commonname"] = commonname
    cert_entry["cert_pem"] = cert_pem
    cert_entry["date_created"] = datetime_isoformat()["date"]
    cert_entry["time_created"] = datetime_isoformat()["time"]
    tbl_certs.save(cert_entry)
    return cert_entry

    
