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

/* ************************************************************************
#asset(qx/icon/${qx.icontheme}/16/actions/list-add.png)
#asset(qx/icon/${qx.icontheme}/16/actions/list-remove.png)
#asset(qx/icon/${qx.icontheme}/16/actions/view-refresh.png)
#asset(qx/icon/${qx.icontheme}/16/actions/dialog-ok.png);
#asset(qx/icon/${qx.icontheme}/16/actions/dialog-cancel.png);
************************************************************************ */
qx.Class.define("cs2.frontend.dialogs.SSLKeyDialog",
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
  members: {
    _edit_key_id:null,
    _edit_key_name:null,
    _edit_key_description:null,
    _edit_key_type:null,
    _edit_key_bits:null,
    _edit_key_cipher:null,
    _edit_key_passphrase:null,
    _dict_key_type:null,
    _dict_key_ciphers:null,
    _createLayout:function() {
      this.set({
        modal:true,
        padding:3,
        showClose:true,
        showMaximize:false,
        showMinimize:false
      });
      this.setLayout(new qx.ui.layout.VBox(5));
      this.setResizable(false,true,false,false);
      var comp=new qx.ui.container.Composite();
      var layout=new qx.ui.layout.Grid(5,5);
      layout.setColumnFlex(1,1);
      comp.setLayout(layout);
      this._initKeyTypes();
      this._initKeyCiphers();
      this._edit_key_name=new qx.ui.form.TextField();
      this._edit_key_description=new qx.ui.form.TextField();
      this._edit_key_type=new qx.ui.form.SelectBox();
      for (var i in this._dict_key_type) {
        this._edit_key_type.add(this._dict_key_type[i]);
      }
      this._edit_key_bits=new qx.ui.form.TextField();
      this._edit_key_cipher=new qx.ui.form.SelectBox();
      for (var i in this._dict_key_ciphers) {
        this._edit_key_cipher.add(this._dict_key_ciphers[i]);
      }
      this._edit_key_cipher.addListener("changeSelection",this._selCipherChanged,this)
      this._edit_key_cipher.setSelection([this._dict_key_ciphers["None"]]);
      this._edit_key_passphrase=new qx.ui.form.TextField();
      comp.add(new qx.ui.basic.Label("Keyname"),{row:0,column:0});
      comp.add(new qx.ui.basic.Label("Description"),{row:1,column:0});
      comp.add(new qx.ui.basic.Label("Type"),{row:2,column:0});
      comp.add(new qx.ui.basic.Label("Bits"),{row:3,column:0});
      comp.add(new qx.ui.basic.Label("Cipher"),{row:4,column:0});
      comp.add(new qx.ui.basic.Label("Passphrase"),{row:5,column:0});
      comp.add(this._edit_key_name,{row:0,column:1});
      comp.add(this._edit_key_description,{row:1,column:1});
      comp.add(this._edit_key_type,{row:2,column:1});
      comp.add(this._edit_key_bits,{row:3,column:1});
      comp.add(this._edit_key_cipher,{row:4,column:1});
      comp.add(this._edit_key_passphrase,{row:5,column:1});
      if (this._edit_key_cipher.getSelection()[0]==this._dict_key_ciphers["None"]) {
        this._edit_key_passphrase.setEnabled(false);
      } else {
        this._edit_key_passphrase.setEnabled(true);
      }
      this.add(comp,{flex:1});
      this.add(this._initializeButtonBar());
    },
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
    _initKeyTypes:function() {
      this._dict_key_type={};
      this._dict_key_type["116"]=new qx.ui.form.ListItem("DSA",null,"116");
      this._dict_key_type["6"]=new qx.ui.form.ListItem("RSA",null,"6");
    },
    _initKeyCiphers:function() {
      this._dict_key_ciphers={};
      this._dict_key_ciphers["None"]=new qx.ui.form.ListItem("None",null,"None");
      this._dict_key_ciphers["des"]=new qx.ui.form.ListItem("DES",null,"des");
      this._dict_key_ciphers["des3"]=new qx.ui.form.ListItem("DES 3",null,"des3");
      this._dict_key_ciphers["aes128"]=new qx.ui.form.ListItem("AES 128",null,"aes128");
      this._dict_key_ciphers["aes192"]=new qx.ui.form.ListItem("AES 192",null,"aes192");
      this._dict_key_ciphers["aes256"]=new qx.ui.form.ListItem("AES 256",null,"aes256");
    },
    _selCipherChanged:function(e) {
      if ( this._edit_key_cipher.getSelection()[0]== this._dict_key_ciphers["None"]) {
        this._edit_key_passphrase.setEnabled(false);
        this._edit_key_passphrase.setValue(null);
      } else {
        this._edit_key_passphrase.setEnabled(true);
      }
    },
    _clkBtnOk:function(e) {
      var data={};
      data["keyname"]=this._edit_key_name.getValue();
      data["description"]=this._edit_key_description.getValue();
      data["bits"]=this._edit_key_bits.getValue();
      data["cipher"]=this._edit_key_cipher.getSelection()[0].getModel();
      data["passphrase"]=this._edit_key_passphrase.getValue();
      data["type"]=this._edit_key_type.getSelection()[0].getModel();
      this.fireDataEvent("addData",data);
      this.close();
    },
    _clkBtnCancel:function(e) {
      this.close();
    },
    setData:function(data) {
      this._edit_key_name.setValue(null);
      this._edit_key_description.setValue(null);
      this._edit_key_passphrase.setValue(null);
      this._edit_key_bits.setValue(null);
    }
  }
});