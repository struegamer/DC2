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

qx.Class.define("dc2.xen.Main", {
  extend: qx.core.Object,
  construct:function() {
    this.base(arguments);
  },
  members: {
    getXenHostPage:function() {
      var xenserver_tbl=new dc2.xen.models.XenServer(dc2.helpers.BrowserCheck.RPCUrl(false));
      var xenserver_dlg=new dc2.xen.dialogs.EditXenServer();
      var xenserver_options={
          enableAddEntry:true,
          enableEditEntry:true,
          enableDeleteEntry:false,
          enableReloadEntry:true,
          tableModel:xenserver_tbl,
          addDialog:xenserver_dlg,
          editDialog:xenserver_dlg,
          columnVisibility:[
                            {
                              column:0,
                              visible:false
                            },
                            {
                              column:3,
                              visible:false
                            }
                            ]
      };
      var xenserver_table=new dc2.widgets.TableWidget(xenserver_options);
      xenserver_table.showData();
      return(xenserver_table);
    },
    getXenVMSPage:function() {
      var comp=new qx.ui.container.Composite(new qx.ui.layout.VBox(5));
      var xenserver_tbl=new dc2.xen.models.XenServer(dc2.helpers.BrowserCheck.RPCUrl(false));
      var xenserver=new qx.ui.form.SelectBox();
      var xenserver_list=xenserver_tbl.getAll();
      var xenvms_tbl=new dc2.xen.models.XenVMS(dc2.helpers.BrowserCheck.RPCUrl(false));
      var xenhost_label=new qx.ui.basic.Label("");
      var xenvm_edit_dlg=new dc2.xen.dialogs.EditXenVM();
      var xenvms_table_options={
          enableAddEntry:false,
          enableEditEntry:true,
          enableDeleteEntry:false,
          enableReloadEntry:true,
          tableModel:xenvms_tbl,
          editDialog:xenvm_edit_dlg,
          columnVisibility:[
                            {
                              column:0,
                              visible:false
                            },
                            {
                              column:3,
                              visible:false
                            },
                            {
                              column:4,
                              visible:false
                            }

                            ]
      };
      var xenvms_table=new dc2.widgets.TableWidget(xenvms_table_options);
      if (xenserver_list.length>0) {
        var emptyItem=new qx.ui.form.ListItem("Xen Host",null,"none");
        emptyItem.setEnabled(false);
        xenserver.add(emptyItem);
        for (var i=0;i<xenserver_list.length;i++) {
          xenserver.add(new qx.ui.form.ListItem(xenserver_list[i]["xen_host"],null,null));
        }
        xenserver.setModelSelection(["none"]);
      }

      var comp1=new qx.ui.container.Composite(new qx.ui.layout.HBox(5));
      var btnXenHostConnect=new qx.ui.form.Button("Connect");
      btnXenHostConnect.setEnabled(false);
      var btnXenHostDisconnect=new qx.ui.form.Button("Disconnect");
      btnXenHostDisconnect.setEnabled(false);

      var comp3=new qx.ui.container.Composite(new qx.ui.layout.HBox(5));
      var chkVMS=new qx.ui.form.CheckBox("VMs");
      chkVMS.setValue(true);
      var chkTpl=new qx.ui.form.CheckBox("Templates");
      var vmtype="vms";

      var chkFunc=function(e) {
        if (chkVMS.getValue() && chkTpl.getValue()) {
          vmtype="both";
        }
        if (chkVMS.getValue() && ! chkTpl.getValue()) {
          vmtype="vms";
        }
        if (!chkVMS.getValue() && chkTpl.getValue()) {
          vmtype="template";
        }
        if (!chkVMS.getValue() && ! chkTpl.getValue()) {
          vmtype="vms";
          chkVMS.setValue(true);
        }
        if (xenserver.getSelection()[0].getModel()!=null) {
          xenvms_tbl.setSessionInfos({"session_id":xenserver.getSelection()[0].getModel(),"xen_host":xenserver.getSelection()[0].getLabel(),"vmtype":vmtype});
          xenvms_table.showData();
        }
      };
      chkVMS.addListener("changeValue",chkFunc,this);
      chkTpl.addListener("changeValue",chkFunc,this);

      comp3.add(new qx.ui.basic.Label("Show"));
      comp3.add(chkVMS);
      comp3.add(chkTpl);
      comp3.exclude();

      btnXenHostConnect.addListener("execute",function(e) {
        btnXenHostDisconnect.setEnabled(true);
        btnXenHostConnect.setEnabled(false);
        var result=xenserver_tbl.login(xenserver.getSelection()[0].getLabel());
        if (result != null && result != "") {
          xenserver.getSelection()[0].setModel(result);
          xenvms_tbl.setSessionInfos({"session_id":result,"xen_host":xenserver.getSelection()[0].getLabel(),"vmtype":vmtype});
          xenvms_table.showData();
          xenhost_label.setValue("Virtual Machines on "+xenserver.getSelection()[0].getLabel());
          comp3.show();
        }
      },this);

      btnXenHostDisconnect.addListener("execute",function(e) {
        btnXenHostDisconnect.setEnabled(false);
        btnXenHostConnect.setEnabled(true);
        xenserver_tbl.logout(xenserver.getSelection()[0].getLabel(),xenserver.getSelection()[0].getModel());
        xenserver.getSelection()[0].setModel(null);
        xenvms_tbl.setSessionInfos(null);
        xenvms_table.showData();
        xenhost_label.setValue("No connected Xen Host");
        comp3.exclude();
      },this);

      comp1.add(new qx.ui.basic.Label("Select Xen Host"));
      comp1.add(xenserver,{flex:1});
      comp1.add(btnXenHostConnect);
      comp1.add(btnXenHostDisconnect);

      xenserver.addListener("changeSelection",function(e) {
        if (xenserver.getSelection()[0].getModel()=="empty") {
          console.log("not selected");
          btnXenHostConnect.setEnabled(false);
          btnXenHostDisconnect.setEnabled(false);
          comp3.exclude();
        } else {
          if (xenserver.getSelection()[0].getModel() == null) {
            btnXenHostConnect.setEnabled(true);
            btnXenHostDisconnect.setEnabled(false);
            xenvms_tbl.setSessionInfos(null);
            xenvms_table.showData();
            xenhost_label.setValue("No connected Xen Host");
            comp3.exclude();
          } else {
            btnXenHostConnect.setEnabled(false);
            btnXenHostDisconnect.setEnabled(true);
            xenvms_tbl.setSessionInfos({"session_id":xenserver.getSelection()[0].getModel(),"xen_host":xenserver.getSelection()[0].getLabel(),"vmtype":vmtype});
            xenvms_table.showData();
            xenhost_label.setValue("Virtual Machines on "+xenserver.getSelection()[0].getLabel());
            comp3.show();
          }
        }
      },this);
      var comp2=new qx.ui.container.Composite(new qx.ui.layout.VBox(5));
      comp2.add(xenhost_label);
      comp2.add(xenvms_table);



      comp.add(comp1);
      comp.add(comp2);
      comp.add(comp3);
      return(comp);
    }
 }
}
);