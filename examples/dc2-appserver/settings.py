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
            "cs2db": {
                "host":"localhost",
                "port":27017,
                "dbname":"cs2db",
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

#LIBVIRT_SERVER= {
#        "xenserver01": {
#            "host":"xenserver01",
#            "method":"tls",
#            "conn":None
#        }
#}


#
# HTTP Access Headers
#
ACCESS_CONTROL_ALLOW_ORIGIN="*"
ACCESS_CONTROL_ALLOW_METHODS="GET,POST,OPTIONS,PUT,DELETE"

#
# HTTP Access Headers
#
ACCESS_CONTROL_ALLOW_ORIGIN="*"
ACCESS_CONTROL_ALLOW_METHODS="GET,POST,OPTIONS,PUT,DELETE"

#
# RPC Modules for RPCDispatcher
#
CS2_ENABLED=False
XEN_ENABLED=False
FREEIPA_ENABLED=False
KERBEROS_AUTH_ENABLED=False

RPCMODULES = ['dc2.appserver.rpcmethods']
if CS2_ENABLED:
    RPCMODULES.append('cs2.rpcmethods')
if XEN_ENABLED:
    RPCMODULES.append("xenrpcmethods")

# 
# DC² Settings for PXE Boot
#
DOWNLOAD_SERVER_URL="http://172.20.0.101/"
XMLRPC_BACKEND_SERVER_URL="http://dc2db.net/RPC"
XMLRPC_BACKEND_SERVER_IP="172.20.0.100"
TEMPLATE_DIR="%s/templates" % os.path.dirname(__file__)
FREEIPA_SERVER_URL=''

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
