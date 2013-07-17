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

qx.Class.define("dc2.dialogs.EditServer",
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
      _editServerId:null,
      _editServerUUID:null,
      _editServerSerialNo:null,
      _editServerProductName:null,
      _editServerManufacturer:null,
      _editServerLocation:null,
      _editServerAssetTags:null,
      _tbl_mac_addr:null,
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
        this.setLayout(new qx.ui.layout.VBox(5));
        this.setResizable(false,true,true,false);

        //
        // Initialize Widgets
        //

        this._initializeEditWidgets();
        var tabView=this._initializeTabView();
        var buttonBar=this._initializeButtonBar();

        //
        // Add widgets to window layout
        //

        this.add(tabView,{flex:1});
        this.add(buttonBar);

      },
      _initializeEditWidgets:function() {
        this._editServerUUID=new qx.ui.form.TextField();
        this._editServerSerialNo=new qx.ui.form.TextField();
        this._editServerProductName=new qx.ui.form.TextField();
        this._editServerManufacturer=new qx.ui.form.TextField();
        this._editServerLocation=new qx.ui.form.TextField();
        this._editServerAssetTags=new qx.ui.form.TextField();
      },
      _initializeTabView:function() {
        var tabView=new qx.ui.tabview.TabView();
        tabView.setWidth(600);
        tabView.add(this._createGeneralServerPage());
        tabView.add(this._createMacAddrServerPage());
        tabView.add(this._createRIBServerPage());
        return(tabView);
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
      _createGeneralServerPage:function() {
        var page=new qx.ui.tabview.Page("General");
        var layout=new qx.ui.layout.Grid(5,5);

        layout.setColumnFlex(1,1);
        //layout.setRowFlex(0,1);
        //layout.setRowFlex(1,1);
        //layout.setRowFlex(2,1);
        //layout.setRowFlex(3,1);
        //layout.setRowFlex(4,1);
        //layout.setRowFlex(5,1);
        page.setLayout(layout);
        page.add(new qx.ui.basic.Label("UUID"),{row:0,column:0});
        page.add(new qx.ui.basic.Label("Serial Number"),{row:1,column:0});
        page.add(new qx.ui.basic.Label("Product Name"),{row:2,column:0});
        page.add(new qx.ui.basic.Label("Manufacturer"),{row:3,column:0});
        page.add(new qx.ui.basic.Label("Location"),{row:4,column:0});
        page.add(new qx.ui.basic.Label("Asset Tags"),{row:5,column:0});

        page.add(this._editServerUUID,{row:0,column:1});
        page.add(this._editServerSerialNo,{row:1,column:1});
        page.add(this._editServerProductName,{row:2,column:1});
        page.add(this._editServerManufacturer,{row:3,column:1});
        page.add(this._editServerLocation,{row:4,column:1});
        page.add(this._editServerAssetTags,{row:5,column:1});
        return(page);
      },
      _createMacAddrServerPage:function() {
        var page=new qx.ui.tabview.Page("Network Interfaces");
        var layout=new qx.ui.layout.VBox(5);
        page.setLayout(layout);
        this._tbl_mac_addr=new dc2.models.MacAddr(dc2.helpers.BrowserCheck.RPCUrl(false));
        var mac_edit_dlg=new dc2.dialogs.EditMAC();
        var mac_table_options = {
          enableAddEntry:true,
          enableDeleteEntry:true,
          enableReloadEntry:true,
          enableEditEntry:true,
          tableModel:this._tbl_mac_addr,
          editDialog:mac_edit_dlg,
          addDialog:mac_edit_dlg
        };
        var tableWidget=new dc2.widgets.TableWidget(mac_table_options);
        tableWidget.showData();
        page.add(tableWidget);
        return(page);
      },
      _createRIBServerPage:function() {
        var page=new qx.ui.tabview.Page("Remote Insight Boards");
        var layout=new qx.ui.layout.VBox(5);
        page.setLayout(layout);
        this._tbl_ribs=new dc2.models.RIB(dc2.helpers.BrowserCheck.RPCUrl(false));
        var rib_edit_dialog=new dc2.dialogs.EditRIB();
        var rib_table_options={
          enableAddEntry:true,
          enableDeleteEntry:true,
          enableReloadEntry:true,
          enableEditEntry:true,
          tableModel:this._tbl_ribs,
          editDialog:rib_edit_dialog,
          addDialog:rib_edit_dialog
        };
        var tableWidget=new dc2.widgets.TableWidget(rib_table_options);
        tableWidget.showData();
        page.add(tableWidget);
        return(page);
      },
      _clkBtnOk:function(e) {
        var data={};
        data["_id"]=this._editServerId;
        data["uuid"]=this._editServerUUID.getValue();
        data["serial_no"]=this._editServerSerialNo.getValue();
        data["product_name"]=this._editServerProductName.getValue();
        data["manufacturer"]=this._editServerManufacturer.getValue();
        data["location"]=this._editServerLocation.getValue();
        data["asset_tags"]=this._editServerAssetTags.getValue();
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
        if ('_id' in data) {
          this._editServerId=data["_id"];
          this._tbl_mac_addr.listData({"server_id":this._editServerId});
          this._tbl_ribs.listData({"server_id":this._editServerId});
        }
        if ('uuid' in data) {
          this._editServerUUID.setValue(data["uuid"]);
        }
        if ('serial_no' in data) {
          this._editServerSerialNo.setValue(data["serial_no"]);
        }
        if ('product_name' in data) {
          this._editServerProductName.setValue(data["product_name"]);
        }
        if ('manufacturer' in data) {
          this._editServerManufacturer.setValue(data["manufacturer"]);
        }
        if ('location' in data) {
          this._editServerLocation.setValue(data["location"]);
        }
        if ('asset_tags' in data) {
          this._editServerAssetTags.setValue(data["asset_tags"]);
        }
        this._checkForUpdate();
      },
      _checkForUpdate:function() {
        if (this._editServerId != "" && this._editServerId != null) {
          this._editServerUUID.setReadOnly(true);
          this._editServerSerialNo.setReadOnly(true);
          this._editServerProductName.setReadOnly(true);
          this._editServerManufacturer.setReadOnly(true);
          this._editServerLocation.setReadOnly(false);
          this._editServerAssetTags.setReadOnly(false);

          this._editServerUUID.setEnabled(false);
          this._editServerSerialNo.setEnabled(false);
          this._editServerProductName.setEnabled(false);
          this._editServerManufacturer.setEnabled(false);
          this._editServerLocation.setEnabled(true);
          this._editServerAssetTags.setEnabled(true);
          this._tbl_mac_addr.setServerId(this._editServerId);
          this._tbl_ribs.setServerId(this._editServerId);
        } else {
          this._editServerUUID.setReadOnly(false);
          this._editServerSerialNo.setReadOnly(false);
          this._editServerProductName.setReadOnly(false);
          this._editServerManufacturer.setReadOnly(false);
          this._editServerLocation.setReadOnly(false);
          this._editServerAssetTags.setReadOnly(false);

          this._editServerUUID.setEnabled(true);
          this._editServerSerialNo.setEnabled(true);
          this._editServerProductName.setEnabled(true);
          this._editServerManufacturer.setEnabled(true);
          this._editServerLocation.setEnabled(true);
          this._editServerAssetTags.setEnabled(true);


        }
      }
    }
  }
);
