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


qx.Class.define("dc2.dialogs.EditRIB",
{
  extend: qx.ui.window.Window,
  construct:function() {
    this.base(arguments);
    this._initRIBTypes();
    this._createLayout();
  },

  events: {
    'addData':"qx.event.type.Data",
    'updateData':"qx.event.type.Data"
  },
  members: {
    _rib_id:null,
    _server_id:null,
    _editRIBType:null,
    _editRIBIP:null,
    _ribTypes:null,
    _createLayout:function() {
      this.setLayout(new qx.ui.layout.VBox(5));
      this.set({
        modal:true,
        padding:3,
        showClose:true,
        showMaximize:false,
        showMinimize:false
      });

      var comp=new qx.ui.container.Composite();
      var layout=new qx.ui.layout.Grid(5,5);
      this.setResizable(false,true,true,false);
      layout.setColumnFlex(1,1);
      comp.setLayout(layout);
      this._editRIBType=new qx.ui.form.SelectBox();
      this._editRIBIP=new qx.ui.form.TextField();
      this._editRIBIP.addListener("focusin",this._editFieldFocus,this);
      comp.add(new qx.ui.basic.Label("RIB Type"),{row:0,column:0});
      comp.add(new qx.ui.basic.Label("RIB IP"),{row:1,column:0});
      comp.add(this._editRIBType,{row:0,column:1});
      comp.add(this._editRIBIP,{row:1,column:1});
      for (var item in this._ribTypes) {
        this._editRIBType.add(this._ribTypes[item]);
      }

      this.add(comp,{flex:1});
      this.add(this._initializeButtonBar());
    },
    _initRIBTypes:function() {
      this._ribTypes={};
      this._ribTypes["ilo1"]=new qx.ui.form.ListItem("HP ILO 1","","ilo1");
      this._ribTypes["ilo2"]=new qx.ui.form.ListItem("HP ILO 2","","ilo2");
      this._ribTypes["ilo3"]=new qx.ui.form.ListItem("HP ILO 3","","ilo3");
      this._ribTypes["fsc"]=new qx.ui.form.ListItem("FSC RIB","","fsc");
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
    _clkBtnOk:function(e) {
      var data={};
      data["_id"]=this._rib_id;
      data["server_id"]=this._server_id;
      data["remote_type"]=this._editRIBType.getSelection()[0].getModel();
      data["remote_ip"]=this._editRIBIP.getValue();
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
    _editFieldFocus:function(e) {
      if (e.getTarget().classname == "qx.ui.form.TextField") {
        e.getTarget().setTextSelection(0);
      }
    },
    setData:function(data) {
      if (data != null) {
        this._rib_id=data["_id"];
        this._server_id=data["server_id"];
        this._editRIBIP.setValue(data["remote_ip"]);
        if (data["remote_type"]=="ilo") {
          data["remote_type"]="ilo2";
        }
        this._editRIBType.setSelection([this._ribTypes[data["remote_type"]]]);
      }
    }

  }

});

