/*
    (DC)² - DataCenter Deployment Control
    Copyright (C) 2010, 2011, 2012  Stephan Adig <sh@sourcecode.de>

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

qx.Class.define("dc2.models.DefaultSystemUsers",
{
  extend:dc2.models.DefaultModel,
  construct:function(RPCUrl) {
    this.base(arguments,RPCUrl);
    this._tableModel.setColumnIds(['_id','username','realname']);
    this._tableModel.setColumns(['ID','Username','Realname']);    
  },
  members: {
    getModelName:function() {
      return("dc2.models.DefaultSystemUsers");      
    },
    getModelCaption:function() {
      return("Default System Users");
    },
    listData:function(search) {
      var _this=this;
      var handler=function(result,ex,id) {
        if (ex!=null) {
          // show Error
        } else {
          _this._setTableData(result);
        }
      };
      if (search == null) {
        this._rpc.callAsync(handler,"dc2.configuration.systemusers.list");      
      } else {
        this._rpc.callAsync(handler,"dc2.configuration.systemusers.list",search);
      }
    },
    addData:function(data) {
      if (data != null) {
        try {
          var response=this._rpc.callSync("dc2.configuration.systemusers.add",data);
          return(true);
        } catch(exc) {
          return(false);
        }
      }
    },
    updateData:function(data) {
      if (data != null) {
        try {
          var response=this._rpc.callSync("dc2.configuration.systemusers.update",data);
          return(true)
        } catch (exc) {
          return(false);
        }
      }
    },
    deleteData:function(data) {
      if (data != null) {
        try {
          var response=this._rpc.callSync("dc2.configuration.systemusers.delete",data);
          return(true);
        } catch (exc) {
          return(false);
        }
      }
    },
    getEmptyData:function() {
      var data={};
      data["_id"]=null;
      data["username"]=null;
      data["realname"]=null;
      data["uid"]=null;
      data["gid"]=null;
      data["cryptpw"]=null;
      data["is_admin"]="0";
      data["ssh_pubkey"]=null;
      return(data);
    }
  }
});
