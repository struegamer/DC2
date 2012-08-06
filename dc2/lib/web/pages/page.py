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
import types

try:
    import web
except ImportError,e:
    print "You didn't install web.py"
    print e
    sys.exit(1)

try:
    from dc2.lib.web.csrf import csrf_token
except ImportError,e:
    print "You didn't have dc2.lib installed"
    print e
    sys.exit(1)

class Page(object):
    def __init__(self,filename=None,environ=None,context=None):
        self._template_name=filename
        self._context=context
        self._tmpl_environ=environ
        self._pagedata={}
        self._page={}

    #
    # Properties
    #

    def _get_template_filename(self):
        return self._template_name
    def _set_template_filename(self,template_filename):
        self._template_name=template_filename
    def _del_template_filename(self):
        del self._template_name
    template_name=property(_get_template_filename,_set_template_filename,_del_template_filename,'Property: template_name')


    # 
    # public methods
    #
    def add_page_data(self,data=None):
        if data is not None and type(data) is types.DictType:
            if data.has_key('context') or data.has_key('page'):
                raise ValueError('page_data can\'t have another "context" key')
            self._pagedata.update(data)
            return True
        raise ValueError('Data is None or Data is not a dictionary')

    def set_jslibs(self,js_array=None):
        if js_array is not None and type(js_array) is types.ListType:
            self._page.update({'js_libs':js_array})
            return True
        raise ValueError('js_array is None or not an array')

    def set_cssfiles(self,css_array=None):
        if css_array is not None and type(css_array) is types.ListType:
            self._page.update({'css_files':css_array})
            return True
        raise ValueError('css_array is None or not an array')
    def set_page_value(self,key,value):
        if key in self._page:
            raise ValueError('key "%s" already in self._page')
        self._page[key]=value

    def set_title(self,title=''):
        self._page['title']=title
    def set_action(self,action=''):
        self._page['action']=action
    def set_index(self,index=''):
        self._page['index']=index
    def create_controller_url(self,action='',id=None,query_string=None):
        path_info=self._context.environ['PATH_INFO']
        if path_info[-1]=='/':
            path_info=path_info[:-1]
        query=None
        if query_string is not None and type(query_string) is types.ListType:
            query=''
            for item in query_string:
                web.debug(item)
                if type(item) is types.DictType:
                    for (key,value) in item.iteritems():
                        if query!='':
                            query+='&'
                        query+='%s=%s' % (key,value)
            
        if action=='index':
            if query is not None and query != '':
                return '%s?%s' % (path_info,query)
            return path_info
        if action=='new':
            if query is not None and query != '':
                return '%s/new?%s' % (path_info,query)
            return '%s/new' % path_info
        if action=='show':
            if id is not None:
                path='%s/%s' % (path_info,id)
                return '%s/%s' % (path_info,kwargs['id'])
            else:
                return path_info
        if action=='edit':
            if 'id' in kwargs:
                return '%s/%s/edit' % (path_info,kwargs['id'])
            else:
                return '%s/edit' % path_info

    def render(self):
        tmpl=self._tmpl_environ.get_template(self._template_name)
        self._page.update({'context':self._context})
        self._page.update({'sectoken':csrf_token})
        self._pagedata.update({'page':self._page})
        funcs={}
        funcs['create_controller_url']=self.create_controller_url
        self._pagedata.update({'controller':funcs})
        web.header('Content-Type','text/html; charset=utf-8')
        return  tmpl.render(self._pagedata)

    

