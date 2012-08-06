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


import sys
import urlparse
import xmlrpclib

try:
    from dc2.lib.auth.kerberos.xmlrpc import KerberosServerProxy
except ImportError,e:
    print 'not installed KerberosServerProxy'
    print e
    sys.exit(1)

def get_xmlrpc_transport(url,kerberos_enabled):
    parsed_url=urlparse.urlparse(url)
    proxy=None
    if kerberos_enabled:
        kerberos_service='HTTP@%s' % parsed_url.hostname
        proxy=KerberosServerProxy(url,service=kerberos_service,allow_none=True)
    else:
        proxy=xmlrpclib.ServerProxy(url,allow_none=True)
    return proxy

