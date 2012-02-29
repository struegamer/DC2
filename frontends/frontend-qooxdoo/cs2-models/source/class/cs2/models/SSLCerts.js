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

qx.Class.define("cs2.models.SSLCerts",
{
  extend: dc2.models.DefaultModel,
  construct:function(RPCUrl) {
    this.base(arguments,RPCUrl);
    this._tableModel.setColumnIds(["_id","commonname","cert_pem"]);
    this._tableModel.setColumns(["ID","Common Name","CERT PEM Format"]);         
  },
  members: {
    getModelName:function() {
      return("cs2.models.SSLCerts");
    },
    getModelCaption:function() {
      return("SSL Certificates");
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
        this._rpc.callAsync(handler,"cs2.ssl.certs.list");
      } else {
        // this._rpc.callAsync(handler,"cs2.ssl.keys.list",search);
      }
    },
    addData:function(data) {
      if (data != null) {        
        try {
          var response=this._rpc.callSync("cs2.ssl.certs.create",data["commonname"],data["serial_no"],data["digest"],data["notBefore"],data["notAfter"]);
          return(true);
        } catch(exc) {
          return(false);
        }
      }
    },
    revokeCert:function(data) {
      if (data != null) {
        try {
          var result=this._rpc.callSync("cs2.ssl.crls.revoke.certificate",data["commonname"],data["reason"]);
          return(true);          
        } catch(exc) {          
          return(false);
        }
      }
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