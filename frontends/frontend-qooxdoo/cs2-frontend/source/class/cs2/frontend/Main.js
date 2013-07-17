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

qx.Class.define("cs2.frontend.Main", {
	extend: qx.core.Object,
	construct:function() {
		this.base(arguments);
	},
	members: {
		getHostKeysPage:function() {
		  // Return Tab Page
		  var sslkey_tbl=new cs2.models.SSLKeys(dc2.helpers.BrowserCheck.RPCUrl(false));
		  var sslkey_dialog=new cs2.frontend.dialogs.SSLKeyDialog();
		  var sslkey_view=new cs2.frontend.dialogs.SSLKeyView();
      var sslkey_table_options={
          enableAddEntry:true,
          enableEditEntry:false,
          enableDeleteEntry:true,
          enableReloadEntry:true,
          enableViewEntry:true,
          columnVisibility:[
                            {
                              column:0,
                              visible:false
                            },
                            {
                              column:3,
                              visible:false
                            }
                            ],
          tableModel:sslkey_tbl,
          addDialog:sslkey_dialog,
          viewDialog:sslkey_view
      };
      var sslkey_table=new dc2.widgets.TableWidget(sslkey_table_options);
      sslkey_table.showData();
      return(sslkey_table);
		},
		getCSRPage:function() {
		  var sslcsr_tbl=new cs2.models.SSLCsrs(dc2.helpers.BrowserCheck.RPCUrl(false));
		  var sslcsr_adddlg=new cs2.frontend.dialogs.SSLCsrDialog();
		  var sslcsr_viewdlg=new cs2.frontend.dialogs.SSLCsrView();
		  var sslcsr_options={
		      enableAddEntry:true,
		      enableDeleteEntry:true,
		      enableViewEntry:true,
		      tableModel:sslcsr_tbl,
		      addDialog:sslcsr_adddlg,
		      viewDialog:sslcsr_viewdlg,
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
		  var sslcsr_table=new dc2.widgets.TableWidget(sslcsr_options);
		  sslcsr_table.showData();
		  return(sslcsr_table);
		},
		getCertPage:function() {
		  var sslcert_tbl=new cs2.models.SSLCerts(dc2.helpers.BrowserCheck.RPCUrl(false));
		  var sslcert_adddlg=new cs2.frontend.dialogs.SSLCertDialog();
		  var sslcert_viewdlg=new cs2.frontend.dialogs.SSLCertView();
		  var sslcert_table=null;
		  var extraCall=function(e) {
		    var rowdata=sslcert_table.getSelectedRowData();
		    if (typeof(rowdata) != "undefined") {
		      var dialog=new cs2.frontend.dialogs.SSLCertRevokeDialog();
		      dialog.setData({"commonname":rowdata["commonname"]});
		      dialog.addListener("close",function(e) {sslcert_table.showData(); delete(dialog)},this);
		      dialog.show();

		    }
		  };
		  var sslcert_options={
		      enableAddEntry:true,
		      enableDeleteEntry:false,
		      enableViewEntry:true,
		      enableReloadEntry:true,
		      tableModel:sslcert_tbl,
		      addDialog:sslcert_adddlg,
		      viewDialog:sslcert_viewdlg,
		      columnVisibility:[
                            {
                              column:0,
                              visible:false
                            },
                            {
                              column:2,
                              visible:false
                            }
                            ],
          enableExtraButtons:true,
          extraButtons:[{
            title: "Revoke",
            callback:extraCall,
            context:this
          }]
		  };
		  sslcert_table=new dc2.widgets.TableWidget(sslcert_options);
		  sslcert_table.showData();
		  return(sslcert_table);
		},
		getCRLPage:function() {
		  var sslcrl_tbl=new cs2.models.SSLCrls(dc2.helpers.BrowserCheck.RPCUrl(false));
		  var sslcrl_viewdlg=new cs2.frontend.dialogs.SSLCrlView();
		  var sslcrl_options={
		      enableViewEntry:true,
		      viewDialog:sslcrl_viewdlg,
          columnVisibility:[
                            {
                              column:0,
                              visible:false
                            },
                            {
                              column:2,
                              visible:false
                            }
                            ],
		      tableModel:sslcrl_tbl
		  };
		  var sslcrl_table=new dc2.widgets.TableWidget(sslcrl_options);
		  sslcrl_table.showData();
		  return(sslcrl_table);
		},
		getISO3166Codes:function() {
		  // return Tab Page
		  var ssliso3166_tbl=new cs2.models.SSLIso3166(dc2.helpers.BrowserCheck.RPCUrl(false));
		  var ssliso3166_options={
		      enableAddEntry:false,
          enableEditEntry:false,
          enableDeleteEntry:false,
          enableReloadEntry:false,
          enableViewEntry:false,
          tableModel:ssliso3166_tbl
		  };
		  var ssliso3166_table=new dc2.widgets.TableWidget(ssliso3166_options);
		  ssliso3166_table.showData();
		  return(ssliso3166_table);
		}
	}
}
);