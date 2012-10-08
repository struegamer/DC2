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

class AdminInterfaceTypesController(AdminController):
    CONTROLLER_IDENT={'title':'DC2 Interface Types','url':'/admin/ifacetypes','show_in_menu':'True'}

    @needs_auth
    @needs_admin
    @Logger()
    def _index(self, *args, **kwargs):
        verb=kwargs.get('verb',None)
        backend_list=backends.backend_list()
        ifacetype_list=interfacetypes.itype_list()
        page=self._prepare_page(verb)
        page.set_title('DC2 Admincenter - Interfacetypes - Index')
        page.add_page_data({'backendlist':backend_list, 'iface_list':ifacetype_list})
        page.set_action('index')
        result=self._prepare_output(verb['request_type'],verb['request_content_type'], output={'content':page.render()})
        return result

    @needs_auth
    @needs_admin
    @Logger()
    def _new(self, *args, **kwargs):
        verb=kwargs.get('verb',None)
        backend_list=backends.backend_list()
        iface=interfacetypes.itype_new()
        page=self._prepare_page(verb)
        page.set_title('DC2 Admincenter - Interfacetypes - New')
        page.add_page_data({'backendlist':backend_list, 'iface':iface})
        page.set_action('new')
        result=self._prepare_output(verb['request_type'],verb['request_content_type'], output={'content':page.render()})
        return result


    @needs_auth
    @needs_admin
    @Logger()
    def _edit(self, *args, **kwargs):
        verb=kwargs.get('verb',None)
        backend_list=backends.backend_list()
        iface=interfacetypes.itype_get({'_id':verb['request_data']['id']})
        page=self._prepare_page(verb)
        page.set_title('DC2 Admincenter - Interfacetypes - Edit')
        page.add_page_data({'backendlist':backend_list, 'iface':iface})
        page.set_action('edit')
        result=self._prepare_output(verb['request_type'],verb['request_content_type'], output={'content':page.render()})
        return result


    @needs_auth
    @needs_admin
    @Logger()
    def _create(self, *args, **kwargs):
        verb=kwargs.get('verb',None)
        params=web.input()
        iface={}
        iface['type']=params.type
        iface['desc']=params.desc
        interfacetypes.itype_add(iface)
        output_format=verb.get('request_output_format')
        if output_format.lower()=='json':
            result=self._prepare_output('json',verb['request_content_type'],verb['request_output_format'],{'redirect':{'url':self._controller_path,'absolute':'true'}})
        else:
            result=self._prepare_output(verb['request_type'],verb['request_content_type'],output={'redirect':{'url':self._controller_path,'absolute':'true'}})
        return result

    @needs_auth
    @needs_admin
    @Logger()
    def _update(self, *args, **kwargs):
        verb=kwargs.get('verb',None)
        params=web.input()
        iface={}
        iface['_id']=params._id
        iface['type']=params.type
        iface['desc']=params.desc
        interfacetypes.itype_update(iface)
        output_format=verb.get('request_output_format')
        if output_format.lower()=='json':
            result=self._prepare_output('json',verb['request_content_type'],verb['request_output_format'],{'redirect':{'url':self._controller_path,'absolute':'true'}})
        else:
            result=self._prepare_output(verb['request_type'],verb['request_content_type'],output={'redirect':{'url':self._controller_path,'absolute':'true'}})
        return result

       
    @needs_auth
    @needs_admin
    @Logger()
    def _delete(self, *args, **kwargs):
        verb=kwargs.get('verb',None)
        request_data=verb.get('request_data',None)
        if request_data is not None and request_data.get('id',None) is not None:
            iface={'_id':request_data.get('id',None)}
            interfacetypes.itype_delete(iface)
        output_format=verb.get('request_output_format',None)
        if output_format is not None and output_format.lower()=='json':
            result=self._prepare_output('json',verb['request_content_type'],verb['request_output_format'],{'redirect':{'url':self._controller_path,'absolute':'true'}})
        else:
            result=self._prepare_output(verb['request_type'],verb['request_content_type'],output={'redirect':{'url':self._controller_path,'absolute':'true'}})
        return result
