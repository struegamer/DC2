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

qx.Class.define("dc2.dialogs.EditDefaultBootmethods",
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
    _edit_id:null,
    _edit_hardware_type:null,
    _edit_pxe_bootmethod:null,
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
      this._edit_hardware_type=new qx.ui.form.TextField();
      this._edit_hardware_type.setEnabled(false);
      this._edit_pxe_bootmethod=new qx.ui.form.SelectBox();
      this._fillBootmethods();
      comp.add(new qx.ui.basic.Label("Hardware Type"),{row:0,column:0});
      comp.add(new qx.ui.basic.Label("PXE Bootmethod"),{row:1,column:0});
      comp.add(this._edit_hardware_type,{row:0,column:1});
      comp.add(this._edit_pxe_bootmethod,{row:1,column:1});
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
    _fillBootmethods:function() {
      this._edit_pxe_bootmethod.add(new qx.ui.form.ListItem("None",null,"none"));
      this._edit_pxe_bootmethod.add(new qx.ui.form.ListItem("LOCALBOOT 0",null,"localboot"));
      this._edit_pxe_bootmethod.add(new qx.ui.form.ListItem("CHAIN.C32",null,"chain.c32"));
      this._edit_pxe_bootmethod.add(new qx.ui.form.ListItem("LOCALBOOT -1",null,"localboot-1"));
    },
    _clkBtnCancel:function(e) {
      this.close();
    },
    _clkBtnOk:function(e) {
      var data={};
      data["_id"]=this._edit_id;
      data["hardware_type"]=this._edit_hardware_type.getValue();
      data["pxe_bootmethod"]=this._edit_pxe_bootmethod.getSelection()[0].getModel();
      if (data["_id"]!=null && data["_id"]!="") {
        this.fireDataEvent("updateData",data);
      } else {
        this.fireDataEvent("addData",data);
      }
      this.close();
    },
    setData:function(data) {
      if (data != null) {
        this._edit_id=data["_id"];
        this._edit_hardware_type.setValue(data["hardware_type"]);
        this._edit_pxe_bootmethod.setModelSelection([data["pxe_bootmethod"]]);
      }
    }
  }
})  
