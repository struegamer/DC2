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


qx.Class.define("dc2.dialogs.EditHosts",
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
    _edit_id:null,
    _edit_server_id:null,
    _edit_server:null,
    _edit_hostname:null,
    _edit_domainname:null,
    _edit_defaultclasses:null,
    _edit_hostclasses:null,
    _edit_fromclasstemplate:null,
    _edit_interface_list:null,
    _edit_interface_types:null,
    _edit_interface_inet_types:null,
    _edit_interface_pre_up:null,
    _edit_interface_pre_down:null,
    _edit_interface_post_up:null,
    _edit_interface_post_down:null,
    _edit_xen_answerfile:null,
    _edit_environments:null,
    _edit_is_xenserver:null,
    _tbl_server:null,
    _tbl_defaultclasses:null,
    _tbl_classtemplates:null,
    _tbl_environments:null,
    _tbl_hosts:null,
    _interface_list:null,
    _detailPage:null,
    _tabView:null,
    _xenAnswerFilePage:null,
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
      this.setWidth(800);
      this._edit_server=new qx.ui.form.SelectBox();
      this._edit_server.setEnabled(false);
      this._edit_hostname=new qx.ui.form.TextField();
      this._edit_domainname=new qx.ui.form.TextField();
      this._edit_is_xenserver=new qx.ui.form.CheckBox();
      this._edit_is_xenserver.addListener("changeValue",this._isXenServerChange,this);
      this._edit_xen_answerfile=new qx.ui.form.TextArea();
      this._from_classtemplate=new qx.ui.form.SelectBox();
      this._edit_defaultclasses=new qx.ui.form.List();
      this._edit_defaultclasses.setDraggable(true);
      this._edit_defaultclasses.setDroppable(true);
      this._edit_hostclasses=new qx.ui.form.List();
      this._edit_hostclasses.setDraggable(true);
      this._edit_hostclasses.setDroppable(true);
      this._edit_defaultclasses.addListener("dragstart",this._dragstartDefaultClasses,this);
      this._edit_defaultclasses.addListener("droprequest",this._droprequestDefaultClasses,this);
      this._edit_defaultclasses.addListener("drop",this._dropDefaultClasses,this)
      this._edit_defaultclasses.setSelectionMode("multi");
      this._edit_hostclasses.addListener("drop",this._dropHostClasses,this);
      this._edit_hostclasses.addListener("dragstart",this._dragstartHostClasses,this);
      this._edit_hostclasses.addListener("droprequest",this._droprequestHostClasses,this);
      this._edit_hostclasses.setSelectionMode("multi");

      this._edit_interface_list=new qx.ui.form.List();
      this._edit_interface_list.addListener("changeSelection",this._evChangedInterfaceList,this);

      this._edit_environments=new qx.ui.form.SelectBox();

      this._tabView=new qx.ui.tabview.TabView();
      this._tabView.setWidth(400);
      this._tabView.add(this._createHostPage());
      this._tabView.add(this._createClassesPage());
      this._tabView.add(this._createInterfacePage());
      this._xenAnswerFilePage=this._createXenAnswerFilePage();
      this._tabView.add(this._xenAnswerFilePage);
      this.add(this._tabView,{flex:1});
      this.add(this._initializeButtonBar());
      this._fillServers();
      this._fillClassTemplates();
      this._fillDefaultClasses();
      this._fillEnvironments();
    },
    /*
     * Private Methods
     */
    _createHostPage:function() {
      var page=new qx.ui.tabview.Page("Host");
      var layout=new qx.ui.layout.Grid(5,5);
      layout.setColumnFlex(1,1);
      page.setLayout(layout);
      var btnUseServer=new qx.ui.form.Button("Use");

      var btnRefresh=new qx.ui.form.Button("Refresh Server List");
      btnRefresh.addListener("execute",function(e) {this._fillServers();}, this);
      var btnRefreshEnvironments=new qx.ui.form.Button("Refresh Environments");
      btnRefreshEnvironments.addListener("execute",function(e) { this._fillEnvironments();},this);
      page.add(new qx.ui.basic.Label("Server"),{row:0,column:0});
      page.add(new qx.ui.basic.Label("Hostname"),{row:1,column:0});
      page.add(new qx.ui.basic.Label("Domainname"),{row:2,column:0});
      page.add(new qx.ui.basic.Label("Environment"),{row:3,column:0});
      page.add(new qx.ui.basic.Label("XenServer"),{row:4,column:0});
      page.add(this._edit_server,{row:0,column:1});
      page.add(btnUseServer,{row:0,column:2});
      page.add(btnRefresh,{row:0,column:3});
      page.add(this._edit_hostname,{row:1,column:1});
      page.add(this._edit_domainname,{row:2,column:1});
      page.add(this._edit_environments,{row:3,column:1});
      page.add(this._edit_is_xenserver,{row:4,column:1});
      page.add(btnRefreshEnvironments,{row:3,column:2});
      return(page);
    },
    _createClassesPage:function() {
      var page=new qx.ui.tabview.Page("Classes");
      var layout=new qx.ui.layout.VBox(5);
      page.setLayout(layout);

      var comp1=new qx.ui.container.Composite();
      var layout1=new qx.ui.layout.HBox(5);
      comp1.setLayout(layout1);
      comp1.add(new qx.ui.basic.Label("Class Template"));
      comp1.add(this._from_classtemplate,{flex:1});
      var btnUse=new qx.ui.form.Button("Use");
      btnUse.addListener("execute",this._btnUse,this);
      var btnRefresh=new qx.ui.form.Button("Refresh List");
      btnRefresh.addListener("execute",function(e) { this._fillClassTemplates(); },this);

      comp1.add(btnUse);
      comp1.add(btnRefresh);

      var comp2=new qx.ui.container.Composite(new qx.ui.layout.VBox(5));
      var btnRefreshDClasses=new qx.ui.form.Button("Refresh Default Classes");

      comp2.add(new qx.ui.basic.Label("Default Classes"));
      comp2.add(this._edit_defaultclasses,{flex:1});
      comp2.add(btnRefreshDClasses);
      var comp3=new qx.ui.container.Composite(new qx.ui.layout.VBox(5));
      var btnClear=new qx.ui.form.Button("Clear Host Classes List");
      btnClear.addListener("execute",function(e) { this._edit_hostclasses.removeAll(); this._fillDefaultClasses();},this);
      comp3.add(new qx.ui.basic.Label("Host Classes"));
      comp3.add(this._edit_hostclasses,{flex:1});
      comp3.add(btnClear);
      var comp4=new qx.ui.container.Composite(new qx.ui.layout.HBox(5));
      comp4.add(comp2,{flex:1});
      comp4.add(comp3,{flex:1});
      page.add(comp1);
      page.add(comp4);
      return(page);
    },
    _createInterfacePage:function() {
      var page=new qx.ui.tabview.Page("Interfaces");
      var layout=new qx.ui.layout.HBox(5);
      page.setLayout(layout);

      page.add(this._createInterfacePage_InterfaceList());
      this._detailPage=new dc2.dialogs.interfaces.Details(this._edit_server_id);
      this._detailPage.addListener("returnData",this._evUpdateDataDetailPage,this)
      page.add(this._detailPage,{flex:1});
      this._detailPage.exclude();

      return(page);
    },

    _createInterfacePage_InterfaceList:function() {
      // Interfaces List
      var compInterfaces=new qx.ui.container.Composite(new qx.ui.layout.VBox(5));

      compInterfaces.add(new qx.ui.basic.Label("Interfaces"));

      var btnAdd=new qx.ui.form.Button("New");
      btnAdd.addListener("execute",this._btnAdd,this);
      var btnDelete=new qx.ui.form.Button("Remove");
      btnDelete.addListener("execute",this._btnDelete,this);
      var btnReload=new qx.ui.form.Button("Reload");

      // Buttonbar for Interfaces
      var compButtonBar=new qx.ui.container.Composite(new qx.ui.layout.HBox(5));
      compButtonBar.add(btnAdd);
      compButtonBar.add(btnDelete);
      compButtonBar.add(btnReload);
      compInterfaces.add(compButtonBar);
      compInterfaces.add(this._edit_interface_list,{flex:1});
      return(compInterfaces);
    },
    _createXenAnswerFilePage:function() {
        var page=new qx.ui.tabview.Page("XEN Deployment Template");
        var layout=new qx.ui.layout.VBox(5);
        page.setLayout(layout);
        page.add(new qx.ui.basic.Label("XEN Answerfile"));
        page.add(this._edit_xen_answerfile,{flex:1});
        return(page);
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
    _fillServers:function() {
      if (this._tbl_servers==null) {
        this._tbl_servers=new dc2.models.Servers(dc2.helpers.BrowserCheck.RPCUrl(false));
      }
      this._edit_server.removeAll();
      var serverlist=this._tbl_servers.getAllServers();
      if (serverlist.length>0) {
        this._edit_server.add(new qx.ui.form.ListItem("Server not set",null,null));
        for (var i=0;i<serverlist.length;i++) {
          this._edit_server.add(new qx.ui.form.ListItem(serverlist[i]["serial_no"],null,serverlist[i]["_id"]));
        }
        if (this._edit_server_id!=null) {
          this._edit_server.setModelSelection([this._edit_server_id]);
        }
      }
    },
    _fillClassTemplates:function() {
      if (this._tbl_classtemplates==null) {
        this._tbl_classtemplates=new dc2.models.ClassTemplates(dc2.helpers.BrowserCheck.RPCUrl(false));
      }
      this._from_classtemplate.removeAll();
      var classtemplatelist=this._tbl_classtemplates.getAllTemplates();
      for (var i=0;i<classtemplatelist.length;i++) {
        this._from_classtemplate.add(new qx.ui.form.ListItem(classtemplatelist[i]["name"],null,classtemplatelist[i]["_id"]));
      }
    },
    _fillDefaultClasses:function() {
      if (this._tbl_defaultclasses==null) {
        this._tbl_defaultclasses=new dc2.models.DefaultClasses(dc2.helpers.BrowserCheck.RPCUrl(false));
      }
      this._edit_defaultclasses.removeAll();
      var defaultclasses=this._tbl_defaultclasses.getAll();
      for (var i=0;i<defaultclasses.length;i++) {
        this._edit_defaultclasses.add(new qx.ui.form.ListItem(defaultclasses[i]["classname"],null,defaultclasses[i]["classname"]));
      }
    },
    _fillEnvironments:function() {
      if (this._tbl_environments==null) {
        this._tbl_environments=new dc2.models.Environments(dc2.helpers.BrowserCheck.RPCUrl(false));
      }
      this._edit_environments.removeAll();
      var environments=this._tbl_environments.getAll();
      for (var i=0;i<environments.length;i++) {
        this._edit_environments.add(new qx.ui.form.ListItem(environments[i]["name"],null,environments[i]["name"]));
      }
    },
    /*
     * Event Methods
     */
    _clkBtnOk:function(e) {
      var data={};
      data["_id"]=this._edit_id;
      data["server_id"]=this._edit_server.getSelection()[0].getModel();
      data["hostname"]=this._edit_hostname.getValue();
      data["domainname"]=this._edit_domainname.getValue();
      data["hostclasses"]=[]
      var items=this._edit_hostclasses.getChildren();
      for (var i=0; i<items.length; i++) {
        data["hostclasses"].push(items[i].getModel());
      }
      var interfaces=this._edit_interface_list.getChildren();
      data["interfaces"]=[];
      for (var i=0;i<interfaces.length;i++) {
        data["interfaces"].push(interfaces[i].getModel());
      }
      data["environments"]=this._edit_environments.getSelection()[0].getModel();
      if (this._edit_id != null && this._edit_id != "") {
        this.fireDataEvent("updateData",data);
      } else {
        // this.fireDataEvent("addData",data);
      }
      this.close();
    },
    _clkBtnCancel:function(e) {
      this.close();
    },
    _btnUse:function(e) {
      var template_name=this._from_classtemplate.getSelection()[0].getModel();
      var record=this._tbl_classtemplates.getClassTemplateRecord(template_name);
      this._edit_hostclasses.removeAll();
      for (var i=0;i<record["classes"].length;i++) {
        this._edit_hostclasses.add(new qx.ui.form.ListItem(record["classes"][i],null,record["classes"][i]));
        var found=this._edit_defaultclasses.findItem(record["classes"][i]);
        if (found != null) {
          this._edit_defaultclasses.remove(found);
        }
      }
    },
    _dragstartDefaultClasses:function(e) {
      e.addType("items");
      e.addAction("copy");
      e.addAction("move");
    },
    _dragstartHostClasses:function(e) {
      e.addType("items");
      e.addAction("copy");
      e.addAction("move");
    },
    _droprequestDefaultClasses:function(e) {
      var action=e.getCurrentAction();
      var type=e.getCurrentType();
      var result;
      if (type=="items") {
        result=this._edit_defaultclasses.getSelection();
        if (action=="copy") {
          var copy=[];
          for (var i=0;i<result.length;i++) {
            copy[i]=result[i].clone();
          }
          result=copy;
        }
        if (action=="move") {
          var selection=this._edit_defaultclasses.getSelection();
          for (var i=0;i<selection.length;i++) {
            this._edit_defaultclasses.remove(selection[i]);
          }
        }
        e.addData(type,result);
      }
    },
    _droprequestHostClasses:function(e) {
      var action=e.getCurrentAction();
      var type=e.getCurrentType();
      var result;
      if (type=="items") {
        result=this._edit_hostclasses.getSelection();
        if (action=="copy") {
          var copy=[];
          for (var i=0; i<result.length;i++) {
            copy[i]=result[i].clone();
          }
          result=copy;
        }
        if (action=="move") {
          var selection=this._edit_hostclasses.getSelection();
          for (var i=0;i<selection.length;i++) {
            this._edit_hostclasses.remove(selection[i]);
          }
        }
        e.addData(type,result);
      }
    },
    _dropDefaultClasses:function(e) {
      var items=e.getData("items");
      for (var i=0;i<items.length;i++) {
        this._edit_defaultclasses.add(items[i]);
      }
      items=this._edit_defaultclasses.getChildren();
      var items1=[];
      for (var i=0;i<items.length;i++) {
        items1[i]=items[i].clone();
      }
      items1.sort(function(a,b) {
        var av=a.getLabel();
        var bv=b.getLabel();
        return av < bv ? -1 :( av == bv ? 0 : 1 );
      });
      this._edit_defaultclasses.removeAll();
      for (var i=0;i<items1.length;i++) {
        this._edit_defaultclasses.add(items1[i]);
      }
    },
    _dropHostClasses:function(e) {
      var items=e.getData("items");
      for (var i=0;i<items.length;i++) {
        this._edit_hostclasses.add(items[i]);
      }
      items=this._edit_hostclasses.getChildren();
      var items1=[];
      for (var i=0;i<items.length;i++) {
        items1[i]=items[i].clone();
      }
      items1.sort(function(a,b) {
        var av=a.getLabel();
        var bv=b.getLabel();
        return av < bv ? -1 :( av == bv ? 0 : 1 );
      });
      this._edit_hostclasses.removeAll();
      for (var i=0;i<items1.length;i++) {
        this._edit_hostclasses.add(items1[i]);
      }
    },
    _evChangedInterfaceList:function(e) {
      if (!this._edit_interface_list.isSelectionEmpty()) {
        if (this._edit_interface_list.getChildren().length>0) {
          this._detailPage.setData(this._edit_interface_list.getSelection()[0].getModel());
          this._detailPage.show();
        } else {
          this._detailPage.exclude();
        }
      } else {
        this._detailPage.exclude();
      }
    },
    _btnAdd:function(e) {
      var interfaces={};
      interfaces["name"]="NewInterface";
      interfaces["type"]="ethernet";
      interfaces["inet"]="static";
      interfaces["ip"]=null;
      interfaces["netmask"]=null;
      interfaces["gateway"]=null;
      interfaces["vlan_raw_device"]=null;
      interfaces["slaves"]=null;
      interfaces["pre_up"]=null;
      interfaces["pre_down"]=null;
      interfaces["post_up"]=null;
      interfaces["post_down"]=null;
      this._edit_interface_list.add(new qx.ui.form.ListItem(interfaces["name"],null,interfaces));
      this._edit_interface_list.setModelSelection([interfaces]);
      this._detailPage.setData(interfaces);
      this._edit_interface_list.setEnabled(false);
    },
    _btnDelete:function(e) {
      if (!this._edit_interface_list.isSelectionEmpty()) {
        this._edit_interface_list.remove(this._edit_interface_list.getSelection()[0]);
        this._edit_interface_list.setSelection([]);
      }
    },
    _evUpdateDataDetailPage:function(e) {
      if (!this._edit_interface_list.isSelectionEmpty()) {
        if (this._edit_interface_list.getSelection()[0].getLabel()=="NewInterface") {
          var item=this._edit_interface_list.getSelection()[0];
          var found=this._edit_interface_list.findItem(e.getData()["name"]);
          if (found == null) {
            if (item != null) {
              item.setLabel(e.getData()["name"]);
              item.setModel(e.getData());
            }
          } else {
            if (item != null && !item["is_ipv6"]) {
              var dialog=new dc2.widgets.MessageBox("error","Error adding new interface","You already have an interface with the name of "+e.getData()["name"]);
              dialog.addListener("close",function(e) { delete dialog; },this);
            }
          }
          this._edit_interface_list.setEnabled(true);
        } else {
          var item=this._edit_interface_list.findItem(e.getData()["name"]);
          if (item != null) {
            item.setModel(e.getData());
          }
          this._edit_interface_list.setEnabled(true);
        }
      }
    },
    _isXenServerChange:function(e) {
        // TODO: Fill me in
        if (this._edit_is_xenserver.getValue()==true) {
            this._xenAnswerFilePage.setEnabled(true);
        } else {
            this._xenAnswerFilePage.setEnabled(false);
        }
    },
    /*
     * Public Methods
     */
    setData:function(data) {
      if (data != null) {
        var hostdata=null;
        if (data["_id"] != null) {
          if (this._tbl_hosts == null) {
            this._tbl_hosts=new dc2.models.Hosts(dc2.helpers.BrowserCheck.RPCUrl(false));
          }
          hostdata=this._tbl_hosts.getHost(data["_id"]);
        } else {
          hostdata=data;
        }
        if (hostdata != null) {
          this._edit_id=hostdata["_id"];
          if ("server_id" in data && hostdata["server_id"]!=null) {
            this._edit_server_id=hostdata["server_id"];
            this._fillServers();
            this._edit_server.setModelSelection([hostdata["server_id"]]);
            this._detailPage.setServerId(hostdata["server_id"]);
            this._edit_hostname.setValue(hostdata["hostname"]);
            this._edit_domainname.setValue(hostdata["domainname"]);
            this._edit_hostclasses.removeAll();
            if ("hostclasses" in data && hostdata["hostclasses"].length>0) {
              for (var i=0;i<hostdata["hostclasses"].length;i++) {
                this._edit_hostclasses.add(new qx.ui.form.ListItem(hostdata["hostclasses"][i],null,hostdata["hostclasses"][i]));
                var found=this._edit_defaultclasses.findItem(hostdata["hostclasses"][i]);
                if (found != null) {
                  this._edit_defaultclasses.remove(found);
                }
              }
            } else {
              this._edit_hostclasses.removeAll();
            }
            if ("interfaces" in data && hostdata["interfaces"].length>0) {
              if (this._interface_list==null) {
                this._interface_list={};
              }
              this._edit_interface_list.removeAll();
              for (var i=0;i<hostdata["interfaces"].length;i++) {
                this._edit_interface_list.add(new qx.ui.form.ListItem(hostdata["interfaces"][i]["name"],null,hostdata["interfaces"][i]));
                if (hostdata["interfaces"][i]["type"]!="loopback" && hostdata["interfaces"][i]["type"]!="vlan"){
                  this._detailPage.addRawInterface(hostdata["interfaces"][i]["name"]);
                }
              }
            } else {
              this._edit_interface_list.removeAll();
            }
            if ("environments" in data) {
              this._edit_environments.setModelSelection([hostdata["environments"]]);
            }
            if ("is_xenserver" in data) {
                if (data["is_xenserver"] != null && data["is_xenserver"] != "") {
                    this._xenAnswerFilePage.setEnabled(true);
                } else {
                    this._xenAnswerFilePage.setEnabled(false);
                }
            } else {
                this._xenAnswerFilePage.setEnabled(false);
            }
          }
        }
      }
    }
  }
});
