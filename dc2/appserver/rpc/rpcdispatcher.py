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
import os
import xmlrpclib
import json
import types

class RPCDispatcher(object):
    def __init__(self):
        self.rpcs = {}

    def register_rpc(self, methodname=None, methodcallback=None):
        if methodname is not None and methodname != "" and methodcallback is not None:
            self.rpcs[methodname] = methodcallback
            return True
        return False

    def unregister_rpc(self, methodname=None):
        if methodname is not None and methodname != "":
            if self.rpcs.has_key(methodname):
                del self.rpcs[methodname]
                return True
        return False

    def content_type(self):
        pass

    def handle_request(self, request_data=None):
        pass

class XMLRPCDispatcher(RPCDispatcher):
    def __init__(self):
        RPCDispatcher.__init__(self)

    def get_list_of_public_methods(self):
        methodlist = []
        methodlist.append("system.listMethods")
        for methodname in self.rpcs.keys():
            methodlist.append(methodname)
        return methodlist

    def content_type(self):
        return "text/xml"

    def handle_request(self, request_data=None):
        if request_data is not None:
            response = None
            params, method = xmlrpclib.loads(request_data)
            if method == "system.listMethods":
                response = xmlrpclib.dumps((self.get_list_of_public_methods(),), methodresponse=True, allow_none=True)
            elif self.rpcs.has_key(method):
                method_response = self.rpcs[method](*params)
                if not isinstance(method_response, xmlrpclib.Fault):
                    response = xmlrpclib.dumps((method_response,), methodresponse=True, allow_none=True)
                else:
                    response = xmlrpclib.dumps(method_response, methodresponse=True)
            else:
                response = xmlrpclib.dumps(xmlrpclib.Fault(-32500, "Method not found!"), methodresponse=True)
            return response
        return None


class JSONRPCDispatcher(RPCDispatcher):
    def __init__(self):
        RPCDispatcher.__init__(self)

    def content_type(self):
        return "application/json"

    def handle_request(self, request_data=None):
        if request_data is not None:
            response = None
            json_call = json.loads(request_data)
            if json_call.has_key("method"):
                if self.rpcs.has_key(json_call["method"]):
                    try:
                        if json_call["params"] is not None or len(json_call["paramnewEntrys"]) > 0:
                            method_response = self.rpcs[json_call["method"]](*json_call["params"])
                            if type(method_response) is xmlrpclib.Fault:
                                response = {}
                                response["id"] = json_call["id"]
                                response["result"] = None
                                response["error"] = method_response.faultString
                                return json.dumps(response)
                        else:
                            method_response = self.rpcs[json_call["method"]]()
                            if type(method_response) is xmlrpclib.Fault:
                                response = {}
                                response["id"] = json_call["id"]
                                response["result"] = None
                                response["error"] = method_response.faultString
                                return json.dumps(response)
                        response = {}
                        response["id"] = json_call["id"]
                        response["result"] = method_response
                        response["error"] = None
                        return json.dumps(response)
                    except Exception,e:
                        response = {}
                        response["id"] = json_call["id"]
                        response["error"] = "Parameter Errors"
                        response["result"] = None
                        return json.dumps(response)
                else:
                    response = {}
                    response["id"] = json_call["id"]
                    response["error"] = "Error"
                    response["result"] = None
                    return json.dumps(response)


