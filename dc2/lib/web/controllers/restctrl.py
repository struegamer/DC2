# -*- coding: utf-8 -*-
###############################################################################
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
###############################################################################

import sys
import os
import os.path
import re
import types
import json

try:
    import web
except ImportError, e:
    print "You need to install web.py"
    sys.exit(1)

try:
    from jinja2 import Environment, FileSystemLoader
except ImportError, e:
    print "You didn't install jinja2 templating engine"
    sys.exit(1)

try:
    from dc2.lib.decorators import Logger
except ImportError, e:
    print 'you do not have dc2.lib installed'
    print e
    sys.exit(1)

class RESTController(object):

    def __init__(self, *args, **kwargs):
        self._request_context = kwargs.get('request_context', None)
        self._controller_path = kwargs.get('controller_path', None)
        self._define_process_methods()
        self._initialize_verbs()

    def set_context(self, ctx):
        self._request_context = ctx

    def _initialize_verbs(self):
        self._verb_methods = {
            'GET':[
                {'urlre':'^%s[/]{0,1}$' % self._controller_path, 'action':'index', 'template':'index.tmpl'},  # index
                {'urlre':'^%s/new$' % self._controller_path, 'action':'new', 'template':'new.tmpl'},  # new
                {'urlre':'^%s/(?P<id>[a-z,0-9,\-,\.A-Z]+)$' % self._controller_path, 'action':'show', 'template':'show.tmpl'},  # show
                {'urlre':'^%s/(?P<id>[a-z,0-9,\-,\.A-Z]+)/edit$' % self._controller_path, 'action':'edit', 'template':'edit.tmpl'},  # edit
            ],
            'POST':[
                {'urlre':'^%s[/]{0,1}$' % self._controller_path, 'action':'create'},  # create
            ],
            'PUT':[
                {'urlre':'^%s/(?P<id>[a-z,0-9,\-,\.A-Z]+)$' % self._controller_path, 'action':'update'},  # update
            ],
            'DELETE':[
                {'urlre':'^%s/(?P<id>[a-z,0-9,\-,\.A-Z]+)$' % self._controller_path, 'action':'delete' }  # delete
            ]
        }


    def add_process_method(self, action_name='', action_method=None):
        if action_name is None or action_name == '':
            raise ValueError('action_name can\'t be None or empty')
        if action_name in self._REQ_METHODS:
            raise ValueError('action_name \'%s\' is already defined' % action_name)
        if action_method is None:
            raise ValueError('action_method is none')

        self._REQ_METHODS[action_name] = action_method

    def add_url_handler_to_verb(self, verb='GET', urlre='^$', action_name='', **kwargs):
        url_regexp = '^%s/%s$' % (self._controller_path, urlre)
        verb_method = {'urlre':url_regexp, 'action':action_name}
        if len(kwargs) > 0:
            for key in kwargs.keys():
                verb_method[key] = kwargs[key]
        self._verb_methods[verb].append(verb_method)


    def _define_process_methods(self):
        self._REQ_METHODS = {
            'index':self._index,
            'new':self._new,
            'show':self._show,
            'edit':self._edit,
            'create':self._create,
            'update':self._update,
            'delete':self._delete,
        }

    def _content_type(self, formats=None):
        content_type = self._request_context.env.get('CONTENT_TYPE', None)
        if formats is None:
            if content_type is None:
                return 'text/html; charset=utf-8'
            else:
                return content_type
        else:
            output_format = formats.get('oformat', None)
            if output_format is not None:
                if output_format.lower() == 'json':
                    return 'application/json; charset=utf-8'
                if output_format.lower() == 'html':
                    return 'text/html; charset=utf-8'
            else:
                if content_type is None:
                    return 'text/html; charset=utf-8'
                else:
                    return content_type
        return 'text/html; charset=utf-8'

    def _output_format(self, content_type):
        if content_type.find('text/html') != -1:
            return 'html'
        if content_type.find('application/json') != -1:
            return 'json'

    def process(self, path='/'):
        verb = self._process_request(path)
        if verb is not None:
            func = self._REQ_METHODS[verb['action']]
            return func(verb=verb)
        return web.notfound()

    def _process_request(self, path):
        verbs = self._verb_methods[self._request_context.method.upper()]
        params = web.input()
        for verb in verbs:
            found = re.search(verb['urlre'], path)
            if found is not None:
                verb['request_data'] = found.groupdict()
                verb['request_type'] = 'html'
                if self._request_context.env.get('X-Request-With', None) is not None:
                    if self._request_context.env['X-Request-With'] == 'XMLHttpRequest':
                        verb['request_type'] = 'ajax'
                verb['request_content_type'] = self._content_type(params)
                verb['request_output_format'] = self._output_format(verb['request_content_type'])
                if verb.get('template', None) is not None:
                    verb['template'] = '%s/%s' % (self._controller_path, verb['template'])
                return verb

    def _prepare_output(self, format='html', content_type='text/html; charset=utf-8', output_format='html', output=None):
        if output is None or type(output) is not types.DictType:
            output = {'output':'No Output'}
        result = {}
        result['format'] = format
        result['content-type'] = content_type
        if output_format == 'json':
            output = json.dumps(output)
        result['output'] = output
        return result

    def _index(self, *args, **kwargs):
        return self._prepare_output()
    def _new(self, *args, **kwargs):
        return self._prepare_output()
    def _show(self, *args, **kwargs):
        return self._prepare_output()
    def _edit(self, *args, **kwargs):
        return self._prepare_output()
    def _create(self, *args, **kwargs):
        return self._prepare_output(output={'redirect':{'url':'/error', 'absolute':True}})
    def _update(self, *args, **kwargs):
        return self._prepare_output(output={'redirect':{'url':'/error', 'absolute':True}})
    def _delete(self, *args, **kwargs):
        return self._prepare_output(output={'redirect':{'url':'/error', 'absolute':True}})


