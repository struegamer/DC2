# -*- coding: utf-8 -*-
###############################################################################
#
#    (DC)² - DataCenter Deployment Control
#    Copyright (C) 2010, 2011, 2012, 2013, 2014  Stephan Adig <sh@sourcecode.de>
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

#
# Std. Python Libs
#
import sys

try:
    from dc2.appserver.rpc import rpcmethod
except ImportError:
    print "You don't have DC² correctly installed"
    sys.exit(1)

try:
    from settings import CS2_ENABLED
    from settings import XEN_ENABLED
    from settings import FREEIPA_ENABLED
    from settings import KERBEROS_AUTH_ENABLED

except ImportError:
    print "You don't have a settings file"
    sys.exit(1)


@rpcmethod(
    name="dc2.backend.settings.get",
    params={}, returns={}, is_xmlrpc=True, is_jsonrpc=True)
def dc2_backend_settings_get():
    result = {'IS_FREEIPA_ENABLED': FREEIPA_ENABLED,
              'IS_CS2_ENABLED': CS2_ENABLED,
              'IS_XEN_ENABLED': XEN_ENABLED,
              'IS_KERBEROS_AUTH_ENABLED': KERBEROS_AUTH_ENABLED}
    return result
