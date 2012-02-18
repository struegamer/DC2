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

class RequestDispatcher(object):
    def __init__(self):
        self._dispatcher = {}
        self._methods = {}
    
    def add_rpcdispatcher(self, dispatcher_content_type=None, dispatcher_instance=None):
        if dispatcher_content_type is not None and \
                dispatcher_content_type != "" and \
                dispatcher_instance is not None and \
                not self._dispatcher.has_key(dispatcher_content_type):
            self._dispatcher[dispatcher_content_type] = dispatcher_instance
            return True
        return False

    def del_rpcdispatcher(self, dispatcher_content_type=None):
        if dispatcher_content_type is not None and \
                dispatcher_content_type != "" and \
                self._dispatcher.has_key(dispatcher_content_type):
            del self._dispatcher[dispatcher_content_type]
            return True
        return False

    def register_rpc(self, content_type=None, methodname=None, methodcallback=None):
        if methodname is not None and \
                methodname != "" and \
                methodcallback is not None:
            # register methods and callbacks for all dispatchers

            if content_type is None or content_type == "":
                for key in self._dispatcher.keys():
                    self._dispatcher[key].register_rpc(methodname, methodcallback)
            elif content_type is not None and content_type != "" and \
                self._dispatcher.has_key(content_type):
                self._dispatcher[content_type].register_rpc(methodname, methodcallback)
            return True
        return False

    def unregister_rpc(self, content_type=None, methodname=None):
        if methodname is not None and methodname != "":
            # unregister methods and callbacks for all dispatchers
            if content_type is None or content_type == "":
                for key in self._dispatcher.keys():
                    self._dispatcher[key].unregister_rpc(methodname)
            elif content_type is not None and content_type != "" and \
                    self._dispatcher.has_key(content_type):
                self._dispatcher[content_type].unregister_rpc(methodname)
            return True
        return False

    def handle_request(self, content_type=None, request_data=None):
        if content_type is not None and content_type != "" and \
                request_data is not None and \
                self._dispatcher.has_key(content_type):
            return_data = [self._dispatcher[content_type].content_type(), self._dispatcher[content_type].handle_request(request_data)]
            return return_data
        return None
        
    def add_rpcmodule(self, modulename=None):
        if modulename is not None:
            app = __import__(modulename, globals(), locals(), ['*'], -1)
            for obj in dir(app):
                method = getattr(app, obj)
                if callable(method) and hasattr(method, 'is_rpc') and method.is_rpc is True:
                        self.register_rpc(None, method.external_name, method)
                        self._methods[method.external_name] = {}
                        self._methods[method.external_name]["method_name"] = method.external_name
                        self._methods[method.external_name]["method_params"] = method.params
                        self._methods[method.external_name]["method_returns"] = method.returns
                        self._methods[method.external_name]["is_xmlrpc"] = method.is_xmlrpc
                        self._methods[method.external_name]["is_jsonrpc"] = method.is_jsonrpc
    def list_rpc_methods(self):
        methodlist=[]
        for methodname in sorted(self._methods.keys()):
            methodlist.append(methodname)
        return methodlist
        
