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

from dc2.api import RPCClient

class BackendSettings(RPCClient):
    def get(self):
        result = {'IS_FREEIPA_ENABLED':False,
                  'IS_CS2_ENABLED':False,
                  'IS_XEN_ENABLED':False,
                  'IS_KERBEROS_AUTH_ENABLED':False
                  }
        try:
            result = self._proxy.dc2.backend.settings.get()
            return result
        except Exception,e:
            return result
        return result


