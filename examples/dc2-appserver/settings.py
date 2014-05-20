# -*- coding: utf-8 -*-
#
#
# (DC)² - DataCenter Deployment Control
# Copyright (C) 2010, 2011, 2012, 2013, 2014  Stephan Adig <sh@sourcecode.de>
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#

# settings.py
import logging
import os
import os.path

#
# MongoDB Server and Database Collections
#

MONGOS = {
    "dc2db": {
        "host": "localhost",
        "port": 27017,
        "dbname": "dc2db",
        "database": None
    },
    "cs2db": {
        "host": "localhost",
        "port": 27017,
        "dbname": "cs2db",
        "database": None
    },
    "xendb": {
        "host": "localhost",
        "port": 27017,
        "dbname": "xendb",
        "database": None
    },
    "userdb": {
        "host": "localhost",
        "port": 27017,
        "dbname": "userdb",
        "database": None
    }
}

# LIBVIRT_SERVER= {
#        "xenserver01": {
#            "host":"xenserver01",
#            "method":"tls",
#            "conn":None
#        }
# }


#
# HTTP Access Headers
#
ACCESS_CONTROL_ALLOW_ORIGIN = "*"
ACCESS_CONTROL_ALLOW_METHODS = "GET,POST,OPTIONS,PUT,DELETE"

#
# HTTP Access Headers
#
ACCESS_CONTROL_ALLOW_ORIGIN = "*"
ACCESS_CONTROL_ALLOW_METHODS = "GET,POST,OPTIONS,PUT,DELETE"

EXT_CONFIG = {}
#
# RPC Modules for RPCDispatcher
#
DHCP_MANAGEMENT = False
CS2_ENABLED = False
XEN_ENABLED = False
FREEIPA_ENABLED = False
KERBEROS_AUTH_ENABLED = False

RPCMODULES = ['dc2.appserver.rpcmethods']
if CS2_ENABLED:
    RPCMODULES.append('cs2.rpcmethods')
if XEN_ENABLED:
    RPCMODULES.append("xenrpcmethods")
if FREEIPA_ENABLED:
    RPCMODULES.append('dc2.appserver.addons.freeipa')

if DHCP_MANAGEMENT:
    RPCMODULES.append('dc2.dhcp.appserver.dhcp_rpcmethods')
    EXT_CONFIG['dhcpd'] = {}
    EXT_CONFIG['dhcpd']['template_file'] = 'dhcpd_subnet.tmpl'
    EXT_CONFIG['dhcpd']['template_dir'] = '/etc/dc2/dhcpd/templates/'
    EXT_CONFIG['dhcpd']['store_directory'] = '/etc/dhcpd/auto.gen.includes/'
    EXT_CONFIG['dhcpd']['template'] = None
    EXT_CONFIG['dhcpd']['range_start'] = 100
    EXT_CONFIG['dhcpd']['range_end'] = 150
    EXT_CONFIG['dhcpd']['dhcp_next_server'] = '127.0.0.1'
    EXT_CONFIG['dhcpd']['dc2db_ipxe_url'] = 'http://dc2db.net/ipxe'
    EXT_CONFIG['dhcpd']['option_domain_name_servers'] = '127.0.0.1'
    EXT_CONFIG['dhcpd']['option_routers'] = '127.0.0.1'

#
# FREEIPA_URL should be 'https://your.freeipa.tld/ipa/xml
#

FREEIPA_URL = None

#
# FREEIPA_SERVICE should be 'HTTP@your.freeipa.tld
#

FREEIPA_SERVICE = None

#
# FREEIPA_FORCE_ADD
# if True: Add host to IPA even when it's not in DNS
# if False: Add host and fail when hostname is not in DNS
#

FREEIPA_FORCE_ADD = False

#
# FAI Boot Settings
#
# ROOTFS_TYPE is the type of rootfile system to be mounted
# ROOTFS_TYPE='squashfs' ==> load rootfs as squashfs image from http
# ROOTFS_TYPE='nfs' ==> root=nfs://...

# ROOTFS_TYPE = 'squashfs'
# ROOTFS_LOCATION = 'http://archivehost.domain.tld/rootfs.img'

#
# DC² Settings for PXE Boot
#
DOWNLOAD_SERVER_URL = "http://172.20.0.101/"
XMLRPC_BACKEND_SERVER_URL = "http://dc2db.net/RPC"
XMLRPC_BACKEND_SERVER_IP = "172.20.0.100"
TEMPLATE_DIR = "%s/templates" % os.path.dirname(__file__)
FREEIPA_SERVER_URL = ''

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
