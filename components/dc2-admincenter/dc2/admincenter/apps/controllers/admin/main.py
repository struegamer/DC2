# -*- coding: utf-8 -*-
#
# (DC)² - DataCenter Deployment Control
# Copyright (C) 2010, 2011, 2012, 2013, 2014 Stephan Adig <sh@sourcecode.de>
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#

import sys

try:
    from dc2.admincenter.globals import logger
except ImportError as e:
    print(e)
    sys.exit(1)

try:
    from jinja2 import Environment, FileSystemLoader
except ImportError as e:
    print(e)
    print "You didn't install jinja2 templating engine"
    sys.exit(1)

try:
    from dc2.lib.decorators import Logger
except ImportError as e:
    print(e)
    sys.exit(1)

try:
    from settings import TEMPLATE_DIR
except ImportError as e:
    print(e)
    sys.exit(1)

try:
    from dc2.admincenter.lib import backends
    from dc2.admincenter.lib.controllers import AdminController
    from dc2.admincenter.lib.auth import needs_auth
    from dc2.admincenter.lib.auth import needs_admin
except ImportError as e:
    print(e)
    sys.exit(1)

tmpl_env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))


class MainAdminController(AdminController):
    CONTROLLER_IDENT = {'title': 'Admin Home',
                        'url': '/admin', 'show_in_menu': 'True'}

    @needs_auth
    @needs_admin
    @Logger(logger=logger)
    def _index(self, *args, **kwargs):
        verb = kwargs.get('verb', None)
        page = self._prepare_page(verb)
        backend_list = backends.backend_list()
        page.set_title('Admin - Index')
        page.add_page_data({'backendlist': backend_list})
        page.set_action('index')
        result = self._prepare_output(verb['request_type'],
                                      verb['request_content_type'],
                                      output={'content': page.render()})
        return result
