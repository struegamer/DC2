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

try:
    from mongoengine import Document
    from mongoengine import StringField
    from mongoengine import ListField
except ImportError as e:
    print('Mongoengine is not installed')
    print(e)
    sys.exit(1)

from model_parameter import PuppetParameter

class PuppetClass(Document):
    classname = StringField(required=True, unique=True)
    description = StringField()

    def to_dict(self):
        rec = {}
        rec['classname'] = self.classname
        rec['description'] = self.description
        rec['_id'] = str(self.id)
        return rec
