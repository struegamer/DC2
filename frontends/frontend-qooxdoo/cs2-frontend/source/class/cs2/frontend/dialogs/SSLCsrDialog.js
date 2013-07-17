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

/*
 *
 *     SUBJECTS = (
        'CN',
        'C',
        'ST',
        'L',
        'O',
        'OU',
        )

        DIGESTS = (
         'md5',
         'md4',
         'md2',
         'sha1',
         'sha',
         'sha224',
         'sha256',
         'sha384',
         'sha512',
         'mdc2',
         'ripemd160'
)

 */

/* ************************************************************************
#asset(qx/icon/${qx.icontheme}/16/actions/list-add.png)
#asset(qx/icon/${qx.icontheme}/16/actions/list-remove.png)
#asset(qx/icon/${qx.icontheme}/16/actions/view-refresh.png)
#asset(qx/icon/${qx.icontheme}/16/actions/dialog-ok.png);
#asset(qx/icon/${qx.icontheme}/16/actions/dialog-cancel.png);
************************************************************************ */
qx.Class.define("cs2.frontend.dialogs.SSLCsrDialog",
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
    _edit_csr_id:null,
    _edit_csr_commonname:null,
    _edit_csr_keyname:null,
    _edit_csr_passphrase:null,
    _edit_csr_digest:null,
    _edit_csr_subjects_commonname:null,
    _edit_csr_subjects_country:null,
    _edit_csr_subjects_state:null,
    _edit_csr_subjects_location:null,
    _edit_csr_subjects_organisation:null,
    _edit_csr_subjects_org_unit:null,
    _list_iso3166:null,
    _createLayout:function() {
      this.set({
        modal:true,
        padding:3,
        showClose:true,
        showMaximize:false,
        showMinimize:false
      });
      this.setLayout(new qx.ui.layout.VBox(5));
      this.setResizable(false,true,false,false);
      var comp=new qx.ui.container.Composite();
      var layout=new qx.ui.layout.Grid(5,5);
      layout.setColumnFlex(1,1);
      comp.setLayout(layout);
      this._edit_csr_commonname=new qx.ui.form.TextField();
      this._edit_csr_commonname.setLiveUpdate(true);
      this._edit_csr_commonname.addListener("changeValue",this._commonnameChange,this)
      this._edit_csr_keyname=new qx.ui.form.SelectBox();
      this._edit_csr_digest=new qx.ui.form.SelectBox();
      this._edit_csr_passphrase=new qx.ui.form.TextField();
      this._edit_csr_subjects_commonname=new qx.ui.form.TextField();
      this._edit_csr_subjects_country=new qx.ui.form.SelectBox();
      this._edit_csr_subjects_state=new qx.ui.form.TextField();
      this._edit_csr_subjects_location=new qx.ui.form.TextField();
      this._edit_csr_subjects_organisation=new qx.ui.form.TextField();
      this._edit_csr_subjects_org_unit=new qx.ui.form.TextField();

      var btnRefreshKeys=new qx.ui.form.Button("Refresh");
      btnRefreshKeys.addListener("execute",this._fillKeyNames,this);

      this._fillIso3166List();
      this._fillKeyNames();
      this._fillDigestNames();


      comp.add(new qx.ui.basic.Label("Commonname"),{row:0,column:0});
      comp.add(new qx.ui.basic.Label("Keyname"),{row:1,column:0});
      comp.add(new qx.ui.basic.Label("Key Passphrase"),{row:2,column:0});
      comp.add(new qx.ui.basic.Label("Digest"),{row:3,column:0});
      comp.add(new qx.ui.basic.Label("Subjects -> CN"),{row:4,column:0});
      comp.add(new qx.ui.basic.Label("Subjects -> Country"),{row:5,column:0});
      comp.add(new qx.ui.basic.Label("Subjects -> State"),{row:6,column:0});
      comp.add(new qx.ui.basic.Label("Subjects -> Location"),{row:7,column:0});
      comp.add(new qx.ui.basic.Label("Subjects -> Organisation"),{row:8,column:0});
      comp.add(new qx.ui.basic.Label("Subjects -> Org. Unit"),{row:9,column:0});

      comp.add(this._edit_csr_commonname,{row:0,column:1});
      comp.add(this._edit_csr_keyname,{row:1,column:1});
      comp.add(btnRefreshKeys,{row:1,column:2});
      comp.add(this._edit_csr_passphrase,{row:2,column:1});
      comp.add(this._edit_csr_digest,{row:3,column:1});
      comp.add(this._edit_csr_subjects_commonname,{row:4,column:1});
      comp.add(this._edit_csr_subjects_country,{row:5,column:1});
      comp.add(this._edit_csr_subjects_state,{row:6,column:1});
      comp.add(this._edit_csr_subjects_location,{row:7,column:1});
      comp.add(this._edit_csr_subjects_organisation,{row:8,column:1});
      comp.add(this._edit_csr_subjects_org_unit,{row:9,column:1});

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
    _fillKeyNames:function() {
      this._edit_csr_keyname.removeAll();
      var _tbl_ssl_keys=new cs2.models.SSLKeys(dc2.helpers.BrowserCheck.RPCUrl(false));
      var result=_tbl_ssl_keys.getKeyNames();
      for (var i=0;i<result.length;i++) {
        this._edit_csr_keyname.add(new qx.ui.form.ListItem(result[i]["keyname"],null,result[i]["keyname"]));
      }
    },
    _fillIso3166List:function() {
      var _tbl_iso3166=new cs2.models.SSLIso3166(dc2.helpers.BrowserCheck.RPCUrl(false));
      var result=_tbl_iso3166.getIso3166List();
      this._list_iso3166={};
      for (var i=0;i<result.length;i++) {
        this._list_iso3166[result[i]["country_code"]]=new qx.ui.form.ListItem(result[i]["country_name"]+" ("+result[i]["country_code"]+")",null,result[i]["country_code"]);
        this._edit_csr_subjects_country.add(this._list_iso3166[result[i]["country_code"]]);
      }
    },
    _fillDigestNames:function() {
      this._edit_csr_digest.add(new qx.ui.form.ListItem("SHA1",null,"sha1"));
      this._edit_csr_digest.add(new qx.ui.form.ListItem("MD5",null,"md5"));
      this._edit_csr_digest.add(new qx.ui.form.ListItem("MD4",null,"MD4"));
      this._edit_csr_digest.add(new qx.ui.form.ListItem("MDC2",null,"mdc2"));
      this._edit_csr_digest.add(new qx.ui.form.ListItem("MD2",null,"md2"));
    },
    _clkBtnOk:function(e) {
      var data={};
      data["commonname"]=this._edit_csr_commonname.getValue();
      data["keyname"]=this._edit_csr_keyname.getSelection()[0].getModel();
      data["passphrase"]=this._edit_csr_passphrase.getValue();
      data["digest"]=this._edit_csr_digest.getSelection()[0].getModel();
      data["subjects"]={};
      data["subjects"]["CN"]=this._edit_csr_subjects_commonname.getValue();
      data["subjects"]["C"]=this._edit_csr_subjects_country.getSelection()[0].getModel();
      data["subjects"]["ST"]=this._edit_csr_subjects_state.getValue();
      data["subjects"]["L"]=this._edit_csr_subjects_location.getValue();
      data["subjects"]["O"]=this._edit_csr_subjects_organisation.getValue();
      data["subjects"]["OU"]=this._edit_csr_subjects_org_unit.getValue();
      this.fireDataEvent("addData",data);
      this.close();
    },
    _clkBtnCancel:function(e) {
      this.close();
    },
    setData:function(data) {
      this._edit_csr_commonname.setValue(null);
      this._edit_csr_passphrase.setValue(null);
      this._edit_csr_subjects_commonname.setValue(null);
      this._edit_csr_subjects_state.setValue(null);
      this._edit_csr_subjects_location.setValue(null);
      this._edit_csr_subjects_organisation.setValue(null);
      this._edit_csr_subjects_org_unit.setValue(null);
    },
    _commonnameChange:function(e) {
      this._edit_csr_subjects_commonname.setValue(e.getData());
    }
  }
});