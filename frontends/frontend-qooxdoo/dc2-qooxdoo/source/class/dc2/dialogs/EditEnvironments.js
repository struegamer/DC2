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



qx.Class.define("dc2.dialogs.EditEnvironments",
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
    _edit_env_id:null,
    _edit_env_name:null,
    _edit_env_description:null,
    _tbl_variables:null,
    _tbl_model_variables:null,
    _tbl_model_data:null,
    _createContent:function() {
      //
      // Set defaults for window
      //

      this.set({
        modal:false,
        padding:3,
        showClose:true,
        showMaximize:false,
        showMinimize:false
      });
      this.setWidth(600);
      this.setLayout(new qx.ui.layout.VBox(5));
      this.setResizable(false,true,true,false);
      this._edit_env_name=new qx.ui.form.TextField();
      this._edit_env_description=new qx.ui.form.TextField();
      this._tbl_variables=new qx.ui.table.Table();
      this._tbl_model_variables=new qx.ui.table.model.Simple();
      this._tbl_model_variables.setColumnIds(["name","value"]);
      this._tbl_model_variables.setColumns(["Name","Value"]);
      this._tbl_variables.setTableModel(this._tbl_model_variables);

      var comp=new qx.ui.container.Composite();
      var layout=new qx.ui.layout.Grid(5,5);
      layout.setColumnFlex(1,1);
      layout.setRowFlex(2,1);
      layout.setRowFlex(3,1);
      layout.setRowFlex(4,1);
      comp.setLayout(layout);
      comp.add(new qx.ui.basic.Label("Name"),{row:0,column:0});
      comp.add(new qx.ui.basic.Label("Description"),{row:1,column:0});
      comp.add(new qx.ui.basic.Label("Variables"),{row:2,column:0,colSpan:2});
      comp.add(this._edit_env_name,{row:0,column:1});
      comp.add(this._edit_env_description,{row:1,column:1});
      comp.add(this._createTableButtonBar(),{row:3,column:0,colSpan:2});
      comp.add(this._tbl_variables,{row:4,column:0,colSpan:2});
      this.add(comp,{flex:1});
      this.add(this._createButtonBar());
      this._tbl_variables.addListener("cellDblclick",this._cellDblclick,this);

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
    _createTableButtonBar:function() {
      var comp=new qx.ui.container.Composite(new qx.ui.layout.HBox(5)).set({alignX:'left'});
      var btnAdd=new qx.ui.form.Button("Add","icon/16/actions/list-add.png");
      var btnDelete=new qx.ui.form.Button("Delete","icon/16/actions/list-remove.png");
      btnAdd.addListener("execute",this._clkBtnAdd,this);
      btnDelete.addListener("execute",this._clkBtnDelete,this);
      comp.add(btnAdd);
      comp.add(btnDelete);
      return (comp);
    },
    _clkBtnAdd:function(e) {
      var data={};
      data["name"]="NewVariable";
      data["value"]="New Value";
      var editVarDlg=new dc2.dialogs.EditVariable();
      editVarDlg.center();
      editVarDlg.setData(data);
      editVarDlg.addListener("close",this._closeWindow,this);
      editVarDlg.addListener("updateData",this._addVariables,this);
      editVarDlg.show();
      this.setEnabled(false);
    },
    _cellDblclick:function(e) {
        var rowdata=this._tbl_model_variables.getRowDataAsMap(this._tbl_variables.getFocusedRow());
        var editVarDlg=new dc2.dialogs.EditVariable();
        editVarDlg.setData(rowdata);
        editVarDlg.addListener("close",this._closeWindow,this);
        editVarDlg.addListener("updateData",this._updateVariables,this);
        editVarDlg.show();
        this.setEnabled(false);

    },
    _clkBtnDelete:function(e) {
        var row=this._tbl_variables.getFocusedRow();
        delete this._tbl_model_data[row];
        this._tbl_model_variables.removeRows(row,1);

    },
    _clkBtnOk:function(e) {
      var data={};
      data["_id"]=this._edit_env_id;
      data["name"]=this._edit_env_name.getValue();
      data["description"]=this._edit_env_description.getValue();
      data["variables"]=this._tbl_model_variables.getDataAsMapArray();
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
    _closeWindow:function(e) {
      this.setEnabled(true);
    },
    _addVariables:function(e) {
      if (this._tbl_model_data != null) {
        var found=false;
        for (var i=0; i<this._tbl_model_data.length;i++) {
            if (this._tbl_model_data[i]["name"]==e.getData()["name"]) {
                found=true;
                break;
            }
        }
        if (found != true) {
          this._tbl_model_data.push({"name":e.getData()["name"],"value":e.getData()["value"]});
          this._tbl_model_variables.setDataAsMapArray(this._tbl_model_data);
        }
      } else {
        this._tbl_model_data=new Array();
        this._tbl_model_data.push({"name":e.getData()["name"],"value":e.getData()["value"]});
        this._tbl_model_variables.setDataAsMapArray(this._tbl_model_data);
      }
    },
    _updateVariables:function(e) {
      if (this._tbl_model_data != null) {
          var found=false;
          var index=-1;
          for (var i=0; i<this._tbl_model_data.length;i++) {
              if (this._tbl_model_data[i]["name"]==e.getData()["name"]) {
                  found=true;
                  index=i;
                  break;
              }
          }
          if (found == true) {
            this._tbl_model_data[index]["name"]=e.getData()["name"]
            this._tbl_model_data[index]["value"]=e.getData()["value"];
            this._tbl_model_variables.setDataAsMapArray(this._tbl_model_data);
          }
      }
    },
    setData:function(data) {
        if (data != null) {
            this._edit_env_id=data["_id"];
            this._edit_env_name.setValue(data["name"]);
            this._edit_env_description.setValue(data["description"]);
            this._tbl_model_data=data["variables"];
            if (this._tbl_model_data != null) {
                this._tbl_model_variables.setDataAsMapArray(this._tbl_model_data);
            } else {
                this._tbl_model_variables.setDataAsMapArray([]);
            }
      }
    }
  }
});