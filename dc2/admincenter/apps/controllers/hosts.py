# -*- coding: utf-8 -*-
#
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
#

import sys
import json

try:
    import web
except ImportError as e:
    print("You need to install web.py")
    sys.exit(1)

try:
    from dc2.admincenter.globals import CSS_FILES
    from dc2.admincenter.globals import JS_LIBS
    from dc2.admincenter.globals import logger
except ImportError as e:
    print("You are missing the necessary DC2 modules")
    sys.exit(1)

try:
    from jinja2 import Environment, FileSystemLoader
except ImportError as e:
    print("You didn't install jinja2 templating engine")
    sys.exit(1)

try:
    from dc2.lib.web.pages import Page
    from dc2.lib.web.controllers import RESTController
    from dc2.lib.transports import get_xmlrpc_transport
    from dc2.lib.decorators import Logger
except ImportError as e:
    print("You are missing the necessary DC2 modules")
    print(e)
    sys.exit(1)

try:
    from settings import TEMPLATE_DIR
except ImportError as e:
    print("You don't have a settings file")
    print(e)
    sys.exit(1)

try:
    from dc2.admincenter.lib import backends
    from dc2.admincenter.lib.auth import needs_auth
    from dc2.admincenter.lib import interfacetypes
    from dc2.admincenter.lib import inettypes
except ImportError as e:
    print("There are dc2.admincenter modules missing")
    print(e)
    sys.exit(1)

try:
    from dc2.api.dc2.inventory import Servers
    from dc2.api.dc2.inventory import Macs
    from dc2.api.dc2.inventory import Ribs
    from dc2.api.dc2.inventory import Hosts
    from dc2.api.dc2.configuration import Environments
    from dc2.api.dc2.configuration import DefaultClasses
    from dc2.api.dc2.configuration import ClassTemplates
    from dc2.api.dc2.settings import BackendSettings
except ImportError as e:
    print('You did not install dc2.api')
    print(e)
    sys.exit(1)

tmpl_env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))


class HostController(RESTController):

    @Logger(logger=logger)
    def __init__(self, *args, **kwargs):
        super(HostController, self).__init__(*args, **kwargs)
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
            user_info[
                'is_dc2admin'] = self._request_context.session.is_dc2admin
            self._page.add_page_data({'user': user_info})
            self._page.add_page_data({'admin_is_link': True})
            self._fill_backends()
        self._page.set_page_value('controller_path', self._controller_path)

    @Logger(logger=logger)
    def _init_backend(self):
        params = web.input()
        self._backend_id = params.get('backend_id', None)
        self._page.add_page_data({'backend_id': self._backend_id})
        self._backend = backends.backend_get({'_id': self._backend_id})
        self._transport = get_xmlrpc_transport(
            self._backend['backend_url'], self._backend['is_kerberos'])
        self._servers = Servers(self._transport)
        self._macs = Macs(self._transport)
        self._ribs = Ribs(self._transport)
        self._hosts = Hosts(self._transport)
        self._backend_settings = BackendSettings(self._transport)
        self._environments = Environments(self._transport)
        self._defaultclasses = DefaultClasses(self._transport)
        self._classtemplates = ClassTemplates(self._transport)
        self._itypes_list = interfacetypes.itype_list()
        self._inet_list = inettypes.inet_list()

    @needs_auth
    @Logger(logger=logger)
    def _show(self, *args, **kwargs):
        verb = kwargs.get('verb', None)
        host_id = None
        self._init_backend()
        self._page.template_name = verb['template']
        self._page.set_action('show')
        self._page.set_page_value('show_button', True)
        request_data = verb.get('request_data', None)
        if request_data is not None:
            host_id = request_data.get('id', None)
        if host_id is not None:
            host = self._hosts.get(id=host_id)
            if host is not None:
                server = self._servers.get(id=host['server_id'])
                server_macs = self._macs.get(server_id=host['server_id'])
                classtemplates = self._classtemplates.list()
                backendsettings = self._backend_settings.get()
                self._page.set_title(
                    'Host %s.%s' % (host['hostname'], host['domainname']))
                self._page.add_page_data({
                    'classtemplates': classtemplates,
                    'itypes': self._itypes_list,
                    'inetlist': self._inet_list,
                    'server': server,
                    'server_macs': server_macs,
                    'host': host,
                    'backend_settings': backendsettings
                })
                result = self._prepare_output(verb['request_type'], verb[
                                              'request_content_type'], output={
                                              'content': self._page.render()})
                return result

    @needs_auth
    @Logger(logger=logger)
    def _edit(self, *args, **kwargs):
        verb = kwargs.get('verb', None)
        host_id = None
        self._init_backend()
        self._page.template_name = verb['template']
        self._page.set_action('edit')
        self._page.set_page_value('update_button', True)
        request_data = verb.get('request_data', None)
        if request_data is not None:
            host_id = request_data.get('id', None)
        if host_id is not None:
            host = self._hosts.get(id=host_id)
            host['hostclasses'] = sorted(host['hostclasses'])
            serverlist = self._servers.list()
            environmentlist = self._environments.list()
            defaultclasses = self._defaultclasses.list()
            classtemplates = self._classtemplates.list()
            server_macs = self._macs.get(server_id=host['server_id'])
            self._page.set_title('Edit Host %s.%s' %
                                 (host['hostname'], host['domainname']))
            self._page.add_page_data({
                'classtemplates': classtemplates,
                'itypes': self._itypes_list,
                'inetlist': self._inet_list,
                'entry_id': host['_id'],
                'serverlist': serverlist,
                'environlist': environmentlist,
                'server_macs': server_macs,
                'defaultclasses': defaultclasses,
                'host': host,
            })
            result = self._prepare_output(verb['request_type'], verb[
                                          'request_content_type'], output=
                                          {'content': self._page.render()})
            return result

    @needs_auth
    @Logger(logger=logger)
    def _update(self, *args, **kwargs):
        params = web.input()
        backend_id = params.get('backend_id', None)
        verb = kwargs.get('verb', None)
        self._init_backend()
        params = web.data()
        data = json.loads(params)['result']
        request_data = verb.get('request_data', None)
        host_id = None
        if request_data is not None:
            host_id = request_data['id']
        host = {}
        host['_id'] = host_id
        host['server_id'] = data['host']['server']
        host['hostname'] = data['host']['hostname']
        host['domainname'] = data['host']['domainname']
        host['environments'] = data['host']['environments']
        host['hostclasses'] = []
        for key in data['host']['hostclasses']:
            if key != 'new':
                host['hostclasses'].append(data['host']['hostclasses'][key])
        host['interfaces'] = []
        for key in data['host']['interfaces']:
            if key != 'new':
                host['interfaces'].append(data['host']['interfaces'][key])
        self._hosts.update(host=host)
        output_format = verb.get('request_output_format', None)
        if output_format.lower() == 'json':
            result = self._prepare_output(
                'json',
                verb['request_content_type'],
                verb['request_output_format'],
                {'redirect':
                    {'url': '{0}/{1}?backend_id={2}'.format(
                        self._controller_path,
                        host_id, backend_id), 'absolute': 'true'}})
        else:
            result = self._prepare_output(
                verb['request_type'],
                verb['request_content_type'], output={
                    'redirect': {'url': '{0}/{1}?backend_id={2}'.format(
                        self._controller_path, host_id, backend_id),
                        'absolute': 'true'}})
        return result

    @Logger(logger=logger)
    def _fill_backends(self):
        backend_list = backends.backend_list()
        self._page.add_page_data({'backendlist': backend_list})
