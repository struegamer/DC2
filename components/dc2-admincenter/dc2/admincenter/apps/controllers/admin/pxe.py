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
    import web
except ImportError as e:
    print(e)
    sys.exit(1)

try:
    from dc2.admincenter.globals import logger
except ImportError as e:
    print(e)
    sys.exit(1)

try:
    from jinja2 import Environment, FileSystemLoader
except ImportError as e:
    print(e)
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
    from dc2.admincenter.lib import pxemethods
    from dc2.admincenter.lib.controllers import AdminController
    from dc2.admincenter.lib.auth import needs_auth
    from dc2.admincenter.lib.auth import needs_admin
except ImportError as e:
    print(e)
    sys.exit(1)

tmpl_env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))


class AdminPXEController(AdminController):
    CONTROLLER_IDENT = {'title': 'DC2 PXE Types',
                        'url': '/admin/pxe',
                        'show_in_menu': 'True'}

    @needs_auth
    @needs_admin
    @Logger(logger=logger)
    def _index(self, *args, **kwargs):
        verb = kwargs.get('verb', None)
        backend_list = backends.backend_list()
        pxe_list = pxemethods.pxe_list()
        page = self._prepare_page(verb)
        page.set_title('DC2 Admincenter - PXE Types - Index')
        page.add_page_data({
            'backendlist': backend_list,
            'pxelist': pxe_list
        })
        page.set_action('index')
        result = self._prepare_output(verb['request_type'],
                                      verb['request_content_type'],
                                      output={'content': page.render()})
        return result

    @needs_auth
    @needs_admin
    @Logger(logger=logger)
    def _new(self, *args, **kwargs):
        verb = kwargs.get('verb', None)
        backend_list = backends.backend_list()
        pxe = pxemethods.pxe_new()
        page = self._prepare_page(verb)
        page.set_title('DC2 Admincenter - PXE Types - New')
        page.add_page_data({
            'backendlist': backend_list,
            'pxe': pxe
        })
        page.set_action('new')
        result = self._prepare_output(verb['request_type'],
                                      verb['request_content_type'],
                                      output={'content': page.render()})
        return result

    @needs_auth
    @needs_admin
    @Logger(logger=logger)
    def _edit(self, *args, **kwargs):
        verb = kwargs.get('verb', None)
        backend_list = backends.backend_list()
        pxe = pxemethods.pxe_get({'_id': verb['request_data']['id']})
        page = self._prepare_page(verb)
        page.set_title('DC2 Admincenter - PXE Types - New')
        page.add_page_data({
            'backendlist': backend_list,
            'pxe': pxe
        })
        page.set_action('edit')
        result = self._prepare_output(verb['request_type'],
                                      verb['request_content_type'],
                                      output={'content': page.render()})
        return result

    @needs_auth
    @needs_admin
    @Logger(logger=logger)
    def _create(self, *args, **kwargs):
        verb = kwargs.get('verb', None)
        params = web.input()
        pxe = {}
        pxe['type'] = params.type
        pxe['name'] = params.name
        pxemethods.pxe_add(pxe)
        output_format = verb.get('request_output_format')
        if output_format.lower() == 'json':
            result = self._prepare_output('json',
                                          verb['request_content_type'],
                                          verb['request_output_format'],
                                          {'redirect':
                                           {'url': self._controller_path,
                                            'absolute': 'true'}})
        else:
            result = self._prepare_output(
                verb['request_type'],
                verb['request_content_type'],
                output={'redirect': {
                    'url': self._controller_path,
                    'absolute': 'true'}})
        return result

    @needs_auth
    @needs_admin
    @Logger(logger=logger)
    def _update(self, *args, **kwargs):
        verb = kwargs.get('verb', None)
        params = web.input()
        pxe = {}
        pxe['_id'] = params._id
        pxe['type'] = params.type
        pxe['name'] = params.name
        pxemethods.pxe_update(pxe)
        output_format = verb.get('request_output_format')
        if output_format.lower() == 'json':
            result = self._prepare_output('json',
                                          verb['request_content_type'],
                                          verb['request_output_format'],
                                          {'redirect':
                                           {'url': self._controller_path,
                                            'absolute': 'true'}})
        else:
            result = self._prepare_output(
                verb['request_type'],
                verb['request_content_type'],
                output={'redirect': {
                    'url': self._controller_path,
                    'absolute': 'true'}})
        return result

    @needs_auth
    @needs_admin
    @Logger(logger=logger)
    def _delete(self, *args, **kwargs):
        verb = kwargs.get('verb', None)
        request_data = verb.get('request_data', None)
        if (request_data is not None and
                request_data.get('id', None) is not None):
            pxe = {'_id': request_data.get('id', None)}
            pxemethods.pxe_delete(pxe)
        output_format = verb.get('request_output_format', None)
        if output_format is not None and output_format.lower() == 'json':
            result = self._prepare_output('json',
                                          verb['request_content_type'],
                                          verb['request_output_format'],
                                          {'redirect':
                                           {'url': self._controller_path,
                                            'absolute': 'true'}})
        else:
            result = self._prepare_output(
                verb['request_type'],
                verb['request_content_type'],
                output={'redirect': {
                    'url': self._controller_path,
                    'absolute': 'true'}})
        return result
