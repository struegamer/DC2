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

#
# Std. Python Libs
#
import sys
import types
import xmlrpclib
import re
import uuid

try:
    import web
except ImportError:
    print "You don't have web.py installed"
    sys.exit(1)


try:
    from dc2.lib.db.mongo import Database
    from dc2.lib.db.mongo import Table
    from dc2.lib.freeipa import IPAConnection
    from dc2.lib.freeipa import IPAHostNotFound
except ImportError:
    print "You don't have DC² correctly installed"
    sys.exit(1)

try:
    from dc2.appserver.helpers import check_record
    from dc2.appserver.rpc import rpcmethod
except ImportError, e:
    print('python-dc2.appserver is not correctly installed')
    print(e)
    sys.exit(1)

try:
    from settings import MONGOS
    from settings import FREEIPA_ENABLED
    from settings import KERBEROS_AUTH_ENABLED
    from settings import FREEIPA_URL
    from settings import FREEIPA_SERVICE
except ImportError:
    print "You don't have a settings file"
    sys.exit(1)


tbl_servers = Table(MONGOS["dc2db"]["database"].get_table("servers"))
tbl_ipa = Table(MONGOS['dc2db']['database'].get_table('ipa'))


IPA_RECORD = {
              'server_id':True,
              'host_id':True,
              'otp':True
}

freeipa = IPAConnection(FREEIPA_URL, FREEIPA_SERVICE)

@rpcmethod(name="dc2.freeipa.hosts.get", params={}, returns={}, is_xmlrpc=True, is_jsonrpc=True)
def dc2_freeipa_hosts_get(fqdn=None):
    if fqdn is None:
        return xmlrpclib.Fault(-32501, "FQDN is None")
    if freeipa is not None:
        try:
            result = freeipa.hosts.get(fqdn)
            return result.to_dict
        except IPAHostNotFound, e:
            return None

@rpcmethod(name='dc2.freeipa.hosts.check', params={}, returns=[], is_xmlrpc=True, is_jsonrpc=True)
def dc2_freeipa_hosts_check(fqdn=None):
    return dc2_freeipa_hosts_get(fqdn)


