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

import sys
import os
import os.path

try:
    import web
except ImportError, e:
    print "You need to install web.py"
    sys.exit(1)

try:
    from dc2.admincenter.globals import connectionpool
    from dc2.admincenter.globals import CSS_FILES
    from dc2.admincenter.globals import JS_LIBS
    from dc2.admincenter.globals import logger
except ImportError, e:
    print "You are missing the necessary DC2 modules"
    sys.exit(1)

try:
    from jinja2 import Environment, FileSystemLoader
except ImportError, e:
    print "You didn't install jinja2 templating engine"
    sys.exit(1)

try:
    from dc2.lib.web.pages import Page
    from dc2.lib.web.csrf import csrf_protected
    from dc2.lib.auth.helpers import get_realname
    from dc2.lib.auth.helpers import check_membership_in_group
    from dc2.lib.web.controllers import RESTController
    from dc2.lib.decorators import Logger
except ImportError, e:
    print "You are missing the necessary DC2 modules"
    print e
    sys.exit(1)

try:
    from settings import TEMPLATE_DIR
    from settings import KERBEROS_AUTH_ENABLED
    from settings import GRP_NAME_DC2ADMINS
except ImportError, e:
    print "You don't have a settings file"
    print e
    sys.exit(1)

try:
    from dc2.admincenter.lib.auth import do_kinit
    from dc2.admincenter.lib.auth import KerberosAuthError
    from dc2.admincenter.lib import backends
except ImportError, e:
    print "There are dc2.admincenter modules missing"
    print e
    sys.exit(1)

tmpl_env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))

class MainController(RESTController):
    @Logger(logger=logger)
    def __init__(self, *args, **kwargs):
        super(MainController, self).__init__(self, *args, **kwargs)
        self._prepare_page()

    @Logger(logger=logger)
    def _prepare_page(self):
        self._page = Page(None, tmpl_env, self._request_context)
        self._page.set_cssfiles(CSS_FILES)
        self._page.set_jslibs(JS_LIBS)
        if ('authenticated' in self._request_context.session and
            self._request_context.session.authenticated):
            user_info = {}
            user_info['username'] = self._request_context.session.username
            user_info['realname'] = self._request_context.session.realname
            user_info['is_dc2admin'] = self._request_context.session.is_dc2admin
            self._page.add_page_data({'user':user_info})
            self._page.add_page_data({'admin_is_link':True})

    @Logger(logger=logger)
    def _index(self, *args, **kwargs):
        verb = kwargs.get('verb', None)
        self._page.template_name = verb['template']
        self._page.set_title('Dashboard')
        self._page.set_action('index')
        self._fill_backends()
        result = self._prepare_output(verb['request_type'], verb['request_content_type'],
                output={'content':self._page.render()})
        return result

    @Logger(logger=logger)
    def _fill_backends(self):
        backend_list = backends.backend_list()
        self._page.add_page_data({'backendlist':backend_list})
