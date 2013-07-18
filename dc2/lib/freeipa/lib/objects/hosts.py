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


import xmlrpclib

from .ipa_base import IPABase
from ..records import RecordHost
from .exceptions import IPAHostNotFound
from .exceptions import IPAHostAddError
from .exceptions import IPAHostDeleteError


class IPAHosts(IPABase):
    CHECK_INFOS = {
        'host_add': ['fqdn', 'force', 'description', 'locality',
        'nshostlocation', 'nshardwareplatform', 'nsosversion', 'userpassword',
        'random', 'randompassword', 'usercertificate', 'krbprincipalname',
        'macaddress', 'ipasshpubkey', 'sshpubkeyfp', 'no_reverse']
    }

    def _check_infos(self, command=None, infos=None):
        if command is None or infos is None:
            return False
        if command not in self.CHECK_INFOS.keys():
            return False
        for i in infos.keys():
            if i not in self.CHECK_INFOS[command]:
                return False
        return True

    def get(self, fqdn):
        try:
            result = self._ipa_proxy.host_show([fqdn])
            if 'result' in result:
                a = RecordHost(result['result'])
                return a
            raise IPAHostNotFound(66667, 'Something went wrong')
        except xmlrpclib.Fault as e:
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
        if not self._check_infos('host_add', add_infos):
            raise IPAHostAddError(66666, 'keywords in host_add infos are not correct')
        try:
            result = self._ipa_proxy.host_add([fqdn], add_infos)
            if 'result' in result:
                a = RecordHost(result['result'])
                return a
            raise IPAHostAddError(66667, 'Something went wrong')
        except xmlrpclib.Fault as e:
            raise IPAHostAddError(e.faultCode, e.faultString)

    def delete(self, fqdn):
        if fqdn is None or fqdn == '':
            raise IPAHostDeleteError(66668, 'Can\'t delete the host from FreeIPA')
        try:
            result = self._ipa_proxy.host_del([fqdn])
            if 'result' in result:
                a = RecordHost(result['result'])
                return a
            raise IPAHostDeleteError(66667, 'Something went wrong')
        except xmlrpclib.Fault as e:
            raise IPAHostDeleteError(e.faultCode, e.faultString)
