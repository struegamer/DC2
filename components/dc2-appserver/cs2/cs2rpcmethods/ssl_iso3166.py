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

tbl_iso3166 = Table(MONGOS["cs2broker"]["database"].get_table("iso3166"))

@rpcmethod(name="cs2.ssl.iso3166.list",returns={},params={},is_xmlrpc=True,is_jsonrpc=True)
def cs2_iso3166_list():
    isolist=tbl_iso3166.find()
    return isolist

@rpcmethod(name="cs2.ssl.iso3166.add",returns={},params={},is_xmlrpc=True,is_jsonrpc=True)
def cs2_iso3166_add(country_name=None,country_code=None):
    if country_name is None or country_name == "":
        return xmlrpclib.Fault(-32500, "Countryname can't be None or empty")
    if country_code is None or country_code == "":
        return xmlrpclib.Fault(-32500, "Country Code can't be None or empty")
    #
    # Check for duplicate
    #
    if tbl_iso3166.find_one({"country_code":country_code}) is not None:
        return xmlrpclib.Fault(-32500, "Country Code already exists in database")
    try:
        cdict={}
        cdict["country_name"]=country_name
        cdict["country_code"]=country_code
        tbl_iso3166.save(cdict)
        return cdict
    except Exception,e:
        return xmlrpclib.Fault(-32500, "Can't save to database")    
    return xmlrpclib.Fault(-32500, "Something really horrible happened")

    

