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
    from flaskext.xmlrpc import XMLRPCHandler, Fault
except ImportError as e:
    print('Flask Extension XMLRPC not installed')
    print(e)
    sys.exit(1)


from dc2.puppet.globals import xmlrpc_handler
from dc2.puppet.db.models import PuppetClass
from dc2.puppet.db.models import PuppetParameter

@xmlrpc_handler.register('dc2.puppet.classes.list')
def classes_list():
    classlist = [i.to_dict() for i in PuppetClass.objects.all()]
    return classlist

@xmlrpc_handler.register('dc2.puppet.classes.count')
def classes_count():
    count = PuppetClass.objects.count()
    return count

@xmlrpc_handler.register('dc2.puppet.classes.add')
def classes_add(classname, description=''):
    if not classname:
        return Fault('{0}: classname'.format('dc2.puppet.classes.add'), 'Classname can not be empty')
    try:
        n = PuppetClass()
        n.classname = classname
        n.description = description
        n.save()
        return n.to_dict()
    except Exception as e:
        return Fault('{0}'.format('dc2.puppet.classes.add'), e.message)

@xmlrpc_handler.register('dc2.puppet.classes.get')
def classes_get(field, value):
    if not field:
        return Fault('{0}: field'.format('dc2.puppet.classes.get'), 'Field not set. Field needs to be one of "id" or "classname"')
    if not value:
        return Fault('{0}: value'.format('dc2.puppet.classes.get'), 'Field value not set.')
    rec = {}
    rec[str(field)] = value
    print rec
    try:
        classrec = PuppetClass.objects.get(**rec)
    except Exception as e:
        print(e)
    return classrec.to_dict()

@xmlrpc_handler.register('dc2.puppet.classes.update')
def classes_update(id, classname, description=''):
    if not id:
        return Fault('{0}: id'.format('dc2.puppet.classes.update'), 'ID can not be empty')
    if not classname:
        return Fault('{0}: classname'.format('dc2.puppet.classes.update'), 'Classname can not be empty')
    try:
        n = PuppetClass.objects.get(id=id)
        n.classname = classname
        n.description = description
        n.save()
        return n.to_dict()
    except Exception as e:
        return Fault('{0}'.format('dc2.puppet.classes.update'), e.message)

@xmlrpc_handler.register('dc2.puppet.classes.delete')
def classes_delete(id):
    if not id:
        return Fault('{0}: id'.format('dc2.puppet.classes.delete'), 'ID can not be empty')
    try:
        n = PuppetClass.objects.get(id=id)
        n.delete()
        return True
    except Exception as e:
        return Fault('{0}'.format('dc2.puppet.classes.delete'), e.message)

