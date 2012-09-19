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
import json

try:
    import web
except ImportError,e:
    print "You need to install web.py"
    sys.exit(1)

try:
    from dc2.admincenter.globals import connectionpool
    from dc2.admincenter.globals import CSS_FILES
    from dc2.admincenter.globals import JS_LIBS
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
    from dc2.lib.transports import get_xmlrpc_transport
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
    from dc2.admincenter.lib.auth import do_kinit
    from dc2.admincenter.lib.auth import KerberosAuthError
    from dc2.admincenter.lib import backends
    from dc2.admincenter.lib.auth import needs_auth
    from dc2.admincenter.lib import ribs
except ImportError,e:
    print "There are dc2.admincenter modules missing"
    print e
    sys.exit(1)

try:
    from dc2.api.dc2.inventory import Servers
    from dc2.api.dc2.inventory import Macs
    from dc2.api.dc2.inventory import Ribs
    from dc2.api.dc2.inventory import Hosts
except ImportError,e:
    print 'You did not install dc2.api'
    print e
    sys.exit(1)

tmpl_env=Environment(loader=FileSystemLoader(TEMPLATE_DIR))

class ServerController(RESTController):
    def __init__(self, *args, **kwargs):
        super(ServerController,self).__init__(*args, **kwargs)
        self._prepare_page()
    def _prepare_page(self):
        self._page=Page(None,tmpl_env,self._request_context)
        self._page.set_cssfiles(CSS_FILES)
        self._page.set_jslibs(JS_LIBS)
        if 'authenticated' in self._request_context.session and self._request_context.session.authenticated:
            user_info={}
            user_info['username']=self._request_context.session.username
            user_info['realname']=self._request_context.session.realname
            user_info['is_dc2admin']=self._request_context.session.is_dc2admin
            self._page.add_page_data({'user':user_info})
            self._page.add_page_data({'admin_is_link':True})
            self._fill_backends()
        self._page.set_page_value('controller_path',self._controller_path)
    def _init_backend(self):
        params=web.input()
        self._backend_id=params.get('backend_id',None)
        self._page.add_page_data({'backend_id':self._backend_id})
        self._backend=backends.backend_get({'_id':self._backend_id})
        self._transport=get_xmlrpc_transport(self._backend['backend_url'],self._backend['is_kerberos'])
        self._servers=Servers(self._transport)
        self._macs=Macs(self._transport)
        self._ribs=Ribs(self._transport)
        self._hosts=Hosts(self._transport)

    @Logger
    @needs_auth
    def _show(self, *args, **kwargs):
        verb=kwargs.get('verb',None)
        server_id=None
        self._init_backend()
        self._page.template_name=verb['template']
        self._page.set_action('show')
        self._page.set_page_value('show_button',True)
        request_data=verb.get('request_data',None)
        if request_data is not None:
            server_id=request_data.get('id',None)
        if server_id is not None:
            server=self._servers.get(id=server_id)
            macs=self._macs.get(server_id=server_id)
            rib=self._ribs.get(server_id=server_id)
            host=self._hosts.get(server_id=server_id)
            rib_def=ribs.rib_list()
            self._page.set_title('Server %s (%s - %s)' % (server['serial_no'],server['manufacturer'],server['product_name']))
            self._page.add_page_data(
                    {
                        'server':server,
                        'macs':macs,
                        'ribs':rib,
                        'host':host,
                        'ribdef':rib_def
                    })
            result=self._prepare_output(verb['request_type'],verb['request_content_type'],
                output={'content':self._page.render()})
            return result

    @Logger
    @needs_auth
    def _edit(self, *args, **kwargs):
        verb=kwargs.get('verb',None)
        self._init_backend()
        self._page.template_name=verb['template']
        self._page.set_action('edit')
        self._page.set_page_value('update_button',True)
        request_data=verb.get('request_data',None)
        server_id=None
        if request_data is not None:
            server_id=request_data.get('id',None)
        if server_id is not None:
            server=self._servers.get(id=server_id)
            macs=self._macs.get(server_id=server_id)
            rib=self._ribs.get(server_id=server_id)
            rib_def=ribs.rib_list()

            self._page.set_title('Edit Server %s (%s - %s)' % (server['serial_no'],server['manufacturer'],server['product_name']))
            self._page.add_page_data(
                    {
                        'entry_id':server['_id'],
                        'server':server,
                        'macs':macs,
                        'ribs':rib,
                        'ribdef':rib_def,
                    })
            result=self._prepare_output(verb['request_type'],verb['request_content_type'],
                output={'content':self._page.render()})
            return result

    @Logger
    @needs_auth
    @csrf_protected
    def _update(self, *args, **kwargs):
        verb=kwargs.get('verb',None)
        self._init_backend()
        params=web.data()
        data=json.loads(params)['result']
        server={}
        server['_id']=data['server_id'].strip()
        server['uuid']=data['uuid'].strip()
        server['serial_no']=data['serial_no'].strip()
        server['manufacturer']=data['manufacturer'].strip()
        server['product_name']=data['product_name'].strip()
        server['location']=data['location'].strip()
        server['asset_tags']=data['asset_tags'].strip()
        self._servers.update(server=server)
        for key in data['mac']:
            mac={}
            if key != 'new':
                if key.find('new')==-1 and key != 'new':
                    mac['_id']=key.strip()
                if data['mac'][key]['mac_addr'] != '' and data['mac'][key]['device_name'] != '':
                    mac['server_id']=data['server_id'].strip()
                    mac['mac_addr']=data['mac'][key]['mac_addr'].strip()
                    mac['device_name']=data['mac'][key]['device_name'].strip()
                if '_id' in mac:
                    self._macs.update(mac=mac)
                else:
                    self._macs.add(mac=mac)
        for key in data['rib']:
            rib={}
            if key != 'new':
                if key.find('new')==-1:
                    rib['_id']=key.strip()
                if data['rib'][key]['remote_ip'] != '':
                    rib['server_id']=data['server_id'].strip()
                    rib['remote_type']=data['rib'][key]['remote_type'].strip()
                    rib['remote_ip']=data['rib'][key]['remote_ip'].strip()
                if '_id' in rib:
                    self._ribs.update(rib=rib)
                else:
                    self._ribs.add(rib=rib)
        result=self._prepare_output('json',verb['request_content_type'],'json',{'redirect':{'url':'%s/%s?backend_id=%s' % (self._controller_path,data['server_id'],self._backend_id),'absolute':'true'}})
        return result

    def _fill_backends(self):
        backend_list=backends.backend_list()
        self._page.add_page_data({'backendlist':backend_list})
