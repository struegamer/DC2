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
import types

try:
    from dc2.lib.auth.kerberos.xmlrpc import KerberosServerProxy
    from dc2.lib.freeipa.lib import IPAHosts
except ImportError, e:
    print "Your DC2 installation is not correct"
    sys.exit(1)


class IPAConnection(object):
    def __init__(self, ipa_server_url, ipa_kerberos_service):
        self._ipa_server_url = ipa_server_url
        self._ipa_kerberos_service = ipa_kerberos_service
        self._ipa_proxy = KerberosServerProxy(ipa_server_url,
                                              ipa_kerberos_service,
                                              allow_none=True)
        self._init_objects()

    @property
    def ipa_proxy(self):
        return self._ipa_proxy

    @property
    def hosts(self):
        return self._hosts

    def _init_objects(self):
        self._hosts = IPAHosts(self.ipa_proxy)

