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
from globals import CA_NAME, CA_KEY, CA_CERT
from settings import MONGOS
from mongodb import Database, Table
import uuid
from helpers import check_record, datetime_isoformat
from rpc import rpcmethod
import web
from ssllib import *

tbl_crls = Table(MONGOS["cs2broker"]["database"].get_table("crls"))
tbl_certs = Table(MONGOS["cs2broker"]["database"].get_table("certs"))

@rpcmethod(name="cs2.ssl.crls.list", returns={}, params={}, is_xmlrpc=True, is_jsonrpc=True)
def cs2_ssl_crls_list():
    crl_list = tbl_crls.find()
    return crl_list

@rpcmethod(name="cs2.ssl.crls.retrieve", returns={}, params={}, is_xmlrpc=True, is_jsonrpc=True)
def cs2_ssl_crls_get(ca_name=None):
    if ca_name is None:
        return None
    crl_entry = tbl_crls.find_one({"ca_name":ca_name})
    return crl_entry

@rpcmethod(name="cs2.ssl.crls.revoke.certificate", returns={}, params={}, is_xmlrpc=True, is_jsonrpc=True)
def cs2_ssl_crls_revoke_cert(commonname=None, reason=None):
    web.debug("here")
    if commonname is None:
        return xmlrpclib.Fault(-35000, "Commonname not set")
    if reason is None:
        return xmlrpclib.Fault(-35000, "Reason not set")
    if reason not in REVOKE_REASONS:
        return xmlrpclib.Fault(-35000, "Reason is not valid")
    
    #
    # Check if CRL record exists
    #
    web.debug("here 1")
    crl_record = tbl_crls.find_one({"ca_name":CA_NAME})
    crl_obj=None
    web.debug("crl_record: %s" % crl_record)
    if crl_record is None:
        #
        # Create CRL Record
        #
        crl_obj = ssl_crl_create(CA_KEY, CA_CERT)
        crl_record = {}
        crl_record["ca_name"] = CA_NAME
        crl_record["crl_pem"] = ssl_crl_export(crl_obj, CA_KEY, CA_CERT)
        crl_record["date_created"] = datetime_isoformat()["date"]
        crl_record["time_created"] = datetime_isoformat()["time"]
        tbl_crls.save(crl_record)
    else:
        crl_obj=ssl_crl_import(crl_record["crl_pem"])
    #
    # Get CERT
    #
    web.debug("here 2")
    cert_entry = tbl_certs.find_one({"commonname":commonname})
    if cert_entry is None:
        return xmlrpclib.Fault(-35000, "Certificate '%s' not found" % commonname)
    cert_obj = ssl_cert_import(cert_entry["cert_pem"])
    
    # 
    # Revoke Certificate
    #
    web.debug("here 3")
    try:
        crl_obj = ssl_crl_revoke_certificate(crl_obj, cert_obj, str(reason))
        crl_pem = ssl_crl_export(crl_obj, CA_KEY, CA_CERT)
        crl_record["crl_pem"] = crl_pem
        tbl_crls.save(crl_record)    
        tbl_certs.remove({"commonname":commonname})
        return crl_record
    except Exception,e:
        return xmlrpclib.Fault(-35000, "Exception %s" % e)
    
