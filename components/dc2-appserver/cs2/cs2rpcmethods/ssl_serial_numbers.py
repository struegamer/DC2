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
from settings import MONGOS, SERIAL_START
from mongodb import Database, Table
import uuid
from helpers import check_record, datetime_isoformat
from rpc import rpcmethod
import web

tbl_serials = Table(MONGOS["cs2broker"]["database"].get_table("serials"))

@rpcmethod(name="cs2.ssl.serial.get", returns={}, params={}, is_xmlrpc=True, is_jsonrpc=True)
def cs2_ssl_serial_get():
    serial_no = SERIAL_START
    if tbl_serials.count() > 0:
        serial_record = tbl_serials.find(sort=[("serial", -1)], limit=1)
        serial_no = int(serial_record[0]["serial"]) + 1
        serial_record[0]["serial"] = serial_no
        tbl_serials.save(serial_record[0])
        return serial_record[0]
    else:
        serial_record = {}
        serial_record["serial"] = serial_no
        serial_record["date_created"] = datetime_isoformat()["date"]
        serial_record["time_created"] = datetime_isoformat()["time"]
        tbl_serials.save(serial_record)
        return serial_record
    
