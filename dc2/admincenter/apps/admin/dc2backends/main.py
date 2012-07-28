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
import re

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
    from dc2.admincenter.lib import backends
except ImportError,e:
    print "There are dc2.admincenter modules missing"
    print e
    sys.exit(1)


tmpl_env=Environment(loader=FileSystemLoader(TEMPLATE_DIR))

class ActionREST(object):
    def __init__(self):
        self._std_template_path=self._get_std_template_path()
        self._page=None
        self._initialize_verbs()
    
    # 
    # Virtual Method
    # Needs to be overwritten
    #
    def _prepare_page(self,template,action):
        self._page=Page(template,tmpl_env,web.ctx)
        self._page.set_action(action)

    # 
    # Virtual Method
    # Override it every time you create a module
    def _get_std_template_path(self):
        return '/'

    def _initialize_verbs(self):
        self._verb_methods={
            'GET':[
                {'urlre':'^[/]{0,1}$','action':self.index,'action_name':'index','template':'%s/index.tmpl' % self._std_template_path}, # index
                {'urlre':'^/new$','action':self.new,'action_name':'new','template':'%s/new.tmpl' % self._std_template_path}, # new
                {'urlre':'^/(?P<id>[a-z,0-9,\-,\.A-Z]+)$','action':self.show,'action_name':'show','template':'%s/show.tmpl' % self._std_template_path}, # show
                {'urlre':'^/(?P<id>[a-z,0-9,\-,\.A-Z]+)/edit$','action':self.edit,'action_name':'edit','template':'%s/edit.tmpl' % self._std_template_path}, # edit
            ],
            'POST':[
                {'urlre':'^[/]{0,1}$','action':self.create,'action_name':'create','redirect':'/'}, # create
            ],
            'PUT':[
                {'urlre':'^/(.*)$','redirect':'/'}, # update
            ],
            'DELETE':[
                {'urlre':'^(.*)$','redirect':'/'},
            ]
        }


    def GET(self,path):
        web.debug('GET PATH: %s' % path)
        verbs=self._verb_methods['GET']
        for verb in verbs:
            found=re.search(verb['urlre'],path)
            if found is not None:
                web.debug('match rule: %s' % verb['urlre'])
                self._prepare_page(verb['template'],verb['action_name'])
                return verb['action'](**found.groupdict())

    def POST(self,path):
        web.debug('POST PATH: %s' % path)
        verbs=self._verb_methods['POST']
        for verb in verbs:
            if re.search(verb['urlre'],path) is not None:
                web.debug('POST match rule: %s' % verb['urlre'])
                redirect,absolute=verb['action']()
                raise web.seeother(redirect,absolute)
                    
                

    def PUT(self,path):
        pass
    def DELETE(self,path):
        pass

    def index(self,*args,**kwargs):
        pass
    def new(self,*args,**kwargs):
        pass
    def show(self,*args,**kwargs):
        pass
    def edit(self,*args,**kwargs):
        pass
    def create(self,*args,**kwargs):
        pass
    def update(self,*args,**kwargs):
        pass
    def delete(self,*args,**kwargs):
        pass

class ActionIndex(ActionREST):

    def _get_std_template_path(self):
        return 'admin/backends'

    def _prepare_page(self, template, action):
        super(ActionIndex,self)._prepare_page(template,action)
        self._page.set_cssfiles(CSS_FILES)
        self._page.set_jslibs(JS_LIBS)
        if 'authenticated' in web.ctx.session and web.ctx.session.authenticated:
            user_info={}
            user_info['username']=web.ctx.session.username
            user_info['realname']=web.ctx.session.realname
            user_info['is_dc2admin']=web.ctx.session.is_dc2admin
            self._page.add_page_data({'user':user_info})
        self._create_menu()

    def _create_menu(self):
        if len(ADMIN_MODULES)>0:
            self._page.add_page_data({'admin_menu':ADMIN_MODULES})

    def index(self,*args,**kwargs):
        self._page.set_title('DC2 Admincenter - Backends - Index')
        backend_list=backends.backend_list()
        self._page.add_page_data({'backends':backend_list})
        return self._page.render()

    def new(self,*args,**kwargs):
        self._page.set_title('DC2 Admincenter - Backends - Add')
        backend=backends.backend_new()
        self._page.add_page_data({'backend':backend})
        return self._page.render()

    def create(self,*args,**kwargs):
        backend=web.input()
        backend_id=backends.backend_add({
            'title':backend.title,
            'backend_url':backend.backend_url,
            'location':backend.location
        })
        return ('/',False)

    def edit(self,*args,**kwargs):
        backend=backends.backend_get({'_id':kwargs.get('id',None)})
        self._page.add_page_data({'backend':backend})
        return self._page.render()

#    def GET(self,path):
#        if web.ctx.session.is_dc2admin:
#            if path == '/' or path == '':
#                backend_list=backends.backend_list()
#                self._page.add_page_data({'backends':backend_list})
#                return self._page.render()
#            elif path == '/add':
#                pass
#        else:
#            web.ctx.session.error=True
#            web.ctx.session.errorno=1020
#            web.ctx.session.errormsg='You are not a DC2 Admin'
#            raise web.seeother('/',absolute=True)

class ActionDelete(object):
    def DELETE(self,data):
       # print data
        if web.ctx.session.is_dc2admin:
           raise web.seeother('delete')


class ActionAdd(object):
    def __init__(self):
        self._page=Page('admin/backends/add.tmpl',tmpl_env,web.ctx)
        self._page.set_title('DC2-AdminCenter - Backends - Add')
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
            raise web.seeother('/',absolute=True)

    @csrf_protected
    def POST(self):
        if web.ctx.session.is_dc2admin:
            params=web.input()
            backend={}
            backend['title']=params.title
            backend['backend_url']=params.backend_url
            backend['location']=params.location
            if backends.backend_add(backend) is not None:
                raise web.seeother('/')


    
