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

/* *************************************
#asset(qx/icon/${qx.icontheme}/16/actions/dialog-ok.png);
#asset(qx/icon/${qx.icontheme}/16/actions/dialog-cancel.png);
*/

qx.Class.define("dc2.dialogs.EditSystemGroups",
{
  extend: qx.ui.window.Window,
  construct:function() {
    this.base(arguments);
    this._createLayout();
  },
  events: {
    'addData':'qx.event.type.Data',
    'updateData':'qx.event.type.Data'
  },
  members: {
    _edit_id:null,
    _edit_groupname:null,
    _edit_gid:null,
    _edit_is_system:null,
    _edit_is_admin:null,
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
      this._edit_groupname=new qx.ui.form.TextField();
      this._edit_gid=new qx.ui.form.TextField();
      this._edit_is_system=new qx.ui.form.CheckBox();
      this._edit_is_admin=new qx.ui.form.CheckBox();
      comp.add(new qx.ui.basic.Label("Groupname"),{row:0,column:0});
      comp.add(new qx.ui.basic.Label("Group ID"),{row:1,column:0});
      comp.add(new qx.ui.basic.Label("Is System Group"),{row:2,column:0});
      comp.add(new qx.ui.basic.Label("Is Admin Group"),{row:3,column:0});
      comp.add(this._edit_groupname,{row:0,column:1});
      comp.add(this._edit_gid,{row:1,column:1});
      comp.add(this._edit_is_system,{row:2,column:1});
      comp.add(this._edit_is_admin,{row:3,column:1});
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
    _clkBtnOk:function(e)  {
      var data={};
      data["_id"]=this._edit_id;
      data["groupname"]=this._edit_groupname.getValue();
      data["gid"]=this._edit_gid.getValue();
      if (this._edit_is_system.getValue()) {
        data["is_system_group"]="1";
      } else {
        data["is_system_group"]="0";
      }
      if (this._edit_is_admin.getValue()) {
        data["is_admin_group"]="1";
      } else {
        data["is_admin_group"]="0";
      }
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
    setData:function(data) {
      if (data != null) {
        this._edit_id=data["_id"];
        this._edit_groupname.setValue(data["groupname"]);
        this._edit_gid.setValue(data["gid"]);
        if (data["is_system_group"]=="1") {
          this._edit_is_system.setValue(true);
        } else {
          this._edit_is_system.setValue(false);
        }
        if (data["is_admin_group"]=="1") {
          this._edit_is_admin.setValue(true);
        } else {
          this._edit_is_admin.setValue(false);
        }
      }
    }
  }
})
