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

from ipa_base import IPABase
from ..records import RecordHost
from .exceptions import IPAHostNotFound

class IPAHosts(IPABase):
    def get(self, fqdn):
        try:
            result = self._ipa_proxy.host_show([fqdn])
            if 'result' in result:
                a = RecordHost(result['result'])
                return a
            raise IPAHostNotFound(e.faultCode, e.faultString)
        except xmlrpclib.Fault, e:
            raise IPAHostNotFound(e.faultCode, e.faultString)

    def find(self, search):
        result = self._ipa_proxy.host_find([search])
        if 'count' in result and result['count'] > 0 and 'result' in result:
            a = []
            for i in result['result']:
                a.append(RecordHost(i))
            return a
        return []

    def add(self, fqdn, add_infos):
        pass
