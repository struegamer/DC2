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

qx.Class.define("dc2.models.RIB",
    {
      extend: dc2.models.DefaultModel,
      construct:function(RPCUrl) {
        this.base(arguments,RPCUrl);
        this._tableModel.setColumnIds(["_id","server_id","remote_type","remote_ip"]);
        this._tableModel.setColumns(["ID","server_id","Type","IP"]);
      },
      members:{
        _server_id:null,
        getModelName:function() {
          return ("dc2.models.RIB");
        },
        getModelCaption:function() {
          return ("Remote Insight Boards");
        },
        setServerId:function(data) {
          this._server_id=data;
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
	    this._rpc.callAsync(handler,"dc2.inventory.servers.rib.list",{"server_id":this._server_id});
	  } else {
	    this._rpc.callAsync(handler,"dc2.inventory.servers.rib.list",search);
	  }
        },
        addData:function(data) {
          if (data != null) {
            try {
              var response=this._rpc.callSync("dc2.inventory.servers.rib.add",data);
              return(true);
            } catch(exc) {
              return(false);
            }
          }
        },
        updateData:function(data) {
          if (data != null) {
            try {
              var response=this._rpc.callSync("dc2.inventory.servers.rib.update",data);
              return(true);
            } catch(exc) {
              return(false);
            }
          }
        },
        deleteData:function(data) {
          if (data != null) {
            try {
              var response=this._rpc.callSync("dc2.inventory.servers.rib.delete",data);
              return(true);
            } catch(exc) {
              return(false);
            }
          }          
        },
        getEmptyData:function() {
          var data={};
          data["server_id"]=this._server_id;
          data["remote_type"]="ilo1";
          data["remote_ip"]="192.168.1.1";
          return(data);
        }
      }
    }
);
