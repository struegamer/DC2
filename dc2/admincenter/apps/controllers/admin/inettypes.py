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
    from dc2.lib.web.helpers import convert_values
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
    from dc2.admincenter.lib import ribs
    from dc2.admincenter.lib import interfacetypes
    from dc2.admincenter.lib.controllers import AdminController
    from dc2.admincenter.lib.auth import needs_auth
    from dc2.admincenter.lib.auth import needs_admin
except ImportError,e:
    print "There are dc2.admincenter modules missing"
    print e
    sys.exit(1)

tmpl_env=Environment(loader=FileSystemLoader(TEMPLATE_DIR))

class AdminInetTypesController(AdminController):
    CONTROLLER_IDENT={'title':'DC² Inet Types','url':'/admin/inettypes'}

    @Logger
    @needs_auth
    @needs_admin
    def _index(self, *args, **kwargs):
        pass

    @Logger
    @needs_auth
    @needs_admin
    def _new(self, *args, **kwargs):
        pass

    @Logger
    @needs_auth
    @needs_admin
    def _edit(self, *args, **kwargs):
        pass

    @Logger
    @needs_auth
    @needs_admin
    def _create(self, *args, **kwargs):
        pass

    @Logger
    @needs_auth
    @needs_admin
    def _update(self, *args, **kwargs):
        pass

    @Logger
    @needs_auth
    @needs_admin
    def _delete(self, *args, **kwargs):
        pass

