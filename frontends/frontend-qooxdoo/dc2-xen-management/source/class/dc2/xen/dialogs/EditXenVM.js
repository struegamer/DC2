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


qx.Class.define("dc2.xen.dialogs.EditXenVM",
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
  members:{
    _session_id:null,
    _xen_host:null,
    _vm_id:null,
    _xenvm_model:null,
    _edit_vm_name_label:null,
    _edit_vm_name_description:null,
    _edit_vm_tags:null,
    _edit_vm_is_a_snapshot:null,
    _edit_vm_is_a_template:null,
    _edit_vm_is_control_domain:null,
    _edit_network_list:null,
    _edit_vm_network_list:null,
    _network_model:null,
    _createLayout:function() {
      this.set({
        modal:true,
        padding:3,
        showClose:true,
        showMaximize:false,
        showMinimize:false
      });
      this._initializeModels();
      this.setLayout(new qx.ui.layout.VBox(5));
      this.setResizable(false,true,true,false);
      var comp=new qx.ui.container.Composite();
      var layout=new qx.ui.layout.VBox(5);
      comp.setLayout(layout);

      var tabView=new qx.ui.tabview.TabView();
      tabView.add(this._initializeCommonPage());
      tabView.add(this._initializeVIFPage(),{flex:1});
      comp.add(tabView);
      this.add(comp,{flex:1});
      this.add(this._initializeButtonBar());
    },
    _initializeModels:function() {
      this._xenvm_model=new dc2.xen.models.XenVMS(dc2.helpers.BrowserCheck.RPCUrl(false));
      this._network_model=new dc2.xen.models.XenNetwork(dc2.helpers.BrowserCheck.RPCUrl(false));
    },
    _initializeCommonPage:function() {
      var page=new qx.ui.tabview.Page("General");
      var layout=new qx.ui.layout.Grid(5,5);
      page.setLayout(layout);
      layout.setColumnFlex(1,1);

      this._edit_vm_name_label=new qx.ui.form.TextField();
      this._edit_vm_name_description=new qx.ui.form.TextArea();
      this._edit_vm_name_description.setWrap(true);
      this._edit_vm_tags=new qx.ui.form.List();
      this._edit_vm_is_a_snapshot=new qx.ui.form.CheckBox();
      this._edit_vm_is_a_template=new qx.ui.form.CheckBox();
      this._edit_vm_is_control_domain=new qx.ui.form.CheckBox();

      page.add(new qx.ui.basic.Label("Name"),{row:0,column:0});
      page.add(new qx.ui.basic.Label("Description"),{row:1,column:0});
      page.add(new qx.ui.basic.Label("Tags"),{row:2,column:0});
      page.add(new qx.ui.basic.Label("Is Template"),{row:3,column:0});
      page.add(new qx.ui.basic.Label("Is Snapshot"),{row:4,column:0});
      page.add(new qx.ui.basic.Label("Is Control Domain"),{row:5,column:0});
      page.add(this._edit_vm_name_label,{row:0,column:1});
      page.add(this._edit_vm_name_description,{row:1,column:1});
      page.add(this._edit_vm_tags,{row:2,column:1});
      page.add(this._edit_vm_is_a_template,{row:3,column:1});
      page.add(this._edit_vm_is_a_snapshot,{row:4,column:1});
      page.add(this._edit_vm_is_control_domain,{row:5,column:1});
      return(page);
    },
    _initializeVIFPage:function() {
      var page=new qx.ui.tabview.Page("Associated Networks");
      var layout=new qx.ui.layout.HBox(5);
      page.setLayout(layout);

      this._edit_network_list=new qx.ui.form.List();
      this._edit_vm_network_list=new qx.ui.form.List();

      var comp1=new qx.ui.container.Composite(new qx.ui.layout.VBox(5));
      comp1.add(new qx.ui.basic.Label("Host Network List"));
      comp1.add(this._edit_network_list);

      var comp2=new qx.ui.container.Composite(new qx.ui.layout.VBox(5));
      comp2.add(new qx.ui.basic.Label("VM Attached Networks"));
      comp2.add(this._edit_vm_network_list);

      page.add(comp1,{flex:1});
      page.add(comp2,{flex:1});
      return(page);

    },
    _fillHostNetworkList:function() {
      console.log("_fillHostNetworkList");
      if (this._session_id != null && this._xen_host != null) {
        console.log("after check");
        var host_network_list=this._network_model.getAll();
        console.log(host_network_list);
        this._edit_network_list.removeAll();
        if (host_network_list.length>0) {
          for (var i=0;i<host_network_list.length;i++) {
            this._edit_network_list.add(new qx.ui.form.ListItem(host_network_list[i]["name_label"],null,host_network_list[i]["network_id"]));
          }
        }

      }
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
    /*
     * Public Methods
     */
    setData:function(data) {
      if (data != null) {
        this._session_id=data["session_id"];
        this._xen_host=data["xen_host"];
        this._vm_id=data["vm_id"];
        this._initializeModels();
        this._xenvm_model.setSessionInfos({"session_id":this._session_id,"xen_host":this._xen_host,"vmtype":"vms"});
        this._network_model.setSessionInfos({"session_id":this._session_id,"xen_host":this._xen_host});
        var result=this._xenvm_model.getVMRecord(this._vm_id);
        this._edit_vm_name_label.setValue(result["name_label"]);
        this._edit_vm_name_description.setValue(result["name_description"]);
        this._edit_vm_tags.removeAll();
        if (result["tags"].length>0) {
          for (var i=0;i<result["tags"].length;i++) {
            this._edit_vm_tags.add(new qx.ui.form.ListItem(result["tags"][i],null,result["tags"][i]));
          }
        }
        this._fillHostNetworkList();
        this._edit_vm_is_a_template.setValue(result["is_a_template"]);
        this._edit_vm_is_a_snapshot.setValue(result["is_a_snapshot"]);
        this._edit_vm_is_control_domain.setValue(result["is_control_domain"]);
      }
    }
  }
});
