# -*- coding: utf-8 -*-
###############################################################################
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
###############################################################################


import xmlrpclib

from .ipa_base import IPABase
from ..records import RecordUser
from .exceptions import IPAHostNotFound


class IPAUsers(IPABase):
    CHECK_INFOS = {
        'user_find': ['login', 'first', 'last', 'cn', 'displayname']
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

    def get(self, loginname):
        try:
            rec = {'login': loginname}
            result = self._ipa_proxy.user_find([], rec)
            if 'result' in result:
                a = RecordUser(result['result'])
                return a
            raise IPAHostNotFound(66667, 'Something went wrong')
        except xmlrpclib.Fault as e:
            raise IPAHostNotFound(e.faultCode, e.faultString)

