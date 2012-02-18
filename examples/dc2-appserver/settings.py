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

# settings.py
import logging
import os
import os.path

# 
# MongoDB Server and Database Collections
#

MONGOS = {
            "dc2db": {
                "host":"localhost",
                "port":27017,
        		"dbname":"dc2db",
                "database":None
            },
            "cs2broker": {
                "host":"localhost",
                "port":27017,
                "dbname":"cs2broker",
                "database":None
            },
            "xendb": {
                "host":"localhost",
                "port":27017,
                "dbname":"xendb",
                "database":None
             },
             "userdb": {
                "host":"localhost",
                "port":27017,
                "dbname":"userdb",
                "database":None
             }
}

#
# RPC Modules for RPCDispatcher
#
CS2_ENABLED=False
XEN_ENABLED=False

RPCMODULES = ['dc2.rpcmethods']
if CS2_ENABLED:
    RPCMODULES.append('cs2rpcmethods')
if XEN_ENABLED:
    RPCMODULES.append("xenrpcmethods")

# 
# DC² Settings for XPE Boot
#
DOWNLOAD_SERVER_URL="http://172.20.0.101/"
XMLRPC_BACKEND_SERVER_URL="http://dc2db.net/RPC"
XMLRPC_BACKEND_SERVER_IP="172.20.0.100"
TEMPLATE_DIR="%s/templates" % os.path.dirname(__file__)

#
# LOGFILE settings
#
if os.path.exists("/var/log/dc2"):
    LOGFILE = "/var/log/dc2/dc2.log"
else:
    LOGFILE = "dc2.log"    
LOGLEVEL = logging.DEBUG


APPNAME = "dc2"

#
# CS² settings
#

CA_KEY_FILE = "/etc/cs2/ca.key"
CA_CERT_FILE = "/etc/cs2/ca.crt"
CA_PASSWORD = "test123"
CA_NAME = "PuppetCA"
SERIAL_START = 10000
