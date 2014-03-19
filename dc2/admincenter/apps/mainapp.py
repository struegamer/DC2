# -*- coding: utf-8 -*-
#################################################################################
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

try:
    from dc2.lib.web.requesthandlers import RequestHandler
    from dc2.lib.decorators import Logger
except ImportError,e:
    print 'errors in dc2'
    print e
    sys.exit(1)

try:
    from dc2.admincenter.globals import logger
except ImportError,e:
    print 'Error: %s in File: %s' % (e, __file__)
    sys.exit(1)

try:
    from settings import CONTROLLER_MAPPINGS
except ImportError,e:
    print 'you do not have a settings file bla'
    print e
    sys.exit(1)

class MainAppHandler(RequestHandler):
    @Logger(logger=logger)
    def _import_controllers(self):
        super(MainAppHandler,self)._import_controllers()
        self._controller_modules={}
        for mod in CONTROLLER_MAPPINGS.keys():
            temp_import_path='dc2.admincenter.apps.controllers.%s' % CONTROLLER_MAPPINGS[mod]
            classname=temp_import_path.split('.')[-1]
            import_path='.'.join(temp_import_path.split('.')[:-1])
            module=__import__(import_path,globals(),locals(),classname)
            self._controller_modules[mod]={'module':module,'classname':classname}
        self._controllers=CONTROLLER_MAPPINGS
