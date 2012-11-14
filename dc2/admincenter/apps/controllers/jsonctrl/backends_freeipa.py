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

import sys
import os
import os.path
import re
import types
import json

try:
    import web
except ImportError, e:
    print "You need to install web.py"
    sys.exit(1)

try:
    from dc2.lib.decorators import Logger
    from dc2.lib.transports import get_xmlrpc_transport
except ImportError, e:
    print 'you do not have dc2.lib installed'
    print e
    sys.exit(1)

try:
    from dc2.admincenter.lib.controllers import JSONController
    from dc2.admincenter.lib import backends
    from dc2.admincenter.lib.auth import needs_auth
    from dc2.admincenter.globals import logger
except ImportError, e:
    print 'you have a problem with dc2.admincenter'
    print e
    sys.exit(1)

try:
    from dc2.api.dc2.addons.freeipa import Hosts as FreeIPAHosts
    from dc2.api.dc2.inventory import Hosts
except ImportError, e:
    print 'you didn\'t have dc2.api installed'
    print e
    sys.exit(1)

class JSONFreeipaHostController(JSONController):
    def __init__(self, *args, **kwargs):
        super(JSONFreeipaHostController, self).__init__(*args, **kwargs)
        self._prepare_urls()

    def _prepare_urls(self):
        self.add_url_handler_to_verb('GET', 'check', 'freeipa_host_check')
        self.add_process_method('freeipa_host_check', self._freeipa_host_check)

    @needs_auth
    @Logger(logger=logger)
    def _freeipa_host_check(self, *args, **kwargs):
        verb = kwargs.get('verb', None)
        if verb is not None:
            params = web.input()
            backend_id = params.get('backend_id', None)
            host_id = params.get('host_id', None)
            web.debug('_freeipa_host_check: backendID: %s, host_id: %s' % (backend_id,host_id))
            
            if backend_id is not None:
                backend = backends.backend_get({'_id':backend_id})
                if backend is not None:
                    transport = get_xmlrpc_transport(backend['backend_url'],
                                                     backend['is_kerberos'])
                    fhosts = FreeIPAHosts(transport)
                    hosts = Hosts(transport)
                    if host_id is not None:
                        h = hosts.get(id=host_id)
                        if h is not None:
                            result = fhosts.check('{0}.{1}'.format(h['hostname'], h['domainname']))
                            if result is not None and result is not False:
                                output = self._prepare_output(result=
                                                  {'backend_id':backend_id,
                                                   'in_freeipa':True})
                                return output
            output = self._prepare_output(result={'backend_id':backend_id, 'in_freeipa':False})
            return output






