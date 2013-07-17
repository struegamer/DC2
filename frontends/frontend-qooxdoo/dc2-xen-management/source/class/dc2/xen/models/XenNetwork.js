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

qx.Class.define("dc2.xen.models.XenNetwork",
    {
      extend: dc2.models.DefaultModel,
      construct:function(RPCUrl) {
        this.base(arguments,RPCUrl);
        this._tableModel.setColumnIds(["network_id","name_label","name_description","default_gateway","default_netmask","xen_host","session_id"]);
        this._tableModel.setColumns(["ID","Name","Description","Default Gateway","Default Netmask","Xen Host","Session ID"]);
      },
      members:{
        _session_id:null,
        _xenhost:null,
        getModelCaption:function() {
          return("Xen Network");
        },
        getModelName:function() {
          return "dc2.models.XenNetwork";
        },
        setSessionInfos:function(data) {
          if (data != null) {
            this._session_id=data["session_id"];
            this._xenhost=data["xen_host"]
          } else {
            this._session_id=null;
            this._xenhost=null;
          }
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
            if (this._session_id!=null && this._xenhost!=null) {
              this._rpc.callAsync(handler,"dc2.inventory.xen.networks.list",this._xenhost,this._session_id);
            } else {
              this._setTableData([]);
            }
          } else {
            this._rpc.callAsync(handler,"dc2.inventory.xen.networks.list",this._xenhost,this._session_id);
          }
        },
        getAll:function() {
          console.log("getAll");
          if (this._session_id!=null && this._xenhost!=null) {
            var result=this._rpc.callSync("dc2.inventory.xen.networks.list",this._xenhost,this._session_id);
            console.log(result);
            return(result);
          } else {
            return ([]);
          }
        },
        getEmptyData:function() {
          var data={};
          data["session_id"]=this._session_id;
          data["xen_host"]=this._xenhost;
          return(data);
        }
      }
    }
);
