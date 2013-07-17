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
qx.Class.define("cs2.frontend.dialogs.SSLCertRevokeDialog",
{
  extend: qx.ui.window.Window,
  construct:function() {
    this.base(arguments);
    this._createLayout();
  },
/*  events: {
      'addData':"qx.event.type.Data",
      'updateData':"qx.event.type.Data"
  },
*/
  members: {
    _commonname:null,
    _revoke_reason:null,
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
      var comp=new qx.ui.container.Composite();
      var layout=new qx.ui.layout.Grid(5,5);
      layout.setColumnFlex(1,1);
      comp.setLayout(layout);
      this._revoke_reason=new qx.ui.form.SelectBox();

      comp.add(new qx.ui.basic.Label("Revoke Reason"),{row:0,column:0});
      comp.add(this._revoke_reason,{row:0,column:1});
      this._fillRevokeReasons();
      this.add(comp,{flex:1});
      this.add(this._initializeButtonBar());
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
    _fillRevokeReasons:function() {
      this._revoke_reason.add(new qx.ui.form.ListItem("Unspecified",null,"unspecified"));
      this._revoke_reason.add(new qx.ui.form.ListItem("Key Compromised",null,"keyCompromise"));
      this._revoke_reason.add(new qx.ui.form.ListItem("CA Compromise",null,"CACompromise"));
      this._revoke_reason.add(new qx.ui.form.ListItem("Affiliation Changed",null,"affiliationChanged"));
      this._revoke_reason.add(new qx.ui.form.ListItem("Superseded",null,"superseded"));
      this._revoke_reason.add(new qx.ui.form.ListItem("Cessation Of Operation",null,"cessationOfOperation"));
      this._revoke_reason.add(new qx.ui.form.ListItem("Certificate Hold",null,"certificateHold"));
      this._revoke_reason.add(new qx.ui.form.ListItem("Remove from CRL",null,"removeFromCRL"));
      this._revoke_reason.setModelSelection(["unspecified"]);
    },
    _revokeCertificate:function(commonname,reason) {
      var cert_tbl=new cs2.models.SSLCerts(dc2.helpers.BrowserCheck.RPCUrl(false));
      cert_tbl.revokeCert({"commonname":commonname,"reason":reason});

    },
    _clkBtnOk:function(e) {
      this._revokeCertificate(this._commonname,this._revoke_reason.getSelection()[0].getModel());
      this.close();
    },
    _clkBtnCancel:function(e) {
      this.close();
    },
    setData:function(data) {
      if (data!=null) {
        this._commonname=data["commonname"];
      }
    }
  }
});