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


import uuid

class Table(object):
    def __init__(self, collection=None):
        self._collection = collection

    def save(self, docs, **kwargs):
        if not docs.has_key("_id") or docs["_id"] is None or docs["_id"] == "":
            docs["_id"] = str(uuid.uuid4())
        
        doc_id = self._collection.save(docs, **kwargs)
        return doc_id
            


    def find(self, spec=None, fields=None, sort_fieldname=None, **kwargs):
        if sort_fieldname is not None:
            return list(self._collection.find(spec,fields, **kwargs).sort(sort_fieldname))
        return list(self._collection.find(spec, fields, **kwargs))

    def find_one(self, spec=None, *args, **kwargs):
        return self._collection.find_one(spec, *args, **kwargs)
    
    def remove(self, spec=None, **kwargs):
        if spec is not None:
            self._collection.remove(spec, **kwargs)
            return True
        return False
            
    def count(self):
        return self._collection.count()

    def get_collection(self):
        return self._collection
