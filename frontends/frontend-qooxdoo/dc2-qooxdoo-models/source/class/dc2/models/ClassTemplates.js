/*
    (DC)² - DataCenter Deployment Control
    Copyright (C) 2010, 2011, 2012, 2013  Stephan Adig <sh@sourcecode.de>

    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 2 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License along
    with this program; if not, write to the Free Software Foundation, Inc.,
    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
*/

qx.Class.define("dc2.models.ClassTemplates",
{
  extend: dc2.models.DefaultModel,
  construct:function(RPCUrl) {
    this.base(arguments,RPCUrl);
    this._tableModel.setColumnIds(["_id","name","description"]);
    this._tableModel.setColumns(["ID","Template Name","Description"]);
  },
  members: {
    getModelName:function() {
      return("dc2.models.ClassTemplates");
    },
    getModelCaption:function() {
      return("Class Templates");
    },
    listData:function(search) {
      var _this=this;
      var handler=function(result,ex,id) {
        if (ex!=null) {
          // show error
        } else {
          _this._setTableData(result);
        }
      };
      if (search == null) {
        this._rpc.callAsync(handler,"dc2.configuration.classtemplates.list");
      } else {
        this._rpc.callAsync(handler,"dc2.configuration.classtemplates.list",search);
      }
    },
    addData:function(data) {
      if (data != null) {
        try {
          var response=this._rpc.callSync("dc2.configuration.classtemplates.add",data);
          return(true);
        } catch(exc) {
          return(false);
        }
      }
    },
    updateData:function(data) {
      if (data != null) {
        try {
          var response=this._rpc.callSync("dc2.configuration.classtemplates.update",data);
          return(true);
        } catch(exc) {
          return(false);
        }
      }
    },
    deleteData:function(data) {
      if (data != null) {
        try {
          var response=this._rpc.callSync("dc2.configuration.classtemplates.remove",{"_id":data["_id"]});
          return(true);
        } catch(exc) {
          return(false);
        }
      }
    },
    getClassTemplateRecord:function(id) {
      var record=this._rpc.callSync("dc2.configuration.classtemplates.get",id);
      return(record);
    },
    getAllTemplates:function() {
      var result=this._rpc.callSync("dc2.configuration.classtemplates.list");
      return(result);
    },
    getEmptyData:function() {
      var data={};
      data["_id"]=null;
      data["name"]="New classname";
      data["description"]="New description";
      data["classes"]=[];
      return(data);
    }
  }
});