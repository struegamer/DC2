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

qx.Class.define("dc2.dialogs.EditNetworks",
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
        _edit_network:null,
        _edit_name:null,
        _edit_description:null,
        _edit_gateway:null,
        _edit_broadcast:null,
        _edit_blocked_ips:null,
        _edit_vlan_no:null,
        _edit_first_ip:null,
        _edit_id:null,
        _model_ipcalc:null,
        _createLayout:function() {
            this.set({
                modal:true,
                padding:3,
                showClose:true,
                showMaximize:false,
                showMinimize:false
            });
            this.setLayout(new qx.ui.layout.VBox(5));
            var comp=new qx.ui.container.Composite();
            var layout=new qx.ui.layout.Grid(5,5);
            this.setResizable(false,true,true,false);
            layout.setColumnFlex(1,1);
            comp.setLayout(layout);

            this._edit_network=new qx.ui.form.TextField();

            this._edit_name=new qx.ui.form.TextField();
            this._edit_description=new qx.ui.form.TextField();
            this._edit_gateway=new qx.ui.form.TextField();
            this._edit_broadcast=new qx.ui.form.TextField();
            this._edit_blocked_ips=new qx.ui.form.TextField();
            this._edit_first_ip=new qx.ui.form.TextField();
            this._edit_vlan_no=new qx.ui.form.TextField();

            comp.add(new qx.ui.basic.Label('Network'),{row:0,column:0});
            comp.add(new qx.ui.basic.Label('Name'),{row:1,column:0});
            comp.add(new qx.ui.basic.Label('Description'),{row:2,column:0});
            comp.add(new qx.ui.basic.Label('Gateway'),{row:3,column:0});
            comp.add(new qx.ui.basic.Label('No. of Blocked IPs'),{row:4,column:0});
            comp.add(new qx.ui.basic.Label('Broadcast'),{row:5,column:0});
            comp.add(new qx.ui.basic.Label('First IP'),{row:6,column:0});
            comp.add(new qx.ui.basic.Label('VLAN No.'),{row:7,column:0});

            comp.add(this._edit_network,{row:0,column:1});
            comp.add(this._edit_name,{row:1,column:1});
            comp.add(this._edit_description,{row:2,column:1});
            comp.add(this._edit_gateway,{row:3,column:1});
            comp.add(this._edit_blocked_ips,{row:4,column:1});
            comp.add(this._edit_broadcast,{row:5,column:1});
            comp.add(this._edit_first_ip,{row:6,column:1});
            comp.add(this._edit_vlan_no,{row:7,column:1});

            var btnCalc=new qx.ui.form.Button("Calculate");
            btnCalc.addListener("execute",this._clkCalculateNetworks,this);
            comp.add(btnCalc,{row:0,column:2});

            this.add(comp,{flex:1});
            this.add(this._createButtonBar());
        },
        _createButtonBar:function() {
            var comp=new qx.ui.container.Composite(new qx.ui.layout.HBox(5).set({alignX:'right'}));
            var btnOk=new qx.ui.form.Button('Ok','icon/16/actions/dialog-ok.png');
            var btnCancel=new qx.ui.form.Button('Cancel','icon/16/actions/dialog-cancel.png');
            btnOk.addListener("execute",this._clkBtnOk,this);
            btnCancel.addListener("execute",this._clkBtnCancel,this);
            comp.add(btnCancel,{flex:0});
            comp.add(btnOk,{flex:0});
            return(comp);
        },
        _clkBtnOk:function(e) {
          var data={}
          data["_id"]=this._edit_id;
          data["network"]=this._edit_network.getValue();
          data["name"]=this._edit_name.getValue();
          data["description"]=this._edit_description.getValue();
          data["gateway"]=this._edit_gateway.getValue();
          data["broadcast"]=this._edit_broadcast.getValue();
          data["blocked_ips"]=this._edit_blocked_ips.getValue();
          data["first_ip"]=this._edit_first_ip.getValue();
          data["vlan_no"]=this._edit_vlan_no.getValue();
          if (data["_id"]!="" && data["_id"]!=null) {
            this.fireDataEvent("updateData",data);
          } else {
            this.fireDataEvent("addData",data);
          }
          this.close();
        },
        _clkBtnCancel:function(e) {
            this.close();
        },
        _clkCalculateNetworks:function(e) {
          if (this._model_ipcalc == null) {
            this._model_ipcalc=new dc2.models.IpCalc(dc2.helpers.BrowserCheck.RPCUrl(false));
          }
          var result=this._model_ipcalc.calcIpnetwork(this._edit_network.getValue());
          if (result != null) {
            if (this._edit_broadcast.getValue()==""||this._edit_broadcast.getValue()==null) {
              this._edit_broadcast.setValue(result["broadcast"]);
            }

            if (this._edit_first_ip.getValue()==""||this._edit_first_ip.getValue()==null) {
              this._edit_first_ip.setValue(result["first_ip"]);
            }
          }
        },
        setData:function(data) {
            if (data != null) {
              this._edit_id=data["_id"];
              this._edit_network.setValue(data["network"]);
              this._edit_name.setValue(data["name"]);
              this._edit_description.setValue(data["description"]);
              this._edit_gateway.setValue(data["gateway"]);
              this._edit_broadcast.setValue(data["broadcast"]);
              this._edit_blocked_ips.setValue(data["blocked_ips"]);
              this._edit_first_ip.setValue(data["first_ip"]);
              this._edit_vlan_no.setValue(data["vlan_no"]);
            }
        }
    }
}
);