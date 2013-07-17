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
qx.Class.define("cs2.frontend.dialogs.SSLKeyView",
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
    _edit_key_pem_contents:null,
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
      layout.setRowFlex(3,1);
      comp.setLayout(layout);
      this._edit_key_name=new qx.ui.basic.Label();
      this._edit_key_description=new qx.ui.basic.Label();
      this._edit_key_pem_contents=new qx.ui.form.TextArea().set({width:400,height:300});
      this._edit_key_pem_contents.setReadOnly(true);
      comp.add(new qx.ui.basic.Label("Keyname"),{row:0,column:0});
      comp.add(new qx.ui.basic.Label("Description"),{row:1,column:0});
      comp.add(new qx.ui.basic.Label("PEM File Contents"),{row:2,column:0});
      comp.add(this._edit_key_name,{row:0,column:1});
      comp.add(this._edit_key_description,{row:1,column:1});
      comp.add(this._edit_key_pem_contents,{row:3,column:0,colSpan:2});
      this.add(comp,{flex:1});
      this.add(this._initializeButtonBar());
    },
    _initializeButtonBar:function() {
      var comp=new qx.ui.container.Composite(new qx.ui.layout.HBox(5).set({alignX:'right'}));
      var btnOk=new qx.ui.form.Button('Close','icon/16/actions/dialog-ok.png');
      btnOk.addListener("execute",this._clkBtnOk,this);
      comp.add(btnOk);
      return(comp);
    },
    _clkBtnOk:function(e) {
      this.close();
    },
    setData:function(data) {
      if (data != null) {
        this._edit_key_name.setValue(data["keyname"]);
        this._edit_key_description.setValue(data["description"]);
        this._edit_key_pem_contents.setValue(data["key_pem"]);
      }
    }
  }
});