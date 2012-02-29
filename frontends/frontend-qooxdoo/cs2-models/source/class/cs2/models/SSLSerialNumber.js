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

qx.Class.define("cs2.models.SSLSerialNumber",
{
  extend: dc2.models.DefaultModel,
  construct:function(RPCUrl) {
    this.base(arguments,RPCUrl);
    this._tableModel.setColumnIds(["_id","serial"]);
    this._tableModel.setColumns(["ID","Serial Number"]);         
  },
  members: {
    getModelName:function() {
      return("cs2.models.SSLSerialNumber");
    },
    getModelCaption:function() {
      return("SSL Serial Numbers");
    },
    getSerialNumber:function() {
      var result=this._rpc.callSync("cs2.ssl.serial.get");
      return(result["serial"]);
    }
  }
});