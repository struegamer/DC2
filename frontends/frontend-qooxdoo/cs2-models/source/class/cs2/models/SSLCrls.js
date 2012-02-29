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

qx.Class.define("cs2.models.SSLCrls",
{
  extend: dc2.models.DefaultModel,
  construct:function(RPCUrl) {
    this.base(arguments,RPCUrl);
    this._tableModel.setColumnIds(["_id","ca_name","crl_pem"]);
    this._tableModel.setColumns(["ID","CA name","CRL PEM"]);         
  },
  members: {
    getModelName:function() {
      return("cs2.models.SSLCrls");
    },
    getModelCaption:function() {
      return("SSL Certification Revocation List");
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
        this._rpc.callAsync(handler,"cs2.ssl.crls.list");
      } else {
        // this._rpc.callAsync(handler,"cs2.ssl.keys.list",search);
      }
    }
  }
});