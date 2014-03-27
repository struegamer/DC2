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
import json
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
    from dc2.lib.transports import get_xmlrpc_transport
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

try:
    from dc2.api.dc2.configuration import SysGroups
except ImportError as e:
    print(e)
    sys.exit(1)

tmpl_env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))


class BackendSysGroupController(AdminController):
    CONTROLLER_IDENT = {'title': 'DC2 Backends System Groups',
                        'url': '/admin/backends/sysgroups',
                        'show_in_menu': 'False'}

    def _init_backend(self, backend):
        self._transport = get_xmlrpc_transport(backend['backend_url'],
                                               backend['is_kerberos'])
        self._sysgroups = SysGroups(self._transport)

    @needs_auth
    @needs_admin
    @Logger(logger=logger)
    def _index(self, *args, **kwargs):
        params = web.input()
        verb = kwargs.get('verb', None)
        page = self._prepare_page(verb)
        backend_list = backends.backend_list()
        backend_id = params.get('backend_id', None)
        backend = backends.backend_get({'_id': backend_id})
        self._init_backend(backend)
        page.set_title('DC2 Admincenter - Backends - System Groups - Index')
        page.add_page_data({
            'backendlist': backend_list,
            'backend_id': backend_id,
            'backend_sysgroups': self._sysgroups.list()
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
        params = web.input()
        verb = kwargs.get('verb', None)
        page = self._prepare_page(verb)
        backendlist = backends.backend_list()
        backend_id = params.get('backend_id', None)
        backend = backends.backend_get({'_id': backend_id})
        self._init_backend(backend)
        group = self._sysgroups.new()
        page.set_title('DC2 Admincenter - Backends - System Groups - Add')
        page.add_page_data({
            'backendlist': backendlist,
            'backend_id': backend_id,
            'group': group
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
        params = web.input()
        verb = kwargs.get('verb', None)
        page = self._prepare_page(verb)
        backendlist = backends.backend_list()
        backend_id = params.get('backend_id', None)
        backend = backends.backend_get({'_id': backend_id})
        self._init_backend(backend)
        group = self._sysgroups.get(id=verb['request_data']['id'])
        page.set_title('DC2 Admincenter - Backends - System Groups - Edit')
        page.add_page_data({
            'backendlist': backendlist,
            'backend_id': backend_id,
            'group': group
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
        params = web.input()
        verb = kwargs.get('verb', None)
        backend_id = params.get('backend_id', None)
        backend = backends.backend_get({'_id': backend_id})
        self._init_backend(backend)
        result = json.loads(web.data())
        rec = {}
        rec = result['result']['group']
        rec['gid'] = str(rec['gid'])
        if 'is_admin_group' in rec:
            rec['is_admin_group'] = str(rec['is_admin_group'])
        else:
            rec['is_admin_group'] = '0'
        if 'is_system_group' in rec:
            rec['is_system_group'] = str(rec['is_system_group'])
        else:
            rec['is_system_group'] = '0'
        self._sysgroups.add(group=rec)
        output_format = verb.get('request_output_format')
        if output_format.lower() == 'json':
            result = self._prepare_output(
                'json',
                verb['request_content_type'],
                verb['request_output_format'],
                {'redirect': {
                    'url': '{0}?backend_id={1}'.format(
                        self._controller_path,
                        backend_id),
                    'absolute': 'true'}})
        else:
            result = self._prepare_output(
                verb['request_type'],
                verb['request_content_type'],
                output={'redirect': {
                    'url': '{0}?backend_id={1}'.format(
                        self._controller_path,
                        backend_id),
                    'absolute': 'true'}})
        return result

    @needs_auth
    @needs_admin
    @Logger(logger=logger)
    def _update(self, *args, **kwargs):
        params = web.input()
        verb = kwargs.get('verb', None)
        backend_id = params.get('backend_id', None)
        backend = backends.backend_get({'_id': backend_id})
        self._init_backend(backend)
        result = json.loads(web.data())
        rec = {}
        rec = result['result']['group']
        rec['gid'] = str(rec['gid'])
        if 'is_admin_group' in rec:
            rec['is_admin_group'] = str(rec['is_admin_group'])
        else:
            rec['is_admin_group'] = '0'
        if 'is_system_group' in rec:
            rec['is_system_group'] = str(rec['is_system_group'])
        else:
            rec['is_system_group'] = '0'

        self._sysgroups.update(group=rec)
        output_format = verb.get('request_output_format')
        if output_format.lower() == 'json':
            result = self._prepare_output(
                'json',
                verb['request_content_type'],
                verb['request_output_format'],
                {'redirect': {
                    'url': '{0}?backend_id={1}'.format(
                        self._controller_path,
                        backend_id),
                    'absolute': 'true'}})
        else:
            result = self._prepare_output(
                verb['request_type'],
                verb['request_content_type'],
                output={'redirect': {
                    'url': '{0}?backend_id={1}'.format(
                        self._controller_path,
                        backend_id),
                    'absolute': 'true'}})
        return result

    @needs_auth
    @needs_admin
    @Logger(logger=logger)
    def _delete(self, *args, **kwargs):
        params = web.input()
        verb = kwargs.get('verb', None)
        request_data = verb.get('request_data', None)
        backend_id = params.get('backend_id', None)
        backend = backends.backend_get({'_id': backend_id})
        self._init_backend(backend)
        if (request_data is not None and
                request_data.get('id', None) is not None):
            self._sysgroups.delete(id=request_data.get('id', None))
        output_format = verb.get('request_output_format', None)
        if output_format is not None and output_format.lower() == 'json':
            result = self._prepare_output(
                'json',
                verb['request_content_type'],
                verb['request_output_format'],
                {'redirect': {
                    'url': '{0}?backend_id={1}'.format(
                        self._controller_path,
                        backend_id),
                    'absolute': 'true'}})
        else:
            result = self._prepare_output(
                verb['request_type'],
                verb['request_content_type'],
                output={'redirect': {
                    'url': '{0}?backend_id={1}'.format(
                        self._controller_path,
                        backend_id),
                    'absolute': 'true'}})
        return result
