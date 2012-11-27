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
    from dc2.appserver.helpers import check_record
    from dc2.appserver.rpc import rpcmethod
except ImportError, e:
    print('python-dc2.appserver is not correctly installed')
    print(e)
    sys.exit(1)

try:
    import dns.resolver
except ImportError, e:
    print('dnspython is not correctly installed')
    print(e)
    sys.exit(1)

@rpcmethod(name='dc2.dns.lookups.query', params={}, result={}, is_xmlrpc=True, is_jsonrpc=True)
def dc2_dns_lookups_query(fqdn=None, nstype='A'):
    if fqdn is None:
        return False
    try:
        answers = dns.resolver.query(fqdn, 'A')
        result = {'fqdn':fqdn,
                'canonical_name':answer.canonical_name}
        a = []
        for i in answers:
            a.append(i.address)
        result['records'] = a
        return result
    except dns.resolver.NXDOMAIN as e:
        raise xmlrpclib.Fault(66668, 'dc2.dns.lookup.query: FQDN doesn\'t exists')

