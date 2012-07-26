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
except ImportError,e:
    print "You are missing the necessary DC2 modules"
    print e
    sys.exit(1)

try:
    from settings import TEMPLATE_DIR
    from settings import KERBEROS_AUTH_ENABLED
except ImportError,e:
    print "You don't have a settings file"
    print e
    sys.exit(1)

try:
    from dc2.admincenter.lib.auth import do_kinit
    from dc2.admincenter.lib.auth import KerberosAuthError
except ImportError,e:
    print "There are dc2.admincenter modules missing"
    print e
    sys.exit(1)

tmpl_env=Environment(loader=FileSystemLoader(TEMPLATE_DIR))

class Index(object):
    def __init__(self):
        self._page=Page('admin/index.tmpl',tmpl_env,web.ctx)
        self._page.set_title('DC2-AdminCenter - Administration')
        self._page.set_cssfiles(CSS_FILES)
        self._page.set_jslibs(JS_LIBS)
        if 'authenticated' in web.ctx.session and web.ctx.session.authenticated:
            user_info={}
            user_info['username']=web.ctx.session.username
            user_info['realname']=web.ctx.session.realname
            user_info['is_dc2admin']=web.ctx.session.is_dc2admin
            self._page.add_page_data({'user':user_info})
        self.create_menu()
    def create_menu(self):
        if len(ADMIN_MODULES)>0:
            self._page.add_page_data({'admin_menu':ADMIN_MODULES})

    def GET(self):
        if web.ctx.session.is_dc2admin:
            return self._page.render()
        else:
            web.ctx.session.error=True
            web.ctx.session.errorno=1020
            web.ctx.session.errormsg='You are not a DC2 Admin'
            raise web.seeother('/')
