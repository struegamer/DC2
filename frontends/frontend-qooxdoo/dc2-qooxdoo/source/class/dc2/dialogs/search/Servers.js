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

qx.Class.define("dc2.dialogs.search.Servers",
{
  extend: dc2.widgets.DialogWidget,
  construct:function() {
    this.base(arguments);
  },
  members: {
    __editSerialNumber:null,
    __editManufacturer:null,
    __editProductName:null,
    __editLocation:null,
    __editAssetTag:null,
    __editUUID:null,
    _createLayout:function() {
      var comp=new qx.ui.container.Composite();
      var layout=new qx.ui.layout.Grid(5,10);
      layout.setColumnFlex(1,5);
      comp.setLayout(layout);
      this.__editUUID=new qx.ui.form.TextField();
      this.__editSerialNumber=new qx.ui.form.TextField();
      this.__editManufacturer=new qx.ui.form.TextField();
      this.__editProductName=new qx.ui.form.TextField();
      this.__editLocation=new qx.ui.form.TextField();
      this.__editAssetTag=new qx.ui.form.TextField();
      comp.add(new qx.ui.basic.Label("UUID"),{row:0,column:0});
      comp.add(new qx.ui.basic.Label("Serial Number"),{row:1,column:0});
      comp.add(new qx.ui.basic.Label("Manufacturer"),{row:2,column:0});
      comp.add(new qx.ui.basic.Label("Product Name"),{row:3,column:0});
      comp.add(new qx.ui.basic.Label("Location"),{row:4,column:0});
      comp.add(new qx.ui.basic.Label("Asset Tag"),{row:5,column:0});
      comp.add(this.__editUUID,{row:0,column:1});
      comp.add(this.__editSerialNumber,{row:1,column:1});
      comp.add(this.__editManufacturer,{row:2,column:1});
      comp.add(this.__editProductName,{row:3,column:1});
      comp.add(this.__editLocation,{row:4,column:1});
      comp.add(this.__editAssetTag,{row:5,column:1});
      return comp;
    },
    _getData:function() {
      var data=null;
      if (this.__editUUID.getValue() != null && this.__editUUID.getValue() != "") {
        if (data == null) {
          data={};
        }
        data["uuid"]=this.__editUUID.getValue();
      }
      if (this.__editSerialNumber.getValue() != null && this.__editSerialNumber.getValue() != "") {
        if (data == null) {
          data={};
        }
       data["serial_no"]=this.__editSerialNumber.getValue();
      }
      if (this.__editProductName.getValue() != null && this.__editProductName.getValue() != "") {
        if (data == null ) {
          data={};
        }
        data["product_name"]=this.__editProductName.getValue();
      }
      if (this.__editManufacturer.getValue() != null && this.__editManufacturer.getValue() != "") {
        if (data == null ) {
          data={};
        }
        data["manufacturer"]=this.__editManufacturer.getValue();
      }
      if (this.__editLocation.getValue() != null && this.__editLocation.getValue()  != "") {
        if (data == null ) {
          data={};
        }
        data["location"]=this.__editLocation.getValue();
      }
      if (this.__editAssetTag.getValue() != null && this.__editAssetTag.getValue() != "") {
        if (data == null ) {
          data={};
        }
        data["asset_tags"]=this.__editAssetTag.getValue();
      }
      return data;
    }
  }
});
