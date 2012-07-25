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
    from ticket import KerberosTicket
except ImportError,e:
    print "Your dc2 installation is not correct"
    sys.exit(1)

class KerberosAuthTransport(xmlrpclib.SafeTransport):
    def __init__(self,use_datetime=0,service='',referer=''):
        self._krb=KerberosTicket(service)
        self._referer=referer
        xmlrpclib.SafeTransport.__init__(self,use_datetime)

    def send_host(self,connection,host):
        connection.putheader('Authorization',self._krb.auth_header)
        connection.putheader('Referer',self._referer)


