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

qx.Class.define("dc2.pages.Preferences",
{
  extend:qx.ui.container.Composite,
  construct:function() {
    this.base(arguments);
    this._createContent();
  },
  members: {
    _edit_rpc_url:null,
    _edit_username:null,
    _edit_password:null,
    _createContent:function() {
      var layout=new qx.ui.layout.Grid(5,5);
      // layout.setColumnFlex(1,1);
      layout.setColumnWidth(1,500);
      this.setLayout(layout);
      
      this._edit_rpc_url=new qx.ui.form.TextField();
      this._edit_username=new qx.ui.form.TextField();
      this._edit_password=new qx.ui.form.PasswordField();
      this.add(new qx.ui.basic.Label("RPC Url"),{row:0,column:0});
      this.add(new qx.ui.basic.Label("Username"),{row:1,column:0});
      this.add(new qx.ui.basic.Label("Password"),{row:2,column:0});
      this.add(this._edit_rpc_url,{row:0,column:1});
      this.add(this._edit_username,{row:1,column:1});
      this.add(this._edit_password,{row:2,column:1});
      var comp1=new qx.ui.container.Composite(new qx.ui.layout.HBox(5).set({alignX:"right"}));
      var btnApply=new qx.ui.form.Button("Apply");
      comp1.add(btnApply);
      // btnApply.setEnabled(false);
      btnApply.addListener("execute",this._putLocalStorageValues,this);
      this.add(comp1,{row:3,column:1});
      this._getLocalStorageValues();
      
    },
    _getLocalStorageValues:function() {
      if ('localStorage' in window && window['localStorage']!==null) {
        this._edit_rpc_url.setValue(localStorage.getItem("DC2-RPCUrl"));
        this._edit_username.setValue(localStorage.getItem("DC2-Username"));
        this._edit_password.setValue(localStorage.getItem("DC2-Password"));
      }
    },
    _putLocalStorageValues:function(e) {
      if ('localStorage' in window && window['localStorage']!==null) {
        localStorage["DC2-RPCUrl"]=this._edit_rpc_url.getValue();
        localStorage["DC2-Username"]=this._edit_username.getValue();
        localStorage["DC2-Password"]=this._edit_password.getValue();
      }
    }
  }
});