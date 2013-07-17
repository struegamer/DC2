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

qx.Class.define("dc2.models.DefaultBootmethods",
{
  extend: dc2.models.DefaultModel,
  construct:function(RPCUrl) {
    this.base(arguments,RPCUrl);
    this._tableModel.setColumnIds(["_id","hardware_type","pxe_bootmethod"]);
    this._tableModel.setColumns(["ID","Hardware Type","PXE Boot Method"]);
  },
  members: {
    getModelName:function() {
      return("dc2.models.DefaultBootmethods");
    },
    getModelCaption:function() {
      return("Default Bootmethods");
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
        this._rpc.callAsync(handler,"dc2.configuration.bootmethods.list");
      } else {
        this._rpc.callAsync(handler,"dc2.configuration.bootmethods.list",search);
      }
    },
    addData:function(data) {
      if (data != null) {
        try {
          var response=this._rpc.callSync("dc2.configuration.bootmethods.add",data);
          return(true);
        } catch(exc) {
          return(false);
        }
      }
    },
    updateData:function(data) {
      if (data != null) {
        try {
          var response=this._rpc.callSync("dc2.configuration.bootmethods.update",data);
          return(true);
        } catch (exc) {
          return(false);
        }
      }
    },
    deleteData:function(data) {
      if (data != null) {
        try {
          var response=this._rpc.callsync("dc2.configuration.bootmethods.delete",{"_id":data["_id"]});
          return(true);
        } catch (exc) {
          return(false);
        }
      }
    },
    updateHardware:function(e) {
      var _this=this;
      var handler=function(result,ex,id) {
        if (ex != null) {
          // show error
        } else {
         _this.listData();
        }
      };
      this._rpc.callAsync(handler,"dc2.configuration.bootmethods.update_hw_types");
    },
    getEmptyData:function() {
      var data={};
      data["_id"]=null;
      data["hardware_type"]=null;
      data["pxe_bootmethod"]=null;
      return(data);
    }
  }
})
