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
    from settings import KERBEROS_AUTH_ENABLED
    from settings import FREEIPA_FORCE_ADD
except ImportError as e:
    print("You don't have a settings file")
    print(e)
    sys.exit(1)

try:
    from dc2.admincenter.lib import backends
    from dc2.admincenter.lib.auth import needs_auth
    from dc2.admincenter.lib import installmethods
except ImportError as e:
    print("There are dc2.admincenter modules missing")
    print(e)
    sys.exit(1)

try:
    from dc2.api.dc2.deployment import InstallState
    from dc2.api.dc2.settings import BackendSettings
    from dc2.api.dc2.inventory import Hosts
except ImportError as e:
    print('You did not install dc2.api')
    print(e)
    sys.exit(1)

tmpl_env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))


class InstallStateController(RESTController):
    @Logger(logger=logger)
    def __init__(self, *args, **kwargs):
        super(InstallStateController, self).__init__(*args, **kwargs)
        self._prepare_page()

    @Logger(logger=logger)
    def _prepare_page(self):
        self._page = Page(None, tmpl_env, self._request_context)
        self._page.set_cssfiles(CSS_FILES)
        self._page.set_jslibs(JS_LIBS)
        if 'authenticated' in self._request_context.session and self._request_context.session.authenticated:
            user_info = {}
            user_info['username'] = self._request_context.session.username
            user_info['realname'] = self._request_context.session.realname
            user_info['is_dc2admin'] = self._request_context.session.is_dc2admin
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
        self._transport = get_xmlrpc_transport(self._backend['backend_url'], self._backend['is_kerberos'])
        self._installstate = InstallState(self._transport)
        self._backend_settings = BackendSettings(self._transport)
        self._hosts = Hosts(self._transport)
        self._freeipa = None
        backendsettings = self._backend_settings.get()
        if backendsettings['IS_FREEIPA_ENABLED']:
            try:
                from dc2.api.dc2.addons.freeipa import Hosts as FreeIPA_Hosts
            except ImportError as e:
                print('You did not install dc2.api')
                print(e)
                sys.exit(1)
            self._freeipa = FreeIPA_Hosts(self._transport)

    @needs_auth
    @Logger(logger=logger)
    def _show(self, *args, **kwargs):
        verb = kwargs.get('verb', None)
        installstate_id = None
        self._init_backend()
        self._page.template_name = verb['template']
        self._page.set_action('show')
        self._page.set_page_value('show_button', True)
        request_data = verb.get('request_data', None)
        if request_data is not None:
            installstate_id = request_data.get('id', None)
        if installstate_id is not None:
            installstate = self._installstate.get(id=installstate_id)
            install_methods = installmethods.installmethod_list()
            backendsettings = self._backend_settings.get()

            self._page.set_title('Deployment State of %s' % installstate['hostname'])
            self._page.add_page_data({
                'entry_id': request_data['id'],
                'installstate': installstate,
                'installmethods': install_methods,
                'backend_settings': backendsettings
            })
            result = self._prepare_output(verb['request_type'], verb['request_content_type'], output={'content': self._page.render()})
            return result

    @needs_auth
    @Logger(logger=logger)
    def _edit(self, *args, **kwargs):
        verb = kwargs.get('verb', None)
        installstate_id = None
        self._init_backend()
        self._page.template_name = verb['template']
        self._page.set_action('edit')
        self._page.set_page_value('update_button', True)
        request_data = verb.get('request_data', None)
        if request_data is not None:
            installstate_id = request_data.get('id', None)
        if installstate_id is not None:
            installstate = self._installstate.get(id=installstate_id)
            self._page.set_title('Deployment State of %s' % installstate['hostname'])
            install_methods = installmethods.installmethod_list()
            backendsettings = self._backend_settings.get()
            self._page.add_page_data({
                'entry_id': request_data['id'],
                'installstate': installstate,
                'installmethods': install_methods,
                'backend_settings': backendsettings
            })
            result = self._prepare_output(verb['request_type'], verb['request_content_type'], output={'content': self._page.render()})
            return result

    @needs_auth
    @Logger(logger=logger)
    def _update(self, *args, **kwargs):
        verb = kwargs.get('verb', None)
        self._init_backend()
        result = json.loads(web.data())
        installstate = {}
        installstate = result['result']['installstate']
        installstate_rec = self._installstate.get(id=installstate['_id'])
        installstate_rec['status'] = installstate['status']
        self._installstate.update(rec=installstate_rec)
        backend_settings = self._backend_settings.get()
        if backend_settings['IS_FREEIPA_ENABLED'] and KERBEROS_AUTH_ENABLED:
            if installstate['status'] == 'deploy':
                host = self._hosts.get(id=installstate_rec['host_id'])
                if self._freeipa.check('{0}.{1}'.format(host['hostname'], host['domainname'])):
                    ipa_result = self._freeipa.delete('{0}.{1}'.format(host['hostname'], host['domainname']))
                ipa_info = {'description': 'Auto-Added from DC2',
                            'random': True}
                if FREEIPA_FORCE_ADD:
                    ipa_info['force'] = True
                ipa_result = self._freeipa.add('{0}.{1}'.format(host['hostname'], host['domainname']), ipa_info)
                print(ipa_result)
        result = self._prepare_output('json', verb['request_content_type'], 'json', {'redirect': {'url': '%s/%s?backend_id=%s' % (self._controller_path, installstate['_id'], self._backend_id), 'absolute': 'true'}})
        return result

    @Logger(logger=logger)
    def _fill_backends(self):
        backend_list = backends.backend_list()
        self._page.add_page_data({'backendlist': backend_list})
