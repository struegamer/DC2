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

qx.Class.define("dc2.dialogs.ServerDialog",
{
  extend: qx.ui.window.Window,
  construct:function() {
    this.base(arguments);
    this.createContent();
  },
  events: {
    'dataChanged':"qx.event.type.Data",
    'newEntry':"qx.event.type.Data"
  },
  members:{
    __editServerId:null,
    __editServerUUID:null,
    __editServerSerial:null,
    __editServerProductName:null,
    __editServerManufacturer:null,
    __editServerLocation:null,
    __editServerAssetTags:null,
    __macTable:null,
    __ribTable:null,
    __macTableModel:null,
    __ribTableModel:null,
    createContent:function() {
      this.set({
	      modal:true,
	      padding:3,
      	showClose:true,
        showMaximize:false,
        showMinimize:false
      });
      this.setLayout(new qx.ui.layout.VBox(5));
      this.addListener("keypress",this._onEnter,this);
      // Create textFields
      this.__editServerUUID=new qx.ui.form.TextField();
      this.__editServerSerial=new qx.ui.form.TextField();
      this.__editServerProductName=new qx.ui.form.TextField();
      this.__editServerManufacturer=new qx.ui.form.TextField();
      this.__editServerLocation=new qx.ui.form.TextField();
      this.__editServerAssetTags=new qx.ui.form.TextField();

      var tabView=new qx.ui.tabview.TabView();
      tabView.setWidth(500);
      this.setResizable(false,false,false,false);
      tabView.add(this._createGeneralPage());
      tabView.add(this._createNetworkPage());
      tabView.add(this._createRibPage());

      var comp=new qx.ui.container.Composite(new qx.ui.layout.HBox(5).set({alignX:'right'}));
      var btn1=new qx.ui.form.Button("Cancel","icon/16/actions/dialog-cancel.png");
      var btn2=new qx.ui.form.Button("Ok","icon/16/actions/dialog-ok.png");
      comp.add(btn1);
      comp.add(btn2);
      btn1.addListener("execute",this._clkCancel,this);
      btn2.addListener("execute",this._clkOk,this);
      this.add(tabView);
      this.add(comp);
    },
    _createGeneralPage:function() {
      var page=new qx.ui.tabview.Page("General");
      var layout=new qx.ui.layout.Grid(5,5);
      layout.setColumnFlex(1,5);
      layout.setColumnFlex(2,5);
      layout.setColumnFlex(3,5);
      layout.setColumnFlex(4,5);
      layout.setRowFlex(7,3);
      page.setLayout(layout);
      // Create Labels
      page.add(new qx.ui.basic.Label("UUID"),{row:0,column:0});
      page.add(new qx.ui.basic.Label("Serial Number"),{row:1,column:0});
      page.add(new qx.ui.basic.Label("Product Name"),{row:2,column:0});
      page.add(new qx.ui.basic.Label("Manufacturer"),{row:3,column:0});
      page.add(new qx.ui.basic.Label("Location:"),{row:4,column:0});
      page.add(new qx.ui.basic.Label("Asset Tags"),{row:5,column:0});
      page.add(this.__editServerUUID,{row:0,column:1,colSpan:4});
      page.add(this.__editServerSerial,{row:1,column:1,colSpan:4});
      page.add(this.__editServerProductName,{row:2,column:1,colSpan:4});
      page.add(this.__editServerManufacturer,{row:3,column:1,colSpan:4});
      page.add(this.__editServerLocation,{row:4,column:1,colSpan:4});
      page.add(this.__editServerAssetTags,{row:5,column:1,colSpan:4});
      return page;
    },
    _createNetworkPage:function() {
      var page=new qx.ui.tabview.Page("Network Interfaces");
      var layout=new qx.ui.layout.VBox(5);
      page.setLayout(layout);
      this.__macTable=new qx.ui.table.Table();
      this.__macTable.addListener("cellDblclick",function(e) {
				    var dialog=new fai.DlgAddNIC();
				    var data={};
				    var modelData=this.__macTable.getTableModel().getRowData(this.__macTable.getFocusedRow());
				    data.mac_address=modelData.mac_addr_mac_address;
				    data.hw_dev_name=modelData.mac_addr_hw_dev_name;
				    data.mac_id=modelData.mac_addr_id;
				    dialog.setData(data);
				    this.getApplicationRoot().add(dialog);
				    dialog.addListener("evDlgOk",function(e) {
							 this.__macTableModel.updateData(e.getData());
							 dialog.destroy();
						       },this);
				    dialog.show();

				  },this);

      var comp=new qx.ui.container.Composite(new qx.ui.layout.HBox(5).set({alignX:'right'}));
      var btnAdd=new qx.ui.form.Button("Add","icon/16/actions/list-add.png");
      var btnDelete=new qx.ui.form.Button("Delete","icon/16/actions/list-remove.png");
      var btnReload=new qx.ui.form.Button("Reload","icon/16/actions/view-refresh.png");
      btnAdd.addListener("execute",function(e) {
			   var dialog=new fai.DlgAddNIC();
			   this.getApplicationRoot().add(dialog);
			   dialog.addListener("evDlgOk",function(e) {
						this.__macTableModel.addData(e.getData());
						dialog.destroy();
					      },this);
			   dialog.show();
			 },this);

      btnDelete.addListener("execute",function(e) {
			      this.__macTableModel.deleteData(this.__macTableModel.getTableModel().getRowData(this.__macTable.getFocusedRow()));
			    },this);
      btnReload.addListener("execute",function(e) {
			      this.__macTableModel.reloadData();
			    },this);
      comp.add(btnAdd);
      comp.add(btnDelete);
      comp.add(btnReload);
      page.add(comp);
      page.add(this.__macTable);
      return page;
    },
    _createRibPage:function() {
      var page=new qx.ui.tabview.Page("Remote Insight Boards");
      var layout=new qx.ui.layout.VBox(5);
      page.setLayout(layout);
      this.__ribTable=new qx.ui.table.Table();
      this.__ribTable.addListener("cellDblclick",function(e) {
				    var modelData=this.__ribTableModel.getTableModel().getRowData(this.__ribTable.getFocusedRow());
				    var dialog=new fai.DlgRIB();
				    this.getApplicationRoot().add(dialog);
				    dialog.setData(modelData);
				    dialog.addListener("evDlgOk",function(e) {
							 this.__ribTableModel.updateData(e.getData());
							 dialog.destroy();
						       },this);
				    dialog.show();
				  },this);

      var comp=new qx.ui.container.Composite(new qx.ui.layout.HBox(5).set({alignX:'right'}));
      var btnAdd=new qx.ui.form.Button("Add","icon/16/actions/list-add.png");
      var btnDelete=new qx.ui.form.Button("Delete","icon/16/actions/list-remove.png");
      var btnReload=new qx.ui.form.Button("Reload","icon/16/actions/view-refresh.png");

      btnAdd.addListener("execute",function(e) {
			   var dialog=new fai.DlgRIB();
			   this.getApplicationRoot().add(dialog);
			   dialog.addListener("evDlgOk",function(e) {
						this.__ribTableModel.addData(e.getData());
						dialog.destroy();
					      },this);
			   dialog.show();
			 },this);
      btnDelete.addListener("execute",function(e) {
			      var modelData=this.__ribTableModel.getTableModel().getRowData(this.__ribTable.getFocusedRow());
			      this.__ribTableModel.deleteData(modelData);
			    },this);
      btnReload.addListener("execute",function(e) {
			      this.__ribTableModel.reloadData();
			    },this);
      comp.add(btnAdd);
      comp.add(btnDelete);
      comp.add(btnReload);
      page.add(comp);
      page.add(this.__ribTable);
      return page;
    },
    setData:function(data) {
      this.__editServerId=data.server_id;
      this.__editServerUUID.setValue(data.server_uuid);
      this.__editServerSerial.setValue(data.server_serial_no);
      this.__editServerProductName.setValue(data.server_product_name);
      this.__editServerManufacturer.setValue(data.server_manufacturer);
      this.__editServerLocation.setValue(data.server_location);
      this.__editServerAssetTags.setValue(data.server_asset_tags);
      this._checkForUpdate();
      if (this.__macTableModel==null) {
        this.__macTableModel=new dc2.models.MacAddr(dc2.helpers.BrowserCheck.RPCUrl(false),this.__editServerId);
        this.__macTable.setTableModel(this.__macTableModel.getTableModel());
        this.__macTable.getTableColumnModel().setColumnVisible(0,false);
      } else {
        this.__macTableModel.setServerId(this.__editServerId);
      }
      if (this.__ribTableModel==null) {
        this.__ribTableModel=new dc2.models.RIB(dc2.helpers.BrowserCheck.RPCUrl(),this.__editServerId);
        this.__ribTable.setTableModel(this.__ribTableModel.getTableModel());
        this.__ribTable.getTableColumnModel().setColumnVisible(0,false);
      } else {
        this.__ribTableModel.setServerId(this.__editServerId);
      }
    },
    _checkForUpdate:function() {
      if (this.__editServerId!=0) {
        this.__editServerUUID.setReadOnly(true);
        this.__editServerSerial.setReadOnly(true);
        this.__editServerProductName.setReadOnly(true);
        this.__editServerManufacturer.setReadOnly(true);
        this.__editServerUUID.setEnabled(false);
        this.__editServerSerial.setEnabled(false);
        this.__editServerProductName.setEnabled(false);
        this.__editServerManufacturer.setEnabled(false);

        this.__editServerLocation.setReadOnly(false);
        this.__editServerAssetTags.setReadOnly(false);
      } else {
        this.__editServerUUID.setReadOnly(false);
        this.__editServerSerial.setReadOnly(false);
        this.__editServerProductName.setReadOnly(false);
        this.__editServerManufacturer.setReadOnly(false);
        this.__editServerLocation.setReadOnly(false);
        this.__editServerAssetTags.setReadOnly(false);

      }
    },
    _clkCancel:function(e) {
      this.close();
    },
    _clkOk:function(e) {
      var data={};
      data.server_id=this.__editServerId;
      data.server_uuid=this.__editServerUUID.getValue();
      data.server_serial_no=this.__editServerSerial.getValue();
      data.server_product_name=this.__editServerProductName.getValue();
      data.server_manufacturer=this.__editServerManufacturer.getValue();
      data.server_location=this.__editServerLocation.getValue();
      data.server_asset_tags=this.__editServerAssetTags.getValue();
      if (data.server_id!=0) {
        this.fireDataEvent("dataChanged",data);
      } else {
        this.fireDataEvent("newEntry",data);
      }
      this.close();
    },
    _onEnter:function(e) {
      if (e.getKeyIdentifier()=="Enter") {
        this._clkOk(e);
      } else if (e.getKeyIdentifier()=="Escape") {
        this._clkCancel(e);
      }
    }
  }
});