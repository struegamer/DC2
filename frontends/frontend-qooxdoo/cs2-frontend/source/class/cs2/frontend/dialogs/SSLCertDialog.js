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


/* ************************************************************************
#asset(qx/icon/${qx.icontheme}/16/actions/list-add.png)
#asset(qx/icon/${qx.icontheme}/16/actions/list-remove.png)
#asset(qx/icon/${qx.icontheme}/16/actions/view-refresh.png)
#asset(qx/icon/${qx.icontheme}/16/actions/dialog-ok.png);
#asset(qx/icon/${qx.icontheme}/16/actions/dialog-cancel.png);
************************************************************************ */
qx.Class.define("cs2.frontend.dialogs.SSLCertDialog",
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
    _edit_cert_csr:null,
    _edit_cert_serial_no:null,
    _edit_cert_digest:null,
    _edit_cert_notBefore:null,
    _edit_cert_notAfter:null,    
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
      this._edit_cert_csr=new qx.ui.form.SelectBox();
      this._edit_cert_serial_no=new qx.ui.form.TextField();
      this._edit_cert_serial_no.setTextAlign("right");
      this._edit_cert_digest=new qx.ui.form.SelectBox();
      this._edit_cert_notBefore=new qx.ui.form.TextField();
      this._edit_cert_notAfter=new qx.ui.form.SelectBox();
      
      
      var btnRefreshCSR=new qx.ui.form.Button("Refresh");
      btnRefreshCSR.addListener("execute",this._fillCSRNames,this);
      
      var btnGetSerial=new qx.ui.form.Button("Get Serial");
      btnGetSerial.addListener("execute",this._getSerialNumber,this);
      this._fillValidYears();
      this._fillCSRNames();
      this._fillDigestNames();          
      comp.add(new qx.ui.basic.Label("Certificate Signging Request"),{row:0,column:0});
      comp.add(new qx.ui.basic.Label("Serial Number"),{row:1,column:0});
      comp.add(new qx.ui.basic.Label("Digest"),{row:2,column:0});
      comp.add(new qx.ui.basic.Label("Valid notBefore"),{row:3,column:0});
      comp.add(new qx.ui.basic.Label("Valid notAfter"),{row:4,column:0});
      
      comp.add(this._edit_cert_csr,{row:0,column:1});
      comp.add(btnRefreshCSR,{row:0,column:2});
      comp.add(this._edit_cert_serial_no,{row:1,column:1});
      comp.add(btnGetSerial,{row:1,column:2});
      comp.add(this._edit_cert_digest,{row:2,column:1});
      comp.add(new qx.ui.basic.Label("Today"),{row:3,column:1});
      comp.add(this._edit_cert_notAfter,{row:4,column:1});
      
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
    _getSerialNumber:function() {
      var md_serial=new cs2.models.SSLSerialNumber(dc2.helpers.BrowserCheck.RPCUrl(false));
      var serial_number=md_serial.getSerialNumber();
      this._edit_cert_serial_no.setValue(serial_number.toString());
    },
    _fillValidYears:function() {
      var seconds_one_year=60*60*24*365;
      for (var i=1;i<11;i++) {
        this._edit_cert_notAfter.add(new qx.ui.form.ListItem(i+" Year(s)",null,seconds_one_year*i))        
      }
      this._edit_cert_notAfter.setModelSelection([seconds_one_year*3]);
    },
    _fillCSRNames:function() {
      this._edit_cert_csr.removeAll();
      var _tbl_ssl_csr=new cs2.models.SSLCsrs(dc2.helpers.BrowserCheck.RPCUrl(false));
      var result=_tbl_ssl_csr.getCsrNames();
      for (var i=0;i<result.length;i++) {
        this._edit_cert_csr.add(new qx.ui.form.ListItem(result[i]["commonname"],null,result[i]["commonname"]));
      }      
    },
    _fillDigestNames:function() {
      this._edit_cert_digest.add(new qx.ui.form.ListItem("SHA1",null,"sha1"));
      this._edit_cert_digest.add(new qx.ui.form.ListItem("MD5",null,"md5"));
      this._edit_cert_digest.add(new qx.ui.form.ListItem("MD4",null,"MD4"));
      this._edit_cert_digest.add(new qx.ui.form.ListItem("MDC2",null,"mdc2"));
      this._edit_cert_digest.add(new qx.ui.form.ListItem("MD2",null,"md2"));
      this._edit_cert_digest.setModelSelection(["sha1"]);
    },
    _clkBtnOk:function(e) {
      var data={};
      data["commonname"]=this._edit_cert_csr.getSelection()[0].getModel();
      data["serial_no"]=this._edit_cert_serial_no.getValue();
      data["digest"]=this._edit_cert_digest.getSelection()[0].getModel();
      data["notBefore"]=0;
      data["notAfter"]=this._edit_cert_notAfter.getSelection()[0].getModel();
      this.fireDataEvent("addData",data);
      this.close();
    },
    _clkBtnCancel:function(e) {
      this.close();
    },
    setData:function(data) {
      
    }
  }
});