/*
    (DC)² - DataCenter Deployment Control
    Copyright (C) 2010  Stephan Adig <sh@sourcecode.de>

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

qx.Class.define("cs2.models.SSLCsrs",
{
  extend: dc2.models.DefaultModel,
  construct:function(RPCUrl) {
    this.base(arguments,RPCUrl);
    this._tableModel.setColumnIds(["_id","commonname","csr_with_key","csr_pem"]);
    this._tableModel.setColumns(["ID","Common Name","Keyname","CSR PEM Format"]);         
  },
  members: {
    getModelName:function() {
      return("cs2.models.SSLCsrs");
    },
    getModelCaption:function() {
      return("SSL Certificate Signing Request");
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
        this._rpc.callAsync(handler,"cs2.ssl.csrs.list");
      } else {
        // this._rpc.callAsync(handler,"cs2.ssl.keys.list",search);
      }
    },
    addData:function(data) {
      if (data != null) {        
        try {
          var response=this._rpc.callSync("cs2.ssl.csrs.create",data["commonname"],data["keyname"],data["passphrase"],data["digest"],data["subjects"]);
          return(true);
        } catch(exc) {
          return(false);
        }
      }
    },
    deleteData:function(data) {
      if (data != null) {
        try {
          var response=this._rpc.callSync("cs2.ssl.csrs.remove",data["commonname"]);
          return(true);
        } catch(exc) {
          return(false);
        }        
      }
    },
    getCsrNames:function() {
      var result=this._rpc.callSync("cs2.ssl.csrs.list");
      return(result);
    },
    getEmptyData:function() {
      var data={};
      data["_id"]=null;
      data["commonname"]="New Keyname";
      data["keyname"]="New description";
      data["passphrase"]="";
      data["digest"]="";
      data["subjects"]="";
      data["passphrase"]="";
      data["key_pem"]="";
      return(data);
    }
  }
});