#!/usr/bin/python
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

import sys
import argparse

try:
    from pymongo import Connection
except ImportError:
    print("You don't have pymongo python library installed")
    sys.exit(1)

try:
    from dc2.lib.db.mongo import Database
except ImportError, e:
        print('You did not install python-dc2.lib')
        print(e)
        sys.exit(1)


def is_table_empty(table=None):
    if table is None:
        return False
    l = table.find()
    if l.count() > 0:
        return False
    return True

def fill_inettypes(db=None):
    if db is None:
        return False
    t = db.get_table("inettypes")
    # check table
    if not is_table_empty(t):
        return False
    t.save({"type" : "loopback", "desc" : "Loopback Configuration"})
    t.save({"type" : "dhcp", "desc" : "DHCP Configuration"})
    t.save({"type" : "static", "desc" : "Static Configuration"})
    t.save({"type" : "manual", "desc" : "Manual Configuration"})

def fill_interfacetypes(db=None):
    if db is None:
        return False
    t = db.get_table('interfacetypes')
    if not is_table_empty(t):
        return False
    t.save({ "type" : "loopback", "desc" : "Loopback Interface" })
    t.save({ "type" : "ethernet", "desc" : "Ethernet Interface" })
    t.save({ "type" : "bond_1", "desc" : "BOND Interface Active/Passive" })
    t.save({ "type" : "bond_2", "desc" : "BOND Interface Active/Active" })
    t.save({ "type" : "vlan", "desc" : "VLAN Interface" })


def fill_pxetypes(db=None):
    if db is None:
        return False
    t = db.get_table('pxetypes')
    if not is_table_empty(t):
        return False
    t.save({ "type" : "none", "name" : "Default Bootmethod" })
    t.save({ "type" : "localboot", "name" : "LOCALBOOT 0" })
    t.save({ "type" : "localboot-1", "name" : "LOCALBOOT -1" })
    t.save({ "type" : "chain.c32", "name" : "CHAIN.C32" })

def fill_ribtypes(db=None):
    if db is None:
        return False
    t = db.get_table('ribtypes')
    if not is_table_empty(t):
        return False
    t.save({ "remote_type" : "ilo", "name" : "HP ILO Version 1" })
    t.save({ "remote_type" : "ilo1", "name" : "HP ILO Version 1" })
    t.save({ "remote_type" : "ilo2", "name" : "HP ILO Version 2" })
    t.save({ "remote_type" : "ilo3", "name" : "HP ILO Version 3" })
    t.save({ "remote_type" : "ilo4", "name" : "HP ILO Version 4" })
    t.save({ "remote_type" : "fsc", "name" : "Fujitsu/Siemens Remote Insight Management" })

def fill_installmethods(db=None):
    if db is None:
        return False
    t = db.get_table('installmethods')
    if not is_table_empty(t):
        return False
    t.save({ "type" : "deploy", "name" : "Deploy Server" })
    t.save({ "type" : "deploy_xen", "name" : "Deploy a Citrix XenServer" })
    t.save({ "type" : "localboot", "name" : "Boot " })

_FILL_TABLE_FUNCS = [fill_inettypes, fill_interfacetypes, fill_pxetypes,
                   fill_ribtypes, fill_installmethods]


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='initial-admincenter-data')
    parser.add_argument('-H', '--db-host', default='127.0.0.1',
                        metavar='IP|HOSTNAME', action='store', dest='db_host',
                        help="DB Host IP or FQDN")
    parser.add_argument('-P', '--db-port', default=27017, action='store',
                        dest='db_port', metavar='PORTNO', help='DB Host Port')
    parser.add_argument('-D', '--db-name', default='admincenter',
                        action='store', metavar='DBNAME', dest='db_name',
                        help='Name of the database')
    args = parser.parse_args()
    c = Connection(args.db_host, args.db_port)
    db = Database(c, args.db_name)
    for i in _FILL_TABLE_FUNCS:
        i(db)

