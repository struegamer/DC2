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

qx.Class.define("cs2.models.SSLIso3166",
{
  extend: dc2.models.DefaultModel,
  construct:function(RPCUrl) {
    this.base(arguments,RPCUrl);
    this._tableModel.setColumnIds(["_id","country_name","country_code"]);
    this._tableModel.setColumns(["ID","Country Name","ISO3166 Country Code"]);         
  },
  members: {
    getModelName:function() {
      return("cs2.models.SSLIso3166");
    },
    getModelCaption:function() {
      return("SSL ISO 3166 Country codes");
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
        this._rpc.callAsync(handler,"cs2.ssl.iso3166.list");
      } else {
        // this._rpc.callAsync(handler,"cs2.ssl.keys.list",search);
      }
    },
    getIso3166List:function() {
      var result=this._rpc.callSync("cs2.ssl.iso3166.list");
      return(result);
    },
    addData:function(data) {
//      if (data != null) {        
//        try {
//          if (data["cipher"]=="None") {
//            data["cipher"]=null;
//          }
//          var response=this._rpc.callSync("cs2.ssl.keys.create",data["keyname"],data["description"],data["type"],data["bits"],data["cipher"],data["passphrase"]);
//          return(true);
//        } catch(exc) {
//          return(false);
//        }
//      }
    },
    deleteData:function(data) {
//      if (data != null) {
//        try {
//          var response=this._rpc.callSync("cs2.ssl.keys.remove",data["keyname"]);
//          return(true);
//        } catch(exc) {
//          return(false);
//        }        
//      }
    },
    getEmptyData:function() {
//      var data={};
//      data["_id"]=null;
//      data["keyname"]="New Keyname";
//      data["description"]="New description";
//      data["key_type"]="";
//      data["key_bits"]="";
//      data["cipher"]="";
//      data["passphrase"]="";
//      data["key_pem"]="";
//      return(data);
    }
  }
});