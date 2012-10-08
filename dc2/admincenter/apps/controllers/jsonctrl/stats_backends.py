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
import os
import os.path
import re
import types
import json

try:
    import web
except ImportError,e:
    print "You need to install web.py"
    sys.exit(1)

try:
    from dc2.lib.logging import Logger
    from dc2.lib.transports import get_xmlrpc_transport
except ImportError,e:
    print 'you do not have dc2.lib installed'
    print e
    sys.exit(1)

try:
    from dc2.admincenter.lib.controllers import JSONController
    from dc2.admincenter.lib import backends
    from dc2.admincenter.lib.auth import needs_auth
    from dc2.admincenter.globals import logger
except ImportError,e:
    print 'you have a problem with dc2.admincenter'
    print e
    sys.exit(1)

try:
    from dc2.api.dc2.inventory import Servers
    from dc2.api.dc2.inventory import Hosts
    from dc2.api.dc2.deployment import InstallState
except ImportError,e:
    print 'you didn\'t have dc2.api installed'
    print e
    sys.exit(1)

class JSONBackendController(JSONController):
    def __init__(self, *args, **kwargs):
        super(JSONBackendController,self).__init__(*args,**kwargs)
        self._prepare_urls()
    
    @Logger(logger=logger)
    def _prepare_urls(self):
        self.add_url_handler_to_verb('GET','backendstats','backend_stats')
        self.add_process_method('backend_stats',self._backend_stats)

        self.add_url_handler_to_verb('GET','backend_servers_stats','backend_servers_stats')
        self.add_process_method('backend_servers_stats',self._backend_servers_stats)

        self.add_url_handler_to_verb('GET','backend_hosts_stats','backend_hosts_stats')
        self.add_process_method('backend_hosts_stats',self._backend_hosts_stats)

        self.add_url_handler_to_verb('GET','backend_deployment_stats','backend_deployment_stats')
        self.add_process_method('backend_deployment_stats',self._backend_deployment_stats)

    @needs_auth
    @Logger(logger=logger)
    def _backend_stats(self,*args,**kwargs):
        web.debug('backend_stats')
        verb=kwargs.get('verb',None)
        web.debug('%s: %s' % (self.__class__.__name__,verb))
        if verb is not None:
            backendlist=backends.backend_list()
            result=self._prepare_output(result={'backend_count':len(backendlist)})
            web.debug('_backend_stats: %s' % result)
            return result
    @needs_auth
    @Logger(logger=logger)
    def _backend_servers_stats(self, *args, **kwargs):
        verb=kwargs.get('verb',None)
        if verb is not None:
            params=web.input()
            backend_id = params.get('backend_id',None)
            if backend_id is not None:
                backend=backends.backend_get({'_id':backend_id})
                if backend is not None:
                    transport=get_xmlrpc_transport(backend['backend_url'],backend['is_kerberos'])
                    s=Servers(transport)
                    count_servers=s.count()
                    result=self._prepare_output(result={'backend_id':backend_id,'server_count':count_servers})
                    return result
            result=self._prepare_output(result={'backend_id':backend_id,'server_count':0})
            return result

    @needs_auth
    @Logger(logger=logger)
    def _backend_hosts_stats(self,*args,**kwargs):
        verb=kwargs.get('verb',None)
        if verb is not None:
            params=web.input()
            backend_id=params.get('backend_id',None)
            if backend_id is not None:
                backend=backends.backend_get({'_id':backend_id})
                if backend is not None:
                    transport=get_xmlrpc_transport(backend['backend_url'],backend['is_kerberos'])
                    s=Hosts(transport)
                    count_hosts=s.count()
                    result=self._prepare_output(result={'backend_id':backend_id,'host_count':count_hosts})
                    return result
            result=self._prepare_output(result={'backend_id':backend_id,'host_count':0})
            return result
    
    @needs_auth
    @Logger(logger=logger)
    def _backend_deployment_stats(self, *args, **kwargs):
        verb=kwargs.get('verb',None)
        if verb is not None:
            params=web.input()
            backend_id=params.get('backend_id',None)
            what=params.get('status',None)
            if backend_id is not None:
                backend=backends.backend_get({'_id':backend_id})
                if backend is not None:
                    transport=get_xmlrpc_transport(backend['backend_url'],backend['is_kerberos'])
                    s=InstallState(transport)
                    if what is not None and what=='all':
                        count_deploy=s.count('deploy')
                        count_localboot=s.count('localboot')
                        result=self._prepare_output(result={
                            'backend_id':backend_id,
                            'status':'all',
                            'count_localboot':count_localbooti,
                            'count_deploy':count_deploy})
                    elif what is not None and what in ('deploy','localboot'):
                        count=s.count(what)
                        result=self._prepare_output(result={
                            'backend_id':backend_id,
                            'status':what,
                            'count':count})
                    return result
            if what is None:
                result=self._prepare_output(result={'backend_id':backend_id,'status':'all','count_localboot':0,'count_deploy':0})
            elif what is not None and what == 'all':
                result=self._prepare_output(result={'backend_id':backend_id,'status':'all','count_localboot':0,'count_deploy':0})
            elif what is not None and what in ('deploy','localboot'):
                result=self._prepare_output(result={'backend_id':backend_id,'status':what,'count':0})
            return result

