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

try:
    import web
except ImportError,e:
    print "You need to install web.py"
    sys.exit(1)

try:
    from dc2.admincenter.globals import connectionpool
    from dc2.admincenter.globals import CSS_FILES
    from dc2.admincenter.globals import JS_LIBS
    from dc2.admincenter.globals import ADMIN_MODULES
except ImportError,e:
    print "You are missing the necessary DC2 modules"
    sys.exit(1)

try:
    from jinja2 import Environment, FileSystemLoader
except ImportError,e:
    print "You didn't install jinja2 templating engine"
    sys.exit(1)

try:
    from dc2.lib.web.pages import Page
    from dc2.lib.web.csrf import csrf_protected
    from dc2.lib.auth.helpers import get_realname
    from dc2.lib.auth.helpers import check_membership_in_group
    from dc2.lib.web.controllers import RESTController
    from dc2.lib.logging import Logger
except ImportError,e:
    print "You are missing the necessary DC2 modules"
    print e
    sys.exit(1)

try:
    from settings import TEMPLATE_DIR
    from settings import KERBEROS_AUTH_ENABLED
    from settings import GRP_NAME_DC2ADMINS
except ImportError,e:
    print "You don't have a settings file"
    print e
    sys.exit(1)

try:
    from dc2.admincenter.lib import backends
except ImportError,e:
    print "There are dc2.admincenter modules missing"
    print e
    sys.exit(1)

tmpl_env=Environment(loader=FileSystemLoader(TEMPLATE_DIR))

class AdminController(RESTController):
    CONTROLLER_IDENT={}
    def __init__(self, *args, **kwargs):
        super(AdminController,self).__init__(*args, **kwargs)
        self._add_to_admin_modules()
    @Logger
    def _add_to_admin_modules(self):
        if self.CONTROLLER_IDENT not in ADMIN_MODULES:
            ADMIN_MODULES.append(self.CONTROLLER_IDENT)

    def _prepare_page(self,verb):
        page=Page(verb['template'],tmpl_env,self._request_context)
        page.set_cssfiles(CSS_FILES)
        page.set_jslibs(JS_LIBS)
        page.set_index(self._controller_path)
        if 'authenticated' in self._request_context.session and self._request_context.session.authenticated:
            user_info={}
            user_info['username']=self._request_context.session.username
            user_info['realname']=self._request_context.session.realname
            user_info['is_dc2admin']=self._request_context.session.is_dc2admin
            page.add_page_data({'user':user_info})
        page.set_page_value('controller_path',self._controller_path)
        page=self._create_menu(page)
        return page

    def _create_menu(self,page):
        if len(ADMIN_MODULES)>0:
            page.add_page_data({'admin_menu':ADMIN_MODULES})
        return page



