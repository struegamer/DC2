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

qx.Class.define("dc2.dialogs.EditSystemUsers",
{
  extend:qx.ui.window.Window,
  construct:function() {
    this.base(arguments);
    this._createLayout();
  },
  events: {
    'addData':"qx.event.type.Data",
    'updateData':"qx.event.type.Data"
  },
  members: {
    _edit_id:null,
    _edit_username:null,
    _edit_realname:null,
    _edit_uid:null,
    _edit_gid:null,
    _edit_cryptpw:null,
    _edit_is_admin:null,
    _edit_ssh_pubkey:null,
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
      this._edit_username=new qx.ui.form.TextField();
      this._edit_realname=new qx.ui.form.TextField();
      this._edit_uid=new qx.ui.form.TextField();
      this._edit_gid=new qx.ui.form.TextField();
      this._edit_cryptpw=new qx.ui.form.TextField();
      this._edit_is_admin=new qx.ui.form.CheckBox();
      this._edit_ssh_pubkey=new qx.ui.form.TextArea();
      comp.add(new qx.ui.basic.Label("Username"),{row:0,column:0});
      comp.add(new qx.ui.basic.Label("Realname"),{row:1,column:0});
      comp.add(new qx.ui.basic.Label("UID"),{row:2,column:0});
      comp.add(new qx.ui.basic.Label("GID"),{row:3,column:0});
      comp.add(new qx.ui.basic.Label("Crypt PW"),{row:4,column:0});
      comp.add(new qx.ui.basic.Label("Is Admin User"),{row:5,column:0});
      comp.add(new qx.ui.basic.Label("SSH Public Key"),{row:6,column:0});
      comp.add(this._edit_username,{row:0,column:1});
      comp.add(this._edit_realname,{row:1,column:1});
      comp.add(this._edit_uid,{row:2,column:1});
      comp.add(this._edit_gid,{row:3,column:1});
      comp.add(this._edit_cryptpw,{row:4,column:1});
      comp.add(this._edit_is_admin,{row:5,column:1});
      comp.add(this._edit_ssh_pubkey,{row:6,column:1});
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
      data["username"]=this._edit_username.getValue();
      data["realname"]=this._edit_realname.getValue();
      data["uid"]=this._edit_uid.getValue();
      data["gid"]=this._edit_gid.getValue();
      data["cryptpw"]=this._edit_cryptpw.getValue();
      data["ssh_pubkey"]=this._edit_ssh_pubkey.getValue();
      if (this._edit_is_admin.getValue()) {
        data["is_admin"]="1";
      } else {
        data["is_admin"]="0";
      }
      if (data["_id"] != "" && data["_id"]!=null) {
        this.fireDataEvent("updatedata",data);        
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
        this._edit_username.setValue(data["username"]);
        this._edit_realname.setValue(data["realname"]);
        this._edit_uid.setValue(data["uid"]);
        this._edit_gid.setValue(data["gid"]);
        this._edit_cryptpw.setValue(data["cryptpw"]);
        this._edit_ssh_pubkey.setValue(data["ssh_pubkey"]);
        if (data["is_admin"]=="0" || data["is_admin"]=="" || data["is_admin"]==null) {
          this._edit_is_admin.setValue(false);
        } else {
          this._edit_is_admin.setValue(true);
        }

      }
    }
  }
});
