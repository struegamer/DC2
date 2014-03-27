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
    from dc2.lib.web.controllers import Controller
except ImportError:
    print('you do not have dc2.lib installed')
    sys.exit(1)


class JSONController(Controller):

    def _content_type(self, *args, **kwargs):
        return 'application/json; charset=utf-8'

    def _prepare_output(self, *args, **kwargs):
        # Takes -> result
        content = kwargs.get('result', None)
        result = {
            'format': 'json',
            'content-type': self._content_type(),
            'output': json.dumps(content)}
        return result
