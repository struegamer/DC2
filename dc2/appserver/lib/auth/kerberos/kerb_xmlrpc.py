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
import xmlrpclib

try:
    from settings import FREEIPA_ENABLED
    from settings import FREEIPA_SERVER_URL
    from settings import FREEIP_KERBEROS_SERVICE
except ImportError,e:
    print "you don't have a settings file"
    sys.exit(1)

try:
    from ticket import KerberosTicket
    from kerb_xmlrpc import KerberosAuthTransport
except ImportError,e:
    print 'Your installation of DC2 is not correct'
    sys.exit(1)

class KerberosServerProxy(xmlrpclib.ServerProxy):
    def __init__(self, uri, service=None, encoding=None, verbose=0,
                 allow_none=0, use_datetime=0):
        kerb_transport=KerberosAuthTransport(use_datetime,service,uri)
        xmlrpclib.ServerProxy.__init__(self,uri,transport=kerb_transport,encoding=encoding,verbose=verbose,allow_none=allow_none, use_datetime=use_datetime)

