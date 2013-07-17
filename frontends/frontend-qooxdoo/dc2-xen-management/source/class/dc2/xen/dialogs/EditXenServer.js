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


qx.Class.define("dc2.xen.dialogs.EditXenServer",
{
  extend: qx.ui.window.Window,
  construct:function() {
    this.base(arguments);
    this._createLayout();
  },
  events: {
      'addData':"qx.event.type.Data",
      'updateData':"qx.event.type.Data"
  },
  members:{
    _edit_id:null,
    _edit_xen_host:null,
    _edit_xen_username:null,
    _edit_xen_password:null,
    _createLayout:function() {
      this.set({
        modal:true,
        padding:3,
        showClose:true,
        showMaximize:false,
        showMinimize:false
      });
      this.setLayout(new qx.ui.layout.VBox(5));
      this.setResizable(false,true,true,false);
      var comp=new qx.ui.container.Composite();
      var layout=new qx.ui.layout.Grid(5,5);
      layout.setColumnFlex(1,1);
      comp.setLayout(layout);
      this._edit_xen_host=new qx.ui.form.TextField();
      this._edit_xen_username=new qx.ui.form.TextField();
      this._edit_xen_password=new qx.ui.form.PasswordField();
      comp.add(new qx.ui.basic.Label("Xen Hostname"),{row:0,column:0});
      comp.add(new qx.ui.basic.Label("Xen Username"),{row:1,column:0});
      comp.add(new qx.ui.basic.Label("Xen Password"),{row:2,column:0});
      comp.add(this._edit_xen_host,{row:0,column:1});
      comp.add(this._edit_xen_username,{row:1,column:1});
      comp.add(this._edit_xen_password,{row:2,column:1});
      this.add(comp,{flex:1});
      this.add(this._initializeButtonBar());
    },
    /*
     * Private Methods
     */
    _initializeButtonBar:function() {
      var comp=new qx.ui.container.Composite(new qx.ui.layout.HBox(5).set({alignX:'right'}));
      var btnOk=new qx.ui.form.Button('Ok','icon/16/actions/dialog-ok.png');
      var btnCancel=new qx.ui.form.Button('Cancel','icon/16/actions/dialog-cancel.png');
      btnOk.addListener("execute",this._clkBtnOk,this);
      btnCancel.addListener("execute",this._clkBtnCancel,this);
      comp.add(btnCancel);
      comp.add(btnOk);
      return(comp);
    },
    /*
     * Event Methods
     */
    _clkBtnOk:function(e) {
      var data={};
      data["_id"]=this._edit_id;
      data["xen_host"]=this._edit_xen_host.getValue()
      data["xen_username"]=this._edit_xen_username.getValue();
      data["xen_password"]=this._edit_xen_password.getValue();
      if (data["_id"] != "" && data["_id"] != null) {
        this.fireDataEvent("updateData",data);
      } else {
        this.fireDataEvent("addData",data);
      }
      this.close();
    },
    _clkBtnCancel:function(e) {
      this.close();
    },
    /*
     * Public Methods
     */
    setData:function(data) {
      if (data != null) {
        this._edit_id=data["_id"];
        this._edit_xen_host.setValue(data["xen_host"]);
        if (data["xen_host"]!=null && data["xen_host"]!="") {
          this._edit_xen_host.setEnabled(false);
        } else {
          this._edit_xen_host.setEnabled(true);
        }
        this._edit_xen_username.setValue(data["xen_username"]);
        this._edit_xen_password.setValue(data["xen_password"]);
      }
    }
  }
});
