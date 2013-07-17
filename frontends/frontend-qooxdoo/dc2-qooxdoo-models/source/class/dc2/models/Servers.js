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

qx.Class.define("dc2.models.Servers",
    {
      extend: dc2.models.DefaultModel,
      construct:function(RPCUrl) {
        this.base(arguments,RPCUrl);
        this._tableModel.setColumnIds(["_id","uuid","serial_no","product_name","manufacturer","location","asset_tags"]);
        this._tableModel.setColumns(["ID","UUID","Serial Number","Product Name","Manufacturer","Location","Asset Tags"]);
      },
      members:{
        getModelName:function() {
          return "dc2.models.Servers";
        },
        getModelCaption:function() {
          return "Servers";
        },
        listData:function(search) {
          // if (search == null) {
          //   var data=this._rpc.callSync("dc2.servers.list");
          //   this._setTableData(data);
          // } else {
          //   var data=this._rpc.callSync("dc2.servers.list",0,0,search);
          //   this._setTableData(data);
          // }
          var _this=this;
          var handler=function(result,ex,id) {
            if (ex!=null) {
              // show error
            } else {
	            _this._setTableData(result);
	          }
	        };
	        if (search == null) {
	          this._rpc.callAsync(handler,"dc2.inventory.servers.list");
	        } else {
	          this._rpc.callAsync(handler,"dc2.inventory.servers.list",0,0,search);
	        }
        },
        updateData:function(data) {
          if (data != null) {
            try {
              var response=this._rpc.callSync("dc2.inventory.servers.update",data);
              return(true);
            } catch(exc) {
              return(false);
            }
          }
        },
        deleteData:function(data) {
          if (data != null) {
            try {
              var response=this._rpc.callSync("dc2.inventory.servers.delete_complete",data);
              return(true);
            } catch(exc) {
              return(false);
            }
          }
        },
        getAllServers:function() {
          var result=this._rpc.callSync("dc2.inventory.servers.list");
          return(result);
        },
        getAllServersWithoutHosts:function() {
          var result=this._rpc.callSync("dc2.inventory.servers.list_without_hosts");
          return(result);
        }
      }
    }
);
