# -*- coding: utf-8 -*-
###############################################################################
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
###############################################################################

import sys
import os
import os.path
import re

try:
    import web
except ImportError, e:
    print "You need to install web.py"
    sys.exit(1)


class RequestHandler(object):
    def __init__(self):
        self._controllers = {}
        self._controller_modules = None
        self._ctrl_instances = {}
        self._import_controllers()
        self._init_controllers()

    def GET(self, path):
        result = self._process_requests(path)
        return result

    def POST(self, path):
        return self._process_requests(path)

    def PUT(self, path):
        return self._process_requests(path)

    def DELETE(self, path):
        return self._process_requests(path)

    def _import_controllers(self):
        pass

    def _init_controllers(self):
        for key in self._controller_modules.keys():
            if self._ctrl_instances.get(key, None) is None:
                ctrlclass = getattr(self._controller_modules.get(key, None)['module'], self._controller_modules.get(key, None)['classname'])
                self._ctrl_instances[key] = ctrlclass(controller_path=key, request_context=web.ctx)

    def _process_requests(self, path):
        if self._controller_modules is not None:
            for pat in reversed(sorted(self._controllers.iterkeys())):
                if path.startswith(pat):
                    self._ctrl_instances[pat].set_context(web.ctx)
                    result = self._ctrl_instances[pat].process(path)
                    output_format = result.get('format', None)
                    if output_format is None:
                        output_format = 'html'
                    if output_format.lower() == 'html':
                        web.header('Content-Type', result.get('content-type', 'text/html; charset=utf-8'))
                        output = result.get('output', None)
                        if output is not None:
                            if output.get('content', None) is not None:
                                return output.get('content', 'No output available')
                            if output.get('redirect', None) is not None:
                                redir = output.get('redirect', None)
                                raise web.seeother(redir['url'], absolute=redir['absolute'])
                    if output_format.lower() == 'json':
                        web.header('Content-Type', result.get('content-type', 'text/html; charset=utf-8'))
                        output = result.get('output', None)
                        if output is not None:
                            return output

