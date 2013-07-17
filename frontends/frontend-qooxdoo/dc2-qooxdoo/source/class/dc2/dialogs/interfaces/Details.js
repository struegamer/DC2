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


qx.Class.define("dc2.dialogs.interfaces.Details",
{
  extend: qx.ui.container.Composite,
  construct:function(server_id) {
    this.base(arguments);
    this._server_id=server_id;
    this._interface_array=[];
    this._createLayout();
  },
  events: {
    'returnData':"qx.event.type.Data"
  },
  members: {
    _server_id:null,
    _interface_data:null,
    _interface_array:null,
    _edit_interface_types:null,
    _edit_interface_inet_types:null,
    _edit_interface_name:null,
    _edit_hw_interface_names:null,
    _edit_interface_ip:null,
    _edit_interface_netmask:null,
    _edit_interface_gateway:null,
    _edit_interface_slaves:null,
    _edit_interface_vlan_raw_device:null,
    _edit_interface_pre_up:null,
    _edit_interface_pre_down:null,
    _edit_interface_post_up:null,
    _edit_interface_post_down:null,
    _compInterfaceSettings:null,
    _compInterfaceNames:null,
    _compInterfaceDetails:null,
    _compInterfaceSettings_interface_type:null,
    _compinterfaceSettings_interface_inet_type:null,
    _compinterfaceSettings_interface_ipv6_type:null,
    _compInterfaceNames_name:null,
    _compInterfaceNames_hwdevices:null,
    _compInterfaceDetails_ip:null,
    _compInterfaceDetails_netmask:null,
    _compInterfaceDetails_gateway:null,
    _compInterfaceBondingSlaves:null,
    _compInterfaceVlanRawDevice:null,
    _compInterfaceIsIpV6:null,
    _btnApply:null,
    _createLayout:function() {
      var layout=new qx.ui.layout.VBox(5);
      this.setLayout(layout);

      this._edit_interface_types=new qx.ui.form.SelectBox();
      this._edit_interface_types.addListener("changeSelection",this._evChangeSelInterfaceTypes,this)
      this._edit_interface_inet_types=new qx.ui.form.SelectBox();
      this._edit_interface_inet_types.addListener("changeSelection",this._evChangeSelInterfaceTypes,this)
      this._initializeTypes();

      this._edit_interface_name=new qx.ui.form.TextField();
      this._edit_hw_interface_names=new qx.ui.form.SelectBox();
      this._edit_interface_ip=new qx.ui.form.TextField();
      this._edit_interface_netmask=new qx.ui.form.TextField();
      this._edit_interface_gateway=new qx.ui.form.TextField();

      this._edit_interface_slaves=new qx.ui.form.List();
      this._edit_interface_slaves.setSelectionMode('multi');

      this._edit_interface_vlan_raw_device=new qx.ui.form.SelectBox();

      this._edit_interface_pre_up=new qx.ui.form.TextArea();
      this._edit_interface_pre_down=new qx.ui.form.TextArea();
      this._edit_interface_post_up=new qx.ui.form.TextArea();
      this._edit_interface_post_down=new qx.ui.form.TextArea();
      this._compInterfaceIsIpV6=new qx.ui.form.CheckBox();
      this._compInterfaceIsIpV6.setValid(false);

      var tabView=new qx.ui.tabview.TabView();
      var interfacePage=new qx.ui.tabview.Page("Interfaces");
      interfacePage.setLayout(new qx.ui.layout.VBox(5));
      var advancedPage=new qx.ui.tabview.Page("Advanced");
      advancedPage.setLayout(new qx.ui.layout.VBox(5));
      tabView.add(interfacePage);
      tabView.add(advancedPage);

      // this._initializeHWInterfaceNames();
      this._initialize_compInterfaceSettings();
      this._initialize_compInterfaceNames();
      this._initialize_compInterfaceDetails();
      this._initialize_compInterfaceBondingSlaves();
      this._initialize_compInterfaceVlanRawDevice();
      interfacePage.add(this._compInterfaceSettings);
      interfacePage.add(this._compInterfaceNames);
      interfacePage.add(this._compInterfaceDetails);
      interfacePage.add(this._compInterfaceBondingSlaves);
      interfacePage.add(this._compInterfaceVlanRawDevice);

      this._initializeAdvancedPage(advancedPage);

      var comp1=new qx.ui.container.Composite(new qx.ui.layout.HBox(5).set({alignX:'right'}));
      this._btnApply=new qx.ui.form.Button("Apply");
      this._btnApply.addListener("execute",this._btnApplyClicked,this);
      this._btnApply.setEnabled(false);
      comp1.add(this._btnApply);
      this.add(tabView,{flex:1});
      this.add(comp1);
    },
    _initializeAdvancedPage:function(page) {
      var comp1=new qx.ui.container.Composite(new qx.ui.layout.VBox(5));
      comp1.add(new qx.ui.basic.Label("Pre Up Commands"));
      comp1.add(this._edit_interface_pre_up);

      var comp2=new qx.ui.container.Composite(new qx.ui.layout.VBox(5));
      comp2.add(new qx.ui.basic.Label("Pre Down Commands"));
      comp2.add(this._edit_interface_pre_down);

      var comp3=new qx.ui.container.Composite(new qx.ui.layout.VBox(5));
      comp3.add(new qx.ui.basic.Label("Post Up Commands"));
      comp3.add(this._edit_interface_post_up);

      var comp4=new qx.ui.container.Composite(new qx.ui.layout.VBox(5));
      comp4.add(new qx.ui.basic.Label("Post Down Commands"));
      comp4.add(this._edit_interface_post_down);

      page.add(comp1,{flex:1});
      page.add(comp2,{flex:1});
      page.add(comp3,{flex:1});
      page.add(comp4,{flex:1});

    },
    _initialize_compInterfaceSettings:function() {
      this._compInterfaceSettings=new qx.ui.groupbox.GroupBox("Interface Details");
      this._compInterfaceSettings.setLayout(new qx.ui.layout.HBox(5));
      this._compInterfaceSettings_interface_type=new qx.ui.container.Composite(new qx.ui.layout.VBox(5));
      this._compInterfaceSettings_interface_type.add(new qx.ui.basic.Label("Interface Type"));
      this._compInterfaceSettings_interface_type.add(this._edit_interface_types);

      this._compinterfaceSettings_interface_inet_type=new qx.ui.container.Composite(new qx.ui.layout.VBox(5));
      this._compinterfaceSettings_interface_inet_type.add(new qx.ui.basic.Label("Inet Type"));
      this._compinterfaceSettings_interface_inet_type.add(this._edit_interface_inet_types);

      this._compinterfaceSettings_interface_ipv6_type=new qx.ui.container.Composite(new qx.ui.layout.VBox(5));
      this._compinterfaceSettings_interface_ipv6_type.add(new qx.ui.basic.Label("IPv6?"));
      this._compinterfaceSettings_interface_ipv6_type.add(this._compInterfaceIsIpV6);


      this._compInterfaceSettings.add(this._compInterfaceSettings_interface_type,{flex:1});
      this._compInterfaceSettings.add(this._compinterfaceSettings_interface_inet_type,{flex:1});
      this._compInterfaceSettings.add(this._compinterfaceSettings_interface_ipv6_type,{flex:1});

    },
    _initialize_compInterfaceNames:function() {
      this._compInterfaceNames=new qx.ui.groupbox.GroupBox("Interface Names");
      this._compInterfaceNames.setLayout(new qx.ui.layout.HBox(5));

      this._compInterfaceNames_name=new qx.ui.container.Composite(new qx.ui.layout.VBox(5));
      this._compInterfaceNames_name.add(new qx.ui.basic.Label("Name"));
      this._compInterfaceNames_name.add(this._edit_interface_name);

      this._compInterfaceNames_hwdevices=new qx.ui.container.Composite(new qx.ui.layout.VBox(5));
      this._compInterfaceNames_hwdevices.add(new qx.ui.basic.Label("HW Device Names"));
      this._compInterfaceNames_hwdevices.add(this._edit_hw_interface_names);

      this._compInterfaceNames.add(this._compInterfaceNames_name,{flex:1});
      this._compInterfaceNames.add(this._compInterfaceNames_hwdevices,{flex:1});
    },
    _initialize_compInterfaceDetails:function() {
      this._compInterfaceDetails=new qx.ui.groupbox.GroupBox("IP Details");
      this._compInterfaceDetails.setLayout(new qx.ui.layout.HBox(5));

      this._compInterfaceDetails_ip=new qx.ui.container.Composite(new qx.ui.layout.VBox(5));
      this._compInterfaceDetails_ip.add(new qx.ui.basic.Label("IP"));
      this._compInterfaceDetails_ip.add(this._edit_interface_ip);

      this._compInterfaceDetails_netmask=new qx.ui.container.Composite(new qx.ui.layout.VBox(5));
      this._compInterfaceDetails_netmask.add(new qx.ui.basic.Label("Netmask"));
      this._compInterfaceDetails_netmask.add(this._edit_interface_netmask);

      this._compInterfaceDetails_gateway=new qx.ui.container.Composite(new qx.ui.layout.VBox(5));
      this._compInterfaceDetails_gateway.add(new qx.ui.basic.Label("Gateway"));
      this._compInterfaceDetails_gateway.add(this._edit_interface_gateway);

      this._compInterfaceDetails.add(this._compInterfaceDetails_ip,{flex:1});
      this._compInterfaceDetails.add(this._compInterfaceDetails_netmask,{flex:1});
      this._compInterfaceDetails.add(this._compInterfaceDetails_gateway,{flex:1});

    },
    _initialize_compInterfaceBondingSlaves:function() {
      this._compInterfaceBondingSlaves=new qx.ui.groupbox.GroupBox("Bonding Slaves");
      this._compInterfaceBondingSlaves.setLayout(new qx.ui.layout.VBox(5));
      this._compInterfaceBondingSlaves.add(new qx.ui.basic.Label("Possible Slave Interfaces"));
      this._compInterfaceBondingSlaves.add(this._edit_interface_slaves,{flex:1});
    },
    _initialize_compInterfaceVlanRawDevice:function() {
      this._compInterfaceVlanRawDevice=new qx.ui.groupbox.GroupBox("VLAN Raw Device");
      this._compInterfaceVlanRawDevice.setLayout(new qx.ui.layout.VBox(5));
      this._compInterfaceVlanRawDevice.add(new qx.ui.basic.Label("Available Devices"));
      this._compInterfaceVlanRawDevice.add(this._edit_interface_vlan_raw_device,{flex:1});
    },
    _initializeTypes:function() {
      this._edit_interface_types.removeAll();
      this._edit_interface_types.add(new qx.ui.form.ListItem("Loopback",null,"loopback"));
      this._edit_interface_types.add(new qx.ui.form.ListItem("Ethernet Device",null,"ethernet"));
      this._edit_interface_types.add(new qx.ui.form.ListItem("BOND Type 1",null,"bond_1"));
      this._edit_interface_types.add(new qx.ui.form.ListItem("BOND Type 2",null,"bond_2"));
      this._edit_interface_types.add(new qx.ui.form.ListItem("VLAN Interface",null,"vlan"));

      this._edit_interface_inet_types.removeAll();
      this._edit_interface_inet_types.add(new qx.ui.form.ListItem("Loopback",null,"loopback"));
      this._edit_interface_inet_types.add(new qx.ui.form.ListItem("DHCP",null,"dhcp"));
      this._edit_interface_inet_types.add(new qx.ui.form.ListItem("Static",null,"static"));
      this._edit_interface_inet_types.add(new qx.ui.form.ListItem("Manual",null,"manual"));
    },
    _initializeHWInterfaceNames:function() {
      var tbl_macaddr=new dc2.models.MacAddr(dc2.helpers.BrowserCheck.RPCUrl(false));
      var hw_names=tbl_macaddr.getMacsByServerId(this._server_id);
      this._edit_hw_interface_names.removeAll();
      this._edit_interface_slaves.removeAll();
      this._edit_interface_vlan_raw_device.removeAll();
      if (hw_names.length>0) {
        for (var i=0;i<hw_names.length;i++) {
          this._edit_hw_interface_names.add(new qx.ui.form.ListItem(hw_names[i]["device_name"],null,hw_names[i]["device_name"]));
          this._edit_interface_slaves.add(new qx.ui.form.ListItem(hw_names[i]["device_name"],null,hw_names[i]["device_name"]));
          this._edit_interface_vlan_raw_device.add(new qx.ui.form.ListItem(hw_names[i]["device_name"],null,hw_names[i]["device_name"]));
        }
      }
    },
    setData:function(data) {
      this._interface_data=data;
      this._edit_interface_types.setModelSelection([]);
      this._edit_interface_inet_types.setModelSelection([]);
      this._edit_interface_types.setModelSelection([data["type"]]);
      this._edit_interface_inet_types.setModelSelection([data["inet"]]);
      this._edit_interface_name.setValue(data["name"]);
      this._edit_interface_ip.setValue(data["ip"]);
      this._edit_interface_netmask.setValue(data["netmask"]);
      this._edit_interface_gateway.setValue(data["gateway"]);
      this._edit_interface_pre_up.setValue(data["pre_up"]);
      this._edit_interface_pre_down.setValue(data["pre_down"]);
      this._edit_interface_post_up.setValue(data["post_up"]);
      this._edit_interface_post_down.setValue(data["post_down"]);
    },
    setInterfaceName:function(interface_name) {
      this._edit_interface_name.setValue(interface_name);
      this._edit_interface_name.setEnabled(false);
      this._edit_hw_interface_names.setModelSelection([interface_name]);
      this._edit_hw_interface_names.setEnabled(false);
    },
    setServerId:function(server_id) {
      this._server_id=server_id;
      this._initializeHWInterfaceNames();
    },
    addRawInterface:function(interface_entry) {
      if (this._edit_interface_vlan_raw_device!=null) {
        if (this._edit_interface_vlan_raw_device.getChildrenContainer().findItem(interface_entry)==null) {
          this._edit_interface_vlan_raw_device.add(new qx.ui.form.ListItem(interface_entry,null,interface_entry));
        }
      }
    },
    //
    // Events
    //
    _evChangeSelInterfaceTypes:function(e) {
      if (this._btnApply != null){
        this._btnApply.setEnabled(true);
      }
      if (!this._edit_interface_types.isSelectionEmpty() && this._edit_interface_types.getSelection()[0].getModel()=="loopback") {
        if (this._compInterfaceNames_hwdevices!=null) {
          this._compInterfaceNames_hwdevices.exclude();
        }
        if (this._interface_data!=null && this._interface_data["name"]=="NewInterface") {
          if (this._compInterfaceNames!=null) {
            this._compInterfaceNames.setEnabled(true);
          }
         } else {
           if (this._compInterfaceNames!=null) {
             this._compInterfaceNames.setEnabled(false);
           }
         }
        var loopbackItem=this._edit_interface_inet_types.getChildrenContainer().findItem("Loopback");
        if (loopbackItem != null) {
          loopbackItem.setEnabled(true);
        }
        if (this._compInterfaceBondingSlaves!= null) {
          this._compInterfaceBondingSlaves.exclude();
        }
        if (this._compInterfaceVlanRawDevice != null) {
          this._compInterfaceVlanRawDevice.exclude();
        }
        if (!this._edit_interface_inet_types.isSelectionEmpty() && this._edit_interface_inet_types.getSelection()[0].getModel()=="loopback") {
          if (this._compInterfaceDetails != null) {
            this._compInterfaceDetails.exclude();
          }
        } else if (!this._edit_interface_inet_types.isSelectionEmpty() && this._edit_interface_inet_types.getSelection()[0].getModel()=="dhcp") {
          if (this._compInterfaceDetails != null) {
            this._compInterfaceDetails.exclude();
          }
        } else {
          if (this._compInterfaceDetails != null) {
            this._compInterfaceDetails.show();
          }
        }
      } else if (!this._edit_interface_types.isSelectionEmpty() && this._edit_interface_types.getSelection()[0].getModel()=="ethernet") {
        if (this._compInterfaceNames_hwdevices!=null) {
          this._compInterfaceNames_hwdevices.show();
        }
        if (this._interface_data!=null && this._interface_data["name"]=="NewInterface") {
         if (this._compInterfaceNames!=null) {
           this._compInterfaceNames.setEnabled(true);
         }
        } else {
          if (this._compInterfaceNames!=null) {
            this._compInterfaceNames.setEnabled(false);
          }
        }
        var loopbackItem=this._edit_interface_inet_types.getChildrenContainer().findItem("Loopback");
        if (loopbackItem != null) {
          loopbackItem.setEnabled(false);
          if (!this._edit_interface_inet_types.isSelectionEmpty() && this._edit_interface_inet_types.getSelection()[0].getModel()=="loopback") {
            this._edit_interface_inet_types.setModelSelection([this._interface_data["inet"]]);
          }
        }
        if (this._compInterfaceBondingSlaves!= null) {
          this._compInterfaceBondingSlaves.exclude();
        }
        if (this._compInterfaceVlanRawDevice != null) {
          this._compInterfaceVlanRawDevice.exclude();
        }

        if (!this._edit_interface_inet_types.isSelectionEmpty() && this._edit_interface_inet_types.getSelection()[0].getModel()=="dhcp") {
          if (this._compInterfaceDetails != null) {
            this._compInterfaceDetails.exclude();
          }
        } else if (!this._edit_interface_inet_types.isSelectionEmpty() && this._edit_interface_inet_types.getSelection()[0].getModel()=="static") {
          if (this._compInterfaceDetails != null) {
            this._compInterfaceDetails.show();
          }
        } else if (!this._edit_interface_inet_types.isSelectionEmpty() && this._edit_interface_inet_types.getSelection()[0].getModel()=="manual") {
          if (this._compInterfaceDetails != null) {
            this._compInterfaceDetails.show();
          }
        }
      } else if (!this._edit_interface_types.isSelectionEmpty() && ( this._edit_interface_types.getSelection()[0].getModel()=="bond_1" || this._edit_interface_types.getSelection()[0].getModel()=="bond_2")) {
        if (this._compInterfaceNames_hwdevices!=null) {
          this._compInterfaceNames_hwdevices.exclude();
        }
        if (this._interface_data!=null && this._interface_data["name"]=="NewInterface") {
         if (this._compInterfaceNames!=null) {
           this._compInterfaceNames.setEnabled(true);
         }
        } else {
          if (this._compInterfaceNames!=null) {
            this._compInterfaceNames.setEnabled(false);
          }
        }
        if (this._compInterfaceBondingSlaves!= null) {
          this._compInterfaceBondingSlaves.show()
        }
        if (this._compInterfaceVlanRawDevice != null) {
          this._compInterfaceVlanRawDevice.exclude();
        }

        var loopbackItem=this._edit_interface_inet_types.getChildrenContainer().findItem("Loopback");
        if (loopbackItem != null) {
          loopbackItem.setEnabled(false);
          if (!this._edit_interface_inet_types.isSelectionEmpty() && this._edit_interface_inet_types.getSelection()[0].getModel()=="loopback") {
            this._edit_interface_inet_types.setModelSelection([this._interface_data["inet"]]);
          }
        }
        //
        // Set Selection to bond slaves
        //
        if (this._interface_data != null) {
          if (this._interface_data["slaves"]!=null) {
            // var iarray=this._interface_data["slaves"].split(" ");
            var iarray=this._interface_data["slaves"]
            this._edit_interface_slaves.setModelSelection(iarray);
          }

        }
        if (!this._edit_interface_inet_types.isSelectionEmpty() && this._edit_interface_inet_types.getSelection()[0].getModel()=="dhcp") {
          if (this._compInterfaceDetails != null) {
            this._compInterfaceDetails.exclude();
          }
        } else if (!this._edit_interface_inet_types.isSelectionEmpty() && this._edit_interface_inet_types.getSelection()[0].getModel()=="static") {
          if (this._compInterfaceDetails != null) {
            this._compInterfaceDetails.show();
          }
        } else if (!this._edit_interface_inet_types.isSelectionEmpty() && this._edit_interface_inet_types.getSelection()[0].getModel()=="manual") {
          if (this._compInterfaceDetails != null) {
            this._compInterfaceDetails.show();
          }
        }
      } else if (!this._edit_interface_types.isSelectionEmpty() && this._edit_interface_types.getSelection()[0].getModel()=="vlan") {
        if (this._compInterfaceNames_hwdevices!=null) {
          this._compInterfaceNames_hwdevices.exclude();
        }
        if (this._interface_data!=null && this._interface_data["name"]=="NewInterface") {
         if (this._compInterfaceNames!=null) {
           this._compInterfaceNames.setEnabled(true);
         }
        } else {
          if (this._compInterfaceNames!=null) {
            this._compInterfaceNames.setEnabled(false);
          }
        }
        if (this._compInterfaceBondingSlaves!= null) {
          this._compInterfaceBondingSlaves.exclude()
        }
        if (this._compInterfaceVlanRawDevice != null) {
          this._compInterfaceVlanRawDevice.show();
        }
        var loopbackItem=this._edit_interface_inet_types.getChildrenContainer().findItem("Loopback");
        if (loopbackItem != null) {
          loopbackItem.setEnabled(false);
          if (!this._edit_interface_inet_types.isSelectionEmpty() && this._edit_interface_inet_types.getSelection()[0].getModel()=="loopback") {
            this._edit_interface_inet_types.setModelSelection([this._interface_data["inet"]]);
          }
        }
        if (this._interface_data != null) {
          this._edit_interface_vlan_raw_device.setModelSelection([this._interface_data["vlan_raw_device"]]);
        }
      }
    },
    _btnApplyClicked:function(e) {
      var interfaces={};
      interfaces["name"]=this._edit_interface_name.getValue();
      interfaces["type"]=this._edit_interface_types.getSelection()[0].getModel();
      interfaces["inet"]=this._edit_interface_inet_types.getSelection()[0].getModel();
      interfaces["is_ipv6"]=this._compInterfaceIsIpV6.getValid();
      if (interfaces["type"]=="loopback" && interfaces["inet"]=="loopback") {
        interfaces["ip"]=null;
        interfaces["netmask"]=null;
        interfaces["gateway"]=null;
      } else if (interfaces["inet"]=="dhcp") {
        interfaces["ip"]=null;
        interfaces["netmask"]=null;
        interfaces["gateway"]=null;
      } else {
        interfaces["ip"]=this._edit_interface_ip.getValue();
        interfaces["netmask"]=this._edit_interface_netmask.getValue();
        interfaces["gateway"]=this._edit_interface_gateway.getValue();
      }
      if (interfaces["type"]=="vlan") {
        interfaces["vlan_raw_device"]=this._edit_interface_vlan_raw_device.getSelection()[0].getModel();
      } else {
        interfaces["vlan_raw_device"]=null;
      }
      if (interfaces["type"]=="bond_1" || interfaces["type"]=="bond_2") {
        interfaces["slaves"]="";
        var slaves=this._edit_interface_slaves.getSelection();
        interfaces["slaves"]=[]
        for (var i=0;i<slaves.length;i++) {
          interfaces["slaves"].push(slaves[i].getModel());
          //  interfaces["slaves"]+" "+slaves[i].getModel();
        }
      } else {
        interfaces["slaves"]=null;
      }
      interfaces["pre_up"]=this._edit_interface_pre_up.getValue();
      interfaces["pre_down"]=this._edit_interface_pre_down.getValue();
      interfaces["post_up"]=this._edit_interface_post_up.getValue();
      interfaces["post_down"]=this._edit_interface_post_down.getValue();
      this.fireDataEvent("returnData",interfaces);
    }
  }
});
