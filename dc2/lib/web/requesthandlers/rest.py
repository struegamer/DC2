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

try:
    import web
except ImportError,e:
    print "You need to install web.py"
    sys.exit(1)


class RESTRequestHandler(object):
    def __init__(self):
        self._controllers={}
        self._controller_module=None
        self._ctrl_instances={}
        self._import_controllers()
    
    def GET(self,path):
        return self._process_requests(path)

    def POST(self,path):
        return self._process_requests(path)

    def PUT(self,path):
        return self._process_requests(path)

    def DELETE(self,path):
        return self._process_requests(path)

    def _import_controllers(self):
        pass

    def _process_requests(self,path):
        web.debug('GET PATH: %s' % path)
        web.debug('REQUEST METHOD: %s' % web.ctx.method.upper())
        if self._controller_module is not None:
            for pat in reversed(sorted(self._controllers.iterkeys())):
                if path.startswith(pat):
                    if self._controllers.get(pat,None) is not None:
                        web.debug('MATCHED PATH : %s' % path)
                        ctrlclass=getattr(self._controller_module,self._controllers.get(pat,None))
                        self._ctrl_instances[pat]=ctrlclass(controller_path=pat,request_context=web.ctx)
                        web.debug(self._ctrl_instances)
                        result=self._ctrl_instances[pat].process(path)
                        web.debug(result)
                        output_format=result.get('format',None)
                        if output_format is not None:
                            if output_format=='html':
                                web.header('Content-Type',result.get('content-type','text/html; charset=utf-8'))
                                if result.get('output',None) is not None:
                                    return result.get('output','No output available')
                                if result.get('redirect',None) is not None:
                                    redir=result.get('redirect',None)
                                    raise web.seeother(redir['url'],absolute=redir['absolute'])
