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

qx.Class.define("dc2.xen.models.XenVMS",
    {
      extend: dc2.models.DefaultModel,
      construct:function(RPCUrl) {
        this.base(arguments,RPCUrl);
        this._tableModel.setColumnIds(["vm_id","vm_name","vm_description","session_id","xen_host"]);
        this._tableModel.setColumns(["ID","Name","Description","Session ID","xen_host"]);
      },
      members:{
        _session_id:null,
        _xenhost:null,
        _vmtype:null,
        getModelCaption:function() {
          return("Xen VMs");
        },
        getModelName:function() {
          return "dc2.models.XenVMS";
        },
        setSessionInfos:function(data) {
          if (data != null) {
            this._session_id=data["session_id"];
            this._xenhost=data["xen_host"]
            this._vmtype=data["vmtype"]
          } else {
            this._session_id=null;
            this._xenhost=null;
            this._vmtype=null;
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
            if (this._session_id!=null && this._xenhost!=null && this._vmtype!=null) {
              this._rpc.callAsync(handler,"dc2.inventory.xenvms.list",this._xenhost,this._session_id,this._vmtype);
            } else {
              this._setTableData([]);
            }
          } else {
            this._rpc.callAsync(handler,"dc2.inventory.xenvms.list",this._xenhost,this._session_id,this._vmtype);
          }
        },
        getVMRecord:function(vm_id) {
          if (vm_id!=null) {
            try {
              var result=this._rpc.callSync("dc2.inventory.xenvms.get",this._xenhost,this._session_id,vm_id);
              return(result);
            } catch (exc) {
              console.log(exc);
            }
          }
        },
        getEmptyData:function() {
          var data={};
          data["session_id"]=this._session_id;
          data["xen_host"]=this._xenhost;
          data["vmtype"]=this._vmtype;
          return(data);
        }
      }
    }
);
