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

qx.Class.define("dc2.dialogs.search.Hosts",
{
  extend: dc2.widgets.DialogWidget,
  construct:function() {
    this.base(arguments);
  },
  members: {
    _edit_hostname:null,
    _edit_domainname:null,
    _createLayout:function() {
      var comp=new qx.ui.container.Composite();
      var layout=new qx.ui.layout.Grid(5,10);
      layout.setColumnFlex(1,1);
      comp.setLayout(layout);
      this._edit_hostname=new qx.ui.form.TextField();
      this._edit_domainname=new qx.ui.form.TextField();
      comp.add(new qx.ui.basic.Label("Hostname"),{row:0,column:0});
      comp.add(new qx.ui.basic.Label("Domainname"),{row:1,column:0});
      comp.add(this._edit_hostname,{row:0,column:1});
      comp.add(this._edit_domainname,{row:1,column:1});
      return(comp);
    },
    _getData:function() {
      var data={};
      if (this._edit_hostname.getValue() != null && this._edit_hostname.getValue() != "") {
        data["hostname"]=this._edit_hostname.getValue();
      }
      if (this._edit_domainname.getValue() != null && this._edit_domainname.getValue() != "") {
        data["domainname"]=this._edit_domainname.getValue();
      }
      return(data);
    }
  }
});
