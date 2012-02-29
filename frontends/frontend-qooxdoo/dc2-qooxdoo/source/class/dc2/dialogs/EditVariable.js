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

qx.Class.define("dc2.dialogs.EditVariable",
{
  extend: qx.ui.window.Window,
  construct:function() {
    this.base(arguments);
    this._createContent();
  },
  events: {
    'addData':"qx.event.type.Data",
    'updateData':"qx.event.type.Data"
  },    
  members: {
    _edit_variable_name:null,
    _edit_variable_value:null,
    _createContent:function() {
      this.set({
        modal:false,
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
      this._edit_variable_name=new qx.ui.form.TextField();
      this._edit_variable_value=new qx.ui.form.TextField();
      comp.add(new qx.ui.basic.Label("Name"),{row:0,column:0});
      comp.add(new qx.ui.basic.Label("Value"),{row:1,column:0});
      comp.add(this._edit_variable_name,{row:0,column:1});
      comp.add(this._edit_variable_value,{row:1,column:1});
      this.add(comp,{flex:1});
      this.add(this._createButtonBar());
    },
    _createButtonBar:function() {
      var comp=new qx.ui.container.Composite(new qx.ui.layout.HBox(5).set({alignX:'right'}));
      var btnOk=new qx.ui.form.Button('Ok','icon/16/actions/dialog-ok.png');
      var btnCancel=new qx.ui.form.Button('Cancel','icon/16/actions/dialog-cancel.png');
      btnOk.addListener("execute",this._clkBtnOk,this);
      btnCancel.addListener("execute",this._clkBtnCancel,this);
      comp.add(btnCancel);
      comp.add(btnOk);
      return(comp);            
    },
    _clkBtnOk:function(e) {
      var data={};
      data["name"]=this._edit_variable_name.getValue();
      data["value"]=this._edit_variable_value.getValue();      
      this.fireDataEvent("updateData",data);
      this.close();
    },
    _clkBtnCancel:function(e) {
      this.close();
    },
    setData:function(data) {
      if (data != null) {
        if (data["name"]!="NewVariable") {
          this._edit_variable_name.setEnabled(false);
        } else {
          this._edit_variable_name.setEnabled(true);
        }        
        this._edit_variable_name.setValue(data["name"]);
        this._edit_variable_value.setValue(data["value"]);
      }
    }
  }
});
