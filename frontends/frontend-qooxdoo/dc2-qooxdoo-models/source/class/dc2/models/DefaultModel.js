/*
    (DC)² - DataCenter Deployment Control
    Copyright (C) 2010, 2011, 2012 Stephan Adig <sh@sourcecode.de>

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
qx.Class.define("dc2.models.DefaultModel",
    {
      extend:qx.core.Object,
      construct:function(RPCUrl) {
        this.base(arguments);
        this._tableModel=new qx.ui.table.model.Simple();
        this._rpc_url=RPCUrl;
        this._rpc=new qx.io.remote.Rpc(this._rpc_url,"");
        var username=dc2.helpers.BrowserCheck.HTTPUsername();
        var password=dc2.helpers.BrowserCheck.HTTPPassword();
        if (username != null) {
          this._rpc.setUseBasicHttpAuth(true);
          this._rpc.setPassword(password);
          this._rpc.setUsername(username);
        }
        this._rpc.setTimeout(10000);
        this._rpc.setCrossDomain(false);
      },
      members:{
        _rpc:null,
        _rpc_url:null,
        _options:null,
        _tableModel:null,
        getModelName:function() {
          return "DefaultModel";
        },
        getModelCaption:function() {
          return "Default";
        },
        getTableModel:function() {
          return this._tableModel;
        },
        _setTableData:function(tableData) {
          this._tableModel.setDataAsMapArray(tableData,true);
        },
        _showError:function(methodName) {
        },
        listData:function(search) {
        },
        getEmptyData:function() {
        },
        addData:function(data) {
        },
        updateData:function(data) {
        },
        deleteData:function(data) {
        }
      }
    }
);



